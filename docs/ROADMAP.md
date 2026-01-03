# Flywheel Roadmap

## Current: v1.6.2 (January 2025)

### Six Gates REAL Enforcement
- Gates 1, 2, 4 enforced via PreToolUse hooks (can block)
- Gate 3 enforced via project-level agent validation
- Gates 5, 6 enforced via session/post hooks (warn only)
- All 8 agents Gate 3 compliant

See [SIX_GATES.md](../packages/claude-plugin/skills/_patterns/SIX_GATES.md) for full specification.

---

## Next: v1.7.0 - Advanced Schema Intelligence

**Goal**: Make frontmatter as powerful as a database.

### New MCP Tools
- `validate_frontmatter(path, schema)` - Validate note against JSON schema
- `find_incomplete_notes(type, required_fields)` - Find notes missing required fields
- `compute_frontmatter(path, fields)` - Auto-compute derived fields from content
- `rename_field(old, new, scope)` - Bulk rename frontmatter fields across vault

### New Skills
- `/schema-define` - Define reusable schemas
- `/schema-apply` - Apply schema to notes
- `/schema-migrate` - Migrate notes between schema versions

### Schema Features
- Schema inheritance (project inherits from base)
- Required vs optional fields
- Type coercion (string dates -> Date objects)
- Computed fields (word_count, last_updated)

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
| 1.6.2 | 2025-01 | Six Gates REAL enforcement, Gate 3 hooks |
| 1.6.1 | 2025-01 | Six Gates framework, session/verify hooks |
| 1.6.0 | 2025-01 | Bidirectional Bridge |
| 1.5.0 | 2024-12 | Startup Ops demo, marketplace installation |
| 1.4.0 | 2024-12 | Periodic note detection |
| 1.3.0 | 2024-11 | Task management tools |
| 1.2.0 | 2024-11 | Structure tools (headings, sections) |
| 1.1.0 | 2024-10 | Temporal tools (stale, concurrent) |
| 1.0.0 | 2024-10 | Initial release |
