---
skill: vault-find-sections
---

# /vault-find-sections - Find Sections By Pattern

Find all sections across vault matching a heading pattern.

## Usage

```
/vault-find-sections "Tasks"         # Find all ## Tasks sections
/vault-find-sections "TODO"          # Find TODO headings
/vault-find-sections "^Meeting"      # Regex: headings starting with Meeting
```

## What It Does

```
Section Search
────────────────────────────────────────────────────────────────
Found: 156 sections matching "Tasks" across 89 notes
────────────────────────────────────────────────────────────────
```

## Pattern Types

| Pattern | Example | Matches |
|---------|---------|---------|
| Plain text | `Tasks` | Any heading containing "Tasks" |
| Regex | `^Meeting` | Headings starting with "Meeting" |
| Exact | `"## Tasks"` | Exact heading match |

## Where Output Goes

| Action | Target | Notes |
|--------|--------|-------|
| Report | Console output | Section locations |
| Summary | Console output | Pattern statistics |

## Example Output

```
Sections Matching: "Tasks"
===============================================

Found 156 sections in 89 notes

BY FOLDER:

projects/ (45 sections):
  projects/Alpha.md - ## Tasks (line 23)
  projects/Beta.md - ## Tasks (line 18)
  projects/Gamma.md - ### Current Tasks (line 45)

daily-notes/ (89 sections):
  daily-notes/2025-12-31.md - ## Tasks (line 5)
  daily-notes/2025-12-30.md - ## Tasks (line 5)
  ...

work/ (22 sections):
  work/sprints/current.md - ## Sprint Tasks (line 12)
  work/meetings/standup.md - ### Tasks Discussed (line 34)

HEADING VARIATIONS:
  "## Tasks": 78 occurrences
  "### Tasks": 34 occurrences
  "## Current Tasks": 23 occurrences
  "### Task List": 12 occurrences
  Other: 9 occurrences

===============================================
```
