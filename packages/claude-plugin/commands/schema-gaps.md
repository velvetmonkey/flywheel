# /schema-gaps - Find Incomplete Notes

Find notes missing expected fields based on folder conventions.

## Usage

```
/schema-gaps                   # Find gaps in entire vault
/schema-gaps projects/         # Gaps in specific folder
```

## What It Does

```
Schema Gap Analysis
────────────────────────────────────────────────────────────────
Found: 34 notes missing expected fields
────────────────────────────────────────────────────────────────
```

## Where Output Goes

| Action | Target | Notes |
|--------|--------|-------|
| Report | Console output | Missing field list |
| Suggestions | Console output | Recommended values |

## Example Output

```
Schema Gaps Report
===============================================

Found 34 incomplete notes

BY FOLDER:

projects/ (12 incomplete):
  Expected: type, status, priority, owner

  projects/Alpha.md - missing: priority, owner
  projects/Beta.md - missing: owner
  projects/Gamma.md - missing: priority

daily-notes/ (22 incomplete):
  Expected: date, mood, energy

  daily-notes/2025-12-31.md - missing: mood, energy
  daily-notes/2025-12-30.md - missing: mood

COMPLETENESS SCORES:

  Folder          Complete    Incomplete    Score
  ─────────────────────────────────────────────────
  projects/           33          12         73%
  daily-notes/       343          22         94%
  tech/               45           0        100%
  work/               28           0        100%

SUGGESTIONS:
  Most impactful: Add "owner" to 8 project notes
  Quick win: Add "mood" to 15 daily notes

===============================================
```
