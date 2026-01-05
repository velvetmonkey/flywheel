---
skill: vault-hubs
---

# /vault-hubs - Find Hub Notes

Find highly connected notes that serve as central points in your knowledge graph.

## Usage

```
/vault-hubs                    # Find all hubs (5+ links)
/vault-hubs 20                 # Hubs with 20+ links
```

## What It Does

```
Hub Analysis
────────────────────────────────────────────────────────────────
Found: 156 hub notes (11% of vault)
Super: 3    Strong: 12    Medium: 45    Weak: 96
────────────────────────────────────────────────────────────────
```

## Hub Strength

| Strength | Links | Meaning |
|----------|-------|---------|
| Super | 100+ | Major knowledge centers |
| Strong | 50-99 | Important topic hubs |
| Medium | 20-49 | Active concepts |
| Weak | 5-19 | Moderate connection |

## Where Output Goes

| Action | Target | Notes |
|--------|--------|-------|
| Report | Console output | Hub list by strength |
| MOC candidates | Console output | Balanced hubs |

## Example Output

```
Hub Notes Report
===============================================

Found 156 hub notes (11% of vault)
Threshold: 5+ total links

TOP HUBS:

1. [[Daily Habit 1]] - 300+ links
   300 backlinks | 2 forward links
   Type: Habit (daily reference)
   Strength: SUPER

2. [[Main Project]] - 68 links
   45 backlinks | 23 forward links
   Type: Project (balanced hub)
   Strength: STRONG - Excellent MOC!

3. [[Core Technology]] - 56 links
   42 backlinks | 14 forward links
   Type: Technology (balanced)
   Strength: STRONG

BREAKDOWN BY TYPE:
  Habits: 3 (super hubs)
  Technologies: 34
  Projects: 18
  People: 23
  Concepts: 45

MOC CANDIDATES (balanced hubs):
  Main Project: 45 in / 23 out
  Core Tech: 34 in / 28 out

===============================================
```
