# smoking-mirror

**Your AI can see your notes without reading them.**

[![npm version](https://badge.fury.io/js/smoking-mirror.svg)](https://www.npmjs.com/package/smoking-mirror)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![MCP](https://img.shields.io/badge/MCP-Compatible-blue)](https://modelcontextprotocol.io/)
[![Node](https://img.shields.io/badge/Node-%3E%3D18-green)](https://nodejs.org/)

**47 tools** · **Privacy by design** · **200x token savings** · **<10ms queries**

---

## The Problem

**Your journals are private.** Traditional AI reads everything to help you find anything.

That's like giving a stranger your diary to help you find a recipe.

### What traditional AI receives: your actual content

```
"March 15, 2024 - Job Hunt Update

Feeling anxious about the Google interview tomorrow. Sarah said I should
practice the STAR method tonight. Bank account down to $2,400 after paying
rent. Really need this job.

TODO: Review system design notes, call Mom about her surgery..."
```

Your private thoughts, finances, health info—all sent to AI. ~2,000 tokens per note.

### What smoking-mirror sends: just the structure

```json
{
  "path": "journal/2024-03-15.md",
  "links": ["Resume", "Google Prep", "Interview Notes"],
  "tags": ["#job-hunt", "#daily"],
  "backlinks": 3,
  "modified": "2024-03-15"
}
```

Claude knows this note exists and connects to your job search. Claude has **no idea** what you actually wrote. ~50 tokens.

---

## The Solution: Map, Not Territory

smoking-mirror gives AI the **map** of your vault—not the **territory**.

Think of it like asking a librarian: *"What books connect to this topic?"* They check the card catalog and tell you the shelf locations. They don't read every book to find out.

**What AI learns:**
- Which notes link to which (the graph)
- What tags and folders exist (the structure)
- When things were modified (the timeline)
- What's orphaned or highly connected (the patterns)

**What AI never sees:**
- Your actual words
- Your private thoughts
- Your sensitive data

---

## See It Work

```
You: "Find notes about my job search"

Claude sees:                          Claude doesn't see:
─────────────────────────────────     ─────────────────────────────────
📁 career/job-hunt.md                 "I'm so nervous about the
  → links to: [[Resume]]               Google interview tomorrow..."
  → links to: [[Companies List]]
  → links to: [[Interview Prep]]
  → tagged: #career #2024
  → modified: 3 days ago
```

```
You: "What's connected to my daily journal?"

Claude sees:                          Claude doesn't see:
─────────────────────────────────     ─────────────────────────────────
📁 journal/2024-01-15.md              Your actual journal entries.
  → 47 notes link here                Not a single word.
  → tags: #reflection #gratitude
  → part of: journal/ folder
```

Then—and only then—you can tell Claude to read the specific notes you choose.

---

## How It Works

```
┌──────────────┐      ┌──────────────────┐      ┌──────────────┐
│              │      │                  │      │              │
│  Your Vault  │ ───► │  smoking-mirror  │ ───► │    Claude    │
│              │      │     (local)      │      │              │
│   📓 Notes   │      │                  │      │  Sees only:  │
│   📊 Data    │      │  Builds index    │      │  • paths     │
│   📝 Journal │      │  of structure    │      │  • links     │
│              │      │                  │      │  • tags      │
└──────────────┘      └──────────────────┘      └──────────────┘
       │                                               │
       │              NEVER LEAVES                     │
       └───────────────────────────────────────────────┘
                    your machine
```

---

## 47 Ways to Navigate

| Category | Tools | What you can ask |
|----------|:-----:|------------------|
| **Graph Intelligence** | 4 | Who links here? Where do orphans hide? |
| **Wikilink Services** | 4 | Suggest links, find broken ones |
| **Vault Health** | 3 | Stats, structure, activity |
| **Smart Search** | 5 | By date, tag, frontmatter |
| **Deep Graph Analysis** | 6 | Find paths between notes, connection strength |
| **Structure Analysis** | 4 | Headings, sections, TOC |
| **Task Management** | 3 | Extract todos, due dates |
| **Frontmatter Intelligence** | 3 | Schema discovery, field values |
| **Temporal Analysis** | 2 | Notes modified together |
| **System** | 2 | Refresh index, list entities |

[**Full 47-tool reference →**](docs/tools-reference.md)

---

## Quick Start

### Step 0: Install Claude Code

If you haven't already, install [Claude Code](https://claude.ai/code):

```bash
npm install -g @anthropic-ai/claude-code
```

### Step 1: Add to your `.mcp.json`

Create or edit `.mcp.json` in your project root (or `~/.claude/.mcp.json` for global access):

**Windows:**

```json
{
  "mcpServers": {
    "smoking-mirror": {
      "command": "cmd",
      "args": ["/c", "npx", "-y", "smoking-mirror"],
      "env": {
        "OBSIDIAN_VAULT_PATH": "C:\\Users\\you\\Documents\\MyVault"
      }
    }
  }
}
```

**macOS / Linux:**

```json
{
  "mcpServers": {
    "smoking-mirror": {
      "command": "npx",
      "args": ["-y", "smoking-mirror"],
      "env": {
        "OBSIDIAN_VAULT_PATH": "/Users/you/Documents/MyVault"
      }
    }
  }
}
```

### Step 2: Verify

```bash
claude mcp list  # Should show: smoking-mirror ✓
```

### Step 3: Try it

```
You: "What are my most connected notes?"
Claude: find_hub_notes({ min_links: 5 })
→ Returns paths and connection counts, not content
```

### Alternative: CLI One-liner

If you prefer the command line:

```bash
# macOS / Linux
claude mcp add smoking-mirror -e OBSIDIAN_VAULT_PATH=/path/to/vault -- npx -y smoking-mirror

# Windows
claude mcp add smoking-mirror -e OBSIDIAN_VAULT_PATH=C:\path\to\vault -- cmd /c npx -y smoking-mirror
```

---

## Part of a Product Family

### smoking-mirror + obsidian-scribe

| Layer | What it does | Tools |
|-------|--------------|-------|
| **smoking-mirror** | Intelligence layer | 47 MCP tools for vault queries |
| **[obsidian-scribe](https://github.com/bencassie/obsidian-scribe)** | Workflow layer | 21 Claude Code skills for common tasks |

**Together:** Complete Obsidian + AI experience.

**obsidian-scribe skills include:**
- `/vault-health` — Comprehensive vault diagnostics
- `/vault-orphans` — Find unlinked notes
- `/vault-hubs` — Detect knowledge hubs
- `/vault-gaps` — Find mentioned but undocumented topics
- `/rollup` — Hierarchical summarization (daily → weekly → monthly → yearly)

*Using smoking-mirror? Open a PR to add your project!*

---

## What IS smoking-mirror?

"Smoking mirror" (*tezcatl* in Nahuatl) is the literal translation of **obsidian**. This MCP server acts as a reflective surface that reveals the *structure* of your vault—without exposing the *content*.

---

# Technical Details

*Everything below is for developers and curious power users.*

---

## How It Compares

| Feature | smoking-mirror | mcp-obsidian | obsidian-mcp-server |
|---------|---------------|--------------|---------------------|
| **Approach** | Metadata-first (privacy) | Full content access | Full content access |
| **Offline support** | Yes (no DB needed) | Yes | Requires Obsidian API |
| **Graph tools** | 47 specialized tools | Basic read/write | Basic operations |
| **Token efficiency** | ~200x savings | Standard | Standard |
| **Unique features** | Backlinks, orphans, hubs, link paths, sections, frontmatter analysis | Direct vault access | Obsidian plugin integration |
| **Best for** | Privacy + large vaults | Full content workflows | Plugin users |

*Each approach has trade-offs. Choose based on your privacy needs and workflow.*

---

## Performance

```
┌────────────────────────────────────────────────────────────────┐
│                    PERFORMANCE BENCHMARKS                       │
├────────────────┬───────────────┬───────────────┬───────────────┤
│   Vault Size   │  Index Build  │  Query Time   │    Memory     │
├────────────────┼───────────────┼───────────────┼───────────────┤
│    100 notes   │    <200ms     │    <10ms      │    ~20MB      │
│    500 notes   │    <500ms     │    <10ms      │    ~30MB      │
│  1,500 notes   │     <2s       │    <10ms      │    ~50MB      │
│  5,000 notes   │     <5s       │    <10ms      │   ~100MB      │
└────────────────┴───────────────┴───────────────┴───────────────┘

Queries are INSTANT because they hit an in-memory index, not your filesystem.
```

---

## Token Economy

Every character Claude reads costs you tokens. Here's the math:

```
Traditional approach: "Read all notes with #project tag"
─────────────────────────────────────────────────────────
📄 50 notes × ~2,000 tokens each = 100,000 tokens
💰 Cost: ~$0.30 per query (Claude pricing)

smoking-mirror: search_notes({ has_tag: "project" })
─────────────────────────────────────────────────────────
📊 Returns: paths, titles, metadata
🎯 ~500 tokens total
💰 Cost: ~$0.0015 per query

═══════════════════════════════════════════════════════════
SAVINGS: 200x fewer tokens per query
═══════════════════════════════════════════════════════════
```

Then Claude can surgically `Read` only the 2-3 notes it actually needs.

---

## Privacy Architecture

```
    YOUR MACHINE                           │    CLOUD
    ────────────────────────────────────── │ ────────────────
                                           │
    ┌─────────────────┐                    │
    │   Obsidian      │                    │
    │     Vault       │                    │
    │  ┌───────────┐  │                    │
    │  │ 📓 Notes  │  │  NEVER LEAVES      │
    │  │ 📊 Data   │  │  ───────────►      │   ❌ Blocked
    │  │ 📝 Journal│  │                    │
    │  └───────────┘  │                    │
    └────────┬────────┘                    │
             │                             │
             │ Parse locally               │
             ▼                             │
    ┌─────────────────┐                    │
    │  smoking-mirror │                    │
    │  ┌───────────┐  │                    │
    │  │  Index    │  │                    │
    │  │ • links   │  │                    │
    │  │ • tags    │  │                    │
    │  │ • paths   │  │                    │
    │  └───────────┘  │                    │
    └────────┬────────┘                    │
             │                             │
             │ Structured responses only   │
             ▼                             │
    ┌─────────────────┐    API calls      ┌─────────────────┐
    │   Claude Code   │ ───────────────►  │    Claude AI    │
    │                 │  (metadata only)  │                 │
    │   "Find hubs"   │ ◄───────────────  │   (processes    │
    │                 │  { paths, counts }│    structure)   │
    └─────────────────┘                    └─────────────────┘
```

**What Claude receives:**
- File paths and names
- Link relationships (A → B)
- Tag lists
- Frontmatter keys/values
- Word counts, modification dates

**What Claude NEVER receives:**
- Your actual note content (unless you explicitly Read it)
- Personal journals
- Private thoughts
- Sensitive data

---

## Security & Privacy

- **Content never leaves your machine** — Claude sees paths, tags, links, not your words
- **No network calls** — Works fully offline
- **No database** — Pure file parsing, nothing persisted beyond runtime
- **Opt-in content reading** — Only when you explicitly use Claude's `Read` tool
- **MIT licensed** — Audit the code yourself

Your vault path is provided to the locally-running MCP server. No data is transmitted to external services by smoking-mirror itself.

---

## Architecture

```
                    ┌────────────────────────────────┐
                    │         smoking-mirror         │
                    │                                │
┌──────────┐        │  ┌──────────────────────────┐  │
│          │        │  │       VaultIndex         │  │
│ Obsidian │  scan  │  │                          │  │
│  Vault   │───────►│  │  notes: Map<path, Note>  │  │
│          │        │  │  backlinks: Map<→Set>    │  │
│  📁 .md  │        │  │  entities: Map<name→path>│  │
│  files   │        │  │  tags: Map<tag→Set>      │  │
│          │        │  │                          │  │
└──────────┘        │  └──────────────────────────┘  │
                    │              │                  │
                    │              ▼                  │
                    │  ┌──────────────────────────┐  │
                    │  │      47 MCP Tools        │  │
                    │  │                          │  │
                    │  │  Queries return          │  │
                    │  │  STRUCTURE not CONTENT   │  │
                    │  │                          │  │
                    │  └──────────────────────────┘  │
                    │                                │
                    └────────────────────────────────┘
                                   │
                                   │ MCP Protocol
                                   ▼
                           ┌──────────────┐
                           │ Claude Code  │
                           └──────────────┘
```

**Key Design Decisions:**

- **File-first**: Parses markdown directly, no database
- **Works offline**: No connection to Obsidian app needed
- **Eager loading**: Full index on startup (fine for <5000 notes)
- **In-memory graph**: Lightning-fast queries
- **Privacy by design**: Content stays local

---

## Error Handling

| Situation | Behavior |
|-----------|----------|
| Malformed YAML | Gracefully skipped, file treated as content |
| Binary files | Detected and skipped |
| Empty files | Indexed with no links/tags |
| Large files (>10MB) | Skipped with warning |
| Missing files | Graceful degradation |

---

## Why not Dataview?

We wanted to use `obsidian-dataview` as a library, but it requires Obsidian's internal `CachedMetadata` API and cannot run standalone. See [this discussion](https://github.com/blacksmithgu/obsidian-dataview/discussions/1811).

Instead, smoking-mirror:

- Parses markdown directly using `gray-matter`
- Builds its own in-memory graph index
- Provides ~80% of Dataview functionality with simpler syntax
- And does it all **without exposing your content to AI**

---

## Development

```bash
bun install
OBSIDIAN_VAULT_PATH=/path/to/vault bun run dev
bun run build
bun run inspect
bun test
```

---

## Roadmap

- [ ] Watch mode for incremental updates
- [ ] `rename_with_links` - Safe note renaming with reference updates
- [ ] MarkdownDB integration for SQL-like queries
- [ ] Semantic search via local embeddings

---

## License

MIT - Ben Cassie

---

## The Philosophy

> Your notes are yours. Your thoughts are private. Your vault is sacred.
>
> AI should help you navigate your knowledge—not consume it.
>
> smoking-mirror gives Claude the **map**, not the **territory**.

---

## Related

- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Claude Code](https://claude.ai/code)
- [Obsidian](https://obsidian.md/)
- [obsidian-scribe](https://github.com/bencassie/obsidian-scribe) - Claude Code plugin powered by smoking-mirror

---

*"tezcatl" — the obsidian mirror that reveals truth without taking it*
