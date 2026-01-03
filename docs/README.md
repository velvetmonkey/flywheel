# Flywheel Documentation

Welcome to the Flywheel documentation. Flywheel is the **Agentic Markdown Operating System** - AI agents operating on plain-text knowledge bases.

---

## Getting Started

| Doc | Description |
|-----|-------------|
| [TUTORIAL](TUTORIAL.md) | 10-minute guided walkthrough |
| [GETTING_STARTED](GETTING_STARTED.md) | Installation and setup |
| [QUICKSTART](QUICKSTART.md) | 5-minute quick start |

---

## Understanding Flywheel

| Doc | Description |
|-----|-------------|
| [ARCHITECTURE](ARCHITECTURE.md) | System design deep dive |
| [AGENTIC_PATTERNS](AGENTIC_PATTERNS.md) | Core patterns (graph-first, agent chains, Six Gates) |
| [SIX_GATES](SIX_GATES.md) | Safety framework (mandatory) |

---

## Reference

| Doc | Description |
|-----|-------------|
| [MCP_REFERENCE](MCP_REFERENCE.md) | 50+ MCP tools with examples |
| [SKILLS_REFERENCE](SKILLS_REFERENCE.md) | 49 skills with triggers |
| [AGENTS_REFERENCE](AGENTS_REFERENCE.md) | 14 multi-step agents |

---

## By Role

### New Users

1. [TUTORIAL](TUTORIAL.md) - 10-minute walkthrough
2. Say "setup flywheel" to configure and onboard
3. Say "check vault health" for your first analysis

### Daily Users

Skills are triggered by natural language:
- "check vault health" - Comprehensive diagnostics
- "add log entry: [text]" - Add to daily note
- "find orphan notes" - Disconnected content
- "do a rollup" - Aggregate your notes
- "show hub notes" - Most connected knowledge

### Developers

1. [ARCHITECTURE](ARCHITECTURE.md) - System design
2. [AGENTIC_PATTERNS](AGENTIC_PATTERNS.md) - Design patterns
3. [SIX_GATES](SIX_GATES.md) - Safety framework (required reading)
4. [AGENTS_REFERENCE](AGENTS_REFERENCE.md) - Creating agents

---

## Core Concepts

### The Dual Paradigm

Flywheel supports BOTH philosophies:

**Graph-Native** (Wikilink-First)
- `[[wikilinks]]`, backlinks, graph traversal
- For: PKM enthusiasts, researchers

**Schema-Native** (Frontmatter-First)
- YAML frontmatter, typed fields, queries
- For: Developers, project managers

### The Bidirectional Bridge

Flywheel's unique value: **wikilinks and frontmatter are the SAME information** in two forms.

| Pattern | Direction | Example |
|---------|-----------|---------|
| Prose → Frontmatter | "Author: [[John]]" → `author: "[[John]]"` |
| Frontmatter → Wikilinks | `author: "John Smith"` → `[[John Smith]]` |

---

## Demo Vaults

| Demo | Replaces | Notes |
|------|----------|-------|
| [artemis-rocket](../demos/artemis-rocket/) | 200-person aerospace corp | 65 notes, graph-first |
| [carter-strategy](../demos/carter-strategy/) | Solo consultant | 30 notes, tasks/rollups |

See [demos/README.md](../demos/README.md) for full list.

---

## Version

- **Current**: 1.9.0
- **Roadmap**: [ROADMAP.md](ROADMAP.md)
- **Changelog**: See git log

---

## Support

- Issues: [github.com/bencassie/flywheel/issues](https://github.com/bencassie/flywheel/issues)
- CLAUDE.md: Project instructions for AI assistants
