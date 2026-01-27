# Flywheel

### Stop burning tokens. Start building agents.

[![npm version](https://img.shields.io/npm/v/@velvetmonkey/flywheel-mcp.svg)](https://www.npmjs.com/package/@velvetmonkey/flywheel-mcp)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-blue.svg)](https://github.com/velvetmonkey/flywheel)

Claude reading your entire vault on every query? **~5,000 tokens burned.**

Flywheel queries an index instead. **~50 tokens.** That's up to 100x savings.

**The real win:** Your agents can now query your knowledge *hundreds of times* during long-running tasks without blowing up the context window.

You couldn't do this before. Now you can.

---

## 44 Tools. Three Query Types.

### Graph Queries — "What connects to what?"

```
"What depends on [[Turbopump]]?"        → 6 backlinks, 4 critical dependencies
"Find orphan notes"                     → 12 disconnected notes need linking
"Show hub notes"                        → 8 knowledge centers with 10+ connections
"Path from [[Invoice]] to [[Project]]"  → 2-hop path via [[Client]]
"Find bidirectional links"              → 23 strongly connected note pairs
"What's connected to [[Q1 Goals]]?"     → Forward links, backlinks, shared neighbors
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

## Why Graph Intelligence Matters

Most file-based tools treat your vault as a filesystem. Flywheel treats it as a **knowledge graph**.

### Vault Health Metrics

| Metric | What It Reveals | Why It Matters |
|--------|-----------------|----------------|
| **Orphan notes** | Notes with zero backlinks | Disconnected knowledge that needs integration |
| **Hub notes** | Notes with 10+ connections | Your vault's knowledge centers — keep them current |
| **Dead ends** | Notes linked TO but linking to nothing | Information sinks that should connect outward |
| **Stale hubs** | Important notes not updated recently | Critical knowledge drifting out of date |

### What Other MCPs Don't Have

Generic file MCPs can read and write files. **Only Flywheel understands:**

- The **link structure** between your notes
- Which notes are **orphaned** vs **well-connected**
- How ideas **flow** through your vault via wikilinks
- When your **knowledge graph is degrading** (stale hubs, broken links)

This is the difference between a filesystem and a **second brain**.

### Connection Discovery

Your vault contains relationships you haven't noticed:

```
"Path from [[Meeting Notes]] to [[Q4 Strategy]]"
→ Meeting Notes → [[Client Feedback]] → [[Product Roadmap]] → Q4 Strategy

"Common neighbors of [[React]] and [[Performance]]"
→ Both link to [[Virtual DOM]], [[Memoization]], [[Bundle Size]]
```

**Graph intelligence reveals the hidden structure of your thinking.**

---

## What This Unlocks

- **Graph intelligence** — backlinks, orphans, hubs, connection paths — your vault as a queryable knowledge graph
- **Vault health monitoring** — find disconnected notes, stale hubs, broken links instantly
- **Connection discovery** — "how does X relate to Y?" answered in milliseconds
- **Schema queries** on frontmatter without reading files
- **Agentic workflows** that query your knowledge hundreds of times without token bloat

---

## Install (30 seconds)

Add to `.mcp.json` in your vault root:

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

That's it. Flywheel uses the current directory as your vault—no config needed.

(details)
(summary)(strong)Platform notes (Windows, WSL, custom vault path)(/strong)(/summary)

**Windows (native):**
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

**Different vault location:**
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

**WSL:** Use `npx` directly (not `cmd /c`), with `/mnt/c/...` paths.

(/details)

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

## The Difference

| Query | Without Flywheel | With Flywheel |
|-------|------------------|---------------|
| **Graph Intelligence** | | |
| "What depends on X?" | Impossible without reading every file | Instant backlink query → **~50 tokens** |
| "Find orphan notes" | Not possible — no link awareness | Index scan → **~80 tokens** |
| "Hub notes needing updates" | Manual review of entire vault | Graph + temporal query → **~100 tokens** |
| **Schema Queries** | | |
| "Invoices where status = paid" | Read files, parse YAML → ~3,000 tokens | Frontmatter query → **~80 tokens** |
| "Notes missing required fields" | Read and validate every file | Schema scan → **~100 tokens** |

**Other MCPs:** File read/write only. No link awareness. No graph queries. No vault health.

**Flywheel:** Your vault is a queryable knowledge graph. Connections, orphans, hubs, paths — all instant.

**Now multiply by 50 queries in an agentic workflow.** That's the difference between possible and impossible.

---

## Try a Demo

5 production-ready vaults representing real knowledge work personas. Each vault is fully validated with 100% valid YAML and authentic linking patterns.

| Demo | Persona | Notes | Try Asking | Validation |
|------|---------|-------|------------|------------|
| **[carter-strategy](demos/carter-strategy/)** | Solo Consultant | 32 | "How much have I billed Acme Corp?" | [✅ Report](demos/carter-strategy/VALIDATION_REPORT.md) |
| **[artemis-rocket](demos/artemis-rocket/)** | Aerospace Engineer | 65 | "What's blocking the propulsion milestone?" | [✅ Report](demos/artemis-rocket/VALIDATION-REPORT.md) |
| **[startup-ops](demos/startup-ops/)** | SaaS Co-Founder | 31 | "Walk me through onboarding DataDriven" | [✅ Report](demos/startup-ops/VALIDATION_REPORT.md) |
| **[nexus-lab](demos/nexus-lab/)** | PhD Researcher | 32 | "How does AlphaFold connect to my experiment?" | [✅ 85%+ links](demos/nexus-lab/README.md) |
| **[solo-operator](demos/solo-operator/)** | Content Creator | 19 | "What's my financial runway?" | [✅ Report](demos/solo-operator/VALIDATION_REPORT.md) |

```bash
# Clone and explore
git clone https://github.com/velvetmonkey/flywheel.git
cd flywheel/demos/artemis-rocket

# Start Claude Code
claude
```

### Validation Status

All demos are comprehensively tested and production-ready:

- ✅ **179 total markdown files** with 100% valid YAML
- ✅ **Persona-specific workflows** validated (invoices, ADRs, experiments, etc.)
- ✅ **Realistic knowledge graphs** with hub notes and bidirectional linking
- ✅ **Authentic linking patterns** from sparse (22%) to dense (94%) resolution

📋 **See [DEMO_VALIDATION.md](DEMO_VALIDATION.md) for comprehensive validation report**

---

## Why Markdown + Graph?

- **Git-native** — version-controlled knowledge
- **Plain text** — future-proof, zero lock-in
- **Privacy** — files stay local, only what you need gets sent
- **Editor-agnostic** — Obsidian, VSCode, Cursor, vim, whatever
- **AI-native** — 44 tools purpose-built for agent workflows

---

## Docs

**User Guides:**
- **[MCP Tools Reference](docs/MCP_REFERENCE.md)** — All 44 tools
- **[Query Guide](docs/QUERY_GUIDE.md)** — Patterns and examples
- **[How It Works](docs/HOW_IT_WORKS.md)** — Architecture and token savings

**Developer:**
- **[Architecture](docs/ARCHITECTURE.md)** — MCP server design and tool development
- **[Documentation Index](docs/)** — Full documentation directory

---

macOS / Linux / WSL / Windows

Apache 2.0 License · [GitHub](https://github.com/velvetmonkey/flywheel) · [Issues](https://github.com/velvetmonkey/flywheel/issues)
