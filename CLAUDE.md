# Flywheel - Claude Code Instructions

## Product Overview

Flywheel is the **Agentic Markdown Operating System** - a unified system combining:

1. **MCP Server** (`packages/mcp-server/`) - Graph + schema intelligence
2. **Claude Plugin** (`packages/claude-plugin/`) - Workflows and automation
3. **Demo Vaults** (`demos/`) - Ready-to-use templates for common workflows

## Core Concept

An Agentic Markdown OS where:
- **Files are data structures** (not just documents)
- **Links are relationships** (not just hypertext)
- **Folders are schemas** (not just organization)
- **AI agents are operators** (not just assistants)

Plain text markdown becomes queryable, executable, automatable.

## The Dual Paradigm

Flywheel supports BOTH philosophies:

### Graph-Native (Wikilink-First)
- Philosophy: Knowledge is a network of interconnected thoughts
- Primitives: `[[wikilinks]]`, backlinks, graph traversal
- Users: PKM enthusiasts, researchers, Obsidian/Roam users

### Schema-Native (Frontmatter-First)
- Philosophy: Knowledge is typed, queryable structured data
- Primitives: YAML frontmatter, schemas, typed fields
- Users: Developers, project managers, VSCode/Cursor users

### The Synthesis
Best systems support BOTH - files have frontmatter schemas AND wikilinks. Users choose their patterns without sacrificing interoperability.

## The Bidirectional Bridge (CRITICAL)

**Key insight**: Wikilinks and frontmatter are the OVERLAP - two representations of the SAME information.

Flywheel's unique value is **bidirectional translation**:

**Pattern 1: Prose → Frontmatter** (help Graph-Native users add structure)
**Pattern 2: Frontmatter → Wikilinks** (help Schema-Native users traverse)
**Pattern 3: Perfect Hybrid** (both layers reinforcing each other)

See full documentation in `packages/mcp-server/docs/BIDIRECTIONAL.md`

## Development Principles

1. **Zero lock-in**: Pure markdown, Git-friendly, works offline
2. **Editor agnostic**: Obsidian, VSCode, Cursor, vim, any text editor
3. **AI-first architecture**: MCP layer gives agents full vault intelligence
4. **Convention over configuration**: Smart defaults, zero-config start
5. **Progressive disclosure**: Simple to start, powerful when needed
6. **Preserve working tech**: WSL + Windows tested and working

## Cross-Platform Support

**CRITICAL**: This codebase works on both WSL and Windows. DO NOT break this.

- Same tooling (TypeScript, npm)
- Same build process
- Tested on both platforms
- If making changes, test on both

## Repository Structure

```
flywheel/
├── packages/
│   ├── mcp-server/          # Graph + schema intelligence
│   │   ├── src/tools/       # MCP tools (graph, frontmatter, periodic)
│   │   └── README.md
│   └── claude-plugin/       # Workflows and automation
│       ├── .claude-plugin/  # Plugin manifest
│       ├── skills/          # User-facing skills
│       ├── hooks/           # Event-driven automation
│       └── agents/          # Multi-step workflows
├── demos/
│   └── artemis-rocket/      # Demo: aerospace startup knowledge base
├── docs/                    # Documentation and guides
├── README.md                # Main project README
├── CLAUDE.md                # This file
└── package.json             # Monorepo configuration
```

## Key Files

**MCP Server**:
- `packages/mcp-server/src/index.ts` - Server entry point
- `packages/mcp-server/src/tools/` - Tool implementations

**Claude Plugin**:
- `packages/claude-plugin/.claude-plugin/plugin.json` - Plugin manifest
- `packages/claude-plugin/skills/` - Skill definitions
- `packages/claude-plugin/hooks/` - Hook scripts

## Working with Demos

Demo vaults demonstrate "2026 Business Replacements" - how AI + markdown replace traditional business software:

| Demo | Replaces | Notes |
|------|----------|-------|
| Artemis Rocket | 200-person aerospace corp | 65 notes, graph-first design |
| Consulting Firm | Partner-heavy firm | Solo consultant + AI |
| Startup Ops | Founders doing everything | AI handles ops |
| Research Lab | Manual lit review | 100 papers/week processed |

Each demo should:
- Show real-world usage patterns
- Demonstrate graph + schema balance
- Include intentional issues for troubleshooting demos
- Work zero-config with Flywheel

## Development Workflow

```bash
# Install dependencies
npm install

# Build all packages
npm run build

# Develop MCP server
npm run dev:mcp

# Develop plugin
npm run dev:plugin

# Run tests
npm run test
```

## Related Documentation

- Agentic Markdown OS concept: `docs/CONCEPT.md`
- Bidirectional bridge design: `docs/BIDIRECTIONAL.md`
- Roadmap: `docs/ROADMAP.md`
- MCP Server docs: `packages/mcp-server/README.md`
- Plugin docs: `packages/claude-plugin/README.md`

**Skill naming**: Keep Claude Code conventions (kebab-case like `auto-log`, `vault-health`) - NOT PowerShell Verb-Noun.

**Trigger support**: Both slash commands (`/vault-health`) AND keywords ("check vault health") for accessibility.

## Vision

"Starting a new business or project? Install Flywheel in Claude Code - it gives you the intelligence and workflows to run your business from day one."

The product aligns with 2026 predictions: long-running agents, proactive AI, non-technical users running businesses with markdown + AI.
