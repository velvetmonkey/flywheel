# Flywheel

### Stop burning tokens. Start building agents.

[![npm version](https://img.shields.io/npm/v/@velvetmonkey/flywheel-mcp.svg)](https://www.npmjs.com/package/@velvetmonkey/flywheel-mcp)
[![License: AGPL-3.0](https://img.shields.io/badge/License-AGPL--3.0-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-blue.svg)](https://github.com/velvetmonkey/flywheel)

---

Claude reading your entire vault on every query? **~5,000 tokens burned.**

Flywheel queries an index instead. **~50 tokens.** That's up to 100x savings.

**The real win:** Your agents can now query your knowledge *hundreds of times* during long-running tasks without blowing up the context window.

You couldn't do this before. Now you can.

---

## Your Vault as a Knowledge Graph

```
                        ┌─────────────────────────────────────────────────────┐
                        │              Your Vault (65 notes)                  │
                        │                        · · ·                        │
                        │   · [[Unlinked]] ·        · [[Unlinked]] ·         │
                        │         ↓                        ↓                  │
                        └─────────────────────────────────────────────────────┘
                                               │
                 ┌─────────────────────────────┼─────────────────────────────┐
                 │                             │                             │
                 ▼                             ▼                             ▼
    ┌────────────────────┐       ┌────────────────────┐       ┌────────────────────┐
    │ [[PDR Review]]     │──────▶│  [[Team Roster]]   │◀──────│[[Year End Review]] │
    │   ───────────      │       │    ───────────     │       │   ──────────────   │
    │   type: meeting    │       │   type: hub        │       │   type: meeting    │
    │   date: 2025-12-18 │       │   status: active   │       │   date: 2025-12-30 │
    │   attendees: [5]   │       │   owner: [[Sarah]] │       │   attendees: [8]   │
    └────────────────────┘       └────────────────────┘       └────────────────────┘
              │                     │    │    │    │                    │
              │          ┌──────────┘    │    │    └──────────┐        │
              │          ▼               ▼    ▼               ▼        │
              │   ┌──────────────┐ ┌──────────────┐ ┌──────────────┐   │
              │   │[[Sarah Chen]]│ │[[Marcus J.]] │ │ [[Elena R.]] │   │
              │   │ ──────────── │ │ ──────────── │ │ ──────────── │   │
              │   │ role: Lead   │ │ role: Prop.  │ │ role: Avion. │   │
              └──▶│ team: Core   │ │ team: Core   │ │ team: Core   │◀──┘
                  └──────────────┘ └──────────────┘ └──────────────┘
                         │                │                │
                         ▼                ▼                ▼
                  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
                  │[[GNC System]]│ │[[Turbopump]] │ │ [[Avionics]] │
                  │ ──────────── │ │ ──────────── │ │ ──────────── │
                  │ status: test │ │ status: dev  │ │ status: done │
                  │ risk: medium │ │ risk: high   │ │ risk: low    │
                  └──────────────┘ └──────────────┘ └──────────────┘

Legend:  ─────▶ Wikilink (edge)     │ type: meeting │ Frontmatter (attributes)
         ◀───── Backlink            │ status: done  │ Queryable via Flywheel
```

**Notes are nodes. Wikilinks are edges. Frontmatter is queryable metadata.**

---

## See It In Action

Real conversations with Claude using Flywheel:

### Finding What You Need

```
You: Find everything about authentication

Claude: [uses search_notes]

Found 7 notes mentioning authentication:
- Auth Architecture.md (hub note, 12 backlinks)
- JWT Implementation.md
- OAuth Provider Setup.md
- Login Flow.md
- Session Management.md
- Security Audit Q3.md
- API Authentication.md

Auth Architecture is your hub - want me to show what links to it?
```

### Tracking Work

```
You: Show me all pending meetings for Project Alpha

Claude: [uses query_notes with frontmatter filter]

Found 3 pending meetings:
- meetings/2026-01-30-alpha-kickoff.md (scheduled for tomorrow)
- meetings/2026-02-05-alpha-review.md
- meetings/2026-02-12-alpha-demo.md

Each has attendees, agenda, and action items in frontmatter.
Want me to show the attendees across all three?
```

### Following Connections

```
You: What meetings mention Sam Chen?

Claude: [uses get_backlinks for "Sam Chen", filters by type: "meeting"]

Sam Chen is mentioned in 5 meetings.

[uses query_notes to check status field]

2 are overdue (status: "pending", date in past):
- meetings/2026-01-15-sprint-planning.md - overdue by 14 days
- meetings/2026-01-22-design-review.md - overdue by 7 days

Want me to update their status or flag them for follow-up?
```

### Discovering Relationships

```
You: What connects my meeting notes to the Q4 strategy?

Claude: Let me trace the path through your vault.
[uses get_shortest_path]

Found a 3-hop connection:
  Meeting Notes → [[Client Feedback]] → [[Product Roadmap]] → Q4 Strategy

The link runs through client feedback captured in your October meetings.
```

---

## Try a Demo

5 production-ready vaults representing real knowledge work personas. Each vault is fully validated with 100% valid YAML and authentic linking patterns.

| Demo | Persona | Notes | Try Asking |
|------|---------|-------|------------|
| **[carter-strategy](demos/carter-strategy/)** | Solo Consultant | 32 | "How much have I billed Acme Corp?" |
| **[artemis-rocket](demos/artemis-rocket/)** | Aerospace Engineer | 65 | "What's blocking the propulsion milestone?" |
| **[startup-ops](demos/startup-ops/)** | SaaS Co-Founder | 31 | "Walk me through onboarding DataDriven" |
| **[nexus-lab](demos/nexus-lab/)** | PhD Researcher | 32 | "How does AlphaFold connect to my experiment?" |
| **[solo-operator](demos/solo-operator/)** | Content Creator | 19 | "What's my financial runway?" |

```bash
# Clone and explore
git clone https://github.com/velvetmonkey/flywheel.git
cd flywheel/demos/artemis-rocket

# Start Claude Code
claude
```

---

## What This Unlocks

- **Graph intelligence** — backlinks, orphans, hubs, connection paths — your vault as a queryable knowledge graph
- **Vault health monitoring** — find disconnected notes, stale hubs, broken links instantly
- **Connection discovery** — "how does X relate to Y?" answered in milliseconds
- **Schema queries** on frontmatter without reading files
- **Agentic workflows** that query your knowledge hundreds of times without token bloat

---

## Quick Start

### Prerequisites

- **Node.js 18+** installed ([download here](https://nodejs.org))
- **Claude Code** or compatible MCP client ([install guide](https://github.com/anthropics/claude-code))
- An **Obsidian vault** (or any markdown folder)

### Install (30 seconds)

**1. Create MCP config** in your vault root as `.mcp.json`:

```json
{
  "mcpServers": {
    "flywheel": {
      "command": "npx",
      "args": ["-y", "@velvetmonkey/flywheel-mcp"]
    }
  }
}
```

> **Windows:** Use `"command": "cmd", "args": ["/c", "npx", "-y", "@velvetmonkey/flywheel-mcp"]`

**2. Restart Claude Code** (if already running)

**3. Verify**: Run `claude mcp list` — you should see `flywheel ✓`

That's it. Flywheel uses the current directory as your vault—no config needed.

---

### First Run: Tool Permissions

When you first use Flywheel, Claude Code asks permission to use its tools:

> "Allow Flywheel to read vault structure?"

**Type `y` to approve.** Flywheel tools are read-only—they query your vault's index but never modify files.

**Pro tip:** For the best experience, add recommended permissions to `.claude/settings.json`:

```json
{
  "permissions": {
    "allow": [
      "mcp__flywheel__*"
    ]
  }
}
```

This pre-approves all Flywheel read tools so Claude can work fluidly.

---

### Configuration Options

#### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PROJECT_PATH` | Auto-detect | Path to your vault. Only needed if running Claude from outside your vault folder. |
| `FLYWHEEL_WATCH` | `false` | When `true`, automatically rebuilds the index when you edit notes. Useful if you're editing in Obsidian while Claude is working. |
| `FLYWHEEL_DEBOUNCE_MS` | `60000` | How long to wait after a file change before rebuilding (in milliseconds). Default 1 minute batches rapid edits together. |
| `FLYWHEEL_TOOLS` | `standard` | Which tool categories to load. Use `minimal` for less context usage, `full` for everything. |

#### Tool Presets

Control which tools are available to reduce token usage:

| Preset | What's included | Best for |
|--------|-----------------|----------|
| `minimal` | Core vault info only | Quick queries, low token usage |
| `standard` | Core + graph + search + tasks | Most users (default) |
| `full` | All 44 tools | Power users who need everything |

Mix and match: `FLYWHEEL_TOOLS=core,graph,tasks`

#### Vault Config File (`.claude/.flywheel.json`)

Flywheel auto-creates this file on first run by analyzing your vault. Edit it to override auto-detected settings.

| Field | What it does |
|-------|--------------|
| `vault_name` | Display name shown in tool responses |
| `paths.daily_notes` | Where your daily notes live (e.g., `"journal/daily"`) |
| `paths.weekly_notes` | Where your weekly notes live |
| `paths.templates` | Your templates folder (excluded from some queries) |
| `exclude_task_tags` | Tags to ignore in task queries (e.g., `["#habit", "#someday"]`) |

**Example** - customize for a non-standard vault layout:
```json
{
  "vault_name": "Work Notes",
  "paths": {
    "daily_notes": "Logs/Daily",
    "templates": "Meta/Templates"
  },
  "exclude_task_tags": ["#recurring", "#habit"]
}
```

> **Tip:** Most users don't need to edit this file. Flywheel auto-detects folders named `daily`, `journal`, `weekly`, `templates`, etc.

<details>
<summary><strong>Platform notes (Windows, WSL, custom vault path)</strong></summary>

**Windows (native):**
```json
{
  "mcpServers": {
    "flywheel": {
      "command": "cmd",
      "args": ["/c", "npx", "-y", "@velvetmonkey/flywheel-mcp"]
    }
  }
}
```

**Different vault location:**
```json
{
  "mcpServers": {
    "flywheel": {
      "command": "npx",
      "args": ["-y", "@velvetmonkey/flywheel-mcp"],
      "env": {
        "PROJECT_PATH": "/path/to/your/vault"
      }
    }
  }
}
```

**WSL:** Use `npx` directly (not `cmd /c`), with `/mnt/c/...` paths.

</details>

<details>
<summary><strong>File watching (auto-rebuild on changes)</strong></summary>

**Enable file watching** to automatically rebuild the index when vault files change:

```json
{
  "mcpServers": {
    "flywheel": {
      "command": "npx",
      "args": ["-y", "@velvetmonkey/flywheel-mcp"],
      "env": {
        "FLYWHEEL_WATCH": "true"
      }
    }
  }
}
```

**Optional: Custom debounce delay** (default is 60000ms / 1 minute):

```json
{
  "mcpServers": {
    "flywheel": {
      "command": "npx",
      "args": ["-y", "@velvetmonkey/flywheel-mcp"],
      "env": {
        "FLYWHEEL_WATCH": "true",
        "FLYWHEEL_DEBOUNCE_MS": "1000"
      }
    }
  }
}
```

**How it works:**
- Watches vault directory for `.md` file changes
- Automatically ignores dotfiles (`.obsidian`, `.trash`, etc.)
- Debounces rapid changes to avoid excessive rebuilds
- Uses `awaitWriteFinish` to prevent indexing partial writes
- Logs rebuild events to stderr

**When to use:** Enable file watching if you're editing notes while an agent is actively working in your vault. Without watching, the agent sees a snapshot from when the MCP server started.

**Performance:** Minimal overhead. Rebuilds only trigger on `.md` file changes, not every filesystem event.

</details>

<details>
<summary><strong>Tool filtering (reduce context usage)</strong></summary>

**Problem:** Flywheel exposes 51 tools. Each tool definition consumes tokens from your context window. If you only need graph queries, loading task and migration tools wastes context.

**Solution:** Use `FLYWHEEL_TOOLS` to load only the categories you need:

```json
{
  "mcpServers": {
    "flywheel": {
      "command": "npx",
      "args": ["-y", "@velvetmonkey/flywheel-mcp"],
      "env": {
        "FLYWHEEL_TOOLS": "standard"
      }
    }
  }
}
```

**Presets:**

| Preset | Categories | Use Case |
|--------|------------|----------|
| `minimal` | core | Just vault stats and metadata |
| `standard` | core, graph, search, tasks | Most common workflows (default) |
| `full` | all | Every tool available |

**Categories:**

| Category | Tools | Description |
|----------|-------|-------------|
| `core` | 9 | health_check, get_vault_stats, refresh_index, get_note_metadata, get_folder_structure, get_all_entities, get_recent_notes, get_unlinked_mentions, find_broken_links |
| `graph` | 6 | get_backlinks, get_forward_links, find_orphan_notes, find_hub_notes, suggest_wikilinks, validate_links |
| `search` | 1 | search_notes |
| `tasks` | 4 | get_all_tasks, get_tasks_from_note, get_tasks_with_due_dates, get_incomplete_tasks |
| `schema` | 8 | get_frontmatter_schema, get_field_values, find_frontmatter_inconsistencies, validate_frontmatter, find_missing_frontmatter, infer_folder_conventions, find_incomplete_notes, suggest_field_values |
| `structure` | 4 | get_note_structure, get_headings, get_section_content, find_sections |
| `temporal` | 6 | detect_periodic_notes, get_notes_modified_on, get_notes_in_range, get_stale_notes, get_contemporaneous_notes, get_activity_summary |
| `advanced` | 13 | Bidirectional bridge tools (detect_prose_patterns, suggest_frontmatter_from_prose, etc.), computed frontmatter, field migrations, graph analysis (get_link_path, find_dead_ends, etc.) |

**Custom combinations:**

```bash
# Core + graph only
FLYWHEEL_TOOLS=core,graph

# Everything except advanced
FLYWHEEL_TOOLS=core,graph,search,tasks,schema,structure,temporal

# Just tasks and search
FLYWHEEL_TOOLS=core,tasks,search
```

**Note:** `core` is recommended in all combinations as it provides essential vault metadata tools.

</details>

### Troubleshooting

| Issue | Solution |
|-------|----------|
| **`npx: command not found`** | Node.js isn't installed. [Download Node.js 18+](https://nodejs.org) |
| **`flywheel ✗` in mcp list** | Wrong file location. `.mcp.json` must be in your vault root |
| **"No notes found"** | Not in vault directory. Run `claude` from inside your vault folder |
| **Windows: spawn errors** | Use `cmd /c npx` config (see Platform notes above) |
| **MCP server won't start** | Check Node version: `node --version` (need 18+) |

---

## 44 Tools. Three Query Types.

### Graph Queries — "What connects to what?"

```
"What depends on [[Turbopump]]?"        → 6 backlinks, 4 critical dependencies
"Find orphan notes"                     → 12 disconnected notes need linking
"Show hub notes"                        → 8 knowledge centers with 10+ connections
"Path from [[Invoice]] to [[Project]]"  → 2-hop path via [[Client]]
"Find bidirectional links"              → 23 strongly connected note pairs
"What's connected to [[Q1 Goals]]?"     → Forward links, backlinks, shared neighbors
```

### Schema Queries — "Find notes where..."

```
"All invoices where status is 'pending'"  → 3 notes, $47K outstanding
"What fields exist in meetings/?"  → attendees, date, decisions, follow-ups
"Notes missing required fields"  → 12 incomplete records
```

### Temporal Queries — "What changed when?"

```
"Activity in the last 7 days"  → 23 notes modified, 4 new
"Stale but important notes"  → 5 hub notes untouched in 30+ days
"What was I working on with [[Client X]]?"  → Timeline of related edits
```

---

## Why Markdown + Graph?

- **Git-native** — version-controlled knowledge
- **Plain text** — future-proof, zero lock-in
- **Privacy** — files stay local, only what you need gets sent
- **Editor-agnostic** — Obsidian, VSCode, Cursor, vim, whatever
- **AI-native** — 44 tools purpose-built for agent workflows

---

## Docs

**User Guides:**
- **[MCP Tools Reference](docs/MCP_REFERENCE.md)** — All 44 tools
- **[Query Guide](docs/QUERY_GUIDE.md)** — Patterns and examples
- **[How It Works](docs/HOW_IT_WORKS.md)** — Architecture and token savings
- **[Vault Health](docs/VAULT_HEALTH.md)** — Monitor and improve vault structure

**Developer:**
- **[Architecture](docs/ARCHITECTURE.md)** — MCP server design and tool development
- **[Documentation Index](docs/)** — Full documentation directory

---

macOS / Linux / WSL / Windows

AGPL-3.0 License · [GitHub](https://github.com/velvetmonkey/flywheel) · [Issues](https://github.com/velvetmonkey/flywheel/issues)
