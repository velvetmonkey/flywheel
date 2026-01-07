---
skill: schema-compute
---

# /schema-compute - Auto-Generate Derived Fields

Auto-compute derived frontmatter fields from note content.

## Usage

```
/schema-compute Project.md     # Compute for specific note
/schema-compute projects/      # Compute for folder
```

## Computable Fields

| Field | Source | Description |
|-------|--------|-------------|
| `word_count` | Content | Total words |
| `link_count` | Content | Wikilinks in note |
| `backlink_count` | Graph | Notes linking here |
| `tag_count` | Tags | Number of tags |
| `reading_time` | Content | Est. minutes to read |
| `created` | Filesystem | Creation date |
| `last_updated` | Filesystem | Modified date |

## Where Output Goes

| Action | Target | Notes |
|--------|--------|-------|
| Preview | Console output | Computed values |
| Edits | Frontmatter | After confirmation |

## Example Output

```
Computed Fields for [[Project Alpha]]
===============================================

Current frontmatter:
  type: project
  status: active

COMPUTED VALUES:

  Field           Value        Source
  ─────────────────────────────────────
  word_count      1,234        Content analysis
  link_count      45           Wikilink count
  backlink_count  23           Graph query
  tag_count       5            Tag count
  reading_time    6 min        Word count / 200
  created         2024-01-15   Filesystem
  last_updated    2025-12-30   Filesystem

PROPOSED FRONTMATTER:

  type: project
  status: active
  word_count: 1234
  link_count: 45
  backlink_count: 23
  reading_time: 6
  created: 2024-01-15
  last_updated: 2025-12-30

Add computed fields? [y/n]

===============================================
```
