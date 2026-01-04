# /schema-migrate - Rename Fields in Bulk

Bulk rename a frontmatter field across notes (dry-run by default).

## Usage

```
/schema-migrate old_name new_name      # Preview rename
/schema-migrate old_name new_name --apply  # Apply changes
```

## What It Does

```
Field Migration
────────────────────────────────────────────────────────────────
Preview: Rename "status" to "state" in 234 notes
────────────────────────────────────────────────────────────────
```

## Process

1. **Scan** - Find notes with old field name
2. **Check** - Detect conflicts (new name already exists)
3. **Preview** - Show proposed changes
4. **Apply** - Rename after confirmation

## Where Output Goes

| Action | Target | Notes |
|--------|--------|-------|
| Preview | Console output | Migration plan |
| Edits | Note files | After --apply |

## Example Output

```
Field Migration Preview
===============================================

Rename: "category" --> "type"

AFFECTED NOTES (234):

  projects/Alpha.md
    Before: category: project
    After:  type: project

  work/tasks/task-1.md
    Before: category: task
    After:  type: task

CONFLICTS (3 notes have both fields):

  work/old-note.md
    Has: category: task, type: item
    CONFLICT: Cannot merge automatically
    Action: Skip or manual review

SUMMARY:
  Notes to update: 231
  Conflicts: 3 (will skip)
  Safe to migrate: 231

Run with --apply to execute migration

===============================================
```
