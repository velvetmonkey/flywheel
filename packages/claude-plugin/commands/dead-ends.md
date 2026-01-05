---
skill: find-dead-ends
---

# /dead-ends - Find Notes With No Outgoing Links

Find notes that have backlinks but no outgoing links (consume but don't contribute).

## Usage

```
/dead-ends                     # Find all dead-end notes
/dead-ends projects/           # Dead-ends in folder
```

## What It Does

```
Dead-End Analysis
────────────────────────────────────────────────────────────────
Found: 45 dead-end notes (referenced but don't link out)
────────────────────────────────────────────────────────────────
```

## Why It Matters

Dead-end notes:
- Receive links but don't link elsewhere
- Break knowledge flow
- May need expansion or context
- Could be "leaf" concepts or incomplete notes

## Where Output Goes

| Action | Target | Notes |
|--------|--------|-------|
| Report | Console output | Dead-end list |
| Suggestions | Console output | Link opportunities |

## Example Output

```
Dead-End Notes Report
===============================================

Found 45 notes with backlinks but no forward links

HIGH-TRAFFIC DEAD-ENDS:

1. [[Person Name]] - 67 backlinks, 0 forward links
   Type: Person note (expected)
   Suggestion: Add links to projects they work on

2. [[Core Concept]] - 34 backlinks, 0 forward links
   Type: Concept (should link out!)
   Suggestion: Add related concepts, examples

3. [[Old Project]] - 23 backlinks, 0 forward links
   Type: Archived (acceptable)
   Status: Archived content

BY CATEGORY:
  People notes: 23 (expected behavior)
  Concepts: 12 (should improve)
  Archived: 8 (acceptable)
  Incomplete: 2 (needs attention)

RECOMMENDATIONS:
  Focus on 12 concept dead-ends
  Add outgoing links to connect knowledge
  People notes can remain as endpoints

===============================================
```
