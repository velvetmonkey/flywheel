# How Flywheel Works

> Technical deep-dive into the graph architecture and token-saving mechanisms.

---

## Who This Is For

You're a **solo operator** — consultant, founder, freelancer, creator.

You run everything yourself: clients, projects, finances, content, decisions.
Your notes ARE your business. Flywheel turns them into queryable infrastructure.

---

## Overview

Flywheel is an MCP (Model Context Protocol) server that provides Claude with intelligent access to your markdown knowledge base. Instead of sending entire files to AI, Flywheel builds an in-memory graph index and exposes 40+ specialized tools for queries and mutations.

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
- Mutations target **specific sections** (append to `## Log`, not rewrite file)

---

## Query Architecture

### Graph Queries (No File Reads)

When you ask "What's blocking the course launch?", Claude uses tools like:

```
get_backlinks(path: "Course Launch Plan.md")
→ Returns: [{source: "Payment Setup.md", line: 12}]

search_notes(where: {status: "blocked"})
→ Returns: [{path: "Course Launch Plan.md", frontmatter: {...}}]
```

These queries hit the **in-memory index**. No files are read from disk.

**Token cost:** ~50 tokens (tool call + structured response)
**Without Flywheel:** ~3,000+ tokens (reading 3-4 full files)

### Section Queries (Targeted File Reads)

When you ask for specific content, Flywheel reads **only the section**:

```
get_section_content(path: "daily/2026-01-04.md", heading: "Log")
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

## Mutation Architecture

Mutations modify files in a controlled way:

### Section Append

```
You: "/log finished the proposal"

Tool: append_to_section(
  path: "daily/2026-01-04.md",
  section: "Log",
  content: "- 14:32 finished the proposal"
)
```

1. Flywheel reads the file
2. Finds the `## Log` section
3. Appends the new line
4. Writes the file back

**Token cost:** ~40 tokens (read section + write confirmation)

### Field Update

```
You: "update Acme status to active"

Tool: update_frontmatter(
  path: "clients/acme.md",
  field: "status",
  value: "active"
)
```

1. Flywheel reads frontmatter
2. Updates the field
3. Writes back (preserving all other content)

**Token cost:** ~30 tokens

### File Creation

```
You: "create a decision record for titanium valves"

Tool: create_note(
  path: "decisions/DR-015-titanium-valves.md",
  frontmatter: {date: "2026-01-04", status: "approved"},
  content: "..."
)
```

Claude generates content, Flywheel writes the file.

---

## Inferred Schema System

Flywheel analyzes your existing notes to detect patterns:

### `infer_folder_conventions(folder: "clients/")`

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

### `find_incomplete_notes(folder: "clients/")`

Uses inferred conventions to find notes missing expected fields:

```json
{
  "incomplete": [
    {"path": "clients/acme.md", "missing": ["rate"], "completeness": 0.67},
    {"path": "clients/beta.md", "missing": ["contact", "rate"], "completeness": 0.33}
  ]
}
```

### `suggest_field_values(field: "status", folder: "clients/")`

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

### `suggest_wikilinks(text: "...")`

Analyzes text and finds mentions of known entities:

```json
{
  "suggestions": [
    {"text": "Acme Corp", "match": "Acme Corp", "start": 45, "end": 54},
    {"text": "Sarah", "match": "Sarah Chen", "start": 112, "end": 117}
  ]
}
```

**How it works:**
1. Builds entity map from: note titles, aliases, people, projects
2. Scans prose for matches (case-insensitive)
3. Returns positions for easy linking

### `suggest_frontmatter_from_prose(path: "...")`

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

### `validate_cross_layer(path: "...")`

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

## The Business Loop

These tools combine into an improvement cycle:

```
┌─────────────────────────────────────────────────────────────┐
│                    THE BUSINESS LOOP                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   1. CAPTURE                                                │
│      User logs work → Claude writes to daily note           │
│                                                             │
│   2. DETECT                                                 │
│      suggest_wikilinks() finds unlinked mentions            │
│      Claude: "I found 3 unlinked mentions. Add links?"      │
│                                                             │
│   3. ENHANCE                                                │
│      infer_folder_conventions() detects patterns            │
│      Claude: "clients/ notes typically have 'rate' field"   │
│                                                             │
│   4. COMPLETE                                               │
│      find_incomplete_notes() identifies gaps                │
│      Claude: "Acme Corp is missing 'rate'. Add it?"         │
│                                                             │
│   5. VALIDATE                                               │
│      validate_cross_layer() checks consistency              │
│      Claude: "Frontmatter says active but prose says closed"│
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Token Savings Summary

| Operation | Without Flywheel | With Flywheel | Savings |
|-----------|------------------|---------------|---------|
| Graph query ("what's blocking X?") | ~5,000 tokens | ~50 tokens | **100x** |
| Log entry | ~800 tokens | ~42 tokens | **19x** |
| Rollup (7 days) | ~7,000 tokens | ~700 tokens | **10x** |
| Check overdue tasks | ~3,000 tokens | ~100 tokens | **30x** |
| Find orphan notes | ~10,000 tokens | ~80 tokens | **125x** |

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

Example chain for "do a rollup":

```
1. get_recent_notes(days: 7)
   → Returns 7 daily note paths

2. get_section_content(path: each, heading: "Log")
   → Returns log sections (not full files)

3. [Claude summarizes the logs]

4. create_note(path: "weekly/2026-W01.md", content: summary)

5. append_to_section(path: "monthly/2026-01.md", section: "Weeks", content: link)

6. append_to_section(path: "Achievements.md", section: "January", content: wins)
```

**Total tokens:** ~700 (section reads + writes)
**Without Flywheel:** ~7,000 (reading 7 full daily notes)

---

## Privacy Architecture

1. **Files stay local** — Flywheel runs on your machine
2. **Index is in-memory** — Rebuilt at startup, not persisted
3. **Sections over files** — Only relevant content goes to Claude
4. **No cloud sync** — Your vault never leaves your disk

The privacy benefit isn't just policy — it's architecture. Claude physically cannot see content that isn't sent.

---

## Extending Flywheel

### Custom Skills

Add `/your-command` skills in `.claude/skills/`:

```markdown
# my-skill.md
---
trigger: /standup
---

Read today's daily note and generate a standup summary.
Use get_section_content for the Log section.
```

### Custom Hooks

React to events in `.claude/hooks/`:

```python
# on-daily-create.py
# Runs when a new daily note is created
# Adds standard template sections
```

### MCP Tool Extensions

Add new graph query tools by extending the MCP server:

```typescript
// src/tools/custom.ts
export function myCustomQuery(index: VaultIndex, params: MyParams) {
  // Query the index
  // Return structured data
}
```

---

## Related Documentation

- [Getting Started](GETTING_STARTED.md) — Installation and first commands
- [MCP Tools Reference](MCP_REFERENCE.md) — All 40+ tools documented
- [Skills Reference](SKILLS_REFERENCE.md) — Slash commands
- [Agentic Patterns](AGENTIC_PATTERNS.md) — Reliable AI workflows
- [Six Gates](SIX_GATES.md) — Safety framework for mutations
