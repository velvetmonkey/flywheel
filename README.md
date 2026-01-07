# Flywheel - Query Your Markdown Like a Database

[![npm version](https://img.shields.io/npm/v/@bencassie/flywheel-mcp.svg)](https://www.npmjs.com/package/@bencassie/flywheel-mcp)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-blue.svg)](https://github.com/bencassie/flywheel)

**Ask questions about your notes without Claude reading every file.**

Flywheel indexes your markdown vault and exposes it through 40+ graph-aware tools. Claude queries the index—not the files—answering in ~50 tokens what would otherwise cost 5,000+.

---

## The Query Paradigm

```
Traditional AI:                    Flywheel:
"What's blocking the launch?"      "What's blocking the launch?"
→ Read 50 files                    → Query the graph index
→ ~50,000 tokens                   → ~50 tokens
→ 30+ seconds                      → <1 second
```

Most AI reads files to find answers. Flywheel indexes structure, relationships, and metadata at startup—then Claude queries the index directly.

### What You Can Query

**Graph intelligence:**
```
"What links to [[Project Alpha]]?"
"Find the path from [[Problem]] to [[Solution]]"
"What notes do Sarah and Mike both reference?"
"Show hub notes with many connections"
```

**Temporal queries:**
```
"What changed in the last 7 days?"
"Find stale notes—important but neglected"
"Show activity for December"
```

**Schema queries:**
```
"What fields exist in projects/?"
"Find notes where status is 'blocked'"
"Show all unique client values"
```

**Search:**
```
"Find notes tagged #urgent in meetings/"
"List everything with 'review' in the title"
```

**[Full Query Guide →](docs/QUERY_GUIDE.md)**

---

## How It Works

```
┌─────────────────────────────────────────┐
│  YOU (thinking, deciding, creating)     │
├─────────────────────────────────────────┤
│  CLAUDE CODE (AI co-processor)          │
│  - Asks questions in natural language   │
│  - Gets answers from the graph          │
│  - Reads files only when needed         │
├─────────────────────────────────────────┤
│  FLYWHEEL (graph intelligence)          │  ← The Index
│  - 40+ query tools                      │
│  - 50+ workflow commands                │
│  - Auto-curation hooks                  │
├─────────────────────────────────────────┤
│  YOUR VAULT (plain markdown)            │
│  - Edit with any tool you want          │
│  - Obsidian, VSCode, vim, whatever      │
│  - Git-versioned, future-proof          │
└─────────────────────────────────────────┘
```

At startup, Flywheel scans your vault and builds an in-memory graph:
- **Titles and aliases** → entity lookup
- **Wikilinks** → relationship traversal
- **Frontmatter** → schema queries
- **Tags** → filtering
- **Modification dates** → temporal analysis

Claude queries this index. Files stay on disk.

---

## Pre-Built Commands

Beyond queries, Flywheel includes 50+ workflow commands:

| Category | Examples |
|----------|----------|
| **Daily ops** | `/log research findings`, `/rollup` (daily → weekly → monthly) |
| **Graph analysis** | `/vault-health`, `/vault-orphans`, `/vault-hubs` |
| **Schema management** | `/vault-schema`, `/normalize-note`, `/promote-frontmatter` |
| **Tasks** | `/vault-tasks`, `/vault-due`, `/extract-actions` |
| **Reviews** | `/weekly-review`, `/okr-review`, `/standup-rollup` |

```
You: "log the client call with Acme"

Claude:
- Queries your entities for [[Acme Corp]]
- Reads only the ## Log section of today's daily note
- Appends timestamped entry with wikilinks
- Confirms: "✓ Added log entry with 3 entities linked"
```

**[Full Command Reference →](docs/SKILLS_REFERENCE.md)**

---

## Build Your Own Skills

Skills are markdown files that teach Claude workflows. No code required.

```markdown
# packages/claude-plugin/skills/weekly-digest/SKILL.md

---
name: weekly-digest
description: Generate digest of vault activity
trigger_keywords:
  - "weekly digest"
  - "what happened this week"
allowed-tools: Read, Write, mcp__flywheel__get_recent_notes
---

## Process

1. Query recent activity (last 7 days)
2. Group by folder
3. Generate summary
4. Present to user
```

When you say "weekly digest", Claude follows your process.

**[Building Skills Guide →](docs/BUILDING_SKILLS.md)**

---

## Quick Start

### 1. Install

```bash
/plugin marketplace add bencassie/flywheel
/plugin install flywheel@bencassie-flywheel
```

### 2. Setup

```
/setup-flywheel
```

Claude configures everything for your platform.

### 3. Try Queries

```
"check vault health"           → Graph + schema diagnostics
"find orphan notes"            → Disconnected notes
"what links to [[My Note]]"    → Backlink traversal
"show notes modified today"    → Temporal query
```

**[Full Installation Guide →](docs/GETTING_STARTED.md)**

---

## See It In Action

Pick a demo vault. Ask questions.

| You Are | Demo | Try Asking |
|---------|------|------------|
| **Consultant** | [Carter Strategy](./demos/carter-strategy/) | "How much have I billed Acme Corp?" |
| **Startup founder** | [Startup Ops](./demos/startup-ops/) | "Walk me through onboarding DataDriven" |
| **Researcher** | [Nexus Lab](./demos/nexus-lab/) | "How does AlphaFold connect to my experiment?" |
| **Technical lead** | [Artemis Rocket](./demos/artemis-rocket/) | "What's blocking the propulsion milestone?" |

```bash
cd demos/carter-strategy
claude
/setup-flywheel
"how much have I billed this quarter?"
```

---

## The Flywheel Loop

Your vault gets smarter over time:

```
┌────────────────────────────────────────────────────────────────┐
│                     THE FLYWHEEL LOOP                          │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  WIKILINKS ←──────────────────────────────→ FRONTMATTER        │
│  [[Acme Corp]]                              status: active     │
│  [[Sarah Chen]]                             contact: Sarah     │
│                                             rate: $250/hr      │
│         ↑                                          ↑           │
│         │         AUTO-CURATION HOOKS              │           │
│         │    ┌──────────────────────────┐          │           │
│         └────│ wikilink-auto.py         │──────────┘           │
│              │ frontmatter-auto.py      │                      │
│              └──────────────────────────┘                      │
│                         ↓                                      │
│         After every Edit/Write, hooks auto-apply:              │
│         ✓ Wikilinks to known entities                          │
│         ✓ Frontmatter from folder patterns                     │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

1. **You write naturally** — hooks add links automatically
2. **More links** → better graph queries
3. **Consistent frontmatter** → better schema queries
4. **Each interaction improves the next**

---

## Token Savings (Real Numbers)

| Operation | Traditional | With Flywheel | Savings |
|-----------|-------------|---------------|---------|
| "What's blocking X?" | ~5,000 tokens | ~50 tokens | **100x** |
| "Find stale notes" | ~10,000 tokens | ~100 tokens | **100x** |
| "/log research" | ~800 tokens | ~42 tokens | **19x** |
| "do a rollup" (7 days) | ~7,000 tokens | ~700 tokens | **10x** |

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
- **Git-native** — your business history, versioned
- **Plain text** — future-proof, no lock-in
- **Extensible** — add your own skills, agents, hooks
- **Privacy** — files stay on disk, only sections sent when needed

---

## Documentation

| Doc | What It Covers |
|-----|----------------|
| **[Query Guide](docs/QUERY_GUIDE.md)** | Graph, temporal, schema queries |
| **[Getting Started](docs/GETTING_STARTED.md)** | Installation, platform setup |
| **[Building Skills](docs/BUILDING_SKILLS.md)** | Create custom workflows |
| **[MCP Tools](docs/MCP_REFERENCE.md)** | All 40+ graph query tools |
| **[Skills Reference](docs/SKILLS_REFERENCE.md)** | 50+ pre-built commands |
| **[Six Gates](docs/SIX_GATES.md)** | Safety framework |

---

## Platform Support

macOS / Linux / WSL / Windows

**[Platform Setup →](docs/GETTING_STARTED.md#platform-specific-notes)**

---

Apache 2.0 License | [GitHub](https://github.com/bencassie/flywheel) | [Issues](https://github.com/bencassie/flywheel/issues)
