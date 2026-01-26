# Flywheel Plugin

**Vault automation infrastructure for markdown-based knowledge management.**

Flywheel provides the foundation layer: safety hooks, wikilink automation, and MCP-powered graph intelligence. For workflow skills (logging, rollups, task management, nutrition tracking), install the separate [vault-personal](https://github.com/velvetmonkey/vault-personal) plugin.

## Core Features

### Six Gates Safety Framework
**Enforced safeguards preventing data corruption and accidental mutations:**

| Gate | Purpose | Enforcement |
|------|---------|-------------|
| **1. Read Before Write** | Read before write | `pre-mutation-gate.py` (BLOCKS) |
| **2. File Exists for Edit** | Validate targets | `pre-mutation-gate.py` (BLOCKS) |
| **3. Agent Chain Validation** | Verify each step | Hook validation (BLOCKS) |
| **4. Mutation Confirmation** | User confirmation | `pre-mutation-gate.py` (BLOCKS) |
| **5. MCP Health Check** | Health check | `session-gate.py` (WARN) |
| **6. Post-Execution Validation** | Verify writes | `verify-mutation.py` (WARN) |

See `docs/SIX_GATES.md` for full specification.

### Automatic Wikilink Management
- **Session Start Hook**: Validates daily notes and rebuilds wikilink cache
- **Suggest Wikilinks Hook**: Auto-applies `[[wikilinks]]` to recognized entities
- **Syntax Validation Hook**: Prevents angle brackets and wrapped wikilinks that break Obsidian

### Frontmatter Automation
- **Auto-injection**: Add context and metadata during file operations
- **Schema validation**: Ensure consistent frontmatter structure
- **Type enforcement**: Validate field types across your vault

### Vault Intelligence (requires Flywheel MCP)
Graph analysis and vault health powered by the Flywheel MCP server:
- **Health Diagnostics**: Overall vault health score
- **Orphan Detection**: Find isolated notes
- **Link Analysis**: Backlinks, forward links, bidirectional connections
- **Hub Discovery**: Find highly connected notes
- **Cluster Detection**: Identify knowledge clusters
- **Gap Analysis**: Find topics needing expansion

## Requirements

| Requirement | Notes |
|-------------|-------|
| Python 3.8+ | Required for hooks (`python3` command) |
| Claude Code | With plugin support enabled |
| Flywheel MCP | Required for vault intelligence |

## Installation

See **[INSTALLATION.md](INSTALLATION.md)** for detailed platform-specific setup instructions.

**Quick Start:**
1. Add plugin to Claude Code settings (see INSTALLATION.md)
2. Create `.flywheel.json` in your vault root (see Configuration)
3. Copy rules to your vault (see [rules.md](rules.md))
4. Restart Claude Code

## Rules (Manual Installation)

Claude Code plugins cannot bundle rules - they must be installed to your project's `.claude/rules/` directory. See **[rules.md](rules.md)** for:

- **obsidian-syntax.md** - Prevents Obsidian-breaking syntax (angle brackets, wrapped wikilinks)
- **daily-notes.md** - Enforces daily note structure and log formatting
- **folder-organization.md** - Protects folder hierarchy
- **platform-requirements.md** - WSL/Windows setup requirements

## Configuration

Create `.flywheel.json` in your markdown vault root:

```json
{
  "$schema": "./plugins/flywheel/config/config-schema.json",
  "vault_name": "My Vault",
  "paths": {
    "daily_notes": "daily-notes",
    "weekly_notes": "weekly-notes",
    "monthly_notes": "monthly-notes",
    "quarterly_notes": "quarterly-notes",
    "yearly_notes": "yearly-notes"
  },
  "folders": {
    "protected": ["personal", "work", "tech"]
  }
}
```

### Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `vault_name` | Your vault's display name | Required |
| `paths.daily_notes` | Path to daily notes folder | `daily-notes` |
| `paths.weekly_notes` | Path to weekly notes folder | `weekly-notes` |
| `paths.monthly_notes` | Path to monthly notes folder | `monthly-notes` |
| `paths.quarterly_notes` | Path to quarterly notes folder | `quarterly-notes` |
| `paths.yearly_notes` | Path to yearly notes folder | `yearly-notes` |
| `folders.protected` | Folders requiring subfolders | `["personal", "work", "tech"]` |

**Note:** Configuration options for `habits`, `achievements`, `sections.log`, `sections.food` are supported for backward compatibility but are vault-personal features. See the [vault-personal plugin](https://github.com/velvetmonkey/vault-personal) for documentation.

## Directory Structure

```
packages/claude-plugin/
├── .claude-plugin/
│   ├── plugin.json           # Plugin manifest
│   └── marketplace.json      # Marketplace metadata
├── config/
│   └── config-schema.json    # Configuration schema
├── hooks/
│   ├── session-start.py      # Session initialization
│   ├── inject-context.py     # Context injection
│   ├── auto-approve-vault.py # Auto-approve vault operations
│   ├── validate-obsidian-syntax.py  # Syntax validation
│   ├── suggest-wikilinks.py  # Wikilink automation
│   ├── pre-mutation-gate.py  # Six Gates enforcement (Gates 1-4)
│   ├── session-gate.py       # MCP health check (Gate 5)
│   └── verify-mutation.py    # Post-execution verification (Gate 6)
├── skills/
│   └── vault-tasks/          # Task extraction and management
└── rules.md                  # Documentation for manual rule installation
```

## Skills Reference

### Core Skill

| Skill | Trigger | Description |
|-------|---------|-------------|
| `vault-tasks` | "show tasks", "find tasks" | Extract and display tasks from vault |

### Workflow Skills (vault-personal)

For daily logging, task management, nutrition tracking, and note rollups, install [vault-personal](https://github.com/velvetmonkey/vault-personal):
- `add-log` - Add entries to daily log
- `task-add` - Add tasks to daily notes
- `food` - Log meals with timestamps
- `food-macros` - Calculate daily nutrition
- `rollup` - Aggregate notes (daily → weekly → monthly → quarterly → yearly)
- And 44 more skills...

## Required: Flywheel MCP Server

This plugin requires the [@bencassie/flywheel-mcp](https://github.com/velvetmonkey/flywheel) MCP server for vault intelligence and wikilink management.

**macOS/Linux/WSL:**
```json
{
  "mcpServers": {
    "flywheel": {
      "command": "npx",
      "args": ["-y", "@bencassie/flywheel-mcp"],
      "env": {
        "PROJECT_PATH": "/path/to/your/vault"
      }
    }
  }
}
```

**Windows (requires `cmd /c` wrapper):**
```json
{
  "mcpServers": {
    "flywheel": {
      "command": "cmd",
      "args": ["/c", "npx", "-y", "@bencassie/flywheel-mcp"],
      "env": {
        "PROJECT_PATH": "C:/Users/YOUR_USER/path/to/vault"
      }
    }
  }
}
```

See [INSTALLATION.md](INSTALLATION.md) for detailed platform-specific instructions.

## Migration from v1.23.x

**Breaking Changes in v1.24.0:**
- Personal vault features moved to separate `vault-personal` plugin
- Templates removed (now in vault-personal)
- Skills removed: `add-log`, `task-add`, `food`, `food-macros`, `rollup`
- Agents removed: All rollup agents

**Backward Compatibility:**
- Existing `.flywheel.json` configs still work (personal config options accepted but unused)
- MCP server unchanged
- Core hooks unchanged
- To continue using personal features, install [vault-personal](https://github.com/velvetmonkey/vault-personal)

See [docs/MIGRATION_v1.24.md](../../docs/MIGRATION_v1.24.md) for full migration guide.

## License

Apache 2.0 License

## Contributing

Contributions welcome! Please open an issue or pull request on GitHub.
