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

**Version**: 1.8.0
**Last Updated**: 2026-01-03

---

## Workflow Integration Examples (v1.8)

This section shows how v1.8 workflows apply the Six Gates in practice.

### Action Extraction Workflow

**Workflow**: `/extract-actions` → action-extraction-agent → meeting note updated

**Gate Application**:

| Gate | Implementation |
|------|----------------|
| **Gate 1** | Agent reads meeting note before extracting actions |
| **Gate 2** | Verifies meeting note exists before reading |
| **Gate 3** | Validates that action items were found before writing |
| **Gate 4** | Shows preview of extracted actions, asks confirmation |
| **Gate 6** | Verifies action items section was updated correctly |

**Example Flow**:

```
1. User: "/extract-actions meetings/2026-01-03-team-sync.md"
2. Gate 2: ✓ File exists
3. Gate 1: Read("meetings/2026-01-03-team-sync.md")
4. Agent: Extract actions from discussion
5. Gate 3: ✓ Found 4 action items
6. Gate 4: Show preview → Ask "Add these 4 actions?"
7. User: "yes"
8. Edit meeting note with action items
9. Gate 6: ✓ Verify action items appear in ## Action Items section
```

---

### Weekly Review Workflow

**Workflow**: `/weekly-review` → weekly-review-agent → rollup + reflection

**Gate Application**:

| Gate | Implementation |
|------|----------------|
| **Gate 1** | Agent reads all 7 daily notes before writing weekly summary |
| **Gate 2** | Verifies daily notes exist (warns if partial week) |
| **Gate 3** | Validates data extraction at each phase (habits, food, logs) |
| **Gate 4** | Shows preview of weekly summary, asks confirmation |
| **Gate 6** | Verifies weekly note was created with expected sections |

**Example Flow**:

```
1. User: "/weekly-review 2026-W01"
2. Gate 2: Check for 7 daily notes → ✓ 7/7 found
3. Gate 1: Read("daily-notes/2025-12-29.md") ... Read("daily-notes/2026-01-04.md")
4. Agent Phase 1: Extract habits → Gate 3: ✓ Verify data
5. Agent Phase 2: Extract food → Gate 3: ✓ Verify data
6. Agent Phase 3: Extract logs → Gate 3: ✓ Verify data
7. Gate 4: Show preview → "Create weekly-notes/2026-W01.md?"
8. User: "yes"
9. Write("weekly-notes/2026-W01.md", content)
10. Gate 6: ✓ Verify ## Achievements, ## Habits, ## Food sections exist
```

**Partial Week Handling**:

```
1. User: "/weekly-review 2026-W01"
2. Gate 2: Check for 7 daily notes → ⚠️ Only 5/7 found
3. Gate 3: Ask "Proceed with partial week (5/7 days)?"
4. User: "yes"
5. Continue with available notes
```

---

### Standup Aggregation Workflow

**Workflow**: `/standup-rollup` → standup-agent → team summary

**Gate Application**:

| Gate | Implementation |
|------|----------------|
| **Gate 1** | Agent reads all team member standup notes before aggregating |
| **Gate 2** | Verifies standup notes exist for all team members |
| **Gate 3** | Validates blocker extraction before writing summary |
| **Gate 4** | Shows preview of team summary, asks confirmation |
| **Gate 6** | Verifies blockers section is populated correctly |

**Example Flow**:

```
1. User: "/standup-rollup 2026-01-03"
2. Find standup notes: standups/alice.md, standups/bob.md, standups/charlie.md
3. Gate 2: ✓ All 3 notes exist
4. Gate 1: Read all 3 standup notes
5. Agent: Aggregate Yesterday/Today/Blockers
6. Gate 3: ✓ Identified 2 common blockers
7. Gate 4: Show preview → "Create team-2026-01-03.md?"
8. User: "yes"
9. Write("standups/team-2026-01-03.md", content)
10. Gate 6: ✓ Verify ## Common Blockers section populated
```

---

### OKR Review Workflow

**Workflow**: `/okr-review` → okr-review-agent → scored OKRs

**Gate Application**:

| Gate | Implementation |
|------|----------------|
| **Gate 1** | Agent reads OKR note + quarterly notes before scoring |
| **Gate 2** | Verifies OKR note exists (creates if missing) |
| **Gate 3** | Validates evidence gathering before scoring |
| **Gate 4** | Shows score calculations, asks confirmation before bulk update |
| **Gate 6** | Verifies all key result scores were updated |

