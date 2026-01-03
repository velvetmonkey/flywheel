# Flywheel Documentation

Welcome to the Flywheel documentation. Flywheel is the **Agentic Markdown Operating System** - AI agents operating on plain-text knowledge bases.

---

## Quick Links

| Doc | Description |
|-----|-------------|
| [QUICKSTART](QUICKSTART.md) | Get running in 5 minutes |
| [GETTING_STARTED](GETTING_STARTED.md) | Installation and first steps |
| [AGENTIC_PATTERNS](AGENTIC_PATTERNS.md) | Core patterns (graph-first, agent chains, Six Gates) |

---

## Reference Docs

| Doc | Description |
|-----|-------------|
| [MCP_REFERENCE](MCP_REFERENCE.md) | 44 MCP tools with examples |
| [SKILLS_REFERENCE](SKILLS_REFERENCE.md) | 37 skills with triggers |
| [AGENTS_REFERENCE](AGENTS_REFERENCE.md) | 8 multi-step agents |
| [SIX_GATES](SIX_GATES.md) | Safety framework (mandatory) |

---

## By Role

### New Users

1. [QUICKSTART](QUICKSTART.md) - Get running in 5 minutes
2. [GETTING_STARTED](GETTING_STARTED.md) - Full setup guide
3. Say "hello flywheel" to start the onboarding flow

### Daily Users

- `/health` - Check vault health
- `/log [entry]` - Add log entry
- `/tasks` - View all tasks
- `/search [query]` - Find notes
- `/hubs` - See most connected notes

### Developers

1. [AGENTIC_PATTERNS](AGENTIC_PATTERNS.md) - Understand the patterns
2. [SIX_GATES](SIX_GATES.md) - Safety framework (required reading)
3. [AGENTS_REFERENCE](AGENTS_REFERENCE.md) - Creating agents
4. [MCP_REFERENCE](MCP_REFERENCE.md) - All available tools

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

See [demos/README.md](../demos/README.md) for full list.

---

## Version

- **Current**: 1.6.3
- **Roadmap**: [ROADMAP.md](ROADMAP.md)
- **Changelog**: See git log

---

## Support

- Issues: [github.com/bencassie/flywheel/issues](https://github.com/bencassie/flywheel/issues)
- CLAUDE.md: Project instructions for AI assistants
