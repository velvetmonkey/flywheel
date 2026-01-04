# /extract-actions - Extract Action Items

Extract action items from meeting notes or documents.

## Usage

```
/extract-actions Meeting.md    # Extract from specific note
/extract-actions               # Extract from current context
```

## What It Does

```
Action Extraction
────────────────────────────────────────────────────────────────
Found: 8 action items in Meeting.md
────────────────────────────────────────────────────────────────
```

## Patterns Detected

- "TODO: ..."
- "Action: ..."
- "@person will ..."
- "Need to ..."
- "Follow up on ..."

## Where Output Goes

| Action | Target | Notes |
|--------|--------|-------|
| Report | Console output | Extracted actions |
| Tasks | Optional: create tasks | Add to task list |

## Example Output

```
Extracted Actions: [[Meeting Notes 2025-12-31]]
===============================================

Found 8 action items

EXPLICIT ACTIONS:

1. "TODO: Review the proposal by Friday"
   Assignee: (unspecified)
   Due: Friday

2. "Action: @John to update the docs"
   Assignee: [[John]]
   Due: (unspecified)

IMPLIED ACTIONS:

3. "We need to follow up with the client"
   Assignee: (team)
   Context: Line 45

4. "@Jane will schedule the demo"
   Assignee: [[Jane]]
   Context: Line 52

BY ASSIGNEE:
  @John: 2 actions
  @Jane: 2 actions
  Team: 3 actions
  Unassigned: 1 action

CREATE TASKS?
  Add these as tasks to daily note? [y/n]

===============================================
```
