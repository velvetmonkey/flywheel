---
skill: schema-infer
---

# /schema-infer - Infer Metadata Conventions

Auto-detect metadata conventions for a folder based on existing patterns.

## Usage

```
/schema-infer                  # Analyze entire vault
/schema-infer projects/        # Analyze specific folder
```

## What It Does

```
Schema Inference
────────────────────────────────────────────────────────────────
Detected: 8 common fields with 85% confidence
────────────────────────────────────────────────────────────────
```

## Where Output Goes

| Action | Target | Notes |
|--------|--------|-------|
| Report | Console output | Inferred schema |
| Confidence | Console output | Pattern reliability |

## Example Output

```
Inferred Schema for projects/
===============================================

Analyzed 45 notes in projects/

DETECTED CONVENTIONS (85%+ confidence):

  Field       Type      Frequency   Common Values
  ─────────────────────────────────────────────────
  type        string    100%        "project" (always)
  status      string    95%         active, done, blocked
  priority    number    78%         1, 2, 3
  owner       string    89%         [[@person]] format
  tags        array     92%         ["work", "..."]

RECOMMENDED SCHEMA:

  type: string (required) - always "project"
  status: string (required) - enum: active|done|blocked
  priority: number (optional) - range: 1-3
  owner: string (recommended) - person reference
  tags: array (recommended) - topic tags

MISSING PATTERNS:
  12 notes (27%) missing "priority"
  5 notes (11%) missing "owner"

USE THIS SCHEMA:
  Run /schema-apply to enforce on folder

===============================================
```
