# /backlinks - Note Connection Navigator

Show all backlinks and forward links for a note.

## Usage

```
/backlinks Project.md          # Specific note
/backlinks [[My Project]]      # By wikilink name
/backlinks                     # Current context note
```

## What It Does

```
Connections Overview
────────────────────────────────────────────────────────────────
Backlinks: 50 notes      Forward Links: 20 notes      Mutual: 15
────────────────────────────────────────────────────────────────
```

## Where Output Goes

| Action | Target | Notes |
|--------|--------|-------|
| Report | Console output | Connection analysis |
| Insights | Console output | Relationship suggestions |

## Process

1. **Identify** - Detect target note from input
2. **Get backlinks** - Notes linking TO this note
3. **Get forward links** - Notes this note links TO
4. **Analyze** - Find bidirectional vs one-way connections
5. **Report** - Show connection patterns

## Example Output

```
Connections for [[MyProject]]
===============================================

Overview:
  Backlinks: 50 notes link here
  Forward Links: 20 notes linked from here
  Bidirectional: 15 mutual connections

BACKLINKS (Top 20):

Bidirectional (mutual):
  1. [[Related Project]] (line 23, 67)
     Strong connection (15 mutual refs)

  2. [[Technology Used]] (line 12)
     Mutual (10 refs each way)

One-way incoming:
  3. [[Planning Doc]] (line 5)
     Suggestion: Link back if relevant

FORWARD LINKS:

Bidirectional:
  1. [[Related Project]] - exists
  2. [[Technology Used]] - exists

Broken:
  3. [[Old Feature]] - BROKEN
     Run /fix-links to repair

===============================================
```
