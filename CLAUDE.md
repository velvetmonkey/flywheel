# Flywheel - Claude Code Instructions

## Product Overview

Flywheel is an **MCP server providing graph intelligence for markdown vaults**:

1. **MCP Server** (`packages/mcp-server/`) - 44 tools for graph + schema intelligence
2. **Demo Vaults** (`demos/`) - Ready-to-use templates for common workflows

## Core Concept

A markdown vault intelligence layer where:
- **Files are data structures** (not just documents)
- **Links are relationships** (not just hypertext)
- **Folders are schemas** (not just organization)

Plain text markdown becomes queryable through MCP tools.

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

**Pattern 1: Prose -> Frontmatter** (help Graph-Native users add structure)
**Pattern 2: Frontmatter -> Wikilinks** (help Schema-Native users traverse)
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

### MCP Configuration

Create `.mcp.json` in your project/vault root with the appropriate platform config:

| Platform | Command | Path style |
|----------|---------|------------|
| Windows (`win32`) | `cmd /c npx` | `C:/...` |
| WSL (`linux`) | `npx` | `/mnt/c/...` |
| macOS (`darwin`) | `npx` | `/Users/...` |

Since `.mcp.json` is gitignored, each environment gets its own config without conflicts.

### MCP Configuration Generation

When generating `.mcp.json` for users, **check the `Platform:` field in env info** (AUTHORITATIVE):

| `Platform:` value | Command | Path style | Example |
|-------------------|---------|------------|---------|
| `linux` | `npx` | `/mnt/c/...` (WSL) or `/home/...` | WSL accessing Windows files |
| `win32` | `cmd /c npx` | `C:/...` | Native Windows |
| `darwin` | `npx` | `/Users/...` | macOS |

**NEVER infer platform from filesystem path.** `/mnt/c/...` means WSL accessing Windows files—the runtime is still Linux, so use `npx` directly (not `cmd /c`).

## Repository Structure

```
flywheel/
├── packages/
│   └── mcp-server/          # Graph + schema intelligence
│       ├── src/tools/       # MCP tools (graph, frontmatter, periodic)
│       └── README.md
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

## Working with Demos

Demo vaults demonstrate how AI + markdown work together:

| Demo | Purpose | Notes |
|------|---------|-------|
| Artemis Rocket | Aerospace knowledge base | 65 notes, graph-first design |

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

# Run tests
npm run test
```

## Related Documentation

- Bidirectional bridge design: `docs/BIDIRECTIONAL.md`
- Roadmap: `docs/ROADMAP.md`
- MCP Server docs: `packages/mcp-server/README.md`

## Release Workflow (MANDATORY)

**CRITICAL**: When bumping version numbers, you MUST create a GitHub release.

### Version Files (keep in sync)

ALL version bumps require updating TWO files:
- `packages/mcp-server/package.json`
- `package.json` (root)

Then run `npm install --package-lock-only` to update `package-lock.json`.

### GitHub Release Process

When version changes:
1. **Commit** version bump with message: `chore: Bump version to vX.Y.Z`
2. **Push** to main
3. **Create GitHub Release**:
   ```bash
   gh release create vX.Y.Z --title "vX.Y.Z" --notes "## Changes\n\n- [list changes]"
   ```
4. Tag should match version (e.g., `v1.6.3`)

### Release Notes Format

```markdown
## Changes

- Feature: [description]
- Fix: [description]
- Docs: [description]

## Migration Notes

[Any breaking changes or migration steps]
```

### Don't Auto-Push

- Only push when user explicitly asks

## Vision

Flywheel provides the graph intelligence layer that makes markdown vaults queryable and navigable by AI agents. Any MCP-compatible client can use these tools to understand vault structure, traverse links, and analyze frontmatter schemas.
