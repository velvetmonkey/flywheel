# Flywheel Roadmap

## Current: v1.25.0 - Pure MCP Server (January 2026)

**Goal**: Focused MCP server for vault intelligence.

### Changes
- Removed Claude plugin infrastructure
- 44 MCP tools for graph and schema intelligence
- Zero external dependencies beyond MCP protocol

---

## Planned: v1.26.0 - Enhanced Graph Analysis

**Goal**: Deeper graph intelligence tools.

### New MCP Tools
- `find_clusters()` - Detect knowledge clusters (groups of highly connected notes)
- `get_neighborhood(path, depth)` - Get all notes within N hops of a note
- `calculate_pagerank()` - Identify most important notes by link structure
- `find_bridges()` - Find notes that connect otherwise separate clusters

### Enhanced Tools
- `get_vault_stats()` - Add graph density, clustering coefficient metrics
- `find_hub_notes()` - Add centrality scoring options

---

## Planned: v1.27.0 - Schema Enforcement

**Goal**: Runtime schema validation for vault consistency.

### New MCP Tools
- `define_schema(folder, schema)` - Set expected schema for a folder
- `validate_vault()` - Check all notes against folder schemas
- `generate_schema_report()` - Comprehensive schema analysis report

### Features
- Schema definition stored in `.flywheel.json`
- Validation returns actionable fix suggestions
- Support for required fields, allowed values, type checking

---

## Future: v2.0 - Multi-Vault Support

**Goal**: Cross-vault intelligence.

### Features
- Cross-vault linking resolution
- Federated search across vaults
- Shared schema definitions

---

## Version History

| Version | Date | Highlights |
|---------|------|------------|
| 1.25.0 | 2026-01 | Clean MCP server - removed plugin infrastructure |
| 1.24.0 | 2026-01 | Architecture split - moved personal features to vault-personal |
| 1.23.0 | 2026-01 | Bidirectional bridge tools |
| 1.22.0 | 2026-01 | Schema intelligence - inferred conventions, 9 new tools |
| 1.21.0 | 2026-01 | Periodic note detection |
| 1.20.0 | 2025-12 | Task management tools |
| 1.19.0 | 2025-12 | Structure tools (headings, sections) |
| 1.18.0 | 2025-11 | Temporal tools (stale, concurrent) |
| 1.0.0 | 2025-10 | Initial release - graph tools |
