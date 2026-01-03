# MCP Tools Reference

Flywheel provides 44 MCP tools organized into 8 categories. All tools return structured JSON.

---

## Quick Reference

| Category | Tools | Purpose |
|----------|-------|---------|
| [Graph](#graph-tools) | 4 | Link relationships, backlinks, hubs |
| [Query](#query-tools) | 1 | Search notes by frontmatter/tags |
| [Wikilinks](#wikilink-tools) | 2 | Suggest and validate wikilinks |
| [Health](#health-tools) | 3 | Vault diagnostics and statistics |
| [System](#system-tools) | 6 | Index, entities, metadata |
| [Temporal](#temporal-tools) | 5 | Date-based note discovery |
| [Structure](#structure-tools) | 4 | Headings and sections |
| [Tasks](#task-tools) | 3 | Task extraction and queries |
| [Graph Advanced](#advanced-graph-tools) | 6 | Paths, neighbors, dead ends |
| [Frontmatter](#frontmatter-tools) | 5 | Schema analysis and validation |
| [Periodic](#periodic-tools) | 1 | Daily/weekly note detection |
| [Bidirectional](#bidirectional-bridge-tools) | 4 | Prose ↔ frontmatter bridge |

---

## Graph Tools

Core graph intelligence for understanding link relationships.

| Tool | Purpose | Key Args |
|------|---------|----------|
| `get_backlinks` | Get notes that link TO this note | `path`, `include_context`, `limit` |
| `get_forward_links` | Get notes this note links TO | `path` |
| `find_orphan_notes` | Notes with no backlinks | `folder`, `limit` |
| `find_hub_notes` | Highly connected notes | `min_links`, `limit` |

### get_backlinks

```json
{
  "path": "projects/Alpha.md",
  "include_context": true,
  "limit": 50
}
```

Returns: `{ note, backlink_count, backlinks: [{ source, line, context }] }`

### find_hub_notes

```json
{
  "min_links": 5,
  "limit": 10
}
```

Returns: `{ hubs: [{ path, title, backlink_count, forward_link_count, total_connections }] }`

---

## Query Tools

Search notes using frontmatter, tags, and folders.

| Tool | Purpose | Key Args |
|------|---------|----------|
| `search_notes` | Search by frontmatter/tags/folder | `where`, `has_tag`, `folder`, `title_contains` |

### search_notes

```json
{
  "where": { "type": "project", "status": "active" },
  "has_tag": "work",
  "folder": "projects",
  "sort_by": "modified",
  "limit": 50
}
```

Returns: `{ total_matches, notes: [{ path, title, modified, tags, frontmatter }] }`

---

## Wikilink Tools

Suggest and validate wikilinks.

| Tool | Purpose | Key Args |
|------|---------|----------|
| `suggest_wikilinks` | Find text that could be linked | `text`, `limit` |
| `validate_links` | Check for broken links | `path` (optional) |

### suggest_wikilinks

```json
{
  "text": "I worked with John Smith on Project Alpha today."
}
```

Returns: `{ suggestions: [{ entity, start, end, target }] }`

---

## Health Tools

Vault diagnostics and statistics.

| Tool | Purpose | Key Args |
|------|---------|----------|
| `health_check` | MCP server health status | none |
| `find_broken_links` | Find links to non-existent notes | `folder`, `limit` |
| `get_vault_stats` | Comprehensive vault statistics | none |

### health_check

Returns: `{ status, vault_accessible, index_built, index_stale, note_count, recommendations }`

### get_vault_stats

Returns: `{ total_notes, total_links, orphan_notes, broken_links, most_linked_notes, top_tags, folders }`

---

## System Tools

Infrastructure primitives.

| Tool | Purpose | Key Args |
|------|---------|----------|
| `refresh_index` | Rebuild vault index | none |
| `get_all_entities` | All linkable titles + aliases | `include_aliases`, `limit` |
| `get_recent_notes` | Recently modified notes | `days`, `limit`, `folder` |
| `get_unlinked_mentions` | Text mentions not linked | `entity`, `limit` |
| `get_note_metadata` | Metadata without full content | `path`, `include_word_count` |
| `get_folder_structure` | Vault folder organization | none |

### get_recent_notes

```json
{
  "days": 7,
  "limit": 20,
  "folder": "daily-notes"
}
```

Returns: `{ count, days, notes: [{ path, title, modified, tags }] }`

---

## Temporal Tools

Date-based note discovery.

| Tool | Purpose | Key Args |
|------|---------|----------|
| `get_notes_modified_on` | Notes modified on specific date | `date` (YYYY-MM-DD) |
| `get_notes_in_range` | Notes in date range | `start_date`, `end_date` |
| `get_stale_notes` | Important notes not recently edited | `days`, `min_backlinks` |
| `get_contemporaneous_notes` | Notes edited around same time | `path`, `hours` |
| `get_activity_summary` | Activity summary over period | `days` |

### get_stale_notes

```json
{
  "days": 90,
  "min_backlinks": 3,
  "limit": 20
}
```

Returns: `{ notes: [{ path, title, backlinks, modified }] }`

---

## Structure Tools

Note headings and sections.

| Tool | Purpose | Key Args |
|------|---------|----------|
| `get_note_structure` | Heading structure of a note | `path` |
| `get_headings` | All headings (lightweight) | `path` |
| `get_section_content` | Content under a heading | `path`, `heading` |
| `find_sections` | Search headings across vault | `pattern`, `folder` |

### get_section_content

```json
{
  "path": "projects/Alpha.md",
  "heading": "## Tasks",
  "include_subheadings": true
}
```

Returns: `{ path, heading, content, line_start, line_end }`

---

## Task Tools

Task extraction and queries.

| Tool | Purpose | Key Args |
|------|---------|----------|
| `get_all_tasks` | All tasks with filters | `status`, `folder`, `tag` |
| `get_tasks_from_note` | Tasks from specific note | `path` |
| `get_tasks_with_due_dates` | Tasks sorted by due date | `status`, `folder` |

### get_all_tasks

```json
{
  "status": "open",
  "tag": "urgent",
  "limit": 50
}
```

Returns: `{ tasks: [{ text, status, due_date, source_path, line }] }`

---

## Advanced Graph Tools

Path finding and graph analysis.

| Tool | Purpose | Key Args |
|------|---------|----------|
| `get_link_path` | Shortest path between notes | `from`, `to`, `max_depth` |
| `get_common_neighbors` | Notes both notes link to | `note_a`, `note_b` |
| `find_bidirectional_links` | Mutual link pairs | `path` (optional) |
| `find_dead_ends` | Notes with backlinks but no outlinks | `folder`, `min_backlinks` |
| `find_sources` | Notes with outlinks but no backlinks | `folder`, `min_outlinks` |
| `get_connection_strength` | Connection strength score | `note_a`, `note_b` |

### get_link_path

```json
{
  "from": "people/Alice.md",
  "to": "projects/Gamma.md",
  "max_depth": 5
}
```

Returns: `{ found, path: ["people/Alice.md", "projects/Alpha.md", "projects/Gamma.md"], length }`

---

## Frontmatter Tools

Schema analysis and validation.

| Tool | Purpose | Key Args |
|------|---------|----------|
| `get_frontmatter_schema` | All fields used across vault | none |
| `get_field_values` | Unique values for a field | `field` |
| `find_frontmatter_inconsistencies` | Fields with mixed types | none |
| `validate_frontmatter` | Validate against schema | `schema`, `folder` |
| `find_missing_frontmatter` | Notes missing required fields | `folder_schemas` |

### validate_frontmatter

```json
{
  "schema": {
    "type": { "required": true, "values": ["project", "meeting", "note"] },
    "status": { "type": "string" }
  },
  "folder": "projects"
}
```

Returns: `{ notes_with_issues, results: [{ path, issues }] }`

### find_missing_frontmatter

```json
{
  "folder_schemas": {
    "projects": ["type", "status", "owner"],
    "meetings": ["date", "attendees"]
  }
}
```

Returns: `{ results: [{ path, missing_fields }] }`

---

## Periodic Tools

Automatic detection of daily/weekly/monthly note patterns.

| Tool | Purpose | Key Args |
|------|---------|----------|
| `detect_periodic_notes` | Find periodic note conventions | `type` (daily/weekly/monthly/quarterly/yearly) |

### detect_periodic_notes

```json
{
  "type": "daily"
}
```

Returns: `{ detected, folder, pattern, confidence, today_path, today_exists, candidates }`

---

## Bidirectional Bridge Tools

Bridge Graph-Native (wikilinks) and Schema-Native (frontmatter) paradigms.

| Tool | Purpose | Key Args |
|------|---------|----------|
| `detect_prose_patterns` | Find "Key: Value" patterns in prose | `path` |
| `suggest_frontmatter_from_prose` | Suggest YAML from prose patterns | `path` |
| `suggest_wikilinks_in_frontmatter` | Convert string values to wikilinks | `path` |
| `validate_cross_layer` | Check frontmatter ↔ prose consistency | `path` |

### detect_prose_patterns

```json
{
  "path": "meetings/2025-01-03.md"
}
```

Returns: `{ patterns: [{ key, value, line, isWikilink }] }`

### suggest_frontmatter_from_prose

```json
{
  "path": "meetings/2025-01-03.md"
}
```

Returns: `{ suggestions: [{ field, value, source_lines, confidence, preserveWikilink }] }`

---

## Pagination

Most list-returning tools support pagination:

| Arg | Default | Description |
|-----|---------|-------------|
| `limit` | 50 | Maximum results to return |
| `offset` | 0 | Skip first N results |

Example:
```json
{
  "limit": 20,
  "offset": 40
}
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

Use `health_check` at session start to verify MCP connectivity.

---

**Version**: 1.6.3
**Last Updated**: 2026-01-03
