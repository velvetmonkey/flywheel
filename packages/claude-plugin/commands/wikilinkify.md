# /wikilinkify - Convert Frontmatter to Wikilinks

Find frontmatter string values that match existing notes and suggest converting to wikilinks.

## Usage

```
/wikilinkify Project.md        # Check specific note
/wikilinkify projects/         # Check folder
```

## What It Does

```
Wikilink Suggestions
────────────────────────────────────────────────────────────────
Found: 8 frontmatter values that should be [[wikilinks]]
────────────────────────────────────────────────────────────────
```

## Why It Matters

Frontmatter like `owner: John Smith` should be `owner: "[[John Smith]]"` to:
- Create backlinks
- Enable graph navigation
- Keep relationships queryable

## Where Output Goes

| Action | Target | Notes |
|--------|--------|-------|
| Report | Console output | Conversion suggestions |
| Edits | Frontmatter | After confirmation |

## Example Output

```
Wikilinkify: [[Project Alpha]]
===============================================

Found 4 frontmatter values to convert

SUGGESTIONS:

1. owner: "John Smith"
   Match: John Smith.md exists
   Convert to: owner: "[[John Smith]]"

2. tech_lead: "Jane Doe"
   Match: Jane Doe.md exists
   Convert to: tech_lead: "[[Jane Doe]]"

3. project: "Main Initiative"
   Match: Main Initiative.md exists
   Convert to: project: "[[Main Initiative]]"

4. team: "Engineering"
   Match: Engineering.md exists
   Convert to: team: "[[Engineering]]"

BEFORE:
  owner: John Smith
  tech_lead: Jane Doe
  project: Main Initiative

AFTER:
  owner: "[[John Smith]]"
  tech_lead: "[[Jane Doe]]"
  project: "[[Main Initiative]]"

Apply conversions? [y/n]

===============================================
```
