# Flywheel

### Stop burning tokens. Start building agents.

[![npm version](https://img.shields.io/npm/v/@bencassie/flywheel-mcp.svg)](https://www.npmjs.com/package/@bencassie/flywheel-mcp)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-blue.svg)](https://github.com/velvetmonkey/flywheel)

Claude reading your entire vault on every query? **5,000 tokens burned.**

Flywheel queries an index instead. **50 tokens.** That's 100x savings.

**The real win:** Your agents can now query your knowledge *hundreds of times* during long-running tasks without blowing up the context window.

You couldn't do this before. Now you can.

---

## What This Unlocks

- **Agentic workflows** that query your vault repeatedly without token bloat
- **Long-running tasks** that reference your knowledge throughout execution
- **Graph intelligence** — backlinks, forward links, hub notes — all instant
- **Schema queries** on frontmatter without reading files
- **Zero context pollution** — files stay on disk until you need them

---

## Install (30 seconds)

Add to `.mcp.json` in your vault root:

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

That's it. Flywheel uses the current directory as your vault—no config needed.

<details>
<summary><strong>Platform notes (Windows, WSL, custom vault path)</strong></summary>

**Windows (native):**
```json
{
  "mcpServers": {
    "flywheel": {
      "command": "cmd",
      "args": ["/c", "npx", "-y", "@bencassie/flywheel-mcp"]
    }
  }
}
```

**Different vault location:**
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

**WSL:** Use `npx` directly (not `cmd /c`), with `/mnt/c/...` paths.

</details>

Verify with `claude mcp list` — you should see `flywheel ✓`

---

## How It Works

Flywheel indexes structure, not content:

| Indexed (instant queries) | Not Indexed (stays on disk) |
|---------------------------|----------------------------|
| Titles, aliases, wikilinks | File content, prose |
| Frontmatter, tags | Code blocks |
| Headings, modification dates | |

Graph queries never read files. Content only loads when you explicitly need it.

---

## 44 Tools. Three Query Types.

### Graph Queries — "What connects to what?"

```
"What depends on [[Turbopump]]?"  → 6 notes link to it, 4 dependencies found
"How does [[Invoice]] connect to [[Project]]?"  → 2-hop path via [[Client]]
"Find hub notes"  → 8 notes with 10+ connections
```

### Schema Queries — "Find notes where..."

```
"All invoices where status is 'pending'"  → 3 notes, $47K outstanding
"What fields exist in meetings/?"  → attendees, date, decisions, follow-ups
"Notes missing required fields"  → 12 incomplete records
```

### Temporal Queries — "What changed when?"

```
"Activity in the last 7 days"  → 23 notes modified, 4 new
"Stale but important notes"  → 5 hub notes untouched in 30+ days
"What was I working on with [[Client X]]?"  → Timeline of related edits
```

---

## The Difference

| Query | Without Flywheel | With Flywheel |
|-------|------------------|---------------|
| "What depends on X?" | Read files, grep, parse → ~5,000 tokens | Index query → **~50 tokens** |
| "Find stale important notes" | Stat files, read content → ~10,000 tokens | Index lookup → **~100 tokens** |
| "Invoices where status = paid" | Read files, parse YAML → ~3,000 tokens | Frontmatter query → **~80 tokens** |

**Now multiply by 50 queries in an agentic workflow.** That's the difference between possible and impossible.

---

## Try a Demo

5 ready-to-use vaults. `cd` in and start asking questions.

| Demo | Try Asking |
|------|------------|
| [artemis-rocket](./demos/artemis-rocket/) | "What's blocking the propulsion milestone?" |
| [carter-strategy](./demos/carter-strategy/) | "How much have I billed Acme Corp?" |
| [nexus-lab](./demos/nexus-lab/) | "How does AlphaFold connect to my experiment?" |
| [solo-operator](./demos/solo-operator/) | "What's my financial runway?" |
| [startup-ops](./demos/startup-ops/) | "Walk me through onboarding DataDriven" |

```bash
cd demos/artemis-rocket && claude
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

- **[MCP Tools Reference](docs/MCP_REFERENCE.md)** — All 44 tools
- **[Query Guide](docs/QUERY_GUIDE.md)** — Patterns and examples
- **[How It Works](docs/HOW_IT_WORKS.md)** — Architecture

---

macOS / Linux / WSL / Windows

Apache 2.0 License · [GitHub](https://github.com/velvetmonkey/flywheel) · [Issues](https://github.com/velvetmonkey/flywheel/issues)