**Example Flow**:

```
1. User: "/okr-review 2026-Q1"
2. Gate 2: Check OKR note → ✓ okrs/2026-Q1.md exists
3. Gate 1: Read("okrs/2026-Q1.md")
4. Gate 1: Read("quarterly-notes/2026-Q1.md") for evidence
5. Agent: Match achievements to key results
6. Gate 3: ✓ Found evidence for 3/3 key results
7. Agent: Calculate scores (KR1: 0.53, KR2: 0.75, KR3: 0.66)
8. Gate 4: Show scores → "Update 3 key results with calculated scores?"
9. User: "yes"
10. Edit("okrs/2026-Q1.md", old_scores, new_scores)
11. Gate 6: ✓ Verify all 3 scores appear in updated note
```

**No Evidence Handling**:

```
1. Gate 3: ⚠️ No evidence found for Key Result 2
2. Agent: Warn "Key Result 2: No achievements matched. Score based on current value only?"
3. User: "yes" → proceed with available data
```

---

### Customer Onboarding Workflow

**Workflow**: `/onboard-customer` → customer-onboarding-agent → populated checklist

**Gate Application**:

| Gate | Implementation |
|------|----------------|
| **Gate 1** | Agent reads template before interpolating variables |
| **Gate 2** | Verifies template exists (critical for this workflow) |
| **Gate 3** | Validates variable interpolation before writing |
| **Gate 4** | Shows preview of customer note, asks confirmation |
| **Gate 6** | Verifies customer note created with all sections |

**Example Flow**:

```
1. User: "/onboard-customer Acme Corp"
2. Gate 2: Check template → ✓ templates/customer-onboarding.md exists
3. Gate 1: Read("templates/customer-onboarding.md")
4. Agent: Interpolate {{customer}} → "Acme Corp", {{date}} → "2026-01-03"
5. Gate 3: ✓ Verify all {{variables}} replaced
6. Gate 4: Show preview → "Create customers/Acme Corp.md?"
7. User: "yes"
8. Write("customers/Acme Corp.md", interpolated_content)
9. Gate 6: ✓ Verify ## Pre-Engagement, ## Discovery sections exist
```

**Missing Template Handling**:

```
1. Gate 2: ❌ Template not found: templates/customer-onboarding.md
2. Agent: Error "Template missing. Create it or check path in .flywheel.json"
3. Workflow stops (cannot proceed without template)
```

---

### Rollup Chain Workflow

**Workflow**: `/rollup` → rollup-agent → chains weekly/monthly/quarterly/yearly agents

**Gate Application**:

| Gate | Implementation |
|------|----------------|
| **Gate 1** | Each agent reads input notes before writing output |
| **Gate 2** | Each agent verifies input notes exist |
| **Gate 3** | Each agent validates output before proceeding to next level |
| **Gate 4** | Asks confirmation at each level (weekly → monthly → etc.) |
| **Gate 6** | Each agent verifies output note was created correctly |

**Example Flow** (Weekly → Monthly):

```
Weekly Agent:
1. Gate 2: Check for 7 daily notes → ✓ Found
2. Gate 1: Read all 7 daily notes
3. Gate 3: ✓ Extracted data successfully
4. Gate 4: "Create weekly-notes/2026-W01.md?"
5. Write weekly note
6. Gate 6: ✓ Verify weekly note exists

rollup-agent checks Gate 3: ✓ Weekly note created successfully

Monthly Agent:
1. Gate 2: Check for 4-5 weekly notes → ✓ Found
2. Gate 1: Read all weekly notes
3. Gate 3: ✓ Aggregated data successfully
4. Gate 4: "Create monthly-notes/2026-01.md?"
5. Write monthly note
6. Gate 6: ✓ Verify monthly note exists

rollup-agent checks Gate 3: ✓ Monthly note created successfully
(Continue to quarterly/yearly if applicable)
```

**Gate 3 Chain Failure**:

```
Weekly Agent:
1-5. Success (weekly note created)
6. Gate 6: ⚠️ Weekly note missing ## Achievements section

rollup-agent Gate 3: ❌ Weekly note incomplete
Action: Stop chain, report error to user
User: Fix weekly note manually, then resume
```

