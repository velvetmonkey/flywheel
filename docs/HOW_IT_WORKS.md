# How Flywheel Works

> Technical deep-dive into the graph architecture and token-saving mechanisms.

---

## Overview

Flywheel is an MCP (Model Context Protocol) server that provides Claude with intelligent access to your markdown knowledge base. Instead of sending entire files to AI, Flywheel builds an in-memory graph index and exposes 40+ specialized query tools.

---

## The Graph Index

At startup, Flywheel scans your vault and builds an in-memory index containing:

| Data | Source | Indexed |
|------|--------|---------|
| Note titles | Filename | ✓ |
| Aliases | Frontmatter `aliases:` | ✓ |
| Wikilinks | `[[target]]` in content | ✓ |
| Frontmatter fields | YAML block | ✓ |
| Tags | `#tag` in content | ✓ |
| Tasks | `- [ ]` checkboxes | ✓ |
| Headings | `## Heading` structure | ✓ |
| File metadata | Modified date, path | ✓ |

**What's NOT indexed:** Full file content, prose text, code blocks.

This means:
- Graph queries use **index only** (zero file reads)
- Content queries read **only relevant sections** (not full files)

---

## Query Architecture

### Graph Queries (No File Reads)

When you ask "What's blocking the course launch?", Claude uses tools like:

```
mcp__flywheel__get_backlinks(path: "Course Launch Plan.md")
→ Returns: [{source: "Payment Setup.md", line: 12}]

mcp__flywheel__search_notes(where: {status: "blocked"})
→ Returns: [{path: "Course Launch Plan.md", frontmatter: {...}}]
```

These queries hit the **in-memory index**. No files are read from disk.

**Token cost:** ~50 tokens (tool call + structured response)
**Without Flywheel:** ~3,000+ tokens (reading 3-4 full files)

### Section Queries (Targeted File Reads)

When you ask for specific content, Flywheel reads **only the section**:

```
mcp__flywheel__get_section_content(path: "daily/2026-01-04.md", heading: "Log")
→ Returns: "- 09:00 Morning review\n- 10:30 Client call"
```

The file is read from disk, but only the `## Log` section is returned to Claude.

**Token cost:** ~40 tokens (section content)
**Without Flywheel:** ~800 tokens (full daily note)

### Full Content (Rare)

Some operations require full file content:
- Creating a new note based on a template
- Major refactoring of a document
- When explicitly requested by user

Even then, Flywheel sends **one file** rather than searching through many.

---

## Inferred Schema System

Flywheel analyzes your existing notes to detect patterns:

### `mcp__flywheel__infer_folder_conventions(folder: "clients/")`

Scans all notes in `clients/` and returns:

```json
{
  "folder": "clients/",
  "note_count": 8,
  "fields": [
    {"name": "status", "frequency": 0.95, "types": ["string"], "values": ["active", "lead", "closed"]},
    {"name": "contact", "frequency": 0.88, "types": ["string"]},
    {"name": "rate", "frequency": 0.75, "types": ["number"]}
  ],
  "confidence": 0.85
}
```

**How it works:**
1. Reads frontmatter from all notes in folder
2. Counts field frequency (>70% = expected)
3. Detects value patterns (enums, numbers, dates)
4. Returns confidence score

### `mcp__flywheel__find_incomplete_notes(folder: "clients/")`

Uses inferred conventions to find notes missing expected fields:

```json
{
  "incomplete": [
    {"path": "clients/acme.md", "missing": ["rate"], "completeness": 0.67},
    {"path": "clients/beta.md", "missing": ["contact", "rate"], "completeness": 0.33}
  ]
}
```

### `mcp__flywheel__suggest_field_values(field: "status", folder: "clients/")`

Suggests values based on what's commonly used:

```json
{
  "suggestions": ["active", "lead", "closed", "churned"],
  "source": "existing values in clients/ folder"
}
```

---

## Auto-Wikilink System

Flywheel can detect unlinked mentions and suggest wikilinks:

### `mcp__flywheel__suggest_wikilinks(text: "...")`

Analyzes text and finds mentions of known entities:

```json
{
  "suggestions": [
    {"text": "Acme Corp", "match": "Acme Corp", "start": 45, "end": 54},
    {"text": "Jordan", "match": "Jordan Lee", "start": 112, "end": 118}
  ]
}
```

**How it works:**
1. Builds entity map from: note titles, aliases, people, projects
2. Scans prose for matches (case-insensitive)
3. Returns positions for easy linking

### `mcp__flywheel__suggest_frontmatter_from_prose(path: "...")`

Detects `Key: Value` patterns in prose:

```json
{
  "suggestions": [
    {"key": "Client", "value": "[[Acme Corp]]", "line": 5},
    {"key": "Status", "value": "active", "line": 8}
  ]
}
```

Useful for migrating unstructured notes to structured frontmatter.

### `mcp__flywheel__validate_cross_layer(path: "...")`

Checks consistency between frontmatter and prose:

```json
{
  "issues": [
    {
      "type": "mismatch",
      "field": "status",
      "frontmatter_value": "active",
      "prose_mentions": ["project wrapped up", "closed last month"]
    }
  ]
}
```

---

## Token Savings Summary

| Operation | Without Flywheel | With Flywheel | Savings |
|-----------|------------------|---------------|---------|
| Graph query ("what's blocking X?") | ~5,000 tokens | ~50 tokens | **up to 100x** |
| Check overdue tasks | ~3,000 tokens | ~100 tokens | **~30x** |
| Find orphan notes | ~10,000 tokens | ~80 tokens | **~125x** |

**Why the savings?**
1. **Index queries** return structured data, not file content
2. **Section reads** return only relevant headings
3. **Parallel queries** batch multiple lookups efficiently

---

## MCP Protocol Integration

Flywheel exposes tools via MCP, so Claude:

1. **Sees all 40+ tools** in its context window
2. **Chooses the right tool** based on the query
3. **Chains tools** for complex operations

Example chain for "what's blocking the milestone?":

```
1. mcp__flywheel__get_backlinks(path: "Propulsion Milestone")
   → Returns notes linking to milestone

2. mcp__flywheel__search_notes(where: { status: "blocked" })
   → Returns blocked items

3. mcp__flywheel__get_link_path(from: "Turbopump Test", to: "Propulsion Milestone")
   → Returns dependency chain

4. [Claude explains the blocker path]
```

**Total tokens:** ~50 (index queries only)
**Without Flywheel:** ~5,000 (reading all related files)

---

## Privacy Architecture

1. **Files stay local** — Flywheel runs on your machine
2. **Index is in-memory** — Rebuilt at startup, not persisted
3. **Sections over files** — Only relevant content goes to Claude
4. **No cloud sync** — Your vault never leaves your disk

The privacy benefit isn't just policy — it's architecture. Claude physically cannot see content that isn't sent.

---

## Related Documentation

- [MCP Tools Reference](MCP_REFERENCE.md) — All 40+ tools documented
- [Query Guide](QUERY_GUIDE.md) — Graph, temporal, and schema queries
