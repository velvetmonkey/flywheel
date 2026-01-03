# Six Gates Safety Framework

**MANDATORY - ENFORCED BY HOOKS**

All Flywheel skills, agents, hooks, and MCP tools MUST observe these gates.

---

## Overview

| Gate | When | Purpose | Enforcement |
|------|------|---------|-------------|
| **1** | Before operation | Read before write | BLOCKS |
| **2** | Before operation | Validate targets exist | BLOCKS |
| **3** | Multi-step | Verify each step | BLOCKS |
| **4** | Before write | User confirmation | BLOCKS |
| **5** | Session start | MCP health check | WARNS |
| **6** | After write | Verify changes | WARNS |

---

## The Six Gates

### Gate 1: Read Before Write

**Requirement**: Use read-only tools before mutations.

```
Bad:  "Add task" → immediately writes
Good: "Add task" → reads file → shows current → confirms → writes
```

**Enforcement**: `pre-mutation-gate.py` (PreToolUse) - BLOCKS

### Gate 2: Validate Targets

**Requirement**: Verify files exist before operating.

```
Bad:  Write to "daily/2024-01-15.md" without checking
Good: Check if file exists → ask "Create?" if not → write
```

**Enforcement**: `pre-mutation-gate.py` (PreToolUse) - BLOCKS

### Gate 3: Agent Chain Validation

**Requirement**: Verify each step in multi-step workflows.

```
Bad:  daily → weekly → monthly (no verification)
Good: daily → ✓ verify → weekly → ✓ verify → monthly → ✓ verify
```

**Enforcement**: `.claude/hooks/validate-agent-gate3.py` - BLOCKS

### Gate 4: Mutation Confirmation

**Requirement**: Show preview and get confirmation before writes.

```
Bad:  User says "add log" → writes immediately
Good: User says "add log" → show preview → "Proceed?" → writes
```

**Enforcement**: `pre-mutation-gate.py` (PreToolUse) - BLOCKS

### Gate 5: MCP Health Check

**Requirement**: Verify MCP connectivity at session start.

```
Bad:  Start → use MCP tools (may silently fail)
Good: Start → health_check → if degraded, refresh_index → proceed
```

**Enforcement**: `session-gate.py` (SessionStart) - WARNS

### Gate 6: Post-Write Validation

**Requirement**: Verify mutations after execution.

```
Bad:  Write file → assume success
Good: Write file → re-read → verify changes present → report
```

**Enforcement**: `verify-mutation.py` (PostToolUse) - WARNS

---

## Hook Architecture

```
Plugin Level (all users)           Project Level (developers)
packages/claude-plugin/hooks/      .claude/hooks/
├── pre-mutation-gate.py (1,2,4)   ├── validate-agent-gate3.py (3)
├── session-gate.py (5)            └── validate-agent-gate3-post.py (3)
└── verify-mutation.py (6)
```

---

## Skill Compliance Template

New skills MUST include a Six Gates checklist:

```markdown
## Six Gates Compliance

- [x] Gate 1: Uses read-only tools before mutations
- [x] Gate 2: Validates target files exist
- [x] Gate 3: N/A (single-step) or verifies each step
- [x] Gate 4: Shows preview before write
- [x] Gate 5: Handles MCP failures gracefully
- [x] Gate 6: Verifies changes after write
```

---

## Agent Compliance Template

Multi-step agents MUST include Gate 3 checkpoints:

```markdown
## Phase 1: [Name]
[Instructions]

**GATE 3 CHECKPOINT:** Before Phase 2, verify:
- [ ] Phase 1 completed successfully
- [ ] Expected outputs present
- [ ] No blocking errors

## Phase 2: [Name]
[Instructions]
```

---

## Code Review Checklist

When reviewing Flywheel code:

- [ ] **Gate 1**: Uses read-only tools before mutations?
- [ ] **Gate 2**: Validates targets exist?
- [ ] **Gate 3**: Verifies multi-step operations?
- [ ] **Gate 4**: Shows preview and gets confirmation?
- [ ] **Gate 5**: Handles MCP failures?
- [ ] **Gate 6**: Verifies writes succeeded?

---

## Examples

### Good: Adding a Log Entry

```
1. Gate 1: Read daily note first
2. Gate 2: Verify daily note exists (or offer to create)
3. Gate 4: Show preview of new entry
4. Gate 4: Ask "Add this entry? (y/n)"
5. Execute: Append to log section
6. Gate 6: Re-read file, confirm entry present
7. Report: "Added: - 10:30 [description]"
```

### Good: Rollup Chain

```
1. Calculate date range
2. For each week:
   a. Call weekly-agent
   b. Gate 3: Verify weekly note updated
   c. If failed, note but continue
3. For each month:
   a. Call monthly-agent
   b. Gate 3: Verify monthly note updated
4. Report: "Processed X weeks, Y months"
```

### Bad: Skipping Verification

```
❌ User: "add task"
❌ Agent: *immediately writes to file*
❌ Agent: "Done"

Why bad:
- Gate 1 violated: No read first
- Gate 2 violated: Didn't check file exists
- Gate 4 violated: No confirmation
- Gate 6 violated: No verification
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.6.2 | 2025-01-03 | Real enforcement via PreToolUse hooks |
| 1.6.1 | 2025-01-02 | Added session-gate.py, verify-mutation.py |
| 1.0.0 | 2024-01-15 | Initial framework |

---

**Version**: 1.6.3
**Last Updated**: 2026-01-03