---

## Gate Compliance Patterns

### Pattern 1: Read-Aggregate-Write

Most v1.8 workflows follow this pattern:

```
1. Gate 2: Verify inputs exist
2. Gate 1: Read all inputs
3. Gate 3: Validate aggregation
4. Gate 4: Confirm with user
5. Write output
6. Gate 6: Verify output
```

**Used By**: weekly-review, standup-rollup, rollup chain

---

### Pattern 2: Read-Extract-Edit

Workflows that modify existing notes:

```
1. Gate 2: Verify target exists
2. Gate 1: Read target
3. Gate 3: Validate extraction
4. Gate 4: Confirm changes
5. Edit target
6. Gate 6: Verify edits applied
```

**Used By**: action-extraction, okr-review

---

### Pattern 3: Read-Interpolate-Write

Template-based workflows:

```
1. Gate 2: Verify template exists
2. Gate 1: Read template
3. Gate 3: Validate interpolation
4. Gate 4: Confirm creation
5. Write new note
6. Gate 6: Verify new note
```

**Used By**: customer-onboarding

---

## Troubleshooting Gate Issues

### Gate 1 Violations

**Symptom**: "Must Read file before editing"

**Cause**: Agent tried to Edit/Write without prior Read

**Fix**:
1. Ensure agent calls Read() before Edit()/Write()
2. Check read-cache.py tracked the Read operation
3. Verify session_id matches between Read and Edit

**Example Fix**:

```python
# BAD
def process_note(path):
    Edit(path, old, new)  # ❌ No Read first

# GOOD
def process_note(path):
    content = Read(path)  # ✓ Read first
    # ... process content ...
    Edit(path, old, new)  # ✓ Can edit after Read
```

---

### Gate 2 Violations

**Symptom**: "File does not exist: X"

**Cause**: Agent tried to operate on non-existent file

**Fix**:
1. Add existence check before operation
2. Use Write() instead of Edit() for new files
3. Offer to create file if missing

**Example Fix**:

```python
# BAD
def add_log(date):
    daily_note = f"daily-notes/{date}.md"
    Edit(daily_note, ...)  # ❌ May not exist

# GOOD
def add_log(date):
    daily_note = f"daily-notes/{date}.md"
    if not exists(daily_note):  # ✓ Check existence
        Write(daily_note, template)  # ✓ Create if missing
    else:
        Edit(daily_note, ...)  # ✓ Edit if exists
```

---

### Gate 3 Violations

**Symptom**: Workflow stops mid-chain with "Validation failed"

**Cause**: Agent didn't verify intermediate step succeeded

**Fix**:
1. Add validation checkpoints between phases
2. Check that expected data was extracted
3. Verify output files were created

**Example Fix**:

```python
# BAD
def rollup_chain():
    weekly_agent()  # ❌ No verification
    monthly_agent()  # ❌ Proceeds blindly

# GOOD
def rollup_chain():
    weekly_result = weekly_agent()
    if not weekly_result.success:  # ✓ Check success
        raise Error("Weekly rollup failed")
    if not exists(weekly_result.output_path):  # ✓ Verify output
        raise Error("Weekly note not created")
    monthly_agent()  # ✓ Safe to proceed
```

---

### Gate 4 Violations

**Symptom**: Bulk changes made without confirmation

**Cause**: Agent skipped confirmation step

**Fix**:
1. Show preview of changes before applying
2. Use Gate 4 ASK decision for bulk operations
3. Wait for user "yes" before proceeding

**Example Fix**:

```python
# BAD
def fix_links(files):
    for file in files:
        Edit(file, ...)  # ❌ No confirmation

# GOOD
def fix_links(files):
    preview = generate_preview(files)
    print(f"Will fix links in {len(files)} files")
    print(preview)
    if ask_user("Proceed?") == "yes":  # ✓ Confirm first
        for file in files:
            Edit(file, ...)  # ✓ Only after confirmation
```

---

## See Also

- [HOOKS.md](./HOOKS.md) - Hook system that enforces gates
- [AGENTS_REFERENCE.md](./AGENTS_REFERENCE.md) - How agents implement gates
- [test_agent_gate_compliance.py](../packages/claude-plugin/hooks/tests/test_agent_gate_compliance.py) - Gate compliance tests
