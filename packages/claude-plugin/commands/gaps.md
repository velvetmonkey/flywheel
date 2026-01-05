---
skill: find-gaps
---

# /gaps - Find Knowledge Gaps

Find potential knowledge gaps in your vault based on link patterns.

## Usage

```
/gaps                          # Find all gaps
/gaps projects/                # Gaps in specific area
```

## What It Does

```
Knowledge Gap Analysis
────────────────────────────────────────────────────────────────
Found: 15 potential knowledge gaps
────────────────────────────────────────────────────────────────
```

## Types of Gaps

| Gap Type | Description |
|----------|-------------|
| Missing hub | Topic referenced but no central note |
| Broken bridge | Cluster with weak external links |
| Orphan cluster | Group of notes disconnected from rest |
| Dead-end topic | Area with no outgoing connections |

## Where Output Goes

| Action | Target | Notes |
|--------|--------|-------|
| Report | Console output | Gap analysis |
| Suggestions | Console output | Notes to create |

## Example Output

```
Knowledge Gaps Report
===============================================

Found 15 potential knowledge gaps

MISSING HUB NOTES:

1. "Machine Learning" - mentioned 23 times
   No central [[Machine Learning]] note exists
   Suggestion: Create hub note for this topic

2. "AWS Services" - mentioned 18 times
   No central [[AWS Services]] note
   Suggestion: Create index note

BROKEN BRIDGES:

3. Cluster "Frontend" <-> "Backend"
   Only 2 links between 45 notes
   Suggestion: Add integration docs

ORPHAN CLUSTERS:

4. "Old Project" cluster (8 notes)
   No links to current work
   Consider: Archive or reconnect

DEAD-END TOPICS:

5. "Security" area
   12 notes, 0 outgoing links
   Suggestion: Add implementation links

SUMMARY:
  Missing hubs: 5
  Broken bridges: 4
  Orphan clusters: 3
  Dead-end topics: 3

PRIORITY ACTIONS:
  1. Create [[Machine Learning]] hub
  2. Bridge Frontend <-> Backend
  3. Review Security documentation

===============================================
```
