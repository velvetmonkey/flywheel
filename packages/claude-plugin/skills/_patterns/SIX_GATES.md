---
name: six-gates
description: Mandatory safety framework for all Flywheel extensions. Explains the six gates pattern and provides compliance templates.
auto_trigger: true
trigger_keywords:
  - "six gates"
  - "safety framework"
  - "gate pattern"
  - "mutation safety"
  - "flywheel safety"
  - "skill template"
  - "compliance checklist"
  - "how to write a skill"
  - "skill guidelines"
  - "extension guidelines"
  - "hook requirements"
  - "mcp tool requirements"
allowed-tools: Read
---

# Six Gates Safety Framework

**STATUS: MANDATORY**

This document defines the Six Gates safety pattern. **All Flywheel skills, agents, hooks, and MCP tools MUST observe these gates.** This is not optional.

---

## The Six Gates

| Gate | When | What | REQUIRED Action |
|------|------|------|-----------------|
| **1. Tool Selection** | Before any operation | Decide: read-only or mutative? | Use read-only tools when query suffices |
| **2. Precondition Checks** | Before execution | Validate targets exist | Call validation tools before mutation |
| **3. Agent Chain Validation** | Multi-step workflows | Verify each step completed | Check success before proceeding |
| **4. Destructive Command Guard** | Before any write/delete | Get user confirmation | Show diff/preview, ask to proceed |
| **5. MCP Connection Verification** | Session start | Verify MCP is working | Call `health_check`, handle failures |
| **6. Post-Execution Validation** | After any mutation | Confirm changes applied correctly | Re-read file, validate syntax |

---

## Gate Implementation Requirements

### Gate 1: Tool Selection

**REQUIRED**: Skills MUST prefer read-only operations.

```markdown
# In skill SKILL.md:

## Gate 1: Read Before Write

Before ANY mutation:
1. Read current state with read-only tools
2. Analyze what needs to change
3. Only then proceed to mutation

Bad:
  "Add a task" → immediately writes

Good:
  "Add a task" → reads file → shows current tasks → confirms addition → writes
```

### Gate 2: Precondition Checks

**REQUIRED**: Validate targets exist before operating.

```markdown
## Gate 2: Validate Targets

Before ANY file operation:
1. Call mcp__flywheel__get_note_metadata(path) to verify note exists
2. If note doesn't exist, ASK user before creating
3. Check file is within vault boundary (PROJECT_PATH)

Bad:
  Write to "daily/2024-01-15.md" without checking if daily/ exists

Good:
  Check "daily/2024-01-15.md" exists → if not, ask "Create daily note?"
```

### Gate 3: Agent Chain Validation

**REQUIRED**: Multi-step operations must verify each step.

```markdown
## Gate 3: Chain Verification

For multi-step workflows (rollups, batch operations):
1. Execute step
2. VERIFY step succeeded before continuing
3. If step fails, STOP and report

Bad:
  daily rollup → weekly rollup → monthly rollup (no verification)

Good:
  daily rollup → verify 7 days aggregated →
  weekly rollup → verify week complete →
  monthly rollup → verify month complete
```

### Gate 4: Destructive Command Guard

**REQUIRED**: All mutations must show preview and get confirmation.

```markdown
## Gate 4: Confirm Mutations

Before ANY write operation:
1. READ current state
2. SHOW user what will change (diff preview)
3. ASK for confirmation: "Proceed? (y/n)"
4. Only execute if confirmed

Users can auto-approve via permissions.allow in settings.

Bad:
  User says "add log entry" → immediately writes to file

Good:
  User says "add log entry" →
  Show: "Will append to daily/2024-01-15.md:
         ## Log
         - [10:30] Your new entry"
  Ask: "Proceed?"
  → User confirms → write
```

### Gate 5: MCP Connection Verification

**REQUIRED**: Session start must verify MCP health.

```markdown
## Gate 5: Verify MCP

On session start:
1. session-gate.py hook runs automatically
2. Hook checks PROJECT_PATH accessibility
3. Skill should call mcp__flywheel__health_check for detailed status
4. If status != "healthy", warn user before proceeding

Bad:
  Start session → immediately use MCP tools (may silently fail)

Good:
  Start session → health_check shows "degraded, index stale" →
  refresh_index → health_check shows "healthy" → proceed
```

