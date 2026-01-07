---
skill: vault-strength
---

# /vault-strength - Connection Strength Calculator

Calculate the connection strength between two notes.

## Usage

```
/vault-strength [[Note A]] [[Note B]]  # Calculate connection strength
```

## What It Does

```
Connection Strength
────────────────────────────────────────────────────────────────
[[Note A]] <--> [[Note B]]: 78% connection strength
────────────────────────────────────────────────────────────────
```

## Strength Factors

| Factor | Weight | Description |
|--------|--------|-------------|
| Direct link | 30% | One links to the other |
| Bidirectional | 25% | Both link to each other |
| Shared neighbors | 20% | Common connections |
| Same folder | 10% | Co-location |
| Same tags | 10% | Shared metadata |
| Edit proximity | 5% | Edited near same time |

## Where Output Goes

| Action | Target | Notes |
|--------|--------|-------|
| Report | Console output | Strength breakdown |
| Recommendations | Console output | How to strengthen |

## Example Output

```
Connection Strength Analysis
===============================================

[[Project A]] <--> [[Technology X]]

Overall Strength: 78% (Strong)

BREAKDOWN:

  Direct Link:        30/30  - A links to X
  Bidirectional:      25/25  - X links back to A
  Shared Neighbors:   15/20  - 6 common connections
  Same Folder:         0/10  - Different folders
  Same Tags:           5/10  - Share 2 of 4 tags
  Edit Proximity:      3/5   - Edited same week

FACTORS:
  Direct: Yes (A -> X)
  Bidirectional: Yes (X -> A)
  Common links: [[Database]], [[API]], [[Team]]...
  Shared tags: #work, #tech
  Last co-edited: 3 days ago

INTERPRETATION:
  Strong connection (78%)
  Well-integrated concepts
  No action needed

===============================================
```
