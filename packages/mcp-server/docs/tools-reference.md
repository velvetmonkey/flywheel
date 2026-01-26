# Flywheel MCP Tool Reference

Complete reference for MCP tools provided by `@bencassie/flywheel-mcp`.

See the [README](../README.md) for installation and configuration.

---

## Graph Intelligence

| Tool | What it does |
|------|--------------|
| `get_backlinks` | Who's linking to this note? |
| `get_forward_links` | What does this note link to? |
| `find_orphan_notes` | Notes nobody loves (no incoming links) |
| `find_hub_notes` | Your vault's superstars (highly connected) |

---

## Wikilink Services

| Tool | What it does |
|------|--------------|
| `suggest_wikilinks` | "You mentioned 'John'—want to link to [[John Smith]]?" |
| `validate_links` | Find broken links before they embarrass you |
| `find_broken_links` | [[Dead Note]] → nowhere |
| `get_unlinked_mentions` | "John" mentioned 47 times, linked 3 times |

---

## Vault Health

| Tool | What it does |
|------|--------------|
| `get_vault_stats` | The big picture: notes, links, tags, orphans |
| `get_folder_structure` | Your vault's anatomy |
| `get_activity_summary` | What's been happening lately? |

---

## Smart Search

| Tool | What it does |
|------|--------------|
| `search_notes` | Query by frontmatter, tags, folders—Dataview vibes |
| `get_recent_notes` | Modified in the last N days |
| `get_stale_notes` | Important notes gathering dust |
| `get_notes_modified_on` | What happened on 2024-01-15? |
| `get_notes_in_range` | Activity between two dates |

---

## Deep Graph Analysis

| Tool | What it does |
|------|--------------|
| `get_link_path` | How do these two notes connect? (A → B → C → D) |
| `get_common_neighbors` | What do these notes have in common? |
| `find_bidirectional_links` | Mutual admirers (A ↔ B) |
| `find_dead_ends` | Popular notes that link nowhere |
| `find_sources` | Link-givers, not link-receivers |
| `get_connection_strength` | How related are these notes, really? |

---

## Structure Analysis

| Tool | What it does |
|------|--------------|
| `get_note_structure` | Full heading tree and sections |
| `get_headings` | Just the headings, quick |
| `get_section_content` | Extract a specific section |
| `find_sections` | Find all "## References" across the vault |

---

## Task Management

| Tool | What it does |
|------|--------------|
| `get_all_tasks` | Every `- [ ]` in your vault |
| `get_tasks_from_note` | Tasks in a specific note |
| `get_tasks_with_due_dates` | What's due? |

---

## Frontmatter Intelligence

| Tool | What it does |
|------|--------------|
| `get_frontmatter_schema` | What fields exist across your vault? |
| `get_field_values` | All unique values for `status` field |
| `find_frontmatter_inconsistencies` | `status: "done"` vs `status: true` chaos |

---

## Temporal Analysis

| Tool | What it does |
|------|--------------|
| `get_contemporaneous_notes` | Edited around the same time |
| `get_note_metadata` | Quick stats without reading content |

---

## System

| Tool | What it does |
|------|--------------|
| `refresh_index` | Rebuilt after Obsidian changes |
| `get_all_entities` | Every linkable thing (titles + aliases) |

---

[← Back to README](../README.md)
