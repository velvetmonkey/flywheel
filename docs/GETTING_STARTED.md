# Getting Started with Flywheel

> Graph intelligence for your vault. One command to set up.

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

### 3. Try It

```
"check vault health"       # Full diagnostics
"find orphan notes"        # Disconnected notes
"do a rollup"              # Daily -> weekly summaries
```

**Done.** You now have 40+ graph-aware tools.

---

## What Just Happened

Flywheel built an **in-memory graph** of your vault. Now when you ask questions, Claude queries the index — not the files.

```
┌─────────────────────────────────────────────────────────────┐
│                    THE FLYWHEEL LOOP                        │
├─────────────────────────────────────────────────────────────┤
│  Your notes  →  Indexed  →  AI queries graph (not files)    │
│                                                             │
│  Result: 50 tokens vs 5,000 for "what's blocking X?"        │
└─────────────────────────────────────────────────────────────┘
```

**Token savings (real numbers):**

| Query | Without Flywheel | With Flywheel |
|-------|------------------|---------------|
| "What's blocking X?" | ~5,000 tokens | ~50 tokens |
| "do a rollup" (7 days) | ~7,000 tokens | ~700 tokens |
| "log research findings" | ~800 tokens | ~42 tokens |

**Auto-curation**: After every edit, hooks automatically:
- Add `[[wikilinks]]` to recognized entities
- Complete frontmatter based on folder patterns

Your notes get smarter without manual tagging.

---

## Try These Commands

### Vault Intelligence

| Say This | What Happens |
|----------|--------------|
| "check vault health" | Orphans, hubs, broken links, schema issues |
| "find orphan notes" | Notes with no backlinks |
| "show hub notes" | Most connected notes (key concepts) |
| "path from X to Y" | Shortest link path between notes |
| "what's blocking X?" | Trace dependencies via frontmatter |

### Daily Operations

| Say This | What Happens |
|----------|--------------|
| "log fixed the bug" | Timestamped entry in today's daily note |
| "do a rollup" | Daily -> weekly -> monthly summaries |
| "show tasks due" | Tasks with due dates |
| "add task: review proposal" | Creates task in daily note |

### Schema Analysis

| Say This | What Happens |
|----------|--------------|
| "show vault schema" | All frontmatter fields in use |
| "find incomplete notes in projects/" | Notes missing expected fields |
| "what values does status have?" | Unique values for a field |

---

## Installation Options

### Marketplace (Recommended)

Already done in Quick Start above. That's all you need.

### From Source (Developers)

```bash
git clone https://github.com/bencassie/flywheel.git
cd flywheel && npm install
cd packages/mcp-server && npm run build && npm link
```

Then run `/setup-flywheel` — it detects your local build.

---

## Try a Demo Vault

See Flywheel in action before using on your vault:

```bash
git clone https://github.com/bencassie/flywheel.git

# Pick your scenario
cd flywheel/demos/carter-strategy    # Consultant (30 notes)
cd flywheel/demos/solo-operator      # Creator (22 notes)
cd flywheel/demos/artemis-rocket     # Aerospace (65 notes)
cd flywheel/demos/startup-ops        # SaaS founder (30 notes)
cd flywheel/demos/nexus-lab          # Researcher (30 notes)

# Start
claude
/setup-flywheel
```

**Full demo guide**: [demos/README.md](../demos/README.md)

---

## Next Steps

| Want To... | Read |
|-----------|------|
| See all 44 MCP tools | [MCP Reference](./MCP_REFERENCE.md) |
| Learn the skills | [Skills Reference](./SKILLS_REFERENCE.md) |
| Understand safety | [Six Gates](./SIX_GATES.md) |
| Build workflows | [Agentic Patterns](./AGENTIC_PATTERNS.md) |
| Configure rollups | [Workflow Configuration](./WORKFLOW_CONFIGURATION.md) |

---

## Troubleshooting

### `/setup-flywheel` Not Working?

Restart Claude Code after installing the plugin, then try again.

### MCP Tools Not Found

If `get_vault_stats()` returns "Tool not found":

1. Ensure Claude Code was restarted after setup
2. Check `.mcp.json` exists in your vault root
3. Verify `PROJECT_PATH` points to correct directory

### Manual Configuration (Fallback)

If `/setup-flywheel` fails, add to `.mcp.json` manually:

**macOS / Linux / WSL:**
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

**Windows:**
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
| Windows | "Connection closed" | Use `cmd /c npx` wrapper (see above) |
| Windows | Backslash paths fail | Use forward slashes: `C:/Users/...` |
| WSL | Hooks fail with "python not found" | `sudo apt install python-is-python3` |
| WSL | Wrong path format | Use `/mnt/c/...` for Windows drives |

---

## Getting Help

- **Docs**: [Documentation Index](./README.md)
- **GitHub Issues**: https://github.com/bencassie/flywheel/issues
- **Demos**: [../demos/README.md](../demos/README.md)

---

**Version**: 1.11.3
**Last Updated**: 2026-01-04
**License**: Apache 2.0
