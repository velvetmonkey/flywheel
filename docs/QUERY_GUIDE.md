# Query Guide

Flywheel's core innovation: **query your markdown without reading files**.

Traditional AI assistants read every file to answer questions. Flywheel indexes your vault on startup, letting you ask questions about structure, relationships, and metadata—returning answers in ~50 tokens instead of 5,000+.

## The Query Paradigm

```
Traditional:          Flywheel:
Read 100 files        Query the index
→ 200K tokens         → 50 tokens
→ 5+ seconds          → <10ms
```

**Structure before content.** Most questions can be answered from metadata, links, and frontmatter—without reading prose.

---

## Query Categories

### Graph Intelligence

Understand relationships between notes.

| Question | How to Ask |
|----------|------------|
| What links to this note? | "Show backlinks to [[Project Alpha]]" |
| What does this note reference? | "What does [[Meeting Notes]] link to?" |
| How are these connected? | "Find path from [[Problem]] to [[Solution]]" |
| What do these have in common? | "What notes do [[Alice]] and [[Bob]] both reference?" |
| Which notes are hubs? | "Find hub notes with many connections" |
| Which notes are isolated? | "Find orphan notes with no links" |
| What's mutually linked? | "Show bidirectional links in projects/" |

**Example queries:**
```
"What's blocking [[Q1 Launch]]?"
→ Returns notes linking to Q1 Launch with 'blocker' tag

"Who should review the avionics decision?"
→ Traverses links to find people connected to avionics topics

"How does AlphaFold connect to my docking experiment?"
→ Shows shortest path through the knowledge graph
```

### Temporal Queries

Understand activity over time.

| Question | How to Ask |
|----------|------------|
| What changed recently? | "Show notes modified in the last 7 days" |
| What happened on a date? | "What was I working on 2024-01-15?" |
| What's related by time? | "Find notes edited around the same time as [[This Note]]" |
| What needs attention? | "Find stale notes—important but not touched recently" |
| Activity summary? | "Show vault activity for December" |

**Example queries:**
```
"What did I work on last week?"
→ Returns notes modified in date range

"Find stale important notes"
→ Notes with many backlinks but old modification dates

"Show everything from the conference week"
→ Notes from specific date range
```

### Schema Queries

Understand your vault's structure.

| Question | How to Ask |
|----------|------------|
| What fields exist? | "What frontmatter fields are used in projects/?" |
| What values are used? | "Show all unique values for 'status' field" |
| What's inconsistent? | "Find frontmatter inconsistencies" |
| What's missing? | "Find notes missing 'owner' field in projects/" |
| What types exist? | "What note types are in the vault?" |

**Example queries:**
```
"How much have I billed Acme Corp?"
→ Queries invoice notes by client field, sums amounts

"Show all active projects"
→ Filters by status: active

"What clients have open proposals?"
→ Queries proposals folder by status and client
```

### Search Queries

Find specific notes.

| Question | How to Ask |
|----------|------------|
| Notes with tag? | "Find notes tagged #urgent" |
| Notes in folder? | "List notes in meetings/" |
| Notes by title? | "Find notes with 'review' in the title" |
| Combined filters? | "Find #urgent notes in projects/ modified this week" |

**Example queries:**
```
"Find all meeting notes about pricing"
→ Search meetings/ folder with title filter

"Show tasks due this week"
→ Queries tasks with due_date in range

"List all notes mentioning 'migration'"
→ Searches across vault with keyword
```

### Structure Queries

Understand note internals without reading.

| Question | How to Ask |
|----------|------------|
| What sections exist? | "Show structure of [[Project Plan]]" |
| Find sections across vault? | "Find all '## Decisions' sections" |
| Extract specific section? | "Get the 'Next Steps' section from [[Meeting Note]]" |

---

## When to Query vs When to Read

| Situation | Approach |
|-----------|----------|
| "How many projects are active?" | **Query** - count notes by status |
| "What's the project plan about?" | **Read** - need the actual content |
| "Who is connected to this topic?" | **Query** - traverse graph links |
| "What did they decide?" | **Read** - need the prose |
| "Which notes need updating?" | **Query** - check modification dates |
| "What's wrong with this note?" | **Read** - analyze content |

**Rule of thumb:** If the answer is a list, count, relationship, or date—query. If the answer requires understanding prose—read.

---

## Query Tools Reference

### Graph Tools
- `get_backlinks` - Notes linking TO a target
- `get_forward_links` - Notes linked FROM a target
- `get_link_path` - Shortest path between notes
- `get_common_neighbors` - Shared references
- `find_hub_notes` - Highly connected notes
- `find_orphan_notes` - Disconnected notes
- `find_bidirectional_links` - Mutual links
- `get_connection_strength` - Relevance scoring

### Temporal Tools
- `get_recent_notes` - Modified in last N days
- `get_notes_modified_on` - Activity on specific date
- `get_notes_in_range` - Activity in date range
- `get_stale_notes` - Important but neglected
- `get_contemporaneous_notes` - Edited around same time
- `get_activity_summary` - Vault activity overview

### Schema Tools
- `get_frontmatter_schema` - Field inventory
- `get_field_values` - Unique values for field
- `find_frontmatter_inconsistencies` - Type mismatches
- `find_missing_fields` - Notes lacking expected fields
- `validate_against_schema` - Check compliance

### Search Tools
- `search_notes` - Multi-filter search (tags, folder, frontmatter, title)

### Structure Tools
- `get_note_structure` - Heading tree
- `get_section_content` - Extract specific section
- `find_sections` - Find sections across vault

---

## Performance

All queries run against the in-memory index:

| Vault Size | Query Time | Index Build |
|------------|------------|-------------|
| 100 notes | <1ms | <100ms |
| 1,000 notes | <5ms | <500ms |
| 5,000 notes | <10ms | <2s |

Compare to reading files: 1,000 notes × 2KB each = 2MB = ~500K tokens.

---

## Natural Language Examples

You don't need to know tool names. Ask naturally:

```
"What's connected to the pricing decision?"
"Show me notes I haven't touched in 3 months"
"Find projects without an owner"
"What do Sarah and Mike both work on?"
"List everything tagged urgent in Q1"
"How does the API design relate to security?"
"What changed since Monday?"
"Find meeting notes missing action items"
```

Flywheel translates these into the appropriate query tools.
