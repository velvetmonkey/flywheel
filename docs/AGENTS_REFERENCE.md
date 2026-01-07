# Agents Reference

Flywheel provides 8 specialized agents for multi-step workflows. All agents follow the Six Gates safety framework.

---

## Quick Reference

| Agent | Purpose | Model |
|-------|---------|-------|
| [rollup-agent](#rollup-agent) | Orchestrate daily→yearly rollup chain | sonnet |
| [weekly-agent](#weekly-agent) | Process daily→weekly summaries | sonnet |
| [monthly-agent](#monthly-agent) | Process weekly→monthly summaries | sonnet |
| [quarterly-agent](#quarterly-agent) | Process monthly→quarterly summaries | sonnet |
| [yearly-agent](#yearly-agent) | Process quarterly→yearly summaries | sonnet |
| [achievement-extraction-agent](#achievement-extraction-agent) | Extract achievements from notes | sonnet |
| [relationship-explorer-agent](#relationship-explorer-agent) | Deep relationship analysis | sonnet |
| [schema-enforcer-agent](#schema-enforcer-agent) | Detect/fix schema inconsistencies | sonnet |

---

## Rollup Chain

The rollup chain processes notes hierarchically: daily → weekly → monthly → quarterly → yearly.

```
┌─────────────┐
│ rollup-agent│ (orchestrator)
└──────┬──────┘
       │
       ├── weekly-agent (×N weeks)
       │
       ├── monthly-agent (×2 months)
       │
       ├── quarterly-agent (if end of quarter)
       │
       └── yearly-agent (if end of year)
```

### rollup-agent

**Purpose**: Orchestrate the complete rollup chain for last 2 months.

**Invocation**:
```python
Task(
    subagent_type="rollup-agent",
    description="Process last 2 months rollup",
    prompt="Execute the complete rollup chain for the last 2 months"
)
```

**Process Flow**:
1. Calculate date range (last 2 months)
2. Identify all ISO weeks in range
3. Call weekly-agent for each week (sequential)
4. Call monthly-agent for each month (sequential)
5. Call quarterly-agent if end of quarter
6. Call yearly-agent if end of year
7. Report summary

**Tools**: `Task`, `Bash(python -c:*)`

### weekly-agent

**Purpose**: Process daily notes into weekly summary.

**Invocation**:
```python
Task(
    subagent_type="rollup-weekly-agent",
    description="Process week 2025-W52",
    prompt="Process week 2025-W52"
)
```

**Input**: Week ID (e.g., "2025-W52")

**Output**: Updated weekly note with aggregated:
- Log entries
- Accomplishments
- Habits
- Work done

### monthly-agent

**Purpose**: Process weekly notes into monthly summary.

**Invocation**:
```python
Task(
    subagent_type="rollup-monthly-agent",
    description="Process month 2025-12",
    prompt="Process month 2025-12"
)
```

**Input**: Month (e.g., "2025-12")

**Output**: Updated monthly note with:
- Key achievements
- Projects worked on
- Patterns and trends

### quarterly-agent

**Purpose**: Process monthly notes into quarterly summary.

**Invocation**:
```python
Task(
    subagent_type="rollup-quarterly-agent",
    description="Process quarter 2025-Q4",
    prompt="Process quarter 2025-Q4"
)
```

**Input**: Quarter (e.g., "2025-Q4")

**Output**: Updated quarterly note with:
- Major milestones
- Quarter achievements
- Strategic progress

### yearly-agent

**Purpose**: Process quarterly notes into yearly summary.

**Invocation**:
```python
Task(
    subagent_type="rollup-yearly-agent",
    description="Process year 2025",
    prompt="Process year 2025"
)
```

**Input**: Year (e.g., "2025")

**Output**: Updated yearly note with:
- Annual achievements
- Yearly themes
- Big picture wins

---

## Analysis Agents

### achievement-extraction-agent

**Purpose**: Extract achievements from notes into Achievements file.

**Invocation**:
```python
Task(
    subagent_type="achievement-extraction-agent",
    description="Extract achievements from notes",
    prompt="Find and extract notable achievements from recent activity"
)
```

**Process**:
1. Scan recent notes for achievement markers
2. Categorize by type (career, project, skill, personal)
3. Update Achievements file

**Tools**: `Read`, `Edit`

### relationship-explorer-agent

**Purpose**: Deep-dive into note relationships, generating comprehensive reports.

**Invocation**:
```python
Task(
    subagent_type="explore-relationships-agent",
    description="Explore relationship between notes",
    prompt="Analyze the relationship between [[Project Alpha]] and [[React]]"
)
```

**Process**:
1. Parse input (identify two notes)
2. `get_connection_strength()` - Overall score
3. `get_link_path()` - Trace direct path
4. `get_common_neighbors()` - Shared references
5. `get_backlinks()` on both - Who references them
6. `get_forward_links()` on both - What they reference
7. `find_bidirectional_links()` - Mutual links
8. Synthesize relationship narrative
9. Generate comprehensive report

**Tools**: MCP graph tools, `Read`

**Output**:
```
Relationship Analysis: [[Note A]] ↔ [[Note B]]
═══════════════════════════════════════════════

Connection Strength: 85% (Strong)
Direct Path: A → C → B (2 hops)

Common References:
- [[Shared Topic 1]]
- [[Shared Topic 2]]

Unique to A: [[X]], [[Y]]
Unique to B: [[Z]]

Relationship Type: Related through shared domain
```

### schema-enforcer-agent

**Purpose**: Detect and fix frontmatter schema inconsistencies.

**Invocation**:
```python
Task(
    subagent_type="enforce-schema-agent",
    description="Check vault schema health",
    prompt="Analyze frontmatter schema and report inconsistencies"
)
```

**Process**:
1. `get_frontmatter_schema()` - Understand current state
2. `find_frontmatter_inconsistencies()` - Find violations
3. For each violation: `get_field_values(field)` - See actual values
4. Determine correct type (based on majority usage)
5. Generate fix suggestions
6. (If fix requested) Apply fixes with confirmation

**Tools**: MCP frontmatter tools, `Read`, `Edit`

**Output**:
```
Schema Analysis Report
═══════════════════════════════════════════════

Fields Analyzed: 15
Inconsistencies Found: 3

Issues:
1. `status` field
   - 85% string: "active", "completed"
   - 15% boolean: true, false
   - Fix: Convert boolean → string

2. `tags` field
   - 90% array: ["a", "b"]
   - 10% string: "a, b"
   - Fix: Convert string → array

Suggested Actions:
- Run with fix flag to apply changes
```

---

## Creating New Agents

Use the template at `packages/claude-plugin/agents/_templates/MULTI_STEP_AGENT.md`.

### Required Sections

1. **Frontmatter**: name, description, allowed-tools, model
2. **Purpose**: What the agent does
3. **Process Flow**: Visual diagram
4. **Phases**: Step-by-step instructions with Gate 3 checkpoints
5. **Critical Rules**: Sequential execution, error handling
6. **Expected Output**: Example output format
7. **Six Gates Compliance**: Checklist

### Gate 3 Checkpoints

Multi-step agents MUST include verification between phases:

```markdown
**GATE 3 CHECKPOINT:** Before proceeding to Phase 3, verify:
- [ ] Phase 2 completed successfully
- [ ] Expected outputs are present
- [ ] No errors that would invalidate Phase 3
```

### Sequential Execution

```markdown
## Critical Rules

### Sequential Execution
- Process phases in order
- **Wait for completion** before calling next phase
- No parallel execution of dependent steps
- Each Task() call must complete before starting the next
```

---

## Six Gates Compliance

All agents observe the Six Gates safety framework:

| Gate | Description | Enforcement |
|------|-------------|-------------|
| 1 | Read Before Write | Read inputs before mutations |
| 2 | File Exists Check | Validate targets exist |
| 3 | Chain Validation | Checkpoints between phases |
| 4 | Mutation Confirm | Preview before write |
| 5 | MCP Health | Verify MCP connectivity |
| 6 | Post Validation | Verify writes succeeded |

Agents that fail Gate 3 validation are **blocked** by project hooks.

---

**Version**: 1.6.3
**Last Updated**: 2026-01-03