### Gate 6: Post-Execution Validation

**REQUIRED**: All mutations must be verified after execution.

```markdown
## Gate 6: Verify Writes

After ANY Edit/Write:
1. verify-mutation.py hook runs automatically
2. Hook validates YAML frontmatter syntax
3. Hook validates wikilink syntax
4. If issues detected, report to user immediately

Skills should also:
1. Re-read the file after writing
2. Verify expected changes are present
3. Report success/failure clearly

Bad:
  Write file → assume success

Good:
  Write file → re-read file →
  verify content matches intent →
  report: "Added 1 task to daily/2024-01-15.md"
```

---

## Skill Template (MANDATORY)

All new skills MUST follow this template:

```markdown
---
name: skill-name
description: What this skill does
auto_trigger: true/false
trigger_keywords:
  - "keyword1"
  - "keyword2"
allowed-tools: mcp__flywheel__tool1, mcp__flywheel__tool2
---

# Skill Name

## Purpose
What this skill does.

## Six Gates Compliance

### Gate 1: Tool Selection
- [ ] Uses read-only tools before mutations
- [ ] Documents which tools are read-only vs mutative

### Gate 2: Precondition Checks
- [ ] Validates target files exist
- [ ] Checks vault boundary

### Gate 3: Agent Chain Validation
- [ ] Verifies each step in multi-step operations
- [ ] Stops on failure

### Gate 4: Destructive Command Guard
- [ ] Shows preview before mutations
- [ ] Asks for confirmation
- [ ] Respects user's permission settings

### Gate 5: MCP Connection Verification
- [ ] Handles MCP tool failures gracefully
- [ ] Warns user if MCP unavailable

### Gate 6: Post-Execution Validation
- [ ] Verifies changes after write
- [ ] Reports success/failure clearly

## Process

### 1. Parse User Input
...

### 2. Precondition Checks (Gate 2)
```
mcp__flywheel__get_note_metadata(path)
# Verify note exists
```

### 3. Show Preview (Gate 4)
```
Show user what will change
Ask for confirmation
```

### 4. Execute
```
mcp__flywheel__tool(...)
```

### 5. Verify (Gate 6)
```
Re-read file
Confirm changes applied
Report result
```
```

---

## Hook Requirements

### Required Hooks (Already Implemented)

1. **session-gate.py** (SessionStart)
   - Verifies PROJECT_PATH
   - Warns if MCP may not work

2. **verify-mutation.py** (PostToolUse: Edit|Write)
   - Validates YAML frontmatter
   - Validates wikilink syntax
   - Reports issues

### Hook Error Handling

**REQUIRED**: Hooks must surface errors, not swallow them.

```python
# Bad - swallows error
except Exception as e:
    sys.exit(0)

# Good - surfaces error then exits cleanly
except Exception as e:
    print(f"[flywheel] Hook error: {e}", file=sys.stderr)
    sys.exit(0)
```

---

## MCP Tool Requirements

### Required: Output Schemas

All MCP tools MUST have output schemas for predictable responses.

### Required: Error Handling

All MCP tools MUST handle:
- Missing files gracefully
- Invalid input with clear error messages
- Vault boundary violations

---

## Enforcement

### Code Review Checklist

When reviewing Flywheel code, verify:

- [ ] **Gate 1**: Does it use read-only tools before mutations?
- [ ] **Gate 2**: Does it validate targets exist?
- [ ] **Gate 3**: Does it verify multi-step operations?
- [ ] **Gate 4**: Does it show preview and get confirmation?
- [ ] **Gate 5**: Does it handle MCP failures?
- [ ] **Gate 6**: Does it verify writes succeeded?

### Automated Verification

The following hooks enforce gates automatically:
- `session-gate.py` → Gate 5
- `verify-mutation.py` → Gate 6
- `syntax-validate.py` → Gate 6 (syntax fixes)
- `wikilink-suggest.py` → Gate 2 (vault boundary check)

---

## Version History

- **1.0.0** (2024-01-15): Initial Six Gates framework
