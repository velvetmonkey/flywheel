---
skill: vault-activity
---

# /vault-activity - Vault Activity Summary

Get a summary of vault editing activity over a time period.

## Usage

```
/vault-activity                      # Last 7 days (default)
/vault-activity 30                   # Last 30 days
/vault-activity this week            # This week
```

## What It Does

```
Activity Summary
────────────────────────────────────────────────────────────────
Modified: 42     Created: 8     Edits: 127     Avg/Day: 18
────────────────────────────────────────────────────────────────
```

## Where Output Goes

| Action | Target | Notes |
|--------|--------|-------|
| Report | Console output | Activity breakdown |
| Trends | Console output | Patterns detected |

## Process

1. **Query** - Get activity data from MCP
2. **Aggregate** - Group by day, folder, note
3. **Analyze** - Detect patterns
4. **Report** - Show trends and insights

## Example Output

```
Vault Activity Summary
===============================================

Period: Last 7 days (2025-12-24 to 2025-12-31)

Overview:
  Notes modified:     42
  Notes created:       8
  Total edits:       127
  Avg edits/day:      18

Daily Breakdown:

  Date          Modified  Created  Edits
  ----------------------------------------
  2025-12-31       12        2       28
  2025-12-30        8        1       19
  2025-12-29        6        0       15
  2025-12-28        4        2       12
  2025-12-27        3        0        8
  2025-12-26        5        1       14
  2025-12-25        2        1        6

Most active day: 2025-12-31 (28 edits)

Activity by Folder:

  Folder              Notes   % of Activity
  ----------------------------------------
  daily-notes/          7        17%
  projects/            12        29%
  tech/                 8        19%
  work/                 6        14%
  personal/             5        12%

Most Active Notes:
  1. projects/Alpha.md           (15 edits)
  2. daily-notes/2025-12-31.md   (12 edits)
  3. tech/frameworks/React.md     (8 edits)

Patterns Detected:
  Trending up: 68% more activity in last 3 days
  Focus area: projects/ folder (29% of activity)

===============================================
```
