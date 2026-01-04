# Carter Strategy - Demo Vault

**Scenario**: A solo strategy consultant running a one-person practice, working with tech startups and enterprise clients on data strategy, API architecture, and digital transformation.

**Practice Focus**: Data migrations, API design, cloud strategy
**Client Mix**: TechStart Inc (startup), Acme Corp (manufacturing), GlobalBank (finance)
**Status**: Active practice, Q1 2026 planning

## Quick Start

1. **Open this folder in your markdown editor**:
   - Obsidian: Open as vault
   - VSCode: Open folder
   - Cursor: Open folder

2. **Install Flywheel** (if you haven't):
   ```
   /plugin marketplace add bencassie/flywheel
   /plugin install flywheel@bencassie-flywheel
   ```

3. **Start exploring**:
   - Try: `/vault-due` - See what tasks are due
   - Try: `/vault-stale` - Find knowledge that needs review
   - Try: `/vault-schema` - See all your frontmatter fields
   - Ask: "What's my revenue this month?"

## What This Demonstrates

**One person = five-person team**: This demo shows how a solo consultant manages clients, projects, proposals, invoices, and reusable knowledge - all with AI leverage.

### Key Features Showcased

| Feature | Tool | Example |
|---------|------|---------|
| **Zero-config detection** | `detect_periodic_notes` | Auto-detects daily/weekly/monthly patterns |
| **Task management** | `/vault-due` | 15 tasks with due dates, overdue alerts |
| **Stale note detection** | `/vault-stale` | Finds important but neglected knowledge |
| **Rich queries** | `search_notes` | Query by frontmatter (type, status, client) |
| **Schema validation** | `/vault-schema-check` | Detects frontmatter inconsistencies |
| **Relationship paths** | `get_link_path` | How does X connect to Y? |
| **Rollup summaries** | `/rollup` | Daily to weekly to monthly aggregation |

### Frontmatter Schema

This vault demonstrates **heavy frontmatter** usage (12+ fields):

| Note Type | Key Fields |
|-----------|------------|
| `daily` | date, billable_hours, clients_worked |
| `client` | status, contact, industry, rate, total_billed |
| `project` | status, client, budget, billed_to_date, priority |
| `proposal` | status, client, value, decision_due |
| `invoice` | status, amount, due, project |
| `knowledge` | category, last_reviewed, used_in |

### File Structure

```
carter-strategy/
├── daily-notes/        # Time logs for billing (8 notes)
├── weekly-notes/       # Weekly summaries (2 notes)
├── monthly-notes/      # Monthly rollups (1 note)
├── clients/            # Client profiles (3 notes)
├── projects/           # Project tracking (4 notes)
├── proposals/          # Sales pipeline (2 notes)
├── invoices/           # Financial tracking (2 notes)
├── knowledge/          # Reusable playbooks (4 notes)
├── admin/              # Business operations (2 notes)
└── README.md

Total: ~30 notes
```

## User Journey Example

```
Solo consultant's morning routine:

1. Session starts
   → Flywheel auto-detects: "Daily notes: daily-notes/YYYY-MM-DD.md"
   → "3 overdue tasks, 2 pending invoices"

2. "What's due this week?"
   → /vault-due
   → 3 overdue, 2 this week, 4 next week
   → "Send TechStart Phase 2 proposal by Sunday"

3. "Show me active projects"
   → search_notes({ type: "project", where: { status: "active" }})
   → Acme Data Migration: $42K billed of $75K budget
   → TechStart MVP Build: $18K billed of $25K budget

4. "What knowledge should I review?"
   → /vault-stale
   → Data Migration Playbook (6 months stale, 8 backlinks)
   → "Heavily referenced but needs updating"

5. "How does my daily note connect to that playbook?"
   → get_link_path("daily-notes/2026-01-02.md", "knowledge/Data Migration Playbook.md")
   → Path: Daily → Acme Data Migration → Playbook (2 hops)

6. "Summarize my December"
   → /rollup
   → 142 billable hours, $42,600 revenue
   → 2 projects active, 3 proposals sent

7. "Check my frontmatter consistency"
   → /vault-schema-check
   → "rate" field has mixed types: number (2), string (1)

Business intelligence in 5 minutes.
```

## Intentional Demo Patterns

**Periodic Notes** (for `detect_periodic_notes`):
- 8 daily notes following `YYYY-MM-DD.md` pattern
- 2 weekly notes following `YYYY-WXX.md` pattern
- 1 monthly note following `YYYY-MM.md` pattern

**Stale Notes** (for `/vault-stale`):
- `knowledge/Data Migration Playbook.md` - 6 months old, heavily referenced
- `projects/GlobalBank API Audit.md` - completed project, not archived

**Tasks with Due Dates** (for `/vault-due`):
- 15 tasks across notes
- 3 intentionally overdue
- Mix of project work, admin, and follow-ups

**Schema Inconsistency** (for `/vault-schema-check`):
- `rate` field: number in some clients, string in others

**Relationship Paths** (for `get_link_path`):
- Daily notes → Projects → Knowledge base (2-hop paths)
- Clients ↔ Invoices (bidirectional, strong connection)

## Comparison: Artemis Rocket vs Carter Strategy

| Aspect | Artemis Rocket | Carter Strategy |
|--------|----------------|-----------------|
| **Scale** | 65 notes, 15-person team | 30 notes, solo |
| **Domain** | Aerospace engineering | Business consulting |
| **Graph** | Deep clusters (propulsion = 10 notes) | Star pattern (client-centric) |
| **Frontmatter** | 4-5 fields | 12+ fields |
| **Tasks** | Meeting-focused | Deadline-driven (15 tasks) |
| **Periodic notes** | Present but not emphasized | Central feature |
| **Primary tools** | /vault-health, /auto-log, /vault-orphans | /vault-due, /vault-stale, /vault-schema, /rollup |

## Why This Works

**vs Spreadsheets**:
- Linked context - click from invoice to project to client
- AI-powered queries - natural language, not formulas
- Automatic summarization - rollup without manual data entry

**vs CRM Software**:
- No monthly fees - plain markdown
- Full ownership - Git-friendly, portable
- AI has full context - not locked behind APIs

**vs Notion/Obsidian Alone**:
- Zero-config intelligence - Flywheel detects patterns automatically
- Task awareness - due dates surfaced proactively
- Schema validation - catch inconsistencies before they compound

## Next Steps

1. Explore the vault - click through wikilinks
2. Try Flywheel queries - `/vault-due`, `/vault-stale`, `/vault-schema`
3. Ask questions - "What's my revenue?", "What needs follow-up?"
4. Run a rollup - `/rollup` to see aggregation in action
5. See the pattern - this scales to any solo practice

## About Flywheel

This demo showcases **Flywheel** - The Agentic Markdown Operating System.

Starting a consulting practice? Install Flywheel - get AI-powered business infrastructure from day one.

Learn more: https://github.com/bencassie/flywheel
