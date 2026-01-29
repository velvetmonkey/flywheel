# Configuration

Complete configuration reference for Flywheel MCP server.

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PROJECT_PATH` | Auto-detect | Path to your vault. Only needed if running Claude from outside your vault folder. |
| `FLYWHEEL_WATCH` | `false` | When `true`, automatically rebuilds the index when you edit notes. Useful if you're editing in Obsidian while Claude is working. |
| `FLYWHEEL_DEBOUNCE_MS` | `60000` | How long to wait after a file change before rebuilding (in milliseconds). Default 1 minute batches rapid edits together. |
| `FLYWHEEL_TOOLS` | `standard` | Which tool categories to load. Use `minimal` for less context usage, `full` for everything. |

---

## Tool Presets

Control which tools are available to reduce token usage:

| Preset | What's included | Best for |
|--------|-----------------|----------|
| `minimal` | Core vault info only | Quick queries, low token usage |
| `standard` | Core + graph + search + tasks | Most users (default) |
| `full` | All 44 tools | Power users who need everything |

Mix and match: `FLYWHEEL_TOOLS=core,graph,tasks`

### Tool Categories

| Category | Tools | Description |
|----------|-------|-------------|
| `core` | 9 | health_check, get_vault_stats, refresh_index, get_note_metadata, get_folder_structure, get_all_entities, get_recent_notes, get_unlinked_mentions, find_broken_links |
| `graph` | 6 | get_backlinks, get_forward_links, find_orphan_notes, find_hub_notes, suggest_wikilinks, validate_links |
| `search` | 1 | search_notes |
| `tasks` | 4 | get_all_tasks, get_tasks_from_note, get_tasks_with_due_dates, get_incomplete_tasks |
| `schema` | 8 | get_frontmatter_schema, get_field_values, find_frontmatter_inconsistencies, validate_frontmatter, find_missing_frontmatter, infer_folder_conventions, find_incomplete_notes, suggest_field_values |
| `structure` | 4 | get_note_structure, get_headings, get_section_content, find_sections |
| `temporal` | 6 | detect_periodic_notes, get_notes_modified_on, get_notes_in_range, get_stale_notes, get_contemporaneous_notes, get_activity_summary |
| `advanced` | 13 | Bidirectional bridge tools (detect_prose_patterns, suggest_frontmatter_from_prose, etc.), computed frontmatter, field migrations, graph analysis (get_link_path, find_dead_ends, etc.) |

### Custom Combinations

```bash
# Core + graph only
FLYWHEEL_TOOLS=core,graph

# Everything except advanced
FLYWHEEL_TOOLS=core,graph,search,tasks,schema,structure,temporal

# Just tasks and search
FLYWHEEL_TOOLS=core,tasks,search
```

**Note:** `core` is recommended in all combinations as it provides essential vault metadata tools.

---

## Vault Config File

Flywheel auto-creates `.claude/.flywheel.json` on first run by analyzing your vault. Edit it to override auto-detected settings.

| Field | What it does |
|-------|--------------|
| `vault_name` | Display name shown in tool responses |
| `paths.daily_notes` | Where your daily notes live (e.g., `"journal/daily"`) |
| `paths.weekly_notes` | Where your weekly notes live |
| `paths.templates` | Your templates folder (excluded from some queries) |
| `exclude_task_tags` | Tags to ignore in task queries (e.g., `["#habit", "#someday"]`) |

**Example** - customize for a non-standard vault layout:
```json
{
  "vault_name": "Work Notes",
  "paths": {
    "daily_notes": "Logs/Daily",
    "templates": "Meta/Templates"
  },
  "exclude_task_tags": ["#recurring", "#habit"]
}
```

Most users don't need to edit this file. Flywheel auto-detects folders named `daily`, `journal`, `weekly`, `templates`, etc.

---

## Platform-Specific Setup

### Windows (native)

```json
{
  "mcpServers": {
    "flywheel": {
      "command": "cmd",
      "args": ["/c", "npx", "-y", "@velvetmonkey/flywheel-mcp"]
    }
  }
}
```

### WSL

Use `npx` directly (not `cmd /c`), with `/mnt/c/...` paths.

### Custom Vault Location

```json
{
  "mcpServers": {
    "flywheel": {
      "command": "npx",
      "args": ["-y", "@velvetmonkey/flywheel-mcp"],
      "env": {
        "PROJECT_PATH": "/path/to/your/vault"
      }
    }
  }
}
```

---

## File Watching

Enable file watching to automatically rebuild the index when vault files change:

```json
{
  "mcpServers": {
    "flywheel": {
      "command": "npx",
      "args": ["-y", "@velvetmonkey/flywheel-mcp"],
      "env": {
        "FLYWHEEL_WATCH": "true"
      }
    }
  }
}
```

### Custom Debounce Delay

Default is 60000ms (1 minute):

```json
{
  "mcpServers": {
    "flywheel": {
      "command": "npx",
      "args": ["-y", "@velvetmonkey/flywheel-mcp"],
      "env": {
        "FLYWHEEL_WATCH": "true",
        "FLYWHEEL_DEBOUNCE_MS": "1000"
      }
    }
  }
}
```

### How It Works

- Watches vault directory for `.md` file changes
- Automatically ignores dotfiles (`.obsidian`, `.trash`, etc.)
- Debounces rapid changes to avoid excessive rebuilds
- Uses `awaitWriteFinish` to prevent indexing partial writes
- Logs rebuild events to stderr

### When to Use

Enable file watching if you're editing notes while an agent is actively working in your vault. Without watching, the agent sees a snapshot from when the MCP server started.

**Performance:** Minimal overhead. Rebuilds only trigger on `.md` file changes, not every filesystem event.

---

## Permissions

For the best experience, pre-approve Flywheel read tools in `.claude/settings.json`:

```json
{
  "permissions": {
    "allow": [
      "mcp__flywheel__*"
    ]
  }
}
```

All Flywheel tools are read-only—they query your vault's index but never modify files.

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| **`npx: command not found`** | Node.js isn't installed. [Download Node.js 18+](https://nodejs.org) |
| **`flywheel ✗` in mcp list** | Wrong file location. `.mcp.json` must be in your vault root |
| **"No notes found"** | Not in vault directory. Run `claude` from inside your vault folder |
| **Windows: spawn errors** | Use `cmd /c npx` config (see Platform-Specific Setup above) |
| **MCP server won't start** | Check Node version: `node --version` (need 18+) |
