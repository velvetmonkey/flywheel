# Agentic Design Patterns

> How Flywheel makes AI workflows reliable

## Why Agentic Patterns Matter

Most AI tools treat your vault like a file system. They `grep` for text, read everything, and hope for the best. This is naive and expensive:

- **High token costs**: Reading 50+ files to find 3 relevant ones
- **No safety rails**: AI can corrupt files, miss steps, or fail silently
- **No relationships**: File content without graph context
- **Unpredictable**: Same query, different results each time

Flywheel solves this with **structured agentic design patterns** - proven workflows that make AI automation reliable.

---

## Pattern 1: Graph-First Navigation

**The Problem**: File-centric tools waste tokens reading everything.

**Before (File-Centric Approach)**:
```
User: "Find all notes about Project Alpha"

grep "Project Alpha" . -r
  → 47 files match

Read all 47 files
  → 50,000+ tokens consumed
  → 10+ minutes of processing

Manual synthesis required
  → What connects to what?
  → Which notes are important?
```

**After (Graph-First with Flywheel)**:
```
User: "Find all notes about Project Alpha"

search_notes({ title_contains: "Project Alpha" })
  → 3 core notes identified

get_backlinks("Project Alpha.md")
  → 12 notes reference it

Read only the 3 core notes
  → ~5,000 tokens consumed
  → 30 seconds
  → Relationship context included
```

### Token Comparison

```
BEFORE (File-centric)                 AFTER (Graph-first)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Search: Grep everything               Search: Semantic queries
  Result: 47 files                      Result: 3 core + 12 refs
  Read: All matches                     Read: Only core (surgical)
  Tokens: 50,000+                       Tokens: ~5,000
  Time: 10+ min                         Time: 30 sec

  ████████████████████████              ████
```

**10x token reduction. 20x faster. Full relationship context.**

### The Graph-First Workflow

```
┌────────────────────────────────────────────────────────────┐
│  Step 1: NAVIGATE (Graph Intelligence)                    │
│  ─────────────────────────────────────                     │
│  Use MCP tools to find targets:                            │
│    • search_notes() - Find by tag, frontmatter, title      │
│    • get_backlinks() - Who references this?                │
│    • find_hub_notes() - What are key concepts?             │
│    • get_link_path() - How do A and B connect?             │
│                                                            │
│  Cost: ~500 tokens (metadata only)                         │
├────────────────────────────────────────────────────────────┤
│  Step 2: READ (Surgical File Operations)                  │
│  ───────────────────────────────────────                   │
│  Read only identified targets:                             │
│    • Read core notes (3 files)                             │
│    • get_section_content() - Extract sections only         │
│    • get_note_metadata() - Headers without content         │
│                                                            │
│  Cost: ~4,500 tokens (actual content)                      │
├────────────────────────────────────────────────────────────┤
│  Step 3: UNDERSTAND (Synthesis with Context)               │
│  ─────────────────────────────────────────                 │
│  You now have:                                             │
│    • Target content                                        │
│    • Relationship graph (what connects)                    │
│    • Metadata (tags, frontmatter)                          │
│    • Temporal context (when edited)                        │
│                                                            │
│  Total: ~5,000 tokens with full context                    │
└────────────────────────────────────────────────────────────┘
```

**Key Insight**: Use your eyes (MCP) to navigate, your hands (file tools) to read. Only touch what you need.

---

## Pattern 2: Agent Chaining

**The Problem**: Complex workflows need multiple steps in sequence.

**Flywheel's Solution**: Hierarchical agent orchestration with verification gates.

### Rollup Chain Example

The rollup workflow aggregates notes from daily → weekly → monthly → quarterly → yearly:

