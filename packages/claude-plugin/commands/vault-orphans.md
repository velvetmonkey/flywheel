---
skill: vault-orphans
---

# /vault-orphans - Find Disconnected Notes

Find orphan notes that have no backlinks (no other notes link to them).

## Usage

```
/vault-orphans                 # Find all orphans
/vault-orphans projects/       # Orphans in specific folder
```

## What It Does

```
Orphan Analysis
────────────────────────────────────────────────────────────────
Found: 250 orphan notes (25% of vault)
────────────────────────────────────────────────────────────────
```

## Where Output Goes

| Action | Target | Notes |
|--------|--------|-------|
| Report | Console output | Orphan list by category |
| Suggestions | Console output | Connection recommendations |

## Process

1. **Scan** - Find notes with zero backlinks
2. **Categorize** - Group by folder and age
3. **Prioritize** - Score by importance
4. **Report** - Show actionable list

## Example Output

```
Orphan Notes Report
===============================================

Found 250 orphan notes (25% of vault)
Total notes: 1,000

BREAKDOWN BY FOLDER:
  work/: 80 orphans (32%)
  tech/: 50 orphans (20%)
  daily-notes/: 40 orphans (16%)
  personal/: 30 orphans (12%)
  other: 50 orphans (20%)

BREAKDOWN BY AGE:
  Recent (<30 days): 20 (8%)
  Medium (30-90 days): 50 (20%)
  Old (90+ days): 180 (72%) - Needs attention

HIGH-PRIORITY ORPHANS:

  work/projects/data-platform.md
  Created: 2024-05-15
  Tags: #work #project
  CRITICAL: Major project with no links!

  tech/frameworks/new-tool.md
  Created: 2024-06-01
  Should connect to: [[Tech Stack]]

Options:
  1. Show full list
  2. Filter by folder/age
  3. Export for review

===============================================
```
