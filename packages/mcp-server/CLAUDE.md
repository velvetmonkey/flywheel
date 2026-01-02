# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

smoking-mirror is an MCP (Model Context Protocol) server that exposes Obsidian vault intelligence to Claude Code. It parses markdown files directly to provide graph queries, wikilink suggestions, and vault health checks.

**First-to-market** in: graph intelligence, wikilink services, vault health for Obsidian MCP servers.

**47 tools** across 9 categories: Graph, Wikilinks, Health, Search, Deep Graph, Structure, Tasks, Frontmatter, Temporal.

## Commands

```bash
bun install          # Install dependencies
bun run dev          # Run server in development (requires OBSIDIAN_VAULT_PATH env var)
bun run build        # Build to dist/ for distribution
bun run inspect      # Test with MCP inspector
bun test             # Run tests
```

To run with a vault:

```bash
OBSIDIAN_VAULT_PATH=/path/to/vault bun run dev
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

**Environment**: Requires `OBSIDIAN_VAULT_PATH` environment variable pointing to the Obsidian vault directory.

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

## Consumer

[obsidian-scribe](https://github.com/bencassie/obsidian-scribe) - A Claude Code plugin with 21 skills powered by smoking-mirror's graph intelligence.
