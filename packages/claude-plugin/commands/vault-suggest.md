---
skill: vault-suggest
---

# /vault-suggest - Suggest Wikilinks

Analyze text and suggest where wikilinks could be added.

## Usage

```
/vault-suggest Project.md            # Suggest links for note
/vault-suggest "text to analyze"     # Analyze provided text
```

## What It Does

```
Link Suggestions
────────────────────────────────────────────────────────────────
Found: 15 potential wikilinks to add
────────────────────────────────────────────────────────────────
```

## How It Works

Finds mentions of:
- Existing note titles
- Note aliases
- Known entities (people, projects, tech)

## Where Output Goes

| Action | Target | Notes |
|--------|--------|-------|
| Report | Console output | Suggested links |
| Quick fix | Console output | Bulk apply option |

## Example Output

```
Link Suggestions for [[Project Alpha]]
===============================================

Found 15 potential wikilinks

HIGH CONFIDENCE (exact title match):

1. Line 23: "discussed with John Smith"
   Suggestion: "discussed with [[John Smith]]"
   Match: Note "John Smith.md" exists

2. Line 45: "using the React framework"
   Suggestion: "using the [[React]] framework"
   Match: Note "React.md" exists

3. Line 67: "connects to Database service"
   Suggestion: "connects to [[Database]] service"
   Match: Note "Database.md" exists

MEDIUM CONFIDENCE (alias match):

4. Line 89: "the API endpoint"
   Suggestion: "the [[API Gateway|API]] endpoint"
   Match: "API" is alias for "API Gateway.md"

LOW CONFIDENCE (partial match):

5. Line 102: "authentication flow"
   Suggestion: "[[Authentication|authentication]] flow"
   Match: Similar to "Authentication.md"

SUMMARY:
  High confidence: 8
  Medium confidence: 4
  Low confidence: 3

QUICK FIX:
  Run /wikilink-apply to add all suggestions

===============================================
```
