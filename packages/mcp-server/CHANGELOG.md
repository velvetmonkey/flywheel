# Changelog

All notable changes to Flywheel MCP server will be documented in this file.

## [1.0.1] - 2026-01-03

### Changed

- **Renamed environment variable** - `OBSIDIAN_VAULT_PATH` → `PROJECT_PATH` for broader applicability

## [1.2.2] - 2026-01-01

### Fixed

- **Executable permissions** - Added chmod to build script to ensure dist/index.js has execute permissions when published

## [1.2.1] - 2026-01-01

### Fixed

- **Windows compatibility guards** - Added validation to prevent crashes from emoji characters in filenames
- **Path length validation** - Guard against Windows MAX_PATH (260 char) limit to prevent fs.stat failures
- Files with emoji or excessive path lengths are now gracefully skipped with warnings instead of crashing the MCP server

## [1.2.0] - 2024-12-XX

### Added

- **23 new tools** bringing total to 47
- Structure analysis: `get_note_structure`, `get_headings`, `get_section_content`, `find_sections`
- Task management: `get_all_tasks`, `get_tasks_from_note`, `get_tasks_with_due_dates`
- Frontmatter intelligence: `get_frontmatter_schema`, `get_field_values`, `find_frontmatter_inconsistencies`
- Deep graph analysis: `get_link_path`, `get_common_neighbors`, `find_bidirectional_links`, `find_dead_ends`, `find_sources`, `get_connection_strength`
- Temporal analysis: `get_contemporaneous_notes`, `get_note_metadata`
- Smart search: `get_recent_notes`, `get_stale_notes`, `get_notes_modified_on`, `get_notes_in_range`
- System: `refresh_index`, `get_all_entities`

### Improved

- Enhanced documentation with comparison tables and security section
- Added obsidian-scribe showcase in README

## [1.1.0] - 2024-XX-XX

### Added

- Wikilink services: `suggest_wikilinks`, `validate_links`, `find_broken_links`, `get_unlinked_mentions`
- Health tools: `get_vault_stats`, `get_folder_structure`, `get_activity_summary`
- Query tools: `search_notes` with frontmatter filtering

## [1.0.0] - Initial Release

### Added

- Core graph tools: `get_backlinks`, `get_forward_links`, `find_orphan_notes`, `find_hub_notes`
- In-memory vault indexing
- Privacy-first architecture (metadata only, no content exposure)
- Support for frontmatter, tags, and wikilinks parsing
