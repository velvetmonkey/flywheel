# /related - Find Related Notes

Find notes that are related to a specific note based on shared connections.

## Usage

```
/related Project.md            # Notes related to Project
/related [[My Note]]           # By wikilink name
```

## What It Does

```
Related Notes Analysis
────────────────────────────────────────────────────────────────
Found: 25 related notes (by shared connections)
────────────────────────────────────────────────────────────────
```

## How Relatedness is Determined

Notes are related when they:
- Share common backlinks (same notes link to both)
- Share common forward links (both link to same notes)
- Are in the same clusters
- Have similar tags/frontmatter

## Where Output Goes

| Action | Target | Notes |
|--------|--------|-------|
| Report | Console output | Related notes list |
| Scores | Console output | Relatedness strength |

## Example Output

```
Related Notes for [[My Project]]
===============================================

Found 25 related notes

MOST RELATED:

1. [[Similar Project]] - 85% related
   Shared: [[Tech A]], [[Person X]], [[Process Y]]
   Same cluster: "Work Projects"

2. [[Tech Stack]] - 72% related
   Shared: [[Framework]], [[Database]]
   Same tags: #work, #tech

3. [[Team Member]] - 65% related
   Shared: [[Project]], [[Meeting Notes]]
   Direct connection exists

GROUPED BY RELATIONSHIP:

Same Project Cluster:
  [[Related Feature]], [[Sprint Planning]]

Shared Technology:
  [[Other Tech Project]], [[Architecture]]

Same Author/Context:
  [[Weekly Review]], [[Goals]]

SUGGESTIONS:
  Consider linking to [[Similar Project]]
  May want to explore [[Tech Stack]] connection

===============================================
```
