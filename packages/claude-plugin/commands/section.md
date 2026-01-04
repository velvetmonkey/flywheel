# /section - Extract Section Content

Get the content under a specific heading in a note.

## Usage

```
/section Project.md "## Tasks"       # Get Tasks section
/section [[Note]] "Implementation"   # Get Implementation heading
```

## What It Does

```
Section Extraction
────────────────────────────────────────────────────────────────
Extracted "## Tasks" section from Project.md (45 lines)
────────────────────────────────────────────────────────────────
```

## Section Matching

- Matches heading text (case-insensitive)
- Includes content until next same-level heading
- Can include or exclude subheadings

## Where Output Goes

| Action | Target | Notes |
|--------|--------|-------|
| Content | Console output | Section text |
| Metadata | Console output | Line count, subheadings |

## Example Output

```
Section: "## Tasks" from [[Project Alpha]]
===============================================

## Tasks

### Completed
- [x] Initial setup
- [x] Database schema
- [x] API endpoints

### In Progress
- [ ] Frontend UI
- [ ] Testing suite

### Blocked
- [ ] Deployment (waiting on infra)

-------------------------------------------------

Section Info:
  Lines: 45
  Subheadings: 3
  Tasks: 6 total (3 complete, 2 in progress, 1 blocked)

===============================================
```
