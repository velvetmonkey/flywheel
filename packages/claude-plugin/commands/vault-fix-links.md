---
skill: vault-fix-links
---

# /vault-fix-links - Repair Broken Wikilinks

Find and repair broken wikilinks across your vault.

## Usage

```
/vault-fix-links                 # Scan entire vault
/vault-fix-links projects/       # Scan specific folder
/vault-fix-links Project.md      # Fix links in specific file
```

## What It Does

```
Broken Links Found              Suggested Fixes
────────────────────────────────────────────────────────────────
[[Proejct Alpha]]  ───────────► [[Project Alpha]]  (typo fix)
[[2025-01-15]]     ───────────► [[2025-12-15]]     (closest date)
[[Old Meeting]]    ───────────► [[Meeting Archive]] (renamed)
[[Deleted Note]]   ───────────► [removed]          (no match)
```

## Where Output Goes

| Action | Target | Notes |
|--------|--------|-------|
| Link repair | Same file (in-place edit) | Broken link replaced with fix |
| Removal | Same file (in-place edit) | Dead link text preserved, wikilink removed |
| Report | Console output | Summary of all changes |

## Process

1. **Scan** - Find all broken wikilinks
2. **Match** - Find closest existing notes
3. **Preview** - Show proposed fixes
4. **Confirm** - User approves changes (Gate 4)
5. **Apply** - Edit files with fixes

## Example Output

```
Broken Links Report
===================

Scanned: 147 notes
Found: 12 broken links

Proposed Fixes:
───────────────
projects/Alpha.md:
  [[Proejct Beta]] → [[Project Beta]] (typo, 1 char diff)
  [[Old Standup]] → [[Standups/2025-12-15]] (renamed)

daily-notes/2026-01-02.md:
  [[2025-13-01]] → [removed] (invalid date, no match)

Apply these fixes? [y/n]
```
