# Skills Reference

Flywheel provides 49 skills organized by function. Skills auto-trigger on keywords or can be invoked via `/skill-name`.

**Skill Types:**
- **READ** - Query/analyze only, no file modifications
- **MUTATE** - Can modify files (follows Six Gates safety framework)

---

## Quick Reference

| Category | Skills | Purpose |
|----------|--------|---------|
| [Onboarding](#onboarding) | 2 | New user welcome, setup |
| [Graph Analysis](#graph-analysis) | 10 | Links, hubs, orphans, paths |
| [Search & Query](#search--query) | 4 | Find notes, sections, content |
| [Health & Maintenance](#health--maintenance) | 4 | Vault health, broken links |
| [Tasks & Logging](#tasks--logging) | 5 | Tasks, logging, due dates, actions |
| [Schema & Frontmatter](#schema--frontmatter) | 11 | Schema, validation, inference |
| [Wikilinks](#wikilinks) | 5 | Suggest, apply, fix links |
| [Rollup & Summaries](#rollup--summaries) | 4 | Periodic summarization, reviews |
| [Bidirectional Bridge](#bidirectional-bridge) | 1 | Bidirectional link analysis |
| [Workflows](#workflows) | 2 | Custom workflow automation |

---

## Onboarding

| Skill | Type | Trigger | Purpose |
|-------|------|---------|---------|
| `/onboard-vault` | READ | "hello flywheel", "getting started" | Welcome + vault health overview |
| `/setup-flywheel` | MUTATE | "setup flywheel", "configure flywheel" | Install and configure Flywheel |

### /onboard-vault

Welcome new users with vault health check, stats, and suggested next steps.

**Triggers**: "onboard", "getting started", "hello flywheel", "what can you do"

**Output**:
- Health status
- Note count, link count, orphan count
- Top hub notes
- Suggested next actions

### /setup-flywheel

Install and configure Flywheel MCP server for a vault.

**Triggers**: "setup flywheel", "configure flywheel", "install flywheel", "flywheel not working"

**Process**:
1. Detect vault location
2. Generate MCP configuration
3. Create `.flywheel/` config directory
4. Test MCP connection

---

## Graph Analysis

| Skill | Type | Trigger | Purpose |
|-------|------|---------|---------|
| `/show-backlinks` | READ | "backlinks to X" | Show incoming/outgoing links |
| `/find-hubs` | READ | "hub notes", "most connected" | Find highly connected notes |
| `/find-orphans` | READ | "orphan notes", "disconnected" | Find notes with no backlinks |
| `/show-path` | READ | "path from X to Y" | Find shortest link path |
| `/find-related-notes` | READ | "related to X" | Find related notes |
| `/show-common-links` | READ | "common between X and Y" | Find shared connections |
| `/find-dead-ends` | READ | "dead ends" | Notes with backlinks but no outlinks |
| `/show-concurrent` | READ | "edited same time as X" | Contemporaneous notes |
| `/find-clusters` | READ | "clusters" | Find note clusters |
| `/check-link-strength` | READ | "connection strength" | Calculate link strength |

### /show-backlinks

Show all backlinks and forward links for a note.

**Triggers**: "backlinks", "who links here", "what links to", "incoming links"

**Example**: "show backlinks to [[Project Alpha]]"

### /find-hubs

Find hub notes (highly connected notes with many links).

**Triggers**: "hubs", "hub notes", "most connected", "popular notes", "key concepts"

**Output**: List of notes sorted by total connections

### /find-orphans

Find orphan notes (notes with no backlinks).

**Triggers**: "orphans", "orphan notes", "disconnected", "isolated notes"

**Output**: List of orphan notes with modification dates

### /show-path

Find the shortest link path between two notes.

**Triggers**: "path from", "path to", "how to get from", "connection between"

**Example**: "find path from [[Alice]] to [[Project Gamma]]"

---

## Search & Query

| Skill | Type | Trigger | Purpose |
|-------|------|---------|---------|
| `/search-vault` | READ | "search", "find notes" | Advanced search with filters |
| `/show-section` | READ | "show section X" | Get content under heading |
| `/find-sections` | READ | "sections matching X" | Find sections across vault |
| `/show-activity` | READ | "recent activity" | Vault activity summary |

### /search-vault

Advanced vault search with filters (folder, tags, frontmatter).

**Triggers**: "search vault", "find notes", "query notes", "notes with"

**Examples**:
- "search for notes in projects folder"
- "find notes tagged with #active"
- "show notes where status = active"

### /show-section

Get the content under a specific heading.

**Triggers**: "show section", "get section", "what's under"

**Example**: "show the Tasks section of [[Project Alpha]]"

---

## Health & Maintenance

| Skill | Type | Trigger | Purpose |
|-------|------|---------|---------|
| `/check-health` | READ | "vault health", "health report" | Full vault diagnostics |
| `/vault-fix-links` | MUTATE | "fix links", "broken links" | Find and repair broken links |
| `/check-folder-health` | READ | "folder health" | Health by folder |
| `/check-link-density` | READ | "link density" | Link density metrics |

### /check-health

Comprehensive vault diagnostics and health report.

**Triggers**: "vault health", "health report", "vault diagnostics", "vault status"

**Output**:
- Health score (0-100%)
- Note/link counts
- Orphan/broken link counts
- Top hubs
- Recommendations

### /vault-fix-links

Find and repair broken wikilinks in vault.

**Triggers**: "fix links", "broken links", "repair vault", "dead links"

**Process**:
1. Find all broken links
2. Suggest fixes (similar note names)
3. Apply fixes with confirmation

---

## Tasks & Logging

| Skill | Type | Trigger | Purpose |
|-------|------|---------|---------|
| `/add-log` | MUTATE | "log X", "captains log" | Add timestamped log entry |
| `/show-tasks` | READ | "all tasks", "show tasks" | List vault tasks |
| `/show-due-tasks` | READ | "due soon", "upcoming tasks" | Tasks with due dates |
| `/add-task` | MUTATE | "add task" | Add task to note |
| `/extract-actions` | MUTATE | "extract actions", "pull action items" | Extract action items from notes |

### /add-log

Auto-log entries to today's daily note.

**Triggers**: "log", "captains log", "record", "note this", "write this down"

**Format**: `- HH:MM [description]`

**Examples**:
- "log Fixed authentication bug"
- "captains log: Meeting with product team"

### /show-tasks

Get all tasks from the vault with filtering options.

**Triggers**: "all tasks", "task list", "show tasks", "open tasks", "todos"

**Filters**: status (open/completed), folder, tag

### /show-due-tasks

Get tasks sorted by due date.

**Triggers**: "due soon", "upcoming tasks", "what's due", "deadlines"

### /extract-actions

Extract action items from notes or conversation context.

**Triggers**: "extract actions", "pull action items", "action items from"

**Output**: List of extracted tasks with source context

---

## Schema & Frontmatter

| Skill | Type | Trigger | Purpose |
|-------|------|---------|---------|
| `/show-schema` | READ | "vault schema" | Analyze frontmatter schema |
| `/check-schema` | READ | "validate schema" | Validate against schema |
| `/show-field-values` | READ | "values for X field" | Get unique field values |
| `/normalize-note` | READ | "normalize note" | Normalize frontmatter |
| `/promote-frontmatter` | READ | "promote to frontmatter" | Move prose patterns to YAML |
| `/find-gaps` | READ | "missing frontmatter" | Find missing fields |
| `/schema-infer` | READ | "infer schema" | Auto-detect folder conventions |
| `/schema-gaps` | READ | "incomplete notes" | Find notes missing fields |
| `/schema-apply` | MUTATE | "apply schema" | Apply conventions to notes |
| `/schema-compute` | MUTATE | "compute fields" | Add computed frontmatter |
| `/schema-migrate` | MUTATE | "rename field" | Rename/transform field values |

### /show-schema

Analyze all frontmatter fields used across the vault.

**Triggers**: "vault schema", "frontmatter schema", "what fields"

**Output**: Field names, types, usage counts

### /check-schema

Validate notes against expected schema.

**Triggers**: "validate schema", "schema check", "check frontmatter"

**Example**: "validate projects folder has type, status, owner"

### /find-gaps

Find notes missing expected frontmatter fields.

**Triggers**: "missing frontmatter", "gaps in", "incomplete notes"

---

## Wikilinks

| Skill | Type | Trigger | Purpose |
|-------|------|---------|---------|
| `/suggest-links` | MUTATE | "suggest links" | Suggest wikilinks for note |
| `/apply-wikilinks` | MUTATE | "apply links" | Add suggested wikilinks |
| `/find-unlinked-mentions` | MUTATE | "unlinked mentions" | Find text that could be linked |
| `/wikilinkify-frontmatter` | READ | "wikilinkify frontmatter" | Convert strings to wikilinks |
| `/rebuild-cache` | MUTATE | "rebuild cache" | Rebuild wikilink entity cache |

### /suggest-links

Suggest wikilinks for current note using entity matching.

**Triggers**: "suggest links", "link suggestions", "what should I link", "linkify"

**Output**: List of text that matches existing note titles/aliases

### /apply-wikilinks

Apply suggested wikilinks to a note.

**Triggers**: "apply links", "add the links", "wikilinkify"

### /find-unlinked-mentions

Find places where an entity is mentioned but not linked.

**Triggers**: "unlinked mentions", "mentions not linked", "should be linked"

**Example**: "find unlinked mentions of [[John Smith]]"

---

## Rollup & Summaries

| Skill | Type | Trigger | Purpose |
|-------|------|---------|---------|
| `/run-rollup` | MUTATE | "rollup", "summarize notes" | Execute rollup chain |
| `/weekly-review` | MUTATE | "weekly review", "review my week" | Weekly reflection workflow |
| `/standup-rollup` | MUTATE | "standup", "team standup" | Team standup summary |
| `/okr-review` | MUTATE | "okr review", "quarterly objectives" | OKR progress review |

### /run-rollup

Execute the complete rollup chain: daily → weekly → monthly → quarterly → yearly → achievements.

**Triggers**: "rollup", "do rollup", "summarize my notes", "weekly summary"

**Process**:
1. Process daily notes → weekly summaries
2. Process weekly → monthly
3. Process monthly → quarterly
4. Process quarterly → yearly
5. Extract achievements

### /weekly-review

Guided weekly reflection workflow.

**Triggers**: "weekly review", "review my week", "reflect on week"

**Output**: Structured weekly summary with wins, learnings, and next week priorities

### /standup-rollup

Generate team standup summary from daily notes.

**Triggers**: "standup", "team standup", "standup blockers"

**Output**: What was done, what's planned, blockers

### /okr-review

Review OKR progress against quarterly objectives.

**Triggers**: "okr review", "quarterly objectives", "key results"

**Output**: OKR progress metrics and recommendations

---

## Bidirectional Bridge

| Skill | Type | Trigger | Purpose |
|-------|------|---------|---------|
| `/check-bidirectional` | READ | "bidirectional check" | Find mutual/reciprocal links |

### /check-bidirectional

Find notes that link to each other (bidirectional/mutual links).

**Triggers**: "bidirectional", "mutual links", "two-way links", "reciprocal links"

**Output**:
- Pairs of notes that link to each other
- Connection strength insights

> **Note**: Pattern detection (`detect_prose_patterns`) and cross-layer validation (`validate_cross_layer`) are available via MCP tools and will be orchestrated by the upcoming `/review` skill.

---

## Stale Notes

| Skill | Type | Trigger | Purpose |
|-------|------|---------|---------|
| `/find-stale-notes` | READ | "stale notes", "old notes" | Find important neglected notes |

### /find-stale-notes

Find important notes (by backlink count) not modified recently.

**Triggers**: "stale notes", "old notes", "neglected notes", "need attention"

**Filters**: days since modified, minimum backlinks

---

## Workflows

| Skill | Type | Trigger | Purpose |
|-------|------|---------|---------|
| `/onboard-customer` | MUTATE | "onboard customer", "new customer" | Customer onboarding workflow |
| `/workflow-define` | MUTATE | "define workflow", "create workflow" | Create custom workflow definitions |

### /onboard-customer

Guided customer onboarding workflow.

**Triggers**: "onboard customer", "new customer setup", "client onboarding"

**Process**:
1. Create customer note from template
2. Set up required frontmatter fields
3. Link to relevant project notes

### /workflow-define

Define and save custom workflow patterns.

**Triggers**: "define workflow", "create workflow", "new workflow"

**Output**: Workflow definition file with steps and triggers

---

## Auto-Trigger Behavior

Skills auto-trigger when user input matches trigger keywords. Examples:

| User Input | Triggers |
|------------|----------|
| "show me the hub notes" | `/find-hubs` |
| "what's the vault health?" | `/check-health` |
| "log fixed bug" | `/add-log` |
| "find orphan notes" | `/find-orphans` |
| "search for notes about AI" | `/search-vault` |

To disable auto-trigger and invoke manually, use the slash command directly.

---

## Configuration

Many skills use config values from `.flywheel/config.yaml`:

```yaml
paths:
  daily_notes: "daily-notes"
  weekly_notes: "weekly-notes"
  projects: "projects"

sections:
  log: "## Log"
  tasks: "## Tasks"
```

---

**Version**: 1.8.0
**Last Updated**: 2026-01-04
