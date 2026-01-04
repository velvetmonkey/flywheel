# Flywheel Architecture

A comprehensive guide to Flywheel's system design for developers and power users.

---

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         YOU (User)                               │
│              "Do rollup" or "find orphan notes"                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                       SKILLS (49)                                │
│     User-facing commands. Detect keywords & natural language     │
│     Read-only: Run immediately                                   │
│     Mutation: Ask Gate 4 confirmation first                      │
│     Delegation: Call Task() to agents                            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                       AGENTS (14)                                │
│     Multi-step workflows. Called by Task() only.                 │
│     Sequential execution (Gate 3).                               │
│     Can call other agents as sub-agents.                         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    MCP TOOLS (50+)                               │
│     Vault intelligence: search, links, frontmatter               │
│     All vault operations go through MCP server                   │
└─────────────────────────────────────────────────────────────────┘
                              │
          ┌───────────────────┼───────────────────┐
          ▼                   ▼                   ▼
┌─────────────────┐   ┌───────────────┐   ┌─────────────────┐
│  HOOKS (Pre)    │   │  Your Vault   │   │  HOOKS (Post)   │
│  Gate 1,2,3,4   │   │  .md files    │   │  Gate 5,6       │
│  Can BLOCK      │   │               │   │  WARN only      │
└─────────────────┘   └───────────────┘   └─────────────────┘
```

---

## Core Components

### 1. Skills (49 total)

Skills are user-facing commands triggered by natural language or keywords.

**Location**: `packages/claude-plugin/skills/`

**Structure**:
```
skills/
├── check-health/
│   └── SKILL.md       # Skill definition
├── auto-log/
│   └── SKILL.md
└── run-rollup/
    └── SKILL.md
```

**Skill Definition Format**:
```yaml
---
name: check-health
description: Comprehensive vault health diagnostics with recommendations
auto_trigger: true
trigger_keywords:
  - "check vault health"
  - "vault health"
  - "health check"
allowed-tools: mcp__flywheel__get_vault_stats, mcp__flywheel__find_orphan_notes
---

# Check Health

[Skill documentation and process]
```

**Skill Categories**:

| Category | Count | Examples |
|----------|-------|----------|
| Graph Analysis (Read-Only) | 12 | backlinks, orphans, hubs |
| Schema Analysis (Read-Only) | 5 | schema, field values |
| Vault Health (Read-Only) | 5 | health, stale notes |
| Task Queries (Read-Only) | 2 | tasks, due dates |
| Logging (Mutation) | 2 | add-log, add-task |
| Wikilink Ops (Mutation) | 4 | fix-links, apply-wikilinks |
| Schema Ops (Mutation) | 4 | apply, migrate, compute |
| Workflows (Delegation) | 6 | rollup, weekly-review |
| Setup | 3 | setup-flywheel, rebuild-cache |

### 2. Agents (14 total)

Agents are multi-step workflow executors called by skills via `Task()`.

**Location**: `packages/claude-plugin/agents/`

**Key Agents**:

| Agent | Triggered By | Purpose |
|-------|--------------|---------|
| `rollup-agent` | `run-rollup` skill | Orchestrate daily→yearly rollup chain |
| `rollup-weekly-agent` | `rollup-agent` | Aggregate daily → weekly |
| `rollup-monthly-agent` | `rollup-agent` | Aggregate weekly → monthly |
| `weekly-review-agent` | `weekly-review` skill | Week reflection + planning |
| `okr-review-agent` | `okr-review` skill | Score OKRs, plan next quarter |
| `action-extraction-agent` | `extract-actions` skill | Parse meetings for tasks |
| `customer-onboarding-agent` | `onboard-customer` skill | Create onboarding checklists |

**Agent Requirements (Gate 3)**:

All multi-step agents MUST include:
- `## Critical Rules` section with sequential execution
- Error handling strategy
- Verification checkpoints between phases
- Expected output showing ✓/✗ for each step

### 3. Hooks

Hooks are event-driven scripts that enforce safety and add automation.

**Location**: `packages/claude-plugin/hooks/`

**Hook Types**:

| Hook | Event | Purpose | Blocks? |
|------|-------|---------|---------|
| `session-start.py` | Session start | Show daily status, available skills | No |
| `session-gate.py` | Session start | Gate 5: MCP health check | Warn |
| `pre-mutation-gate.py` | Before Edit/Write | Gates 1, 2, 4 | Yes |
| `validate-agent-gate3.py` | Before agent Write | Gate 3: agent compliance | Yes |
| `read-cache.py` | After Read | Record reads for Gate 1 | No |
| `verify-mutation.py` | After Edit/Write | Gate 6: validate output | Warn |
| `wikilink-auto.py` | After Edit/Write | Auto-apply wikilinks | No |
| `frontmatter-auto.py` | After Edit/Write | Auto-add frontmatter | No |
| `achievement-detect.py` | After Edit/Write | Detect achievements | No |

