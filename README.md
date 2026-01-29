# Flywheel

### Stop burning tokens. Start building agents.

[![npm version](https://img.shields.io/npm/v/@velvetmonkey/flywheel-mcp.svg)](https://www.npmjs.com/package/@velvetmonkey/flywheel-mcp)
[![License: AGPL-3.0](https://img.shields.io/badge/License-AGPL--3.0-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-blue.svg)](https://github.com/velvetmonkey/flywheel)

Claude reading your entire vault on every query? **~5,000 tokens burned.**

Flywheel queries an index instead. **~50 tokens.** That's up to 100x savings.

**The real win:** Your agents can now query your knowledge *hundreds of times* during long-running tasks without blowing up the context window.

You couldn't do this before. Now you can.

---

## Your Vault as a Knowledge Graph

```
                        ┌─────────────────────────────────────────────────────┐
                        │              Your Vault (65 notes)                  │
                        │                        · · ·                        │
                        │    ·  Orphan  ·              ·  Orphan  ·           │
                        │         ↓                        ↓                  │
                        └─────────────────────────────────────────────────────┘
                                               │
                 ┌─────────────────────────────┼─────────────────────────────┐
                 │                             │                             │
                 ▼                             ▼                             ▼
    ┌────────────────────┐       ┌────────────────────┐       ┌────────────────────┐
    │   PDR Review       │──────▶│    Team Roster     │◀──────│  Year End Review   │
    │   ───────────      │       │    ───────────     │       │   ──────────────   │
    │   type: meeting    │       │   type: hub        │       │   type: meeting    │
    │   date: 2025-12-18 │       │   status: active   │       │   date: 2025-12-30 │
    │   attendees: [5]   │       │   owner: [[Sarah]] │       │   attendees: [8]   │
    └────────────────────┘       └────────────────────┘       └────────────────────┘
              │                     │    │    │    │                    │
              │          ┌──────────┘    │    │    └──────────┐        │
              │          ▼               ▼    ▼               ▼        │
              │   ┌──────────────┐ ┌──────────────┐ ┌──────────────┐   │
              │   │ Sarah Chen   │ │ Marcus J.    │ │ Elena R.     │   │
              │   │ ──────────── │ │ ──────────── │ │ ──────────── │   │
              │   │ role: Lead   │ │ role: Prop.  │ │ role: Avion. │   │
              └──▶│ team: Core   │ │ team: Core   │ │ team: Core   │◀──┘
                  └──────────────┘ └──────────────┘ └──────────────┘
                         │                │                │
                         ▼                ▼                ▼
                  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
                  │ GNC System   │ │ Turbopump    │ │ Avionics     │
                  │ ──────────── │ │ ──────────── │ │ ──────────── │
                  │ status: test │ │ status: dev  │ │ status: done │
                  │ risk: medium │ │ risk: high   │ │ risk: low    │
                  └──────────────┘ └──────────────┘ └──────────────┘

Legend:  ─────▶ Wikilink (edge)     │ type: meeting │ Frontmatter (attributes)
         ◀───── Backlink            │ status: done  │ Queryable via Flywheel
```

**Notes are nodes. Wikilinks are edges. Frontmatter is queryable metadata.**

---

## See It In Action

Real conversations with Claude using Flywheel:

### Finding Connections

```
You: What connects my meeting notes to the Q4 strategy?

Claude: Let me trace the path through your vault.
[uses get_shortest_path]

Found a 3-hop connection:
  Meeting Notes → [[Client Feedback]] → [[Product Roadmap]] → Q4 Strategy

The link runs through client feedback captured in your October meetings.
```

### Vault Health Check

```
You: Is my vault healthy?

Claude: Let me check the key metrics.
[uses get_orphan_notes, get_hub_notes, get_dead_ends]

Your vault has 847 notes:
- 12 orphan notes (no backlinks) - consider linking these
- 8 hub notes (10+ connections) - your knowledge centers
- 3 stale hubs not updated in 30+ days - may need attention

Would you like me to list the orphans?
```

### Semantic Search

```
You: Find everything about authentication

Claude: [uses search_notes]

Found 7 notes mentioning authentication:
- Auth Architecture.md (hub note, 12 backlinks)
- JWT Implementation.md
- OAuth Provider Setup.md
- Login Flow.md
- Session Management.md
- Security Audit Q3.md
- API Authentication.md

Auth Architecture is your hub - want me to show what links to it?
```

### Frontmatter as Queryable Attributes

```
You: Show me all pending meetings for Project Alpha

Claude: [uses query_notes with frontmatter filter]

Found 3 pending meetings:
- meetings/2026-01-30-alpha-kickoff.md (scheduled for tomorrow)
- meetings/2026-02-05-alpha-review.md
- meetings/2026-02-12-alpha-demo.md

Each has attendees, agenda, and action items in frontmatter.
Want me to show the attendees across all three?
```

### Combining Graph + Attributes

```
You: What meetings mention Sam Chen, and are any of them overdue?

Claude: [uses get_backlinks for "Sam Chen", filters by type: "meeting"]

Sam Chen is mentioned in 5 meetings.

[uses query_notes to check status field]

2 are overdue (status: "pending", date in past):
- meetings/2026-01-15-sprint-planning.md - overdue by 14 days
- meetings/2026-01-22-design-review.md - overdue by 7 days

Want me to update their status or flag them for follow-up?
```

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

## Installation

### Prerequisites

- **Node.js 18+** installed ([download here](https://nodejs.org))
- **Claude Code** or compatible MCP client ([install guide](https://github.com/anthropics/claude-code))
- An **Obsidian vault** (or any markdown folder)

### Quick Start (30 seconds)

**1. Create MCP config** in your vault root as `.mcp.json`:

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

> **📁 Config File Scopes:**
> - **`.mcp.json`** (in vault root) — **PROJECT-SCOPED** config. Recommended for vault-specific servers like Flywheel. Can be version controlled.
> - **`~/.claude.json`** (in home directory) — **USER-SCOPED** config. For personal servers used across all projects (e.g., filesystem, git).
>
> **Use `.mcp.json` in your vault root** for Flywheel — this makes the server available only when working in that vault, keeping your setup clean and portable.

**2. Restart Claude Code** (if already running)

**3. Verify**: Run `claude mcp list` — you should see `flywheel ✓`

That's it. Flywheel uses the current directory as your vault—no config needed.

<details>
<summary><strong>Platform notes (Windows, WSL, custom vault path)</strong></summary>

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

</details>

<details>
<summary><strong>File watching (auto-rebuild on changes)</strong></summary>

**Enable file watching** to automatically rebuild the index when vault files change:

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

**Optional: Custom debounce delay** (default is 500ms):

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

**How it works:**
- Watches vault directory for `.md` file changes
- Automatically ignores dotfiles (`.obsidian`, `.trash`, etc.)
- Debounces rapid changes to avoid excessive rebuilds
- Uses `awaitWriteFinish` to prevent indexing partial writes
- Logs rebuild events to stderr

**When to use:** Enable file watching if you're editing notes while an agent is actively working in your vault. Without watching, the agent sees a snapshot from when the MCP server started.

**Performance:** Minimal overhead. Rebuilds only trigger on `.md` file changes, not every filesystem event.

</details>

### Test It

Try your first query to confirm Flywheel is working:

```bash
cd /path/to/your/vault
claude
```

Then ask:
- **"Find my hub notes"** → See your most-connected notes
- **"What notes did I modify this week?"** → Recent activity
- **"Show me orphan notes"** → Disconnected notes that need linking

### Troubleshooting

| Issue | Solution |
|-------|----------|
| **`npx: command not found`** | Node.js isn't installed. [Download Node.js 18+](https://nodejs.org) |
| **`flywheel ✗` in mcp list** | Wrong file location. `.mcp.json` must be in your vault root |
| **"No notes found"** | Not in vault directory. Run `claude` from inside your vault folder |
| **Windows: spawn errors** | Use `cmd /c npx` config (see Platform notes above) |
| **MCP server won't start** | Check Node version: `node --version` (need 18+) |

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

| Demo | Persona | Notes | Try Asking |
|------|---------|-------|------------|
| **[carter-strategy](demos/carter-strategy/)** | Solo Consultant | 32 | "How much have I billed Acme Corp?" |
| **[artemis-rocket](demos/artemis-rocket/)** | Aerospace Engineer | 65 | "What's blocking the propulsion milestone?" |
| **[startup-ops](demos/startup-ops/)** | SaaS Co-Founder | 31 | "Walk me through onboarding DataDriven" |
| **[nexus-lab](demos/nexus-lab/)** | PhD Researcher | 32 | "How does AlphaFold connect to my experiment?" |
| **[solo-operator](demos/solo-operator/)** | Content Creator | 19 | "What's my financial runway?" |

```bash
# Clone and explore
git clone https://github.com/velvetmonkey/flywheel.git
cd flywheel/demos/artemis-rocket

# Start Claude Code
claude
```

### Validation Status

All demos are production-ready:

- ✅ **179 total markdown files** with 100% valid YAML
- ✅ **Persona-specific workflows** (invoices, ADRs, experiments, etc.)
- ✅ **Realistic knowledge graphs** with hub notes and bidirectional linking
- ✅ **Authentic linking patterns** from sparse (22%) to dense (94%) resolution

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

AGPL-3.0 License · [GitHub](https://github.com/velvetmonkey/flywheel) · [Issues](https://github.com/velvetmonkey/flywheel/issues)
