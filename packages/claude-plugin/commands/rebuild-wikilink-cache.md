---
skill: rebuild-wikilink-cache
---

# /rebuild-wikilink-cache - Rebuild Wikilink Cache

Rebuild the Flywheel entity cache for wikilink resolution.

## Usage

```
/rebuild-wikilink-cache                 # Rebuild entire cache
```

## What It Does

```
Cache Rebuild
────────────────────────────────────────────────────────────────
Rebuilding entity cache for 1,000 notes...
────────────────────────────────────────────────────────────────
```

## When to Use

- After bulk note imports
- When wikilink suggestions seem stale
- After renaming many notes
- If link resolution fails

## Where Output Goes

| Action | Target | Notes |
|--------|--------|-------|
| Status | Console output | Rebuild progress |
| Cache | MCP server | Updated index |

## Example Output

```
Cache Rebuild
===============================================

Rebuilding Flywheel entity cache...

PROGRESS:
  Scanning notes...     [========] 100%
  Indexing titles...    [========] 100%
  Indexing aliases...   [========] 100%
  Building graph...     [========] 100%

RESULTS:
  Notes indexed: 1,000
  Titles cached: 1,000
  Aliases cached: 234
  Links indexed: 15,000

CACHE STATS:
  Previous: 950 notes (outdated)
  Current: 1,000 notes (fresh)
  Added: 50 new notes
  Updated: 23 modified notes

Cache rebuild complete!

Next refresh will be automatic.

===============================================
```
