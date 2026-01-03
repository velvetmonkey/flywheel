# /normalize - Harmonize Frontmatter and Wikilinks

Synchronize a note's frontmatter and prose wikilinks so they reinforce each other.

## Usage

```
/normalize Project.md       # Normalize specific note
/normalize projects/        # Normalize all notes in folder
```

## What It Does

```
Before Normalization                After Normalization
────────────────────────────────────────────────────────────────
---                                 ---
type: project                       type: project
client: Acme Corp                   client: "[[Acme Corp]]"
status: active                      status: active
---                                 owner: "[[Ben Carter]]"
                                    ---
Lead: [[Ben Carter]]
Client: [[Acme Corp]]               Lead: [[Ben Carter]]
                                    Client: [[Acme Corp]]

(frontmatter has plain text)        (frontmatter has wikilinks)
(prose has wikilinks)               (prose patterns promoted)
```

## Where Output Goes

| Action | Target | Notes |
|--------|--------|-------|
| Frontmatter update | Same file (in-place edit) | Wikilinks added to values |
| Prose pattern promotion | Frontmatter section | Key: Value → YAML field |

## Process

1. **Analyze** - Read note's frontmatter and prose
2. **Detect Patterns** - Find Key: [[Value]] in prose
3. **Cross-Reference** - Compare frontmatter values to wikilinks
4. **Preview** - Show proposed changes
5. **Confirm** - User approves (Gate 4)
6. **Apply** - Update note

## Example Output

```
Normalize: projects/Alpha.md
============================

Changes Proposed:
─────────────────

Frontmatter Updates:
  client: "Acme Corp" → client: "[[Acme Corp]]"
  (found [[Acme Corp]] in prose, adding link to frontmatter)

Prose Pattern Promotion:
  "Lead: [[Ben Carter]]" → add `lead: "[[Ben Carter]]"` to frontmatter
  (prose pattern detected, promoting to structured data)

Apply changes? [y/n]
```
