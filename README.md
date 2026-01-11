# Flywheel - Query Your Markdown Like a Database

[![npm version](https://img.shields.io/npm/v/@velvetmonkey/flywheel-mcp.svg)](https://www.npmjs.com/package/@velvetmonkey/flywheel-mcp)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-blue.svg)](https://github.com/velvetmonkey/flywheel)

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

## Quick Start

### 1. Install

```bash
/plugin marketplace add velvetmonkey/flywheel
/plugin install flywheel@velvetmonkey-flywheel
```

### 2. Pick a Demo

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
```

### 3. Try Queries

```
"find orphan notes"            → Disconnected notes
"what links to [[My Note]]"    → Backlink traversal
"show notes modified today"    → Temporal query
"how much have I billed this quarter?"
```

**[Full Installation Guide →](docs/GETTING_STARTED.md)**

---

## Token Savings (Real Numbers)

| Operation | Traditional | With Flywheel | Savings |
|-----------|-------------|---------------|---------|
| "What's blocking X?" | ~5,000 tokens | ~50 tokens | **100x** |
| "Find stale notes" | ~10,000 tokens | ~100 tokens | **100x** |

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
- **Extensible** — add your own workflows
- **Privacy** — files stay on disk, only sections sent when needed

---

## Documentation

| Doc | What It Covers |
|-----|----------------|
| **[Query Guide](docs/QUERY_GUIDE.md)** | Graph, temporal, schema queries |
| **[Getting Started](docs/GETTING_STARTED.md)** | Installation, platform setup |
| **[MCP Tools](docs/MCP_REFERENCE.md)** | All 40+ graph query tools |

---

## Platform Support

macOS / Linux / WSL / Windows

**[Platform Setup →](docs/GETTING_STARTED.md#platform-specific-notes)**

---

Apache 2.0 License | [GitHub](https://github.com/velvetmonkey/flywheel) | [Issues](https://github.com/velvetmonkey/flywheel/issues)
