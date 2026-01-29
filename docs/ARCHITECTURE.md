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
| **Graph** | `mcp__flywheel__get_backlinks`, `mcp__flywheel__get_forward_links`, `mcp__flywheel__find_hub_notes`, `mcp__flywheel__find_orphan_notes`, `mcp__flywheel__get_link_path`, `mcp__flywheel__find_bidirectional_links`, `mcp__flywheel__find_dead_ends`, `mcp__flywheel__get_connection_strength`, `mcp__flywheel__get_common_neighbors` | Link traversal and graph analysis |
| **Search** | `mcp__flywheel__search_notes`, `mcp__flywheel__find_sections`, `mcp__flywheel__get_recent_notes`, `mcp__flywheel__get_stale_notes`, `mcp__flywheel__get_notes_modified_on`, `mcp__flywheel__get_notes_in_range`, `mcp__flywheel__get_contemporaneous_notes` | Finding and filtering notes |
| **Schema** | `mcp__flywheel__get_frontmatter_schema`, `mcp__flywheel__validate_frontmatter`, `mcp__flywheel__find_frontmatter_inconsistencies`, `mcp__flywheel__infer_folder_conventions`, `mcp__flywheel__find_incomplete_notes`, `mcp__flywheel__suggest_field_values`, `mcp__flywheel__compute_frontmatter`, `mcp__flywheel__rename_field`, `mcp__flywheel__migrate_field_values` | Frontmatter analysis and management |
| **Tasks** | `mcp__flywheel__get_all_tasks`, `mcp__flywheel__get_tasks_from_note`, `mcp__flywheel__get_tasks_with_due_dates` | Task extraction from notes |
| **Structure** | `mcp__flywheel__get_note_structure`, `mcp__flywheel__get_headings`, `mcp__flywheel__get_section_content`, `mcp__flywheel__get_note_metadata` | Note content analysis |
| **Periodic** | `mcp__flywheel__detect_periodic_notes` | Auto-detect daily/weekly/monthly note patterns |
| **Wikilinks** | `mcp__flywheel__suggest_wikilinks`, `mcp__flywheel__validate_links`, `mcp__flywheel__find_broken_links`, `mcp__flywheel__get_unlinked_mentions`, `mcp__flywheel__suggest_wikilinks_in_frontmatter` | Link suggestions and validation |
| **Vault** | `mcp__flywheel__health_check`, `mcp__flywheel__get_vault_stats`, `mcp__flywheel__get_folder_structure`, `mcp__flywheel__get_activity_summary`, `mcp__flywheel__get_all_entities`, `mcp__flywheel__refresh_index` | Vault-wide operations |
| **Prose** | `mcp__flywheel__detect_prose_patterns`, `mcp__flywheel__suggest_frontmatter_from_prose`, `mcp__flywheel__validate_cross_layer` | Bidirectional bridge tools |

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

Create `.claude/.flywheel.json` to override auto-detection:

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
