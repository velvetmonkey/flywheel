# Changelog

All notable changes to Flywheel MCP server will be documented in this file.

## [1.6.3] - 2026-01-03

### Fixed

- **Registered missing frontmatter tools** - `validate_frontmatter` and `find_missing_frontmatter` now properly exported and available via MCP
- All 5 frontmatter tools now accessible

## [1.6.2] - 2026-01-03

### Added

- **Six Gates REAL enforcement** - Gates 1, 2, 4 enforced via PreToolUse hooks (can block operations)

## [1.6.1] - 2026-01-03

### Added

- **Six Gates framework** - Session and verify hooks for safety enforcement

## [1.6.0] - 2026-01-03

### Added

- **Bidirectional Bridge tools** - Bridge between Graph-Native and Schema-Native paradigms
  - `detect_prose_patterns` - Find "Key: Value" patterns in prose
  - `suggest_frontmatter_from_prose` - Convert prose patterns to YAML suggestions
  - `suggest_wikilinks_in_frontmatter` - Convert string values to wikilinks
  - `validate_cross_layer` - Check frontmatter ↔ prose consistency

## [1.5.0] - 2026-01-03

### Added

- **Periodic note detection** - Zero-config detection of daily/weekly/monthly notes
  - `detect_periodic_notes` - Auto-detect periodic note patterns in vault
- Marketplace installation support
- Startup Ops demo vault

## [1.4.0] - 2026-01-03

### Added

- **Frontmatter validation** - Schema enforcement for vault consistency
  - `validate_frontmatter` - Validate notes against a schema
  - `find_missing_frontmatter` - Find notes missing required fields by folder

## [1.3.0] - 2026-01-03

### Added

- **Task management tools** - Extract and query tasks from vault
  - `get_all_tasks` - Get all tasks with filtering (status, folder, tag)
  - `get_tasks_from_note` - Get tasks from a specific note
  - `get_tasks_with_due_dates` - Get tasks sorted by due date

## [1.2.0] - 2026-01-03

### Added

- **Structure analysis tools**
  - `get_note_structure` - Get heading structure of a note
  - `get_headings` - Get all headings (lightweight)
  - `get_section_content` - Get content under a heading
  - `find_sections` - Search headings across vault

- **Frontmatter intelligence**
  - `get_frontmatter_schema` - Analyze all fields across vault
  - `get_field_values` - Get unique values for a field
  - `find_frontmatter_inconsistencies` - Detect type mismatches

- **Deep graph analysis**
  - `get_link_path` - Find shortest path between notes
  - `get_common_neighbors` - Find notes both notes link to
  - `find_bidirectional_links` - Find mutual link pairs
  - `find_dead_ends` - Notes with backlinks but no outlinks
  - `find_sources` - Notes with outlinks but no backlinks
  - `get_connection_strength` - Calculate connection strength

- **Temporal analysis**
  - `get_contemporaneous_notes` - Notes edited around same time
  - `get_note_metadata` - Metadata without full content
  - `get_recent_notes` - Recently modified notes
  - `get_stale_notes` - Important notes not recently edited
  - `get_notes_modified_on` - Notes modified on specific date
  - `get_notes_in_range` - Notes in date range
  - `get_activity_summary` - Activity summary over period

- **System tools**
  - `refresh_index` - Rebuild vault index
  - `get_all_entities` - All linkable titles and aliases

### Fixed

- **Windows compatibility** - Guards for emoji filenames and MAX_PATH limits
- **Executable permissions** - chmod in build script for published dist

## [1.1.0] - 2026-01-03

### Added

- **Wikilink services**
  - `suggest_wikilinks` - Find text that could be linked
  - `validate_links` - Check for broken links
  - `find_broken_links` - Find links to non-existent notes
  - `get_unlinked_mentions` - Find unlinked entity mentions

- **Health tools**
  - `get_vault_stats` - Comprehensive vault statistics
  - `get_folder_structure` - Vault folder organization
  - `health_check` - MCP server health status

- **Query tools**
  - `search_notes` - Search by frontmatter/tags/folder

## [1.0.0] - 2026-01-02

### Added

- Core graph tools: `get_backlinks`, `get_forward_links`, `find_orphan_notes`, `find_hub_notes`
- In-memory vault indexing
- Privacy-first architecture (metadata only, no content exposure)
- Support for frontmatter, tags, and wikilinks parsing

---

*Note: Versions 1.0.0 - 1.6.3 were consolidated in the Flywheel monorepo on 2026-01-02/03.*
