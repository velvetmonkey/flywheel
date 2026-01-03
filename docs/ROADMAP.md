# Flywheel Roadmap

## Current: v1.8.0 - Workflow Templates (January 2026)

**Goal**: Pre-built automation for common business processes.

### New Skills (6)
- `/extract-actions` - Extract action items from meeting notes (NLP parsing)
- `/weekly-review` - Comprehensive weekly review with reflection and planning
- `/standup-rollup` - Aggregate team standups into summary
- `/okr-review` - Quarterly OKR scoring and next quarter planning
- `/onboard-customer` - Create customer onboarding checklist from template
- `/workflow-define` - Define custom workflows as markdown

### New Agents (5)
- `action-extraction-agent` - Parse meetings for explicit and implicit action items
- `weekly-review-agent` - Rollup + reflection + goal progress + planning
- `standup-agent` - Team standup aggregation with blocker analysis
- `okr-review-agent` - OKR scoring (0-1.0) with evidence matching
- `customer-onboarding-agent` - Template-based checklist creation

### New Templates (4)
- `meeting.md` - Standard meeting note with attendees, agenda, actions
- `standup.md` - Team standup format (Yesterday/Today/Blockers)
- `okr.md` - OKR tracking with objectives and key results tables
- `customer-onboarding.md` - Phased onboarding checklist

### Features
- NLP-style action extraction (not just checkboxes)
- Team workflow support (standups, OKRs)
- Template interpolation with variables
- Workflow definition format for custom processes

---

## Previous: v1.7.x (January 2025)

### v1.7.4 - Bug Fixes
- Fix read-cache locking bug for parallel Reads
- Gate 1 now allows Write to new files
- Gate 1 session cache for context summarization

### v1.7.0 - Advanced Schema Intelligence

**Goal**: Make frontmatter as powerful as a database - with zero configuration.

#### New MCP Tools (6)
- `infer_folder_conventions(folder)` - Auto-detect metadata conventions per folder
- `find_incomplete_notes(folder)` - Find notes missing expected fields
- `suggest_field_values(field, context)` - Context-aware value suggestions
- `compute_frontmatter(path, fields)` - Auto-compute derived fields
- `rename_field(old, new, scope)` - Bulk rename frontmatter fields
- `migrate_field_values(field, mapping)` - Transform values in bulk

#### New Skills (5)
- `/schema-infer`, `/schema-gaps`, `/schema-apply`, `/schema-compute`, `/schema-migrate`

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
| 1.8.0 | 2026-01 | Workflow Templates - 6 skills, 5 agents, 4 templates for business workflows |
| 1.7.4 | 2026-01 | Bug fixes - read-cache locking, Gate 1 improvements |
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
