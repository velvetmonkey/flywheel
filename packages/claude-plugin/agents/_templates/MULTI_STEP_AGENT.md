---
name: your-agent-name
description: One-line description of what this agent does
allowed-tools: Task, Read, Edit
model: sonnet
---

# Agent Name

## Purpose

What this agent does and when it should be invoked.

## When You're Called

```python
Task(
    subagent_type="your-agent-name",
    description="Brief description",
    prompt="Detailed instructions"
)
```

## Process Flow

```
Phase 1: [Description]
     ↓
Phase 2: [Description] → VERIFY before proceeding
     ↓
Phase 3: [Description] → VERIFY before proceeding
     ↓
Report Summary
```

## Phase 1: [Name]

[Detailed instructions for this phase]

## Phase 2: [Name]

[Detailed instructions for this phase]

**GATE 3 CHECKPOINT:** Before proceeding to Phase 3, verify:
- [ ] Phase 2 completed successfully
- [ ] Expected outputs are present
- [ ] No errors that would invalidate Phase 3

## Phase 3: [Name]

[Detailed instructions for this phase]

## Critical Rules

### Sequential Execution

- Process phases in order
- **Wait for completion** before calling next phase
- No parallel execution of dependent steps
- Each Task() call must complete before starting the next

### Error Handling

- If a phase fails, note it but continue if possible
- Report all failures in final summary
- Never proceed if verification fails
- Track which sub-tasks succeeded and which failed

## Expected Output

```
Phase Results:
✓ Phase 1: [Description] - Completed
✓ Phase 2: [Description] - Completed (X items processed)
✗ Phase 3: [Description] - Failed (reason)

Summary:
- Total phases: 3
- Completed: 2
- Failed: 1

Errors:
- Phase 3: [Specific error message]
```

## Six Gates Compliance

| Gate | Status | Notes |
|------|--------|-------|
| 1. Read Before Write | ✅ | Reads all inputs before mutations |
| 2. File Exists Check | ✅ | Validates targets in Phase 1 |
| 3. Chain Validation | ✅ | Checkpoints between phases |
| 4. Mutation Confirm | ✅ | Reports preview before write |
| 5. MCP Health | N/A | [Adjust based on MCP tool usage] |
| 6. Post Validation | ✅ | Verifies writes in summary |

## Example Invocations

### From Parent Agent
```python
Task(
    subagent_type="your-agent-name",
    description="Process [something]",
    prompt="Process [details]"
)
```

### From User (Manual)
```python
Task(
    subagent_type="your-agent-name",
    description="Manual invocation",
    prompt="[User's request]"
)
```

## Notes

- [Additional implementation notes]
- [Edge cases to be aware of]
- [Dependencies on other agents/tools]