```
┌──────────────────────────────────────────────────────────────────┐
│                         ROLLUP CHAIN                             │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  rollup-agent (Orchestrator)                                     │
│       │                                                          │
│       ├─▶ weekly-agent                                           │
│       │    ├─ Read daily-notes/2025-01-*.md (7 notes)            │
│       │    ├─ Extract: habits, food, log entries                 │
│       │    ├─ Write weekly-notes/2025-W01.md                     │
│       │    └─ VERIFY ✓ File exists, content valid               │
│       │                                                          │
│       ├─▶ monthly-agent                                          │
│       │    ├─ Read weekly-notes/2025-W*.md (4 weeks)             │
│       │    ├─ Aggregate: totals, achievements, trends            │
│       │    ├─ Write monthly-notes/2025-01.md                     │
│       │    └─ VERIFY ✓ File exists, data accurate               │
│       │                                                          │
│       ├─▶ quarterly-agent (if end of quarter)                    │
│       │    ├─ Read monthly-notes/2025-*.md (3 months)            │
│       │    ├─ Synthesize: quarter highlights, goal progress      │
│       │    ├─ Write quarterly-notes/2025-Q1.md                   │
│       │    └─ VERIFY ✓ File exists, synthesis complete          │
│       │                                                          │
│       └─▶ Report Summary                                         │
│            ✓ Weekly: 2025-W01.md created                         │
│            ✓ Monthly: Not triggered (week 1)                     │
│            ✓ Quarterly: Not triggered                            │
└──────────────────────────────────────────────────────────────────┘
```

### Agent Spawning Pattern

```python
# Parent agent spawns sub-agent
Task(
    subagent_type="rollup-weekly-agent",
    description="Process week 2025-W01",
    prompt="Process daily notes for week 2025-W01 (Jan 1-7). Extract habits, food entries, and log summaries."
)

# Sub-agent executes, returns results
# Parent verifies success before continuing
```

### Key Rules for Agent Chains

1. **Sequential Execution**: Each agent completes before next starts
2. **Verification Gates**: Check success before proceeding (Gate 3)
3. **Error Continuation**: Log failures but continue chain
4. **Clear Reporting**: ✓/✗ status for each step

---

## Pattern 3: Six Gates Safety Framework

**The Problem**: AI can corrupt files, skip steps, or fail silently.

**Flywheel's Solution**: Six enforced safety gates that make workflows reliable.

### The Six Gates (Quick Reference)

| Gate | Purpose | Enforced By | Blocks? |
|------|---------|-------------|---------|
| **1. Read Before Write** | Must read current state before mutation | pre-mutation-gate.py | ✓ YES |
| **2. File Exists Check** | Validate Edit targets exist | pre-mutation-gate.py | ✓ YES |
| **3. Chain Validation** | Verify multi-step operations | validate-agent-gate3.py | ✓ YES |
| **4. Mutation Confirmation** | User confirms writes (or auto-allow) | pre-mutation-gate.py | ✓ YES |
| **5. MCP Health Check** | Verify MCP on session start | session-gate.py | ⚠ WARN |
| **6. Post-Write Validation** | Verify writes succeeded | verify-mutation.py | ⚠ WARN |

**Enforcement**: Gates 1-4 are **blocking** - they prevent unsafe operations. Gates 5-6 **warn** users of issues.

### Gate 3 in Practice: Agent Chain Validation

Multi-step agents MUST verify each step before continuing:

```markdown
## Phase 1: Extract Daily Notes

1. Find daily notes for week
2. Read each note
3. Extract habits, food, log data
4. **GATE 3 CHECKPOINT**: Verify 7 days extracted ✓

## Phase 2: Aggregate to Weekly

5. Calculate weekly totals
6. Write weekly-notes/2025-W01.md
7. **GATE 3 CHECKPOINT**: Verify file created ✓

## Phase 3: Report

8. Confirm success to user
```

**If any checkpoint fails, the chain STOPS and reports the error.**

### Why This Matters

Without gates:
- ❌ AI writes without reading (corrupts data)
- ❌ Edit fails silently on missing file
- ❌ Multi-step process skips validation
- ❌ Files written with syntax errors

With gates:
- ✓ AI reads first, shows diff, asks confirmation
- ✓ Edit blocked on missing file (create first)
- ✓ Each step verified before next
- ✓ Syntax validated after write

**Read the full framework**: [SIX_GATES.md](./SIX_GATES.md) (coming soon)

---

## Pattern 4: Parallel Subagent Execution

**When to Parallelize**: Independent tasks with no data dependencies.

**Example**: Content source research for AI briefing

```python
# BAD: Sequential (slow)
Task(subagent_type="research-arxiv", ...)
# Wait for completion...
Task(subagent_type="research-reddit", ...)
# Wait for completion...
Task(subagent_type="research-hackernews", ...)

# GOOD: Parallel (3x faster)
# Single message with 3 Task calls
Task(subagent_type="research-arxiv", ...)
Task(subagent_type="research-reddit", ...)
Task(subagent_type="research-hackernews", ...)
# All execute simultaneously
```

