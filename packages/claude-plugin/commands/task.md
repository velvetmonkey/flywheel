---
skill: add-task
---

# /task - Add Task With Due Date

Add a task with optional due date to a note.

## Usage

```
/task Review PR by Friday
/task Submit report @2025-01-15
/task Call client Project.md          # Add to specific note
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
- `- [ ] Task description`
- With due date: `- [ ] Task @due(2025-01-15)`

## Where Output Goes

| Action | Target | Notes |
|--------|--------|-------|
| Task | Note's ## Tasks section | New task item |
| Due date | Inline annotation | If specified |

## Example Output

```
Task Added
===============================================

Added to: daily-notes/2025-12-31.md

## Tasks

- [ ] Review PR by Friday @due(2025-01-03)  <-- NEW

-------------------------------------------------

Current tasks in note:
- [ ] Review PR by Friday @due(2025-01-03)
- [ ] Submit monthly report @due(2025-01-05)
- [x] Complete code review (done)

===============================================
```
