# MCP Tools Reference

Flywheel provides 44 MCP tools for querying your vault. All tools return structured JSON without reading file content (unless explicitly needed).

---

## Quick Reference

### Query Tools (Read-Only)

| Category | Tools | Purpose |
|----------|-------|---------|
| [Search](#search-tools) | 1 | Filter by frontmatter, tags, folders |
| [Graph Intelligence](#graph-intelligence-tools) | 10 | Backlinks, paths, hubs, connections |
| [Temporal](#temporal-tools) | 5 | Date-based queries |
| [Schema](#schema-tools) | 5 | Frontmatter analysis |
| [Structure](#structure-tools) | 4 | Headings and sections |
| [Tasks](#task-tools) | 3 | Task extraction |
| [Health](#health--system-tools) | 9 | Diagnostics, metadata |

### Utility Tools

| Category | Tools | Purpose |
|----------|-------|---------|
| [Wikilinks](#wikilink-tools) | 2 | Suggest and validate links |
| [Bidirectional](#bidirectional-tools) | 4 | Prose ↔ frontmatter bridge |
| [Periodic](#periodic-tools) | 1 | Daily/weekly note detection |

---

## Search Tools

The primary query interface for filtering notes.

### search_notes

Search by frontmatter fields, tags, folder, and title.

```json
{
  "where": { "type": "project", "status": "active" },
  "has_tag": "work",
  "folder": "projects",
  "title_contains": "review",
  "sort_by": "modified",
  "limit": 50
}
```

**Returns:** `{ total_matches, notes: [{ path, title, modified, tags, frontmatter }] }`

**Example queries:**
- Find active projects: `{ "where": { "status": "active" }, "folder": "projects" }`
- Find urgent items: `{ "has_tag": "urgent" }`
- Find client notes: `{ "where": { "client": "Acme Corp" } }`

---

## Graph Intelligence Tools

Understand relationships between notes.

| Tool | Purpose | Key Args |
|------|---------|----------|
| `get_backlinks` | Notes linking TO this note | `path`, `include_context` |
| `get_forward_links` | Notes this note links TO | `path` |
| `find_hub_notes` | Most connected notes | `min_links`, `limit` |
| `find_orphan_notes` | Notes with no backlinks | `folder`, `limit` |
| `get_link_path` | Shortest path between notes | `from`, `to`, `max_depth` |
| `get_common_neighbors` | Notes both reference | `note_a`, `note_b` |
| `find_bidirectional_links` | Mutual link pairs | `path` |
| `find_dead_ends` | Has backlinks, no outlinks | `folder`, `min_backlinks` |
| `find_sources` | Has outlinks, no backlinks | `folder`, `min_outlinks` |
| `get_connection_strength` | Relevance score | `note_a`, `note_b` |

### get_backlinks

```json
{
  "path": "projects/Alpha.md",
  "include_context": true,
  "limit": 50
}
```

**Returns:** `{ note, backlink_count, backlinks: [{ source, line, context }] }`

### find_hub_notes

```json
{
  "min_links": 5,
  "limit": 10
}
```

**Returns:** `{ hubs: [{ path, title, backlink_count, forward_link_count, total_connections }] }`

### get_link_path

```json
{
  "from": "people/Alice.md",
  "to": "projects/Gamma.md",
  "max_depth": 5
}
```

**Returns:** `{ found, path: ["people/Alice.md", "projects/Alpha.md", "projects/Gamma.md"], length }`

### get_common_neighbors

```json
{
  "note_a": "people/Alice.md",
  "note_b": "people/Bob.md"
}
```

**Returns:** `{ common: [{ path, linked_by_a, linked_by_b }] }`

---

## Temporal Tools

Query notes by modification date.

| Tool | Purpose | Key Args |
|------|---------|----------|
| `get_recent_notes` | Modified in last N days | `days`, `limit`, `folder` |
| `get_notes_modified_on` | Modified on specific date | `date` (YYYY-MM-DD) |
| `get_notes_in_range` | Modified in date range | `start_date`, `end_date` |
| `get_stale_notes` | Important but neglected | `days`, `min_backlinks` |
| `get_contemporaneous_notes` | Edited around same time | `path`, `hours` |
| `get_activity_summary` | Activity overview | `days` |

### get_recent_notes

```json
{
  "days": 7,
  "limit": 20,
  "folder": "daily-notes"
}
```

**Returns:** `{ count, days, notes: [{ path, title, modified, tags }] }`

### get_stale_notes

```json
{
  "days": 90,
  "min_backlinks": 3,
  "limit": 20
}
```

**Returns:** `{ notes: [{ path, title, backlinks, modified }] }`

---

## Schema Tools

Analyze frontmatter patterns.

| Tool | Purpose | Key Args |
|------|---------|----------|
| `get_frontmatter_schema` | All fields in use | none |
| `get_field_values` | Unique values for field | `field` |
| `find_frontmatter_inconsistencies` | Fields with mixed types | none |
| `validate_frontmatter` | Check against schema | `schema`, `folder` |
| `find_missing_frontmatter` | Notes missing fields | `folder_schemas` |

### get_frontmatter_schema

**Returns:** `{ fields: [{ name, types, count, example_values }] }`

### get_field_values

```json
{
  "field": "status"
}
```

**Returns:** `{ field, values: ["active", "blocked", "done"], counts: { "active": 15, "blocked": 3 } }`

### find_missing_frontmatter

```json
{
  "folder_schemas": {
    "projects": ["type", "status", "owner"],
    "meetings": ["date", "attendees"]
  }
}
```

**Returns:** `{ results: [{ path, missing_fields }] }`

---

## Structure Tools

Query note internal structure.

| Tool | Purpose | Key Args |
|------|---------|----------|
| `get_note_structure` | Full heading tree | `path` |
| `get_headings` | Headings only (lightweight) | `path` |
| `get_section_content` | Content under heading | `path`, `heading` |
| `find_sections` | Search headings across vault | `pattern`, `folder` |

### get_section_content

```json
{
  "path": "projects/Alpha.md",
  "heading": "## Tasks",
  "include_subheadings": true
}
```

**Returns:** `{ path, heading, content, line_start, line_end }`

### find_sections

```json
{
  "pattern": "## Action Items",
  "folder": "meetings"
}
```

**Returns:** `{ matches: [{ path, heading, line }] }`

---

## Task Tools

Extract and query tasks.

| Tool | Purpose | Key Args |
|------|---------|----------|
| `get_all_tasks` | All tasks with filters | `status`, `folder`, `tag` |
| `get_tasks_from_note` | Tasks from specific note | `path` |
| `get_tasks_with_due_dates` | Tasks sorted by due | `status`, `folder` |

### get_all_tasks

```json
{
  "status": "open",
  "tag": "urgent",
  "limit": 50
}
```

**Returns:** `{ tasks: [{ text, status, due_date, source_path, line }] }`

### get_tasks_with_due_dates

```json
{
  "status": "open",
  "folder": "projects"
}
```

**Returns:** `{ tasks: [{ text, due_date, source_path }] }` (sorted by due_date)

---

## Health & System Tools

Diagnostics and infrastructure.

| Tool | Purpose | Key Args |
|------|---------|----------|
| `health_check` | MCP server status | none |
| `get_vault_stats` | Comprehensive statistics | none |
| `find_broken_links` | Links to non-existent notes | `folder`, `limit` |
| `refresh_index` | Rebuild vault index | none |
| `get_all_entities` | All linkable titles + aliases | `include_aliases` |
| `get_unlinked_mentions` | Text mentions not linked | `entity`, `limit` |
| `get_note_metadata` | Metadata without content | `path` |
| `get_folder_structure` | Vault organization | none |

### health_check

**Returns:** `{ status, vault_accessible, index_built, note_count, recommendations }`

### get_vault_stats

**Returns:** `{ total_notes, total_links, orphan_notes, broken_links, most_linked_notes, top_tags, folders }`

---

## Wikilink Tools

Suggest and validate links.

| Tool | Purpose | Key Args |
|------|---------|----------|
| `suggest_wikilinks` | Find linkable text | `text`, `limit` |
| `validate_links` | Check for broken links | `path` |

### suggest_wikilinks

```json
{
  "text": "I worked with John Smith on Project Alpha today."
}
```

**Returns:** `{ suggestions: [{ entity, start, end, target }] }`

---

## Bidirectional Tools

Bridge prose and frontmatter.

| Tool | Purpose | Key Args |
|------|---------|----------|
| `detect_prose_patterns` | Find "Key: Value" in prose | `path` |
| `suggest_frontmatter_from_prose` | YAML from prose patterns | `path` |
| `suggest_wikilinks_in_frontmatter` | Convert strings to links | `path` |
| `validate_cross_layer` | Check prose ↔ YAML consistency | `path` |

### suggest_frontmatter_from_prose

```json
{
  "path": "meetings/2025-01-03.md"
}
```

**Returns:** `{ suggestions: [{ field, value, confidence }] }`

---

## Periodic Tools

Detect daily/weekly/monthly note patterns.

### detect_periodic_notes

```json
{
  "type": "daily"
}
```

**Returns:** `{ detected, folder, pattern, confidence, today_path, today_exists }`

---

## Pagination

Most tools support pagination:

| Arg | Default | Description |
|-----|---------|-------------|
| `limit` | 50 | Maximum results |
| `offset` | 0 | Skip first N |

```json
{ "limit": 20, "offset": 40 }
```

Returns page 3 (items 41-60).

---

## Error Handling

All tools return structured errors:

```json
{
  "error": "Note not found",
  "path": "missing/note.md"
}
```

Use `health_check` at session start to verify connectivity.
