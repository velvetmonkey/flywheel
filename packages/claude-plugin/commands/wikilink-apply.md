# /wikilink-apply - Apply Wikilink Suggestions

Apply suggested wikilinks from /suggest to a note.

## Usage

```
/wikilink-apply Project.md     # Apply to specific note
```

## What It Does

```
Wikilink Application
────────────────────────────────────────────────────────────────
Applied: 12 new wikilinks to Project.md
────────────────────────────────────────────────────────────────
```

## Process

1. **Analyze** - Run /suggest analysis
2. **Preview** - Show all proposed links
3. **Select** - User picks which to apply
4. **Apply** - Edit note with new links

## Where Output Goes

| Action | Target | Notes |
|--------|--------|-------|
| Preview | Console output | Proposed changes |
| Edits | Note content | After confirmation |

## Example Output

```
Apply Wikilinks: [[Project Alpha]]
===============================================

Found 15 suggestions (12 high confidence)

HIGH CONFIDENCE (auto-apply):

  Line 23: "discussed with John Smith"
        --> "discussed with [[John Smith]]"

  Line 45: "using the React framework"
        --> "using the [[React]] framework"

  Line 67: "connects to Database service"
        --> "connects to [[Database]] service"

  ... (9 more)

MEDIUM CONFIDENCE (review):

  Line 89: "the API endpoint"
        --> "the [[API Gateway|API]] endpoint"
        Accept? [y/n/skip]

SUMMARY:
  High confidence: 12 (will apply)
  Medium confidence: 3 (ask each)

Proceed? [y/n]

-------------------------------------------------

Applied 14 wikilinks to Project Alpha.md

New backlinks created:
  [[John Smith]] +1
  [[React]] +1
  [[Database]] +1
  ...

===============================================
```
