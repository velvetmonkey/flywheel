> **Part of the Flywheel Suite:** This is the read-only graph intelligence server. See [Flywheel Crank](https://github.com/velvetmonkey/flywheel-crank) for safe vault mutations with auto-commit and undo.

<div align="center">
  <img src="header.png" alt="Flywheel" width="256"/>
</div>

# Flywheel

### Stop burning tokens. Start building agents.

[![npm version](https://img.shields.io/npm/v/@velvetmonkey/flywheel-mcp.svg)](https://www.npmjs.com/package/@velvetmonkey/flywheel-mcp)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache--2.0-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0)
[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-blue.svg)](https://github.com/velvetmonkey/flywheel)

---

Claude reading your entire vault on every query? **~5,000 tokens burned.**

Flywheel queries an index instead. **~50 tokens.** That's up to 100x savings.

**The real win:** Your agents can now query your knowledge *hundreds of times* during long-running tasks without blowing up the context window.

---

## Quick Start

**Prerequisites:** Node.js 18+, Claude Code or MCP client, an Obsidian vault (or any markdown folder)

**1. Create `.mcp.json`** in your vault root:

```json
{
  "mcpServers": {
    "flywheel": {
      "command": "npx",
      "args": ["-y", "@velvetmonkey/flywheel-mcp"]
    }
  }
}
```

> **Windows:** Use `"command": "cmd", "args": ["/c", "npx", "-y", "@velvetmonkey/flywheel-mcp"]`

**2. Restart Claude Code** and verify with `claude mcp list` — you should see `flywheel ✓`

That's it. Flywheel uses the current directory as your vault—no config needed.

See [Configuration](docs/CONFIGURATION.md) for environment variables, tool filtering, and platform setup.

---

## See It In Action

### Finding What You Need

```
You: Find everything about authentication

Claude: [uses search_notes]

Found 7 notes mentioning authentication:
- Auth Architecture.md (hub note, 12 backlinks)
- JWT Implementation.md
- OAuth Provider Setup.md
...

Auth Architecture is your hub - want me to show what links to it?
```

### Tracking Work

```
You: Show me all pending meetings for Project Alpha

Claude: [uses query_notes with frontmatter filter]

Found 3 pending meetings:
- meetings/2026-01-30-alpha-kickoff.md (scheduled for tomorrow)
- meetings/2026-02-05-alpha-review.md
- meetings/2026-02-12-alpha-demo.md

Each has attendees, agenda, and action items in frontmatter.
```

### Discovering Relationships

```
You: What connects my meeting notes to the Q4 strategy?

Claude: [uses get_shortest_path]

Found a 3-hop connection:
  Meeting Notes → [[Client Feedback]] → [[Product Roadmap]] → Q4 Strategy
```

---

## Try a Demo

5 production-ready vaults representing real knowledge work personas:

| Demo | Persona | Notes | Try Asking |
|------|---------|-------|------------|
| **[carter-strategy](demos/carter-strategy/)** | Solo Consultant | 32 | "How much have I billed Acme Corp?" |
| **[artemis-rocket](demos/artemis-rocket/)** | Aerospace Engineer | 65 | "What's blocking the propulsion milestone?" |
| **[startup-ops](demos/startup-ops/)** | SaaS Co-Founder | 31 | "Walk me through onboarding DataDriven" |
| **[nexus-lab](demos/nexus-lab/)** | PhD Researcher | 32 | "How does AlphaFold connect to my experiment?" |
| **[solo-operator](demos/solo-operator/)** | Content Creator | 19 | "What's my financial runway?" |

```bash
git clone https://github.com/velvetmonkey/flywheel.git
cd flywheel/demos/artemis-rocket && claude
```

---

## What This Unlocks

- **Graph intelligence** — backlinks, orphans, hubs, connection paths
- **Vault health monitoring** — find disconnected notes, stale hubs, broken links
- **Connection discovery** — "how does X relate to Y?" answered in milliseconds
- **Schema queries** on frontmatter without reading files
- **Agentic workflows** that query your knowledge hundreds of times without token bloat

---

## 44 Tools. Three Query Types.

### Graph Queries — "What connects to what?"

```
"What depends on [[Turbopump]]?"        → 6 backlinks, 4 critical dependencies
"Find orphan notes"                     → 12 disconnected notes need linking
"Path from [[Invoice]] to [[Project]]"  → 2-hop path via [[Client]]
```

### Schema Queries — "Find notes where..."

```
"All invoices where status is 'pending'"  → 3 notes, $47K outstanding
"Notes missing required fields"           → 12 incomplete records
```

### Temporal Queries — "What changed when?"

```
"Activity in the last 7 days"     → 23 notes modified, 4 new
"Stale but important notes"       → 5 hub notes untouched in 30+ days
```

---

## Why Markdown + Graph?

- **Git-native** — version-controlled knowledge
- **Plain text** — future-proof, zero lock-in
- **Privacy** — files stay local, only what you need gets sent
- **Editor-agnostic** — Obsidian, VSCode, Cursor, vim, whatever
- **AI-native** — 44 tools purpose-built for agent workflows

---

## Docs

- **[Configuration](docs/CONFIGURATION.md)** — Environment variables, tool presets, platform setup
- **[MCP Tools Reference](docs/MCP_REFERENCE.md)** — All 44 tools
- **[Query Guide](docs/QUERY_GUIDE.md)** — Patterns and examples
- **[How It Works](docs/HOW_IT_WORKS.md)** — Architecture and token savings
- **[Vault Health](docs/VAULT_HEALTH.md)** — Monitor and improve vault structure
- **[Performance](docs/PERFORMANCE.md)** — Benchmarks and optimization
- **[Privacy](docs/PRIVACY.md)** — Data handling and security
- **[Troubleshooting](docs/TROUBLESHOOTING.md)** — Common issues and fixes

---

macOS / Linux / WSL / Windows

Apache-2.0 License · [GitHub](https://github.com/velvetmonkey/flywheel) · [Issues](https://github.com/velvetmonkey/flywheel/issues)
