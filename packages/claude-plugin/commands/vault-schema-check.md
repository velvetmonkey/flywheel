---
skill: vault-schema-check
---

# /vault-schema-check - Frontmatter Type Consistency

Find frontmatter fields with inconsistent types (schema violations).

## Usage

```
/vault-schema-check            # Check for type mismatches
```

## What It Does

```
Type Inconsistencies Found
────────────────────────────────────────────────────────────────
Field       Expected    Violations    Example
tags        array       12 notes      tags: "work" (should be array)
priority    number       5 notes      priority: "high" (should be 1)
────────────────────────────────────────────────────────────────
```

## Where Output Goes

| Action | Target | Notes |
|--------|--------|-------|
| Report | Console output | Inconsistencies found |
| Fix suggestions | Console output | How to correct each |

## Process

1. **Scan** - Analyze field types across vault
2. **Detect** - Find mixed types for same field
3. **Report** - Show violations with examples
4. **Suggest** - Provide fix recommendations

## Example Output

```
Frontmatter Schema Check
===============================================

Found 3 fields with type inconsistencies

-------------------------------------------------

Field: tags
  Expected: array (majority usage)
  Inconsistencies: 12 notes

  Type Distribution:
    array:   89 notes (88%)  Expected
    string:  12 notes (12%)  Should be array

  Example violations:
    - daily-notes/2025-12-15.md: tags: "work"
    - projects/alpha.md: tags: "project, active"

  Fix suggestion:
    Convert string values to arrays:
    tags: "work" --> tags: ["work"]

-------------------------------------------------

Field: priority
  Expected: number (majority usage)
  Inconsistencies: 5 notes

  Example violations:
    - tasks/review.md: priority: "high"

  Fix suggestion:
    Convert to numeric values:
    priority: "high" --> priority: 1

-------------------------------------------------

Summary:
  Total fields checked: 15
  Fields with issues: 3
  Notes affected: 19

===============================================
```
