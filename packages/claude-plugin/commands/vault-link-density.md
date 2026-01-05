---
skill: vault-link-density
---

# /vault-link-density - Link Pattern Analysis

Analyze linking patterns and density across your vault.

## Usage

```
/vault-link-density            # Full link analysis
```

## What It Does

```
Link Density Analysis
────────────────────────────────────────────────────────────────
Total Links: 15,000    Avg Density: 15 links/note    Status: Good
────────────────────────────────────────────────────────────────
```

## Optimal Ranges

| Density | Status | Meaning |
|---------|--------|---------|
| 10-20 links/note | Optimal | Well-connected graph |
| 5-10 links/note | Moderate | Room for improvement |
| <5 links/note | Low | Isolated knowledge |
| >20 links/note | High | May need restructuring |

## Where Output Goes

| Action | Target | Notes |
|--------|--------|-------|
| Report | Console output | Density analysis |
| Outliers | Console output | Over/under-linked notes |

## Process

1. **Calculate** - Get link counts from MCP
2. **Analyze** - Density by folder
3. **Find outliers** - Over and under-linked notes
4. **Recommend** - Suggest improvements

## Example Output

```
Link Density Analysis
===============================================

Vault Overview:
  Total Notes: 1,000
  Total Links: 15,000
  Average Density: 15 links/note
  Status: Well-connected

Density by Folder:
  work/projects/ - 22 links/note (high)
  tech/ - 18 links/note (optimal)
  personal/ - 8 links/note (moderate)
  templates/ - 2 links/note (low, expected)

Over-Linked Notes (>40 links):
  [[Main Hub]] - 127 links (consider splitting)
  [[Core Tech]] - 89 links (central hub)
  [[Key Project]] - 76 links (central hub)

Under-Linked Notes (<3 links):
  150 notes (15% of vault)
  Mostly in: personal/, daily-notes/

Insights:
  Work projects are well-integrated
  Personal notes could use more connections
  Consider splitting [[Main Hub]] into sub-topics

===============================================
```
