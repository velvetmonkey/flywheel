---
skill: vault-common
---

# /vault-common - Find Common Neighbors

Find notes that both specified notes link to (shared connections).

## Usage

```
/vault-common [[Note A]] [[Note B]]  # Find common neighbors
```

## What It Does

```
Common Neighbors
────────────────────────────────────────────────────────────────
[[Note A]] and [[Note B]] share 8 common connections
────────────────────────────────────────────────────────────────
```

## Why It Matters

Common neighbors indicate:
- Shared context between notes
- Overlapping topics
- Potential for stronger connection
- Related knowledge areas

## Where Output Goes

| Action | Target | Notes |
|--------|--------|-------|
| Report | Console output | Shared connections |
| Insights | Console output | Relationship analysis |

## Example Output

```
Common Neighbors
===============================================

[[Project A]] and [[Project B]] share 8 connections

SHARED CONNECTIONS:

1. [[Technology X]] - both link here
   Project A: line 12 ("uses Technology X")
   Project B: line 34 ("built with Technology X")

2. [[Team Member]] - both link here
   Project A: line 8 ("owned by Team Member")
   Project B: line 15 ("Team Member contributed")

3. [[Architecture Doc]] - both link here
   Project A: line 45
   Project B: line 22

RELATIONSHIP ANALYSIS:

Shared topics: Technology, Team, Architecture
Connection strength: 8 shared (strong overlap)
Suggestion: Consider linking these projects directly

VENN DIAGRAM:

  [Project A only]     [Shared]     [Project B only]
       12 links    -->  8 links  <--   15 links

===============================================
```
