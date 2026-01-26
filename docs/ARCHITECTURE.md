# Flywheel Architecture

A guide to Flywheel's MCP server design for developers.

---

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    MCP Client (Claude, etc.)                     │
│              Requests vault intelligence via MCP                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FLYWHEEL MCP SERVER                           │
│            44 tools for vault intelligence                       │
│                                                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │   Graph     │  │   Schema    │  │   Search    │             │
│  │   Tools     │  │   Tools     │  │   Tools     │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
│                                                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │   Tasks     │  │  Structure  │  │  Periodic   │             │
│  │   Tools     │  │   Tools     │  │   Tools     │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Your Markdown Vault                         │
│                        .md files                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## MCP Server (44 tools)

The MCP server provides vault intelligence to any MCP-compatible client.

**Location**: `packages/mcp-server/`

### Tool Categories

| Category | Tools | Purpose |
|----------|-------|---------|
| **Graph** | `get_backlinks`, `get_forward_links`, `find_hub_notes`, `find_orphan_notes`, `get_link_path`, `find_bidirectional_links`, `find_dead_ends`, `get_connection_strength`, `get_common_neighbors` | Link traversal and graph analysis |
| **Search** | `search_notes`, `find_sections`, `get_recent_notes`, `get_stale_notes`, `get_notes_modified_on`, `get_notes_in_range`, `get_contemporaneous_notes` | Finding and filtering notes |
| **Schema** | `get_frontmatter_schema`, `validate_frontmatter`, `find_frontmatter_inconsistencies`, `infer_folder_conventions`, `find_incomplete_notes`, `suggest_field_values`, `compute_frontmatter`, `rename_field`, `migrate_field_values` | Frontmatter analysis and management |
| **Tasks** | `get_all_tasks`, `get_tasks_from_note`, `get_tasks_with_due_dates` | Task extraction from notes |
| **Structure** | `get_note_structure`, `get_headings`, `get_section_content`, `get_note_metadata` | Note content analysis |
| **Periodic** | `detect_periodic_notes` | Auto-detect daily/weekly/monthly note patterns |
| **Wikilinks** | `suggest_wikilinks`, `validate_links`, `find_broken_links`, `get_unlinked_mentions`, `suggest_wikilinks_in_frontmatter` | Link suggestions and validation |
| **Vault** | `health_check`, `get_vault_stats`, `get_folder_structure`, `get_activity_summary`, `get_all_entities`, `refresh_index` | Vault-wide operations |
| **Prose** | `detect_prose_patterns`, `suggest_frontmatter_from_prose`, `validate_cross_layer` | Bidirectional bridge tools |

### Tool Design Principles

1. **Read-only by default**: Tools query but don't modify files
2. **Pagination built-in**: All list tools support `limit` and `offset`
3. **Confidence scores**: Detection tools return confidence levels
4. **Auto-detection**: No configuration required for common patterns

---

## Configuration System

### Convention Over Configuration

Flywheel uses **auto-detection** by default. No config file required.

**How Auto-Detection Works**:

```
mcp__flywheel__detect_periodic_notes(type="daily")

Returns:
{
  "detected": true,
  "folder": "daily-notes",           <- Found by scanning
  "pattern": "YYYY-MM-DD",           <- Detected from filenames
  "confidence": 0.87,                <- Based on evidence
  "today_path": "daily-notes/2026-01-03.md"
}
```

Detection process:
1. Scan ALL files in vault
2. Match filenames against date patterns
3. Group by folder + pattern
4. Score by note count, recency, folder name
5. Return best-guess with confidence

### Optional Config Override

Create `.flywheel.json` in vault root to override auto-detection:

```json
{
  "paths": {
    "daily_notes": "journal",
    "weekly_notes": "reviews/weekly"
  },
  "sections": {
    "log": "Daily Log",
    "tasks": "To Do"
  }
}
```

### Section Matching

Section matching is **forgiving by design**:
- Case-insensitive (`"log"` matches `## Log`, `## LOG`)
- Level-agnostic (`"Log"` matches `# Log`, `## Log`, `### Log`)
- Whitespace-trimmed

**Config values use text only, no `#` prefix**:
```json
{
  "sections": {
    "log": "Log",
    "tasks": "Tasks"
  }
}
```

### Priority Order

1. `.flywheel.json` explicit config (highest)
2. MCP auto-detection (smart defaults)
3. Built-in defaults (fallback)

---

## File Locations

| What | Where |
|------|-------|
| MCP server entry | `packages/mcp-server/src/index.ts` |
| MCP tools | `packages/mcp-server/src/tools/` |
| Configuration | `packages/mcp-server/src/config/` |
| Tests | `packages/mcp-server/src/__tests__/` |

---

## Development Workflow

### Building

```bash
# Install dependencies
npm install

# Build MCP server
npm run build

# Run in development mode
npm run dev:mcp
```

### Testing

```bash
# Run tests
npm test

# Run MCP server against a vault
PROJECT_PATH=/path/to/vault npm run dev:mcp
```

### Adding a New Tool

1. Create tool file in `packages/mcp-server/src/tools/`
2. Export tool definition with name, description, parameters
3. Implement handler function
4. Register in `index.ts`
5. Add tests

---

## Integration

### MCP Configuration

Add to your `.mcp.json`:

```json
{
  "mcpServers": {
    "flywheel": {
      "command": "npx",
      "args": ["-y", "@velvetmonkey/flywheel-mcp"],
      "env": {
        "PROJECT_PATH": "/path/to/vault"
      }
    }
  }
}
```

### Platform-Specific Commands

| Platform | Command |
|----------|---------|
| Linux/WSL | `npx` |
| macOS | `npx` |
| Windows | `cmd /c npx` |
