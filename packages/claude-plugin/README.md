# Flywheel Plugin

A comprehensive Claude Code plugin for markdown vault automation, note rollups, and knowledge graph management.

## Features

### Automatic Wikilink Management
- **Session Start Hook**: Validates daily notes and rebuilds wikilink cache
- **Suggest Wikilinks Hook**: Auto-applies `[[wikilinks]]` to recognized entities
- **Syntax Validation Hook**: Prevents angle brackets and wrapped wikilinks that break Obsidian

### Note Rollup System
Automated aggregation from daily notes up through yearly summaries:
- **Daily → Weekly**: Extract achievements, habits, macros, weight data
- **Weekly → Monthly**: Aggregate weekly summaries into monthly overviews
- **Monthly → Quarterly**: Synthesize quarterly progress and goals
- **Quarterly → Yearly**: Compile annual reviews

### Nutrition Tracking
- **Food Logging**: Log meals with timestamps to daily notes
- **Macro Calculation**: Calculate daily nutrition totals from food entries

### Vault Intelligence (requires Flywheel MCP)
16 vault analysis skills powered by the Flywheel MCP server:
- **Health Diagnostics**: Overall vault health score
- **Orphan Detection**: Find isolated notes
- **Link Analysis**: Backlinks, forward links, bidirectional connections
- **Hub Discovery**: Find highly connected notes
- **Cluster Detection**: Identify knowledge clusters
- **Gap Analysis**: Find topics needing expansion
- And more...

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
    "yearly_notes": "yearly-notes",
    "templates": "templates",
    "achievements": "personal/goals/Achievements.md"
  },
  "habits": [
    { "name": "Walk", "tag": "#habit" },
    { "name": "Stretch", "tag": "#habit" },
    { "name": "Vitamins", "tag": "#habit" }
  ],
  "sections": {
    "log": "## Log",
    "food": "# Food",
    "habits": "# Habits"
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
| `paths.templates` | Path to templates folder | `templates` |
| `paths.achievements` | Path to achievements file | `personal/goals/Achievements.md` |
| `habits` | Array of habits to track | Walk, Stretch, Vitamins |
| `sections.log` | Log section header in daily notes | `## Log` |
| `sections.food` | Food section header in daily notes | `# Food` |
| `sections.habits` | Habits section header in daily notes | `# Habits` |
| `folders.protected` | Folders requiring subfolders | `["personal", "work", "tech"]` |

## Directory Structure

```
packages/claude-plugin/
├── plugin.json           # Plugin manifest
├── config/
│   └── config-schema.json
├── hooks/
│   ├── session-start.py
│   ├── inject-context.py
│   ├── auto-approve-vault.py
│   ├── validate-obsidian-syntax.py
│   ├── suggest-wikilinks.py
│   └── detect-achievement.py
├── skills/
│   ├── core/
│   │   ├── rollup/
│   │   ├── rebuild-wikilink-cache/
│   │   ├── task-add/
│   │   ├── task-status/
│   │   └── auto-log/
│   ├── nutrition/
│   │   ├── food/
│   │   └── food-macros/
│   └── vault/
│       ├── health/
│       ├── orphans/
│       ├── backlinks/
│       └── ... (16 total)
├── agents/
│   └── rollup/
│       ├── rollup-agent.md
│       ├── weekly-agent.md
│       ├── monthly-agent.md
│       ├── quarterly-agent.md
│       └── yearly-agent.md
├── rules.md              # Documentation for manual rule installation
└── templates/
    ├── daily.md
    ├── weekly.md
    ├── monthly.md
    ├── quarterly.md
    └── yearly.md
```

## Skills Reference

### Core Skills
| Skill | Trigger | Description |
|-------|---------|-------------|
| `rollup` | "rollup", "summarize week" | Run the complete rollup chain |
| `rebuild-wikilink-cache` | "rebuild cache", "refresh entities" | Rebuild wikilink entity cache |
| `task-add` | "add task", "new task" | Add tasks to daily notes |
| `task-status` | "task status", "show tasks" | Show task status |
| `auto-log` | "log", "add to log" | Add entries to daily log |

### Nutrition Skills
| Skill | Trigger | Description |
|-------|---------|-------------|
| `food` | "I ate", "breakfast", "lunch" | Log food to daily note |
| `food-macros` | "macros", "calories" | Calculate daily macros |

### Vault Skills (requires Flywheel MCP)
| Skill | Description |
|-------|-------------|
| `health` | Overall vault health diagnostics |
| `orphans` | Find orphan notes |
| `backlinks` | Show note backlinks |
| `fix-links` | Repair broken wikilinks |
| `hubs` | Find hub notes |
| `clusters` | Find knowledge clusters |
| `stale` | Find stale notes |
| `gaps` | Find knowledge gaps |

## Agents

### Rollup Agents
Autonomous agents for note aggregation:

| Agent | Invocation | Description |
|-------|------------|-------------|
| `rollup-agent` | Automatic | Orchestrates complete rollup chain |
| `rollup-weekly-agent` | `2025-W52` | Daily → Weekly aggregation |
| `rollup-monthly-agent` | `2025-12` | Weekly → Monthly aggregation |
| `rollup-quarterly-agent` | `2025-Q4` | Monthly → Quarterly aggregation |
| `rollup-yearly-agent` | `2025` | Quarterly → Yearly aggregation |

## Required: Flywheel MCP Server

This plugin requires the [@bencassie/flywheel-mcp](https://github.com/bencassie/flywheel) MCP server for vault intelligence and wikilink management.

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

## License

Apache 2.0 License

## Contributing

Contributions welcome! Please open an issue or pull request on GitHub.
