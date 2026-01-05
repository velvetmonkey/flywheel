---
skill: vault-path
---

# /vault-path - Find Link Path Between Notes

Find the shortest connection path between any two notes.

## Usage

```
/vault-path [[Note A]] [[Note Z]]  # Find path between notes
/vault-path from.md to.md          # By file paths
```

## What It Does

```
Path Finding
────────────────────────────────────────────────────────────────
[[Note A]] ---> [[B]] ---> [[C]] ---> [[Note Z]]
           3 hops (indirect connection)
────────────────────────────────────────────────────────────────
```

## Path Interpretation

| Hops | Meaning |
|------|---------|
| 1 | Direct link (strong) |
| 2 | One intermediary (moderate) |
| 3-4 | Indirect connection |
| 5+ | Weak/distant |
| None | Disconnected (different islands) |

## Where Output Goes

| Action | Target | Notes |
|--------|--------|-------|
| Report | Console output | Path visualization |
| Suggestions | Console output | Connection improvements |

## Example Output

```
Link Path: [[Note A]] to [[Note Z]]
===============================================

Path Found (4 hops):

  [[Note A]]
       |
       v  (links via "See also")
  [[Note B]]
       |
       v  (links via "References")
  [[Note C]]
       |
       v  (links via "Technology used")
  [[Note Z]]

-------------------------------------------------

Summary:
  Path length: 4 hops
  Intermediate notes: 2
  Connection strength: Moderate (indirect)

Insights:
  Notes connect through [[Note B]] and [[Note C]]
  Consider direct link if frequently related

===============================================
```

**No Path Found:**

```
Link Path: [[Note A]] to [[Note Z]]
===============================================

No path found within 10 hops.

These notes are not connected.

Suggestions:
  They may be in different knowledge domains
  Consider if they should be connected
  Check if intermediate notes are missing

===============================================
```
