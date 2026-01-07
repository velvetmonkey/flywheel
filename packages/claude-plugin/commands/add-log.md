---
skill: add-log
---

# /add-log - Add Timestamped Log Entry

Add a timestamped log entry to today's daily note.

## Usage

```
/add-log Fixed the authentication bug
/add-log Meeting with John about project
/add-log Completed code review for PR #123
```

## What It Does

```
Log Entry Added
────────────────────────────────────────────────────────────────
Added to daily-notes/2025-12-31.md at 14:30
────────────────────────────────────────────────────────────────
```

## Where Output Goes

| Action | Target | Notes |
|--------|--------|-------|
| Entry | Daily note | Appended to ## Log section |
| Timestamp | Auto-generated | HH:MM format |

## Example Output

```
Log Entry Added
===============================================

Added to: daily-notes/2025-12-31.md

## Log

- 14:30 Fixed the authentication bug

-------------------------------------------------

Today's log so far:
- 09:15 Started work on [[Project Alpha]]
- 10:30 Code review for PR #123
- 12:00 Lunch break
- 14:30 Fixed the authentication bug  <-- NEW

===============================================
```
