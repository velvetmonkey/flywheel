# Skills Reference

Flywheel provides 42 skills organized by function. Skills auto-trigger on keywords or can be invoked via `/skill-name`.

**Skill Types:**
- **READ** - Query/analyze only, no file modifications
- **MUTATE** - Can modify files (follows Six Gates safety framework)

---

## Quick Reference

| Category | Skills | Purpose |
|----------|--------|---------|
| [Onboarding](#onboarding) | 1 | New user welcome |
| [Graph Analysis](#graph-analysis) | 10 | Links, hubs, orphans, paths |
| [Search & Query](#search--query) | 4 | Find notes, sections, content |
| [Health & Maintenance](#health--maintenance) | 4 | Vault health, broken links |
| [Tasks & Logging](#tasks--logging) | 4 | Tasks, logging, due dates |
| [Schema & Frontmatter](#schema--frontmatter) | 11 | Schema, validation, inference |
| [Wikilinks](#wikilinks) | 4 | Suggest, apply, fix links |
| [Rollup & Summaries](#rollup--summaries) | 1 | Periodic summarization |
| [Bidirectional Bridge](#bidirectional-bridge) | 3 | Prose ↔ frontmatter |

---

## Onboarding

| Skill | Type | Trigger | Purpose |
|-------|------|---------|---------|
| `/onboard` | READ | "hello flywheel", "getting started" | Welcome + vault health overview |

### /onboard (onboard-vault)

Welcome new users with vault health check, stats, and suggested next steps.

**Triggers**: "onboard", "getting started", "hello flywheel", "what can you do"

**Output**:
- Health status
- Note count, link count, orphan count
- Top hub notes
- Suggested next actions

---

## Graph Analysis

| Skill | Type | Trigger | Purpose |
|-------|------|---------|---------|
| `/backlinks` | READ | "backlinks to X" | Show incoming/outgoing links |
| `/hubs` | READ | "hub notes", "most connected" | Find highly connected notes |
| `/orphans` | READ | "orphan notes", "disconnected" | Find notes with no backlinks |
| `/path` | READ | "path from X to Y" | Find shortest link path |
| `/related` | READ | "related to X" | Find related notes |
| `/common` | READ | "common between X and Y" | Find shared connections |
| `/dead-ends` | READ | "dead ends" | Notes with backlinks but no outlinks |
| `/concurrent` | READ | "edited same time as X" | Contemporaneous notes |
| `/clusters` | READ | "clusters" | Find note clusters |
| `/strength` | READ | "connection strength" | Calculate link strength |

### /backlinks (show-backlinks)

Show all backlinks and forward links for a note.

**Triggers**: "backlinks", "who links here", "what links to", "incoming links"

**Example**: "show backlinks to [[Project Alpha]]"

### /hubs (find-hubs)

Find hub notes (highly connected notes with many links).

**Triggers**: "hubs", "hub notes", "most connected", "popular notes", "key concepts"

**Output**: List of notes sorted by total connections

### /orphans (find-orphans)

Find orphan notes (notes with no backlinks).

**Triggers**: "orphans", "orphan notes", "disconnected", "isolated notes"

**Output**: List of orphan notes with modification dates

### /path (find-path)

Find the shortest link path between two notes.

**Triggers**: "path from", "path to", "how to get from", "connection between"

**Example**: "find path from [[Alice]] to [[Project Gamma]]"

---

## Search & Query

| Skill | Type | Trigger | Purpose |
|-------|------|---------|---------|
| `/search` | READ | "search", "find notes" | Advanced search with filters |
| `/section` | READ | "show section X" | Get content under heading |
| `/find-sections` | READ | "sections matching X" | Find sections across vault |
| `/activity` | READ | "recent activity" | Vault activity summary |

### /search (search-vault)

Advanced vault search with filters (folder, tags, frontmatter).

**Triggers**: "search vault", "find notes", "query notes", "notes with"

**Examples**:
- "search for notes in projects folder"
- "find notes tagged with #active"
- "show notes where status = active"

### /section (get-section)

Get the content under a specific heading.

**Triggers**: "show section", "get section", "what's under"

**Example**: "show the Tasks section of [[Project Alpha]]"

---

## Health & Maintenance

| Skill | Type | Trigger | Purpose |
|-------|------|---------|---------|
| `/health` | READ | "vault health", "health report" | Full vault diagnostics |
| `/fix-links` | MUTATE | "fix links", "broken links" | Find and repair broken links |
| `/folder-health` | READ | "folder health" | Health by folder |
| `/link-density` | READ | "link density" | Link density metrics |

### /health (check-health)

Comprehensive vault diagnostics and health report.

**Triggers**: "vault health", "health report", "vault diagnostics", "vault status"

**Output**:
- Health score (0-100%)
- Note/link counts
- Orphan/broken link counts
- Top hubs
- Recommendations

### /fix-links (fix-links)

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
| `/log` | MUTATE | "log X", "captains log" | Add timestamped log entry |
| `/tasks` | READ | "all tasks", "show tasks" | List vault tasks |
| `/due` | READ | "due soon", "upcoming tasks" | Tasks with due dates |
| `/add-task` | MUTATE | "add task" | Add task to note |

### /log (add-log)

Auto-log entries to today's daily note.

**Triggers**: "log", "captains log", "record", "note this", "write this down"

**Format**: `- HH:MM [description]`

**Examples**:
- "log Fixed authentication bug"
- "captains log: Meeting with product team"

### /tasks (show-tasks)

Get all tasks from the vault with filtering options.

**Triggers**: "all tasks", "task list", "show tasks", "open tasks", "todos"

**Filters**: status (open/completed), folder, tag

### /due (tasks-due)

Get tasks sorted by due date.

**Triggers**: "due soon", "upcoming tasks", "what's due", "deadlines"

---

## Schema & Frontmatter

| Skill | Type | Trigger | Purpose |
|-------|------|---------|---------|
| `/schema` | READ | "vault schema" | Analyze frontmatter schema |
| `/schema-check` | READ | "validate schema" | Validate against schema |
| `/field-values` | READ | "values for X field" | Get unique field values |
| `/normalize` | READ | "normalize note" | Normalize frontmatter |
| `/promote-fm` | READ | "promote to frontmatter" | Move prose patterns to YAML |
| `/gaps` | READ | "missing frontmatter" | Find missing fields |
| `/schema-infer` | READ | "infer schema" | Auto-detect folder conventions |
| `/schema-gaps` | READ | "incomplete notes" | Find notes missing fields |
| `/schema-apply` | MUTATE | "apply schema" | Apply conventions to notes |
| `/schema-compute` | MUTATE | "compute fields" | Add computed frontmatter |
| `/schema-migrate` | MUTATE | "rename field" | Rename/transform field values |

### /schema (vault-schema)

Analyze all frontmatter fields used across the vault.

**Triggers**: "vault schema", "frontmatter schema", "what fields"

**Output**: Field names, types, usage counts

### /schema-check (validate-schema)

Validate notes against expected schema.

**Triggers**: "validate schema", "schema check", "check frontmatter"

**Example**: "validate projects folder has type, status, owner"

### /gaps (find-gaps)

Find notes missing expected frontmatter fields.

**Triggers**: "missing frontmatter", "gaps in", "incomplete notes"

---

## Wikilinks

| Skill | Type | Trigger | Purpose |
|-------|------|---------|---------|
| `/suggest` | MUTATE | "suggest links" | Suggest wikilinks for note |
| `/apply-links` | MUTATE | "apply links" | Add suggested wikilinks |
| `/unlinked` | MUTATE | "unlinked mentions" | Find text that could be linked |
| `/wikilinkify-fm` | READ | "wikilinkify frontmatter" | Convert strings to wikilinks |
| `/rebuild-cache` | MUTATE | "rebuild cache" | Rebuild wikilink entity cache |

### /suggest (suggest-links)

Suggest wikilinks for current note using entity matching.

**Triggers**: "suggest links", "link suggestions", "what should I link", "linkify"

**Output**: List of text that matches existing note titles/aliases

### /apply-links (wikilink-apply)

Apply suggested wikilinks to a note.

**Triggers**: "apply links", "add the links", "wikilinkify"

### /unlinked (unlinked-mentions)

Find places where an entity is mentioned but not linked.

**Triggers**: "unlinked mentions", "mentions not linked", "should be linked"

**Example**: "find unlinked mentions of [[John Smith]]"

---

## Rollup & Summaries

| Skill | Type | Trigger | Purpose |
|-------|------|---------|---------|
| `/rollup` | MUTATE | "rollup", "summarize notes" | Execute rollup chain |

### /rollup (run-rollup)

Execute the complete rollup chain: daily → weekly → monthly → quarterly → yearly → achievements.

**Triggers**: "rollup", "do rollup", "summarize my notes", "weekly summary"

**Process**:
1. Process daily notes → weekly summaries
2. Process weekly → monthly
3. Process monthly → quarterly
4. Process quarterly → yearly
5. Extract achievements

---

## Bidirectional Bridge

| Skill | Type | Trigger | Purpose |
|-------|------|---------|---------|
| `/detect-patterns` | READ | "detect patterns" | Find Key: Value patterns in prose |
| `/cross-layer` | READ | "validate layers" | Check frontmatter ↔ prose consistency |
| `/bidirectional` | READ | "bidirectional check" | Full bidirectional analysis |

### /bidirectional (vault-bidirectional)

Full bidirectional analysis between frontmatter and prose.

**Triggers**: "bidirectional", "check layers", "frontmatter vs prose"

**Output**:
- Prose patterns detected
- Frontmatter suggestions
- Consistency issues

---

## Stale Notes

| Skill | Type | Trigger | Purpose |
|-------|------|---------|---------|
| `/stale` | READ | "stale notes", "old notes" | Find important neglected notes |

### /stale (find-stale-notes)

Find important notes (by backlink count) not modified recently.

**Triggers**: "stale notes", "old notes", "neglected notes", "need attention"

**Filters**: days since modified, minimum backlinks

---

## Auto-Trigger Behavior

Skills auto-trigger when user input matches trigger keywords. Examples:

| User Input | Triggers |
|------------|----------|
| "show me the hub notes" | `/hubs` |
| "what's the vault health?" | `/health` |
| "log fixed bug" | `/log` |
| "find orphan notes" | `/orphans` |
| "search for notes about AI" | `/search` |

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

**Version**: 1.7.0
**Last Updated**: 2026-01-03
