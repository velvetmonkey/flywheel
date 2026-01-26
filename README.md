# Flywheel - Query Your Markdown Like a Database

[![npm version](https://img.shields.io/npm/v/@bencassie/flywheel-mcp.svg)](https://www.npmjs.com/package/@bencassie/flywheel-mcp)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-blue.svg)](https://github.com/velvetmonkey/flywheel)

**Ask questions about your notes without Claude reading every file.**

Flywheel indexes your markdown vault and exposes it through 40+ graph-aware MCP tools. Claude queries the index—not the files—answering in ~50 tokens what would otherwise cost 5,000+.

---

## Install

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

(details)
(summary)(strong)Platform notes (Windows, WSL, custom vault path)(/strong)(/summary)

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

(/details)

Verify: `claude mcp list` should show `flywheel ✓`

---

## Core Concepts

Flywheel builds an in-memory index at startup. Understanding what gets indexed explains why queries are fast.

### The Index

| Indexed | Not Indexed |
|---------|-------------|
| Titles, aliases | File content |
| Wikilinks `[[Target]]` | Prose text |
| Frontmatter fields | Code blocks |
| Tags `#tag` | |
| Modification dates | |
| Headings structure | |

**Why this matters:** Graph queries use the index only—zero file reads. Content stays on disk until you explicitly need it.

### Wikilinks

`[[Target]]` creates a navigable link AND a graph connection.

```markdown
# INV-2025-047

**Client**: [[Acme Corp]]
**Project**: [[Acme Data Migration]]
```

This invoice now has outbound links to the client and project. The client gains backlinks from the invoice. Flywheel tracks all of this.

### Frontmatter

YAML at the top of a file creates typed, queryable fields:

```yaml
---
type: invoice
status: paid
client: "[[Acme Corp]]"
amount: 15000
due: 2025-12-15
---
```

Now you can query: "Find all paid invoices" or "What's the total amount for Acme Corp?"

### The Graph

Wikilinks create a graph. Flywheel exposes it:

- **Backlinks** — What notes link TO this one?
- **Forward links** — What does this note link TO?
- **Hub notes** — Most connected notes (key concepts, central entities)
- **Orphan notes** — Notes with no incoming links (disconnected)
- **Link paths** — How is note A connected to note B?

---

## What You Can Query

### Graph Intelligence

```
"What links to [[Acme Corp]]?"
"Find the path from [[Invoice]] to [[Project]]"
"Show hub notes with many connections"
"Find orphan notes—disconnected from the graph"
```

| Without Flywheel | With Flywheel |
|------------------|---------------|
| Read every file, grep for `[[Acme Corp]]`, parse results | `get_backlinks` → instant from index |
| ~5,000 tokens | ~50 tokens |

### Schema Queries

```
"Find notes where status is 'paid'"
"What fields exist in invoices/?"
"Show all unique client values"
"Find notes missing expected fields"
```

| Without Flywheel | With Flywheel |
|------------------|---------------|
| Read all files, parse YAML frontmatter, aggregate | `search_notes`, `get_frontmatter_schema` → index-only |
| ~3,000 tokens | ~80 tokens |

### Temporal Queries

```
"What changed in the last 7 days?"
"Find stale notes—important but neglected"
"Show activity summary for this month"
```

| Without Flywheel | With Flywheel |
|------------------|---------------|
| Stat every file, read content to check importance | `get_recent_notes`, `get_stale_notes` → file metadata + backlink count |
| ~10,000 tokens | ~100 tokens |

### Tasks & Structure

```
"Show open tasks across the vault"
"What's due this week?"
"Read the Financial Summary section from Acme Corp"
```

| Without Flywheel | With Flywheel |
|------------------|---------------|
| Read every file, regex for `- [ ]`, parse dates | `get_all_tasks` → indexed at startup |
| Read full file to get one section | `get_section_content` → returns only that heading |
| ~3,000 tokens | ~60 tokens |

---

## See It In Action

Here's what working with Flywheel looks like in Claude Code:

### Graph Query

```
You: "What depends on the Turbopump?"

┌─ QUERY ──────────────────────────────────────────┐
│ Source: Graph index (backlinks + forward links)  │
│ Tokens: ~80 vs ~4,000 without Flywheel           │
└──────────────────────────────────────────────────┘

Turbopump Dependencies
======================

Linked FROM (6 notes depend on this):
- Engine Design → Turbopump specifications
- Risk Register → R-003 delivery delay risk
- Project Roadmap → Critical path item
- ADR-001 Propellant Selection → Selection rationale
- Vendor Meeting Acme Aerospace → Supplier negotiations
- Upcoming Tests → Test 4 requires flight unit

Linked TO (4 dependencies):
- Propulsion System → Parent system
- Marcus Johnson → Component owner
- Precision Components Inc → Backup supplier
- Engine Controller → Control interface

Impact: High connectivity (10 links) - changes cascade widely.
```

### Schema Query

```
You: "Show me all pending invoices"

┌─ QUERY ──────────────────────────────────────────┐
│ Source: Frontmatter index (status: pending)      │
│ Tokens: ~50 vs ~1,500 without Flywheel           │
└──────────────────────────────────────────────────┘

Pending Invoices (1)
====================

INV-2025-048
  Client:  Acme Corp
  Amount:  $12,000
  Issued:  2025-12-15
  Due:     2026-01-15
  Project: Acme Data Migration

Total Outstanding: $12,000
```

### Temporal Query

```
You: "Find important notes I haven't touched in 2 weeks"

┌─ QUERY ──────────────────────────────────────────┐
│ Source: Modification dates + backlink counts     │
│ Tokens: ~100 vs ~8,000 without Flywheel          │
└──────────────────────────────────────────────────┘

Stale Hub Notes (3)
===================

ADR-001 Propellant Selection
  Last modified: 2025-08-20 (144 days ago)
  Backlinks: 12
  → Referenced by Engine Design, Risk Register, Project Roadmap

Safety Requirements
  Last modified: 2025-11-15 (57 days ago)
  Backlinks: 8
  → Referenced by Risk Register, Test Campaign, Fairing Design

Budget Tracker
  Last modified: 2025-12-01 (41 days ago)
  Backlinks: 6
  → Referenced by Project Roadmap, Risk Register

Recommendation: Review these high-impact notes for accuracy.
```

---

## Try a Demo

| You Are | Demo | Try Asking |
|---------|------|------------|
| **Consultant** | [Carter Strategy](./demos/carter-strategy/) | "How much have I billed Acme Corp?" |
| **Startup founder** | [Startup Ops](./demos/startup-ops/) | "Walk me through onboarding DataDriven" |
| **Researcher** | [Nexus Lab](./demos/nexus-lab/) | "How does AlphaFold connect to my experiment?" |
| **Technical lead** | [Artemis Rocket](./demos/artemis-rocket/) | "What's blocking the propulsion milestone?" |

```bash
cd demos/carter-strategy
claude
```

---

## Token Savings

| Operation | Traditional | With Flywheel | Savings |
|-----------|-------------|---------------|---------|
| "What's blocking X?" | ~5,000 tokens | ~50 tokens | **100x** |
| "Find stale notes" | ~10,000 tokens | ~100 tokens | **100x** |
| "Check overdue tasks" | ~3,000 tokens | ~80 tokens | **40x** |

Flywheel reads sections, not files. Queries index, not content.

---

## Why Flywheel

| Traditional AI | Flywheel |
|----------------|----------|
| Reads files to answer | Queries graph index |
| Sends full content | Sends metadata only |
| 5,000+ tokens per question | 50-200 tokens |
| Slow, expensive | Fast, cheap |

**Plus:**
- **Git-native** — your vault is version-controlled
- **Plain text** — future-proof, no lock-in
- **Privacy** — files stay on disk, only sections sent when needed
- **Editor-agnostic** — Obsidian, VSCode, vim, whatever

---

## Documentation

| Doc | What It Covers |
|-----|----------------|
| **[MCP Tools Reference](docs/MCP_REFERENCE.md)** | All 40+ tools with parameters |
| **[Query Guide](docs/QUERY_GUIDE.md)** | Graph, temporal, schema query patterns |
| **[How It Works](docs/HOW_IT_WORKS.md)** | Technical architecture |

---

## Platform Support

macOS / Linux / WSL / Windows

---

Apache 2.0 License | [GitHub](https://github.com/velvetmonkey/flywheel) | [Issues](https://github.com/velvetmonkey/flywheel/issues)
