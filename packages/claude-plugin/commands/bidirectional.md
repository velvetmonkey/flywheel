---
skill: check-bidirectional
---

# /bidirectional - Find Mutual Links

Find pairs of notes that link to each other (mutual/bidirectional links).

## Usage

```
/bidirectional                 # All mutual links in vault
/bidirectional Project.md      # Mutual links for specific note
```

## What It Does

```
Bidirectional Links
────────────────────────────────────────────────────────────────
Found: 234 mutual link pairs
────────────────────────────────────────────────────────────────
```

## Why It Matters

Bidirectional links indicate:
- Strong relationships between concepts
- Well-integrated knowledge
- Active topic connections
- Natural MOC candidates

## Where Output Goes

| Action | Target | Notes |
|--------|--------|-------|
| Report | Console output | Mutual link pairs |
| Strength scores | Console output | Connection quality |

## Example Output

```
Bidirectional Links Report
===============================================

Found 234 mutual link pairs

STRONGEST CONNECTIONS:

1. [[Project A]] <--> [[Technology X]]
   Forward: 12 refs | Back: 8 refs
   Strength: 95%

2. [[Main Hub]] <--> [[Core Concept]]
   Forward: 8 refs | Back: 6 refs
   Strength: 87%

3. [[Work Process]] <--> [[Tools]]
   Forward: 5 refs | Back: 5 refs
   Strength: 100% (perfectly balanced)

BY FOLDER:
  work/ <-> tech/: 45 pairs
  projects/ <-> tech/: 38 pairs
  personal/ <-> work/: 12 pairs

INSIGHTS:
  Strong bidirectional network
  Work and tech well-integrated
  Personal notes less connected

===============================================
```
