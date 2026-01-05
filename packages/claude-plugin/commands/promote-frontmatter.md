---
skill: promote-frontmatter
---

# /promote-frontmatter - Extract Prose Patterns to YAML

Find "Key: Value" patterns in note prose and suggest promoting to frontmatter.

## Usage

```
/promote-frontmatter Project.md   # Analyze specific note
```

## What It Does

```
Prose Pattern Detection
────────────────────────────────────────────────────────────────
Found: 5 key-value patterns in prose to promote to frontmatter
────────────────────────────────────────────────────────────────
```

## Pattern Detection

Finds patterns like:
- `Owner: John Smith`
- `Status: Active`
- `Due: 2025-01-15`
- `Priority: High`

## Where Output Goes

| Action | Target | Notes |
|--------|--------|-------|
| Report | Console output | Detected patterns |
| Edits | Frontmatter | After confirmation |

## Example Output

```
Promote Frontmatter: [[Project Alpha]]
===============================================

Found 5 prose patterns to promote

DETECTED PATTERNS:

1. Line 12: "Owner: John Smith"
   Promote to: owner: "[[John Smith]]"

2. Line 15: "Status: Active"
   Promote to: status: active

3. Line 18: "Due Date: 2025-02-15"
   Promote to: due: 2025-02-15

4. Line 23: "Priority: High"
   Promote to: priority: 1

5. Line 28: "Team: Engineering"
   Promote to: team: "[[Engineering]]"

CURRENT FRONTMATTER:
  type: project

PROPOSED FRONTMATTER:
  type: project
  owner: "[[John Smith]]"
  status: active
  due: 2025-02-15
  priority: 1
  team: "[[Engineering]]"

PROSE CLEANUP:
  Remove promoted lines from prose? [y/n]

Apply changes? [y/n]

===============================================
```
