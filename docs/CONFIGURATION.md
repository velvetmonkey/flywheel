# Configuration

Complete configuration reference for Flywheel MCP server.

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PROJECT_PATH` | Auto-detect | Path to your vault. Only needed if running Claude from outside your vault folder. |
| `FLYWHEEL_WATCH` | `true` | File watching enabled by default. Set to `false` to disable automatic index rebuilds when you edit notes. |
| `FLYWHEEL_DEBOUNCE_MS` | `200` | Per-path debounce in milliseconds. Events on the same file are coalesced during this window. |
| `FLYWHEEL_FLUSH_MS` | `1000` | Maximum interval (ms) before flushing batched events, even if per-path debounce hasn't expired. |
| `FLYWHEEL_BATCH_SIZE` | `50` | Maximum paths to accumulate before forcing a flush. |
| `FLYWHEEL_WATCH_POLL` | `false` | When `true`, use polling instead of native file watchers. Useful for network drives or WSL. |
| `FLYWHEEL_POLL_INTERVAL` | `500` | Polling interval in milliseconds when `FLYWHEEL_WATCH_POLL=true`. |
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

### Tuning for Large Vaults

For vaults with 10,000+ notes, increase debounce to prevent thrashing during active editing:

```json
{
  "mcpServers": {
    "flywheel": {
      "command": "npx",
      "args": ["-y", "@velvetmonkey/flywheel-mcp"],
      "env": {
        "FLYWHEEL_WATCH": "true",
        "FLYWHEEL_DEBOUNCE_MS": "5000",
        "FLYWHEEL_FLUSH_MS": "10000"
      }
    }
  }
}
```

| Vault Size | Recommended Settings |
|------------|---------------------|
| Small (<1000 notes) | Default (200ms/1000ms) |
| Medium (1000-5000 notes) | 1000ms/5000ms |
| Large (5000-10000 notes) | 3000ms/10000ms |
| Very Large (10000+ notes) | 5000ms/10000ms |

Higher debounce values let you edit freely without triggering rebuilds until you pause.

### How It Works

- Watches vault directory for `.md` file changes
- Automatically ignores dotfiles (`.obsidian`, `.trash`, etc.)
- Per-path debouncing: each file has its own debounce timer
- Event coalescing: rapid add/change/unlink sequences resolve to single actions
- Uses `awaitWriteFinish` to prevent indexing partial writes
- Logs rebuild events to stderr

### Self-Healing Recovery

The watcher automatically recovers from common errors:

| Error | Recovery Action |
|-------|-----------------|
| `EMFILE` (too many open files) | Exponential backoff retry (1s, 2s, 4s...) |
| `ENOSPC` (inotify limit on Linux) | Retry with backoff, then fallback to polling |
| `ENOTSUP`, `EPERM`, `EACCES` | Immediate fallback to polling mode |

During recovery, the index is marked "dirty" and continues serving stale data with warnings.

### Known Limitations

- **WSL2 /mnt/c/ paths**: File changes on Windows drives accessed via `/mnt/c/` may not be detected. Consider using native Windows paths or polling mode.
- **Network drives**: Use `FLYWHEEL_WATCH_POLL=true` for reliable detection.
- **Very large vaults**: With default 200ms debounce, editing can trigger excessive rebuilds. Increase debounce for 10k+ note vaults.

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
