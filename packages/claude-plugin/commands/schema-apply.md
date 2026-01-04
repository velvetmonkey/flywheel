# /schema-apply - Apply Inferred Conventions

Apply inferred schema conventions to notes in a folder.

## Usage

```
/schema-apply projects/        # Apply to projects folder
```

## What It Does

```
Schema Application
────────────────────────────────────────────────────────────────
Applied conventions to 12 notes (preview mode)
────────────────────────────────────────────────────────────────
```

## Process

1. **Infer** - Detect folder conventions
2. **Preview** - Show proposed changes
3. **Confirm** - User approves
4. **Apply** - Add missing fields

## Where Output Goes

| Action | Target | Notes |
|--------|--------|-------|
| Preview | Console output | Proposed changes |
| Edits | Note files | After confirmation |

## Example Output

```
Schema Application Preview
===============================================

Folder: projects/
Inferred schema: type, status, priority, owner

PROPOSED CHANGES (12 notes):

1. projects/Alpha.md
   Add: priority: 2 (suggested from similar notes)
   Add: owner: (needs input)

2. projects/Beta.md
   Add: owner: (needs input)

3. projects/Gamma.md
   Add: priority: 3 (suggested)

-------------------------------------------------

Summary:
  Notes to update: 12
  Fields to add: 15
  Fields needing input: 3

Proceed with changes? [y/n]

(Fields needing input will prompt for values)

===============================================
```
