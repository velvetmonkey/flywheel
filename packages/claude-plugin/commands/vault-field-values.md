---
skill: vault-field-values
---

# /vault-field-values - List Unique Frontmatter Values

Get all unique values for a specific frontmatter field.

## Usage

```
/vault-field-values status           # All unique status values
/vault-field-values type             # All unique type values
/vault-field-values project          # All unique project values
```

## What It Does

```
Field Values
────────────────────────────────────────────────────────────────
Field "status" has 8 unique values across 234 notes
────────────────────────────────────────────────────────────────
```

## Where Output Goes

| Action | Target | Notes |
|--------|--------|-------|
| Report | Console output | Value distribution |
| Suggestions | Console output | Normalization opportunities |

## Example Output

```
Field Values: "status"
===============================================

8 unique values across 234 notes

VALUE DISTRIBUTION:

  Value          Count    Percentage
  ─────────────────────────────────────
  active           89       38%
  done             67       29%
  blocked          23       10%
  in-progress      21        9%
  planned          18        8%
  on-hold           8        3%
  cancelled         5        2%
  archived          3        1%

INSIGHTS:
  Most common: "active" (38%)
  Least common: "archived" (1%)

POTENTIAL ISSUES:
  "in-progress" vs "active" - similar meaning?
  Consider consolidating to reduce values

USAGE EXAMPLES:
  status: active
    → projects/Alpha.md
    → work/feature-x.md

  status: blocked
    → projects/Beta.md (blocked by infra)

===============================================
```
