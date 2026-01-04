# /folder-health - Vault Organization Analysis

Analyze vault folder structure and organization health.

## Usage

```
/folder-health                 # Full folder analysis
```

## What It Does

```
Folder Categories
────────────────────────────────────────────────────────────────
Empty (cleanup)     Overloaded (split)     Shallow (consolidate)
     5                    3                      25
────────────────────────────────────────────────────────────────
```

## Where Output Goes

| Action | Target | Notes |
|--------|--------|-------|
| Report | Console output | Folder health analysis |
| Suggestions | Console output | Organization recommendations |

## Process

1. **Scan** - Get folder structure from MCP
2. **Categorize** - Empty, overloaded, shallow, healthy
3. **Score** - Calculate organization health
4. **Recommend** - Suggest cleanup actions

## Example Output

```
Folder Health Report
===============================================

Total Folders: 100

CLEANUP CANDIDATES (5)
Empty folders with no notes or subfolders:
- old-projects/archive
- temp/scratch
Action: Review and delete if no longer needed

OVERLOADED FOLDERS (3)
Folders with 50+ notes (consider splitting):
- work/tickets (100+ notes)
- tech/tools (80 notes)

SHALLOW FOLDERS (25)
Folders with only 1-2 notes:
- tech/temp (1 note)
- projects/ideas (2 notes)

FOLDER DEPTH
Max depth: 4 levels (healthy)

SUMMARY
Healthy: 47 folders (47%)
Needs attention: 33 folders (33%)

===============================================
```