### Parallel Execution Rules

✓ **Parallelize when**:
- Tasks are independent (no shared state)
- No data dependencies between tasks
- Results can be aggregated afterward

✗ **Don't parallelize when**:
- Tasks depend on prior results (rollup chain)
- Order matters (weekly before monthly)
- Shared file mutations (write conflicts)

---

## Pattern 5: Validation Checkpoints

**The Problem**: Silent failures accumulate.

**The Solution**: Explicit verification at each step.

### Checkpoint Template

```markdown
### Step 3: Write Weekly Summary

1. Execute write operation
2. **CHECKPOINT**: Verify file exists
   ```
   get_note_metadata("weekly-notes/2025-W01.md")
   # Expected: File exists, created date = today
   ```
3. **CHECKPOINT**: Verify content
   ```
   get_section_content("weekly-notes/2025-W01.md", "## Habits")
   # Expected: 7 days of habit data
   ```
4. **CHECKPOINT**: Validate syntax
   ```
   verify-mutation.py runs automatically
   # Checks: YAML valid, wikilinks correct
   ```
5. Report: ✓ Week 2025-W01 created successfully
```

### What to Verify

| Operation | Verify |
|-----------|--------|
| **Write** | File exists, content present, syntax valid |
| **Edit** | Changes applied, no corruption, backup available |
| **Agent spawn** | Agent completed, expected output exists, no errors |
| **Batch operation** | N items processed, M succeeded, P failed |

---

## Pattern 6: Shared Logic Libraries

**The Problem**: Duplicate code between hooks and agents.

**The Solution**: Python modules in `hooks/lib/` for shared functionality.

### Example: Achievement Detection

```
hooks/lib/achievement_detector.py  ← Shared library
├─ Used by: hooks/achievement-detect.py (real-time)
└─ Used by: agents/achievement/extract-agent.md (batch)
```

**Benefits**:
- Single source of truth
- Consistent behavior
- Easier testing
- DRY principle

---

## Writing Your Own Agents

### Quick Checklist

- [ ] **Frontmatter**: name, description, allowed-tools, model
- [ ] **Purpose section**: What the agent does (1-2 sentences)
- [ ] **Process Flow**: Numbered phases with clear steps
- [ ] **GATE 3 checkpoints**: Verify each step before next
- [ ] **Critical Rules**: Sequential execution, error handling
- [ ] **Expected Output**: Success/failure format with ✓/✗
- [ ] **Six Gates Compliance**: Document which gates apply

### Template

See [MULTI_STEP_AGENT.md](../packages/claude-plugin/agents/_templates/MULTI_STEP_AGENT.md) for full template.

### Gate 3 Requirement

If your agent calls `Task()` to spawn sub-agents, it MUST include:
- Gate 3 checkpoints between steps
- Verification of sub-agent outputs
- Error continuation strategy
- Clear success/failure reporting

**Agents without Gate 3 compliance will be blocked by `validate-agent-gate3.py` hook.**

---

## Summary

Flywheel's agentic patterns make AI workflows reliable:

| Pattern | Benefit | Token Savings | Reliability |
|---------|---------|---------------|-------------|
| **Graph-First** | Navigate before reading | 10x reduction | High (targeted) |
| **Agent Chaining** | Orchestrate complex workflows | N/A | High (verified) |
| **Six Gates** | Safety rails for mutations | N/A | Very High (enforced) |
| **Parallel Execution** | Speed up independent tasks | N/A | High (concurrent) |
| **Validation Checkpoints** | Catch failures early | N/A | Very High (explicit) |

**The result**: Predictable, efficient, safe AI automation for your knowledge base.

---

## Next Steps

- **Try it**: [demos/](../demos/) - 4 demo vaults with concrete examples
- **Install**: [GETTING_STARTED.md](./GETTING_STARTED.md) - 30-second setup
- **Deep dive**: [SIX_GATES.md](./SIX_GATES.md) - Full safety framework
- **Build**: [AGENTS_REFERENCE.md](./AGENTS_REFERENCE.md) - Write your own agents

---

**Last Updated**: 2026-01-03
**Version**: 1.6.2
