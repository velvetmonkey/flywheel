# /concurrent - Find Contemporaneous Notes

Find notes that were edited around the same time as a given note.

## Usage

```
/concurrent Project.md         # Notes edited near Project
/concurrent Project.md 48      # Within 48 hours
```

## What It Does

```
Contemporaneous Notes
────────────────────────────────────────────────────────────────
Found: 12 notes edited within 24 hours of [[Project]]
────────────────────────────────────────────────────────────────
```

## Why It Matters

Notes edited together often:
- Share context from same session
- Relate to same topic/project
- Should be linked
- Represent a "work session"

## Where Output Goes

| Action | Target | Notes |
|--------|--------|-------|
| Report | Console output | Time-clustered notes |
| Suggestions | Console output | Missing links |

## Example Output

```
Contemporaneous Notes
===============================================

Reference: [[Project Alpha]]
Last modified: 2025-12-15 14:30

Notes edited within 24 hours:

SAME HOUR (14:00-15:00):
  [[Meeting Notes]] - 14:15
  [[Task List]] - 14:45
  Likely same session

SAME DAY:
  [[Daily Note]] - 09:00
  [[Tech Decision]] - 11:30
  [[Sprint Planning]] - 16:00

PREVIOUS DAY:
  [[Research Doc]] - 2025-12-14 20:00
  [[Draft Proposal]] - 2025-12-14 21:30

INSIGHTS:
  Work session detected: 14:00-15:00
  4 notes edited in same session
  Consider linking [[Meeting Notes]] to [[Project Alpha]]

MISSING CONNECTIONS:
  [[Task List]] mentions Project Alpha but no link
  [[Tech Decision]] relates but not connected

===============================================
```
