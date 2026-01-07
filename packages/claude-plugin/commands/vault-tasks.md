---
skill: vault-tasks
---

# /vault-tasks - Show All Tasks

Get all tasks from the vault with filtering options.

## Usage

```
/vault-tasks                         # All open tasks
/vault-tasks done                    # Completed tasks
/vault-tasks projects/               # Tasks in folder
/vault-tasks #work                   # Tasks with tag
```

## What It Does

```
Task Overview
────────────────────────────────────────────────────────────────
Found: 45 open tasks across 23 notes
────────────────────────────────────────────────────────────────
```

## Where Output Goes

| Action | Target | Notes |
|--------|--------|-------|
| Report | Console output | Task list |
| Summary | Console output | Statistics |

## Example Output

```
Tasks Report
===============================================

Found 45 open tasks

BY DUE DATE:

OVERDUE (3):
  - [ ] Submit report @due(2025-12-28)
        from: work/reports.md
  - [ ] Review PR #45 @due(2025-12-29)
        from: daily-notes/2025-12-29.md
  - [ ] Follow up with client @due(2025-12-30)
        from: projects/client-x.md

DUE THIS WEEK (8):
  - [ ] Complete feature X @due(2025-01-03)
  - [ ] Team meeting prep @due(2025-01-02)
  ...

NO DUE DATE (34):
  - [ ] Refactor authentication
  - [ ] Update documentation
  ...

BY FOLDER:
  daily-notes/: 15 tasks
  projects/: 18 tasks
  work/: 12 tasks

SUMMARY:
  Open: 45
  Overdue: 3
  Due this week: 8
  Completed today: 5

===============================================
```
