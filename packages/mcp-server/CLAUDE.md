# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Flywheel MCP server exposes Obsidian vault intelligence to Claude Code. It parses markdown files directly to provide graph queries, wikilink suggestions, and vault health checks.

**First-to-market** in: graph intelligence, wikilink services, vault health for Obsidian MCP servers.

Tools across 9 categories: Graph, Wikilinks, Health, Search, Deep Graph, Structure, Tasks, Frontmatter, Temporal.

## Commands

```bash
npm install          # Install dependencies
npm run dev          # Run server in development (requires PROJECT_PATH env var)
npm run build        # Build to dist/ for distribution
npm run inspect      # Test with MCP inspector
npm test             # Run tests
```

To run with a vault:

```bash
PROJECT_PATH=/path/to/vault npm run dev
```

## Architecture

```
src/
├── index.ts                 # MCP server entry, tool registration
├── core/
│   ├── vault.ts            # Vault scanner, file discovery
│   ├── parser.ts           # Markdown parser (frontmatter, links, tags)
│   ├── graph.ts            # In-memory link graph + VaultIndex
│   └── types.ts            # Shared TypeScript types
├── tools/
│   ├── graph.ts            # Backlinks, forward links, orphans, hubs
│   ├── graph-analysis.ts   # Link paths, neighbors, bidirectional, dead ends
│   ├── wikilinks.ts        # Suggest, validate, broken links, unlinked mentions
│   ├── health.ts           # Vault stats, folder structure, activity
│   ├── query.ts            # Search notes, recent, stale, date ranges
│   ├── structure.ts        # Headings, sections, note structure
│   ├── tasks.ts            # Task extraction, due dates
│   ├── frontmatter.ts      # Schema, field values, inconsistencies
│   └── temporal.ts         # Contemporaneous notes, metadata
```

**Key design decisions**:

- **File-first**: parses markdown directly, no database, works offline
- **Eager loading**: full vault scan on startup (fine for <5000 notes)
- **In-memory graph**: VaultIndex holds notes, backlinks, entities, tags
- **Privacy by design**: returns structure/metadata, not content
- **No Dataview dependency**: Dataview requires Obsidian internals; we use native queries instead

**Dependencies**:

- `@modelcontextprotocol/sdk` - MCP protocol handling
- `gray-matter` - YAML frontmatter parsing
- `zod` - schema validation

**Environment**: `PROJECT_PATH` environment variable points to the vault directory. If not set, defaults to current working directory.

## Development

Use `/mcp-dev` for build/test workflow.

Quick commands:

```bash
npx tsc --noEmit                    # Type check
npx @modelcontextprotocol/inspector npx tsx src/index.ts  # Interactive testing
```

## Key Types

```typescript
interface VaultNote {
  path: string;              // Relative to vault root
  title: string;             // Filename without .md
  aliases: string[];         // From frontmatter
  frontmatter: Record<string, unknown>;
  outlinks: OutLink[];       // [[wikilinks]] this note contains
  tags: string[];            // #tags in content + frontmatter
  modified: Date;
}

interface VaultIndex {
  notes: Map<string, VaultNote>;
  backlinks: Map<string, Set<string>>;
  entities: Map<string, string>;
  tags: Map<string, Set<string>>;
}
```

## Related

See `packages/claude-plugin/` - Claude Code plugin with skills powered by Flywheel's graph intelligence.
