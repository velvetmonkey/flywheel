# Flywheel Roadmap

## Current: v1.7.0 - Advanced Schema Intelligence (January 2025)

**Goal**: Make frontmatter as powerful as a database - with zero configuration.

### Design Philosophy
- **Inferred-only schemas** - No explicit schema files, auto-detect from vault patterns
- **Convention over configuration** - Zero-config, smart defaults
- **Actionable output** - Clear recommendations, not just data dumps

### New MCP Tools (6)
- `infer_folder_conventions(folder)` - Auto-detect metadata conventions per folder
- `find_incomplete_notes(folder)` - Find notes missing expected fields
- `suggest_field_values(field, context)` - Context-aware value suggestions
- `compute_frontmatter(path, fields)` - Auto-compute derived fields (word_count, link_count, etc.)
- `rename_field(old, new, scope)` - Bulk rename frontmatter fields
- `migrate_field_values(field, mapping)` - Transform values in bulk

### New Skills (5)
- `/schema-infer` - "What conventions does this folder use?"
- `/schema-gaps` - "Find notes with missing fields"
- `/schema-apply` - "Apply inferred conventions to incomplete notes"
- `/schema-compute` - "Add computed fields (word_count, reading_time)"
- `/schema-migrate` - "Rename fields or transform values"

### New Agent (1)
- `schema-intelligence-agent` - Comprehensive multi-step analysis (Gate 3 compliant)

### Schema Features
- Field frequency analysis (required vs optional)
- Enumerable field detection
- Naming pattern detection (e.g., "YYYY-MM-DD.md")
- Computed fields (word_count, link_count, reading_time, backlink_count)
- Dry-run by default for all mutations

---

## Previous: v1.6.x (January 2025)

### v1.6.3 - Foundation Fix
- Registered missing frontmatter MCP tools
- Added `/onboard` skill for first-run experience
- Added `docs/QUICKSTART.md`

### v1.6.2 - Six Gates REAL Enforcement
- Gates 1, 2, 4 enforced via PreToolUse hooks (can block)
- Gate 3 enforced via project-level agent validation
- All 8 agents Gate 3 compliant

See [SIX_GATES.md](../packages/claude-plugin/skills/_patterns/SIX_GATES.md) for full specification.

---

## v1.8.0 - Workflow Templates

**Goal**: Pre-built automation for common business processes.

### Templates
- Weekly review workflow
- Meeting notes -> action items
- Daily standup rollup
- Quarterly OKR review
- Customer onboarding checklist

### Features
- Workflow editor (define steps, triggers, conditions)
- Trigger-based automation (on file create, on schedule)
- Workflow variables and templating

---

## v2.0 - Enterprise Features

**Goal**: Ready for teams and enterprises.

### Multi-Vault
- Cross-vault linking
- Vault federation
- Shared schemas across vaults

### Collaboration
- Real-time presence (who's editing what)
- Comment threads on notes
- Review workflows

### Compliance
- Audit logging
- Access control
- Data retention policies

---

## Version History

| Version | Date | Highlights |
|---------|------|------------|
| 1.7.0 | 2025-01 | Advanced Schema Intelligence - inferred schemas, 6 new MCP tools, 5 new skills |
| 1.6.3 | 2025-01 | Register missing frontmatter tools, /onboard skill, QUICKSTART.md |
| 1.6.2 | 2025-01 | Six Gates REAL enforcement, Gate 3 hooks |
| 1.6.1 | 2025-01 | Six Gates framework, session/verify hooks |
| 1.6.0 | 2025-01 | Bidirectional Bridge |
| 1.5.0 | 2024-12 | Startup Ops demo, marketplace installation |
| 1.4.0 | 2024-12 | Periodic note detection |
| 1.3.0 | 2024-11 | Task management tools |
| 1.2.0 | 2024-11 | Structure tools (headings, sections) |
| 1.1.0 | 2024-10 | Temporal tools (stale, concurrent) |
| 1.0.0 | 2024-10 | Initial release |