### 4. MCP Server (50+ tools)

The MCP server provides vault intelligence to Claude.

**Location**: `packages/mcp-server/`

**Tool Categories**:

| Category | Examples |
|----------|----------|
| Graph | `get_backlinks`, `find_hub_notes`, `get_link_path` |
| Search | `search_notes`, `find_sections`, `get_recent_notes` |
| Schema | `get_frontmatter_schema`, `validate_frontmatter` |
| Tasks | `get_all_tasks`, `get_tasks_with_due_dates` |
| Structure | `get_note_structure`, `get_section_content` |
| Periodic | `detect_periodic_notes` (auto-finds daily/weekly/etc folders) |

---

## Six Gates Safety Framework

### Gate Summary

| Gate | Name | Enforces | Blocks? | Hook |
|------|------|----------|---------|------|
| 1 | Read Before Write | Must read file before editing | ✅ YES | `pre-mutation-gate.py` |
| 2 | File Exists Check | Edit only existing files | ✅ YES | `pre-mutation-gate.py` |
| 3 | Agent Chain Validation | Agents have checkpoints | ✅ YES | `validate-agent-gate3.py` |
| 4 | Mutation Confirm | User confirms writes | ✅ YES | `pre-mutation-gate.py` |
| 5 | MCP Health Check | MCP is accessible | ⚠️ WARN | `session-gate.py` |
| 6 | Post-Write Verify | Output is valid | ⚠️ WARN | `verify-mutation.py` |

### What Each Gate Does

**Gate 1 - Read Before Write**:
- Tracks `Read(file_path)` calls
- Blocks `Edit(file_path)` if not read
- Prevents blind file modifications

**Gate 2 - File Exists Check**:
- Validates file exists before Edit
- Write can create new files
- Edit only modifies existing

**Gate 3 - Agent Chain Validation**:
- Checks agent markdown for required sections
- Verifies sequential execution is documented
- Only structural compliance, not runtime enforcement

**Gate 4 - Mutation Confirm**:
- User must confirm before Edit/Write
- Can be bypassed if tool is whitelisted
- Shows what will change before applying

**Gate 5 - MCP Health Check**:
- Runs at session start
- Warns if MCP not responding
- Does not block session

**Gate 6 - Post-Write Verify**:
- Validates YAML is parseable
- Checks wikilink syntax
- Warns on issues, doesn't block

### Gate 3 Clarification

Gate 3 ensures agents are *designed* for safety via documentation requirements. It does NOT guarantee runtime enforcement.

**What Gate 3 VALIDATES**:
- `## Critical Rules` section exists
- Sequential execution documented
- Error handling considered
- Verification format (✓/✗) used

**What Gate 3 does NOT guarantee**:
- Actual sequential execution (depends on Claude following docs)
- Error recovery (documented, not enforced at runtime)
- Correct agent behavior

### Gate 4 Whitelist Caveat

Gate 4 confirmation can be bypassed if `Edit`/`Write` is in the user's permission whitelist.

**Recommendation**: Don't whitelist `Edit`/`Write` to preserve Gate 4 protection for mutations.

---

## Configuration System

### Convention Over Configuration

Flywheel uses **auto-detection** by default. No config file required.

**How Auto-Detection Works**:

```
mcp__flywheel__detect_periodic_notes(type="daily")

Returns:
{
  "detected": true,
  "folder": "daily-notes",           ← Found by scanning
  "pattern": "YYYY-MM-DD",           ← Detected from filenames
  "confidence": 0.87,                ← Based on evidence
  "today_path": "daily-notes/2026-01-03.md"
}
```

Detection process:
1. Scan ALL files in vault
2. Match filenames against date patterns
3. Group by folder + pattern
4. Score by note count, recency, folder name
5. Return best-guess with confidence

### Optional Config Override

Create `.flywheel.json` in vault root to override auto-detection:

```json
{
  "paths": {
    "daily_notes": "journal",
    "weekly_notes": "reviews/weekly"
  },
  "sections": {
    "log": "Daily Log",
    "tasks": "To Do"
  }
}
```

### Section Matching

