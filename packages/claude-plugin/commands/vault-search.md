---
skill: vault-search
---

# /vault-search - Advanced Vault Search

Search notes by frontmatter fields, tags, folders, or title.

## Usage

```
/vault-search type:project           # Find notes by field value
/vault-search #work                  # Find notes with tag
/vault-search projects/ status:active # Folder + field filter
/vault-search title:meeting          # Title contains "meeting"
```

## What It Does

```
Search Results
────────────────────────────────────────────────────────────────
Found: 45 notes matching criteria
────────────────────────────────────────────────────────────────
```

## Search Filters

| Filter | Example | Description |
|--------|---------|-------------|
| `field:value` | `status:active` | Frontmatter field |
| `#tag` | `#work` | Tag filter |
| `folder/` | `projects/` | Folder scope |
| `title:text` | `title:meeting` | Title contains |

## Where Output Goes

| Action | Target | Notes |
|--------|--------|-------|
| Report | Console output | Matching notes list |
| Summary | Console output | Result statistics |

## Example Output

```
Search Results
===============================================

Query: type:project status:active

Found 45 notes

RESULTS:

1. projects/Alpha.md
   type: project | status: active
   Modified: 2025-12-30

2. projects/Beta.md
   type: project | status: active
   Modified: 2025-12-28

3. work/initiatives/Gamma.md
   type: project | status: active
   Modified: 2025-12-25

... (42 more)

BY FOLDER:
  projects/: 30 notes
  work/: 12 notes
  other: 3 notes

BY MODIFIED DATE:
  This week: 15
  This month: 35
  Older: 10

===============================================
```
