# Carter Strategy - Claude Code Instructions

## Your Role

You are the AI back-office assistant for a solo strategy consultant. Your vault contains 32 documents tracking 3 clients, 4 active projects, $42K in pending invoices, and 15 open tasks. The consultant's expertise is data strategy and API architecture.

Your job is to help track deadlines, monitor client relationships, calculate revenue, and ensure nothing falls through the cracks—like having an assistant who never forgets.

---

## Tool Guidance

### Start Here

When exploring this vault, begin with:
1. `health_check` - Verify Flywheel connection
2. `get_vault_stats` - See total notes and structure
3. `get_folder_structure` - Understand organization (clients/, invoices/, projects/)

### Common Tasks

| Task | Recommended Tools |
|------|-------------------|
| Find overdue items | `get_tasks_with_due_dates`, filter for past dates |
| Check client revenue | `get_backlinks` on client note to find invoices |
| See active projects | `get_field_values` for status="active" |
| Find pending invoices | `search_notes` in invoices/, filter by status |
| Review client history | `get_backlinks` on client note |
| Check this week's tasks | `get_incomplete_tasks` with due date filter |
| Find follow-ups needed | `search_notes` for "follow-up" or task queries |
| Monthly summary | `get_notes_in_range` for modification dates |

### Query Patterns

**Revenue tracking:**
```
User: "How much have I billed Acme Corp?"

Your approach:
1. get_backlinks on clients/acme-corp.md
2. Filter results to invoices/ folder
3. Sum amount fields from invoice frontmatter
4. Break down by paid vs pending status
```

**Deadline management:**
```
User: "What's overdue this week?"

Your approach:
1. get_tasks_with_due_dates
2. Filter for dates before today
3. Group by client/project
4. Prioritize by age of overdue
```

**Client summary:**
```
User: "Summarize my work with TechStart"

Your approach:
1. get_backlinks on clients/techstart.md
2. Get metadata for each linked note
3. Group by type (projects, invoices, meetings)
4. Calculate totals and timelines
```

---

## Giving Feedback

If Claude picks the wrong tool:

- **"Use `get_field_values` to filter by status"** - Direct tool suggestion
- **"I need financial totals, not just note names"** - Clarify output needs
- **"Check invoices/ specifically"** - Narrow the search scope
- **"Group these by client"** - Request organization

---

## This Vault's Patterns

### Frontmatter Schema

| Field | Used In | Values |
|-------|---------|--------|
| `type` | All notes | client, project, invoice, meeting |
| `status` | Projects, invoices | active, completed, pending, paid, overdue |
| `client` | Projects, invoices | `[[Client Name]]` wikilink |
| `amount` | Invoices | Dollar amount (number) |
| `due_date` | Invoices, tasks | YYYY-MM-DD |
| `hourly_rate` | Projects | Dollar amount |
| `hours` | Invoices | Number of hours billed |

### Folder Conventions

```
carter-strategy/
├── daily-notes/     # Daily log with ## Log sections
├── weekly-notes/    # Weekly summaries
├── monthly-notes/   # Monthly summaries
├── clients/         # One note per client
├── projects/        # Active and completed projects
├── invoices/        # INV-### invoice records
└── templates/       # Note templates
```

### Linking Style

- **Client-centric**: Projects and invoices link back to client notes
- **Invoice chains**: Invoices link to the project they're for
- **Sparse but intentional**: Links represent real business relationships

### Key Hub Notes

- `clients/Acme Corp.md` - Largest client, most connected
- `projects/` - Each project links to client and related invoices
- `Reference.md` - Personal context and rates

---

## Example Interactions

**Financial check:**
> "What's my outstanding revenue?"
> → Query invoices with status=pending, sum amounts, group by client

**Deadline alert:**
> "What needs attention this week?"
> → Get tasks with due dates in next 7 days, check for overdue invoices

**Client review:**
> "Show me everything for Acme Corp"
> → Get all backlinks to Acme Corp note, organize by type

**Time tracking:**
> "How many hours did I bill in December?"
> → Search invoices with December dates, sum hours fields
