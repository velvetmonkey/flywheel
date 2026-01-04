# /unlinked-mentions - Find Unlinked Mentions

Find places where a note title is mentioned in text but not linked.

## Usage

```
/unlinked-mentions [[Project]] # Find unlinked mentions of Project
/unlinked-mentions "John"      # Search for name mentions
```

## What It Does

```
Unlinked Mentions
────────────────────────────────────────────────────────────────
Found: 23 mentions of "Project Alpha" not wrapped in [[wikilinks]]
────────────────────────────────────────────────────────────────
```

## Why It Matters

Unlinked mentions:
- Missed connection opportunities
- Weaken your knowledge graph
- Make discovery harder
- Should probably be wikilinks

## Where Output Goes

| Action | Target | Notes |
|--------|--------|-------|
| Report | Console output | Mention locations |
| Fix suggestions | Console output | Wikilink conversions |

## Example Output

```
Unlinked Mentions: [[Project Alpha]]
===============================================

Found 23 unlinked mentions

MENTIONS BY FILE:

1. daily-notes/2025-12-15.md (line 23)
   "...discussed Project Alpha with team..."
   Should be: "...discussed [[Project Alpha]]..."

2. work/meetings/standup.md (line 45)
   "...Project Alpha blockers include..."
   Should be: "...[[Project Alpha]] blockers..."

3. tech/decisions.md (line 12)
   "...for Project Alpha we chose..."
   Should be: "...for [[Project Alpha]]..."

SUMMARY:
  Files with mentions: 15
  Total mentions: 23
  Converting would add 23 new backlinks

QUICK FIX:
  Run /wikilink-apply to convert all mentions

===============================================
```
