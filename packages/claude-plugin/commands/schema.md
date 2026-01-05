---
skill: show-schema
---

# /schema - Frontmatter Schema Analysis

Analyze all frontmatter fields used across your vault.

## Usage

```
/schema                        # Show all metadata fields
```

## What It Does

```
Field Overview
────────────────────────────────────────────────────────────────
Field         Type        Usage     Most Common Values
type          string       234      "project", "note", "person"
status        string       156      "active", "done", "blocked"
tags          array         89      ["work"], ["personal"]
────────────────────────────────────────────────────────────────
```

## Where Output Goes

| Action | Target | Notes |
|--------|--------|-------|
| Report | Console output | Schema overview |
| Field stats | Console output | Usage patterns |

## Process

1. **Scan** - Analyze frontmatter across vault
2. **Identify** - List all unique fields
3. **Categorize** - Show types and usage counts
4. **Report** - Most common values per field

## Example Output

```
Frontmatter Schema Analysis
===============================================

Total Fields: 15 unique fields across vault

Field Overview:
-------------------------------------------------

  Field         Type(s)        Usage    Notes
  ------------------------------------------------
  type          string         234      Most common: "project"
  status        string         156      Most common: "active"
  date          string         342      Format: YYYY-MM-DD
  tags          array          89       Avg 3 tags per note
  priority      number         23       Range: 1-5

Type Distribution:
  string:  10 fields (67%)
  array:   3 fields (20%)
  number:  1 field (7%)
  boolean: 1 field (7%)

Top 5 Most Used Fields:
  1. date (342 notes)
  2. type (234 notes)
  3. status (156 notes)
  4. tags (89 notes)
  5. project (78 notes)

===============================================
```
