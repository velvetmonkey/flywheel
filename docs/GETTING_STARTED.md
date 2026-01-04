# Getting Started with Flywheel

> Install in 30 seconds, graph intelligence forever

[![npm version](https://img.shields.io/npm/v/@bencassie/flywheel-mcp.svg)](https://www.npmjs.com/package/@bencassie/flywheel-mcp)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-blue.svg)](https://github.com/bencassie/flywheel)

---

## 30-Second Quick Start

```bash
# Step 1: Install MCP server (choose one)
npm install -g @bencassie/flywheel-mcp    # Global install
# OR use npx (no install required)

# Step 2: Add to .mcp.json (in your Obsidian vault root)
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

# Step 3: Try it (in Claude Code)
get_vault_stats()    # → Vault overview
/vault-health        # → Full health report (requires plugin)
```

**Done**. You now have graph intelligence for your vault.

---

## Installation Paths

### Path 1: Marketplace (Recommended)

**For the plugin** (skills like `/vault-health`, `/auto-log`):

```bash
# In Claude Code
/plugin marketplace add bencassie/flywheel
/plugin install flywheel@bencassie-flywheel
```

**For the MCP server** (tools like `get_backlinks()`, `search_notes()`):

Add to `.mcp.json` in your vault:
```json
{
  "mcpServers": {
    "flywheel": {
      "command": "npx",
      "args": ["-y", "@bencassie/flywheel-mcp"],
      "env": {
        "PROJECT_PATH": "."
      }
    }
  }
}
```

### Path 2: From Source (Developers)

```bash
# Clone repo
git clone https://github.com/bencassie/flywheel.git
cd flywheel

# Install dependencies
npm install

# Build MCP server
cd packages/mcp-server
npm run build

# Link locally (instead of npx)
npm link

# In .mcp.json, use:
{
  "command": "flywheel-mcp",
  "env": { "PROJECT_PATH": "/path/to/vault" }
}
```

---

## Platform-Specific Notes

Create `.mcp.json` in your vault root. This file is typically gitignored since paths are machine-specific.

### Windows

**Requirement**: Wrap `npx` with `cmd /c` to avoid "Connection closed" errors.

```json
{
  "mcpServers": {
    "flywheel": {
      "command": "cmd",
      "args": ["/c", "npx", "-y", "@bencassie/flywheel-mcp"],
      "env": {
        "PROJECT_PATH": "C:/Users/YourName/Documents/ObsidianVault"
      }
    }
  }
}
```

**Note**: Use forward slashes (`/`) in paths, not backslashes.

### WSL (Windows Subsystem for Linux)

**Requirement**: Install `python-is-python3` for hooks to work.

```bash
sudo apt install python-is-python3
python --version  # Should show Python 3.x.x
```

**Paths**: Use `/mnt/c/...` format for Windows drives.

```json
{
  "mcpServers": {
    "flywheel": {
      "command": "npx",
      "args": ["-y", "@bencassie/flywheel-mcp"],
      "env": {
        "PROJECT_PATH": "/mnt/c/Users/YourName/Documents/ObsidianVault"
      }
    }
  }
}
```

### macOS / Linux

No special requirements. Use `npx` or global install.

```json
{
  "mcpServers": {
    "flywheel": {
      "command": "npx",
      "args": ["-y", "@bencassie/flywheel-mcp"],
      "env": {
        "PROJECT_PATH": "/Users/YourName/Documents/ObsidianVault"
      }
    }
  }
}
```

---

## Your First Commands

### MCP Tools (Available Immediately)

```bash
# Get vault overview
get_vault_stats()
# → Total notes, folders, links, tags, etc.

# Find disconnected notes
find_orphan_notes()
# → Notes with no backlinks

# Find key concepts (hubs)
find_hub_notes({ min_links: 5 })
# → Highly connected notes

# Search by tag or frontmatter
search_notes({ has_tag: "project" })
search_notes({ where: { status: "active" } })

# Who links to this note?
get_backlinks({ path: "MyNote.md" })

# How do two notes connect?
get_link_path({ from: "A.md", to: "B.md" })
```

### Skills (Requires Plugin Installation)

```bash
# Comprehensive health check
/vault-health
# → Orphans, hubs, broken links, stale notes, schema issues

# Add timestamped log entry
/auto-log "Finished project proposal"
# → Appends to today's daily note

# Find and fix broken wikilinks
/vault-fix-links
# → Detects broken links, suggests fixes

# Daily → weekly → monthly rollup
/rollup
# → Aggregates time-series notes

# Get tasks by due date
/vault-due
# → Overdue, this week, upcoming
```

---

## Verifying Installation

### Test MCP Connection

```bash
# In Claude Code, run:
get_vault_stats()

# Expected output:
{
  "total_notes": 42,
  "total_folders": 5,
  "total_links": 127,
  "total_tags": 18,
  ...
}
```

If you get "Tool not found", check:
1. `.mcp.json` is in project root or global config
2. `PROJECT_PATH` points to correct directory
3. Claude Code restarted after config change

### Test Plugin Installation

```bash
# In Claude Code, run:
/vault-health

# Expected output:
Vault Health Report
-------------------
Total notes: 42
Orphans: 3
Hubs: 5 (>5 links)
Broken links: 0
...
```

If skill not found:
```bash
/plugin install flywheel@bencassie-flywheel
```

---

## Configuration Options

### Environment Variables

| Variable | Required | Default | Purpose |
|----------|----------|---------|---------|
| `PROJECT_PATH` | ✓ YES | - | Path to Obsidian vault |
| `ENABLE_CACHE` | No | `true` | Cache vault index for performance |
| `LOG_LEVEL` | No | `info` | Logging verbosity (debug/info/warn/error) |

### Example with Options

```json
{
  "mcpServers": {
    "flywheel": {
      "command": "npx",
      "args": ["-y", "@bencassie/flywheel-mcp"],
      "env": {
        "PROJECT_PATH": "/path/to/vault",
        "ENABLE_CACHE": "true",
        "LOG_LEVEL": "debug"
      }
    }
  }
}
```

---

## Try a Demo Vault

**Want to see Flywheel in action before using on your vault?**

Try one of the 4 demo vaults with real-world scenarios:

```bash
# Clone Flywheel repo
git clone https://github.com/bencassie/flywheel.git

# Choose a demo (ordered by complexity)
cd flywheel/demos/carter-strategy    # Solo consultant (30 notes)
# OR
cd flywheel/demos/artemis-rocket     # Aerospace startup (65 notes)
# OR
cd flywheel/demos/startup-ops        # B2B SaaS (30 notes)
# OR
cd flywheel/demos/nexus-lab          # Research lab (30 notes)

# Start Claude Code and setup
claude
/setup-flywheel

# Try commands
/vault-health
/vault-orphans
get_backlinks({ path: "README.md" })
```

**Full demo guide**: [demos/README.md](../demos/README.md)

---

## Next Steps

### Learn the Patterns

**[Agentic Patterns](./AGENTIC_PATTERNS.md)** - How Flywheel makes AI workflows reliable:
- Graph-first navigation (10x token reduction)
- Agent chaining (hierarchical orchestration)
- Six Gates safety framework (enforced reliability)
- Parallel execution (speed up workflows)

### Explore the Tools

**[MCP Reference](./MCP_REFERENCE.md)** (coming soon) - All 40+ MCP tools:
- Graph tools (backlinks, hubs, orphans, paths)
- Search tools (semantic queries, temporal)
- Structure tools (headings, sections, tasks)
- Wikilink tools (suggest, validate, fix)

### Use the Skills

**[Skills Reference](./SKILLS_REFERENCE.md)** (coming soon) - All 33 plugin skills:
- Core: `/auto-log`, `/rollup`, `/task-add`
- Vault Health: `/vault-health`, `/vault-orphans`, `/vault-hubs`
- Graph: `/vault-backlinks`, `/vault-clusters`, `/vault-path`
- Schema: `/vault-schema`, `/vault-schema-check`

### Understand Safety

**[Six Gates](./SIX_GATES.md)** (coming soon) - Enforced safety framework:
- Gate 1: Read before write
- Gate 2: File exists check
- Gate 3: Agent chain validation
- Gate 4: Mutation confirmation
- Gate 5: MCP health check
- Gate 6: Post-write validation

---

## Troubleshooting

### MCP Not Connecting

**Symptom**: "Tool not found" when calling `get_vault_stats()`

**Solutions**:
1. Check `.mcp.json` exists in project root or global config
2. Verify `PROJECT_PATH` points to correct vault directory
3. Restart Claude Code after config changes
4. Check server logs: `~/.claude/debug/<session-id>.txt`

### Plugin Skills Not Working

**Symptom**: "/vault-health" shows "Command not found"

**Solution**:
```bash
# Install plugin
/plugin marketplace add bencassie/flywheel
/plugin install flywheel@bencassie-flywheel

# Verify
/plugin list
# Should show: flywheel@bencassie-flywheel (enabled)
```

### Windows "Connection Closed" Error

**Symptom**: MCP server immediately disconnects

**Solution**: Wrap `npx` with `cmd /c`:
```json
{
  "command": "cmd",
  "args": ["/c", "npx", "-y", "@bencassie/flywheel-mcp"]
}
```

### WSL Python Error

**Symptom**: Hooks fail with "python: command not found"

**Solution**:
```bash
sudo apt install python-is-python3
python --version  # Verify Python 3.x.x
```

**More help**: [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) (coming soon)

---

## Getting Help

- **Docs**: [../docs/](./README.md) - Full documentation
- **GitHub Issues**: https://github.com/bencassie/flywheel/issues
- **Demos**: [../demos/README.md](../demos/README.md) - Try it risk-free

---

**Version**: 1.6.2
**Last Updated**: 2026-01-03
**License**: MIT