Section matching is **forgiving by design**:
- Case-insensitive (`"log"` matches `## Log`, `## LOG`)
- Level-agnostic (`"Log"` matches `# Log`, `## Log`, `### Log`)
- Whitespace-trimmed

**Config values use text only, no `#` prefix**:
```json
{
  "sections": {
    "log": "Log",        // NOT "## Log"
    "tasks": "Tasks"
  }
}
```

### Priority Order

1. `.flywheel.json` explicit config (highest)
2. MCP auto-detection (smart defaults)
3. DEFAULTS in `config/loader.py` (fallback)

---

## Skill Invocation

### How Skills Are Triggered

Skills are triggered by **semantic matching**, not slash commands.

**Matching Process**:
1. User says: "check vault health"
2. Claude matches against skill `description` field
3. Skill's `trigger_keywords` provide additional matching hints
4. Matched skill is executed

**Note**: `trigger_keywords` is Flywheel-specific metadata, not official Claude Code.

### Invocation Patterns

| Say This | Matches Skill | Why |
|----------|---------------|-----|
| "check vault health" | `check-health` | Trigger keyword match |
| "find orphan notes" | `find-orphans` | Description match |
| "do a rollup" | `run-rollup` | Trigger keyword match |
| "setup flywheel" | `setup-flywheel` | Trigger keyword match |

### Read-Only vs Mutation

| Type | Behavior | Example |
|------|----------|---------|
| Read-Only | Runs immediately | "find orphan notes" |
| Mutation | Asks confirmation (Gate 4) | "add log entry: fixed bug" |
| Delegation | Launches agent, then confirms | "do a rollup" |

---

## File Locations

| What | Where |
|------|-------|
| Plugin manifest | `packages/claude-plugin/.claude-plugin/plugin.json` |
| All skills | `packages/claude-plugin/skills/` (49 folders) |
| All agents | `packages/claude-plugin/agents/` (14 files) |
| All hooks | `packages/claude-plugin/hooks/` |
| Slash commands | `packages/claude-plugin/commands/` |
| Config loader | `packages/claude-plugin/config/loader.py` |
| Six Gates spec | `packages/claude-plugin/skills/_patterns/SIX_GATES.md` |
| Agent template | `packages/claude-plugin/agents/_templates/MULTI_STEP_AGENT.md` |
| MCP server | `packages/mcp-server/src/index.ts` |
| MCP tools | `packages/mcp-server/src/tools/` |

---

## Development Workflow

### Adding a New Skill

1. Create folder: `skills/my-skill/SKILL.md`
2. Define frontmatter with name, description, triggers
3. Document the process
4. Add Six Gates compliance checklist
5. Test skill invocation

### Adding a New Agent

1. Check if multi-step (calls `Task()`)
2. Use template: `agents/_templates/MULTI_STEP_AGENT.md`
3. Include `## Critical Rules` section
4. Add verification checkpoints
5. Run `npm run validate:agents`

### Validation

```bash
# Validate all agents (Gate 3 compliance)
npm run validate:agents

# Build MCP server
npm run build:mcp

# Test hooks
npm run test:hooks
```

---

## Appendix: Complete Skills Reference

### Graph Analysis (Read-Only)

| Skill | Say This |
|-------|----------|
| `show-backlinks` | "show backlinks for X" |
| `find-orphans` | "find orphan notes" |
| `find-hubs` | "what are my hub notes" |
| `find-dead-ends` | "find dead end notes" |
| `check-bidirectional` | "find mutual links" |
| `show-common-links` | "what do X and Y both link to" |
| `show-path` | "how do X and Y connect" |
| `check-link-strength` | "how related are X and Y" |

### Workflow & Reviews (Delegation)

| Skill | Say This | Agent |
|-------|----------|-------|
| `run-rollup` | "do a rollup" | `rollup-agent` |
| `weekly-review` | "run weekly review" | `weekly-review-agent` |
| `okr-review` | "review my OKRs" | `okr-review-agent` |
| `extract-actions` | "extract actions from meeting" | `action-extraction-agent` |
| `standup-rollup` | "aggregate team standups" | `standup-agent` |
| `onboard-customer` | "onboard customer Acme" | `customer-onboarding-agent` |

### Mutation Skills

| Skill | Say This | Output |
|-------|----------|--------|
| `add-log` | "add log entry: [text]" | Daily note → Log section |
| `add-task` | "add task: [text]" | Daily note → Tasks section |
| `fix-links` | "fix broken links" | In-place edits |
| `normalize-note` | "normalize this note" | In-place edit |
