---
skill: task-add
---

# /task-add - Add Task With Due Date

Add a task with optional due date to a note.

## Usage

```
/task-add Review PR by Friday
/task-add Submit report @2025-01-15
/task-add Call client Project.md          # Add to specific note
```

## What It Does

```
Task Added
────────────────────────────────────────────────────────────────
Added task to daily-notes/2025-12-31.md
────────────────────────────────────────────────────────────────
```

## Task Format

Tasks are added in standard markdown format:
- `- [ ] HH:MM Task description`
- With due date: `- [ ] HH:MM Task 📅 2025-01-15`

## Where Output Goes

| Action | Target | Notes |
|--------|--------|-------|
| Task | Note's ## Log section | New task item |
| Due date | 📅 YYYY-MM-DD suffix | If specified |

## Example Output

```
Task Added
===============================================

Added to: daily-notes/2025-12-31.md

## Log

- [ ] 14:30 Review PR by Friday 📅 2025-01-03  <-- NEW

-------------------------------------------------

Current tasks in note:
- [ ] 14:30 Review PR by Friday 📅 2025-01-03
- [ ] 10:15 Submit monthly report 📅 2025-01-05
- [x] 09:00 Complete code review

===============================================
```
