---
skill: vault-stale
---

# /vault-stale - Find Neglected Notes

Find important notes (by backlink count) that haven't been modified recently.

## Usage

```
/vault-stale                         # Stale notes (90+ days old)
/vault-stale 30                      # Stale for 30+ days
```

## What It Does

```
Stale Notes Analysis
────────────────────────────────────────────────────────────────
Found: 45 important notes not updated in 90+ days
────────────────────────────────────────────────────────────────
```

## Why It Matters

Stale notes that are frequently referenced:
- May contain outdated information
- Need review and updates
- Could mislead if outdated
- Priority for maintenance

## Where Output Goes

| Action | Target | Notes |
|--------|--------|-------|
| Report | Console output | Stale note list |
| Priority | Console output | By backlink importance |

## Example Output

```
Stale Notes Report
===============================================

Found 45 important notes not updated in 90+ days

CRITICAL (high backlinks, very stale):

1. [[Process Doc]] - 156 backlinks
   Last modified: 2024-06-15 (180 days ago)
   URGENT: Highly referenced but outdated!

2. [[Tech Standards]] - 89 backlinks
   Last modified: 2024-07-01 (165 days ago)
   May need review

3. [[Team Structure]] - 67 backlinks
   Last modified: 2024-08-15 (120 days ago)
   Check if still accurate

MEDIUM PRIORITY (moderate backlinks):
  [[Old Project]] - 34 backlinks, 95 days
  [[Architecture]] - 28 backlinks, 92 days
  [[Onboarding]] - 23 backlinks, 100 days

BY FOLDER:
  work/: 20 stale notes
  tech/: 15 stale notes
  docs/: 10 stale notes

RECOMMENDATIONS:
  Review [[Process Doc]] immediately
  Schedule tech docs review
  Archive if truly obsolete

===============================================
```
