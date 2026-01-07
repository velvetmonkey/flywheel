# Getting Started with Flywheel

> Query your markdown vault. One command to set up.

[![npm version](https://img.shields.io/npm/v/@bencassie/flywheel-mcp.svg)](https://www.npmjs.com/package/@bencassie/flywheel-mcp)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-blue.svg)](https://github.com/bencassie/flywheel)

---

## Quick Start

### 1. Install Plugin

```bash
# In Claude Code
/plugin marketplace add bencassie/flywheel
/plugin install flywheel@bencassie-flywheel
```

### 2. Setup

```
/setup-flywheel
```

Claude detects your platform, generates config, validates the connection.

### 3. Query Your Vault

```
"what links to [[My Project]]"    # Graph query
"find orphan notes"               # Disconnected notes
"show notes modified this week"   # Temporal query
"what fields exist in projects/"  # Schema query
```

**Done.** Your vault is now queryable.

---

## Try Queries First

Start with read-only queries to explore your vault:

### Graph Intelligence

| Ask This | What Happens |
|----------|--------------|
| "what links to [[Note]]" | Find all backlinks |
| "show hub notes" | Most connected notes |
| "find orphan notes" | Notes with no connections |
| "path from [[A]] to [[B]]" | Shortest link path |
| "what do X and Y both link to" | Common references |

### Temporal Queries

| Ask This | What Happens |
|----------|--------------|
| "show notes modified today" | Recent activity |
| "what changed last week" | 7-day activity |
| "find stale important notes" | High-connection, old modification |

### Schema Queries

| Ask This | What Happens |
|----------|--------------|
| "show vault schema" | All frontmatter fields |
| "what values does status have" | Unique field values |
| "find notes missing owner in projects/" | Schema gaps |

### Search

| Ask This | What Happens |
|----------|--------------|
| "find notes tagged #urgent" | Filter by tag |
| "list notes in meetings/" | Filter by folder |
| "search for 'review' in titles" | Title matching |

**[Full Query Guide →](./QUERY_GUIDE.md)**

---

## Then Try Commands

Once comfortable with queries, try workflow commands:

### Daily Operations

| Say This | What Happens |
|----------|--------------|
| "log fixed the bug" | Timestamped entry in daily note |
| "do a rollup" | Daily → weekly → monthly summaries |
| "show tasks due" | Tasks with due dates |

### Vault Maintenance

| Say This | What Happens |
|----------|--------------|
| "check vault health" | Full diagnostics |
| "fix broken links" | Find and resolve dead links |
| "normalize this note" | Apply folder schema |

### Reviews

| Say This | What Happens |
|----------|--------------|
| "/weekly-review" | Generate weekly summary |
| "/extract-actions" | Pull action items from meeting notes |

**[Full Command Reference →](./SKILLS_REFERENCE.md)**

---

## Build Your Own Skills

When you find yourself repeating workflows, create a skill:

```markdown
# packages/claude-plugin/skills/my-skill/SKILL.md

---
name: my-skill
description: What this skill does
trigger_keywords:
  - "trigger phrase"
allowed-tools: Read, mcp__flywheel__search_notes
---

## Process
1. First step
2. Second step
3. Verify and confirm
```

**[Building Skills Guide →](./BUILDING_SKILLS.md)**

---

## How It Works

Flywheel builds an **in-memory graph** at startup:

```
┌─────────────────────────────────────────────────────────────┐
│  Your vault  →  Scanned  →  Graph index in memory            │
│                                                             │
│  Claude queries index (50 tokens) not files (5,000 tokens)  │
└─────────────────────────────────────────────────────────────┘
```

**What gets indexed:**
- Note titles and aliases
- Wikilinks (relationships)
- Frontmatter fields
- Tags
- Modification dates

**What stays on disk:**
- File content (only read when needed)
- Full prose (privacy preserved)

**Token savings:**

| Query | Without Flywheel | With Flywheel |
|-------|------------------|---------------|
| "What links to X?" | ~5,000 tokens | ~50 tokens |
| "Find stale notes" | ~10,000 tokens | ~100 tokens |
| "do a rollup" | ~7,000 tokens | ~700 tokens |

---

## Try a Demo Vault

See Flywheel before using on your own vault:

```bash
git clone https://github.com/bencassie/flywheel.git
cd flywheel/demos/carter-strategy
claude
/setup-flywheel
"how much have I billed this quarter?"
```

| Demo | Notes | Good For |
|------|-------|----------|
| [carter-strategy](../demos/carter-strategy/) | 30 | Consultant queries |
| [startup-ops](../demos/startup-ops/) | 30 | SaaS founder workflows |
| [artemis-rocket](../demos/artemis-rocket/) | 65 | Technical graph traversal |
| [nexus-lab](../demos/nexus-lab/) | 30 | Research connections |

---

## Next Steps

| Want To... | Read |
|-----------|------|
| Master queries | [Query Guide](./QUERY_GUIDE.md) |
| See all commands | [Skills Reference](./SKILLS_REFERENCE.md) |
| Build custom skills | [Building Skills](./BUILDING_SKILLS.md) |
| See all MCP tools | [MCP Reference](./MCP_REFERENCE.md) |
| Understand safety | [Six Gates](./SIX_GATES.md) |

---

## Troubleshooting

### `/setup-flywheel` Not Working?

Restart Claude Code after installing the plugin, then try again.

### MCP Tools Not Found

If queries return "Tool not found":

1. Restart Claude Code after setup
2. Check `.mcp.json` exists in your vault root
3. Verify `PROJECT_PATH` in `.mcp.json` if using explicit path

### Manual Configuration (Fallback)

If `/setup-flywheel` fails, add to `.mcp.json` manually.

**Zero-config** — place `.mcp.json` in your vault root:

```json
{
  "mcpServers": {
    "flywheel": {
      "command": "npx",
      "args": ["-y", "@bencassie/flywheel-mcp"]
    }
  }
}
```

> **Windows**: Use `"command": "cmd", "args": ["/c", "npx", "-y", "@bencassie/flywheel-mcp"]`

**With explicit vault path**:

macOS / Linux / WSL:
```json
{
  "mcpServers": {
    "flywheel": {
      "command": "npx",
      "args": ["-y", "@bencassie/flywheel-mcp"],
      "env": { "PROJECT_PATH": "/path/to/vault" }
    }
  }
}
```

Windows:
```json
{
  "mcpServers": {
    "flywheel": {
      "command": "cmd",
      "args": ["/c", "npx", "-y", "@bencassie/flywheel-mcp"],
      "env": { "PROJECT_PATH": "C:/path/to/vault" }
    }
  }
}
```

### Platform-Specific Issues

| Platform | Issue | Fix |
|----------|-------|-----|
| Windows | "Connection closed" | Use `cmd /c npx` wrapper |
| Windows | Backslash paths fail | Use forward slashes: `C:/Users/...` |
| WSL | Hooks fail with "python not found" | `sudo apt install python-is-python3` |
| WSL | Wrong path format | Use `/mnt/c/...` for Windows drives |

---

## Getting Help

- **Docs**: [Documentation Index](./README.md)
- **GitHub Issues**: https://github.com/bencassie/flywheel/issues
- **Demos**: [../demos/README.md](../demos/README.md)
