---
skill: vault-due
---

# /vault-due - Show Tasks With Due Dates

Get tasks sorted by due date.

## Usage

```
/vault-due                           # All tasks with due dates
/vault-due overdue                   # Only overdue tasks
/vault-due this week                 # Due this week
```

## What It Does

```
Due Tasks
────────────────────────────────────────────────────────────────
Found: 23 tasks with due dates (3 overdue)
────────────────────────────────────────────────────────────────
```

## Where Output Goes

| Action | Target | Notes |
|--------|--------|-------|
| Report | Console output | Sorted task list |
| Alerts | Console output | Overdue warnings |

## Example Output

```
Tasks By Due Date
===============================================

OVERDUE (3) - Needs attention!

  2025-12-28 (3 days ago):
    - [ ] Submit monthly report
          from: work/reports.md

  2025-12-29 (2 days ago):
    - [ ] Review PR #45
          from: daily-notes/2025-12-29.md

  2025-12-30 (1 day ago):
    - [ ] Client follow-up
          from: projects/client-x.md

TODAY (2):
  - [ ] Team standup @due(2025-12-31)
  - [ ] Code review @due(2025-12-31)

TOMORROW (3):
  - [ ] Sprint planning @due(2026-01-01)
  - [ ] Deploy to staging @due(2026-01-01)
  - [ ] Documentation review @due(2026-01-01)

THIS WEEK (8):
  - [ ] Complete feature X @due(2026-01-03)
  - [ ] User testing @due(2026-01-04)
  ...

LATER (7):
  - [ ] Quarterly review @due(2026-01-15)
  ...

SUMMARY:
  Overdue: 3 (address immediately!)
  Due today: 2
  Due this week: 13
  Total with dates: 23

===============================================
```
