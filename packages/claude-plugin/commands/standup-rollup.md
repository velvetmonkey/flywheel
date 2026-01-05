---
skill: standup-rollup
---

# /standup-rollup - Aggregate Team Standups

Aggregate team standup notes into a summary.

## Usage

```
/standup-rollup                # Today's standups
/standup-rollup 2025-12-31     # Specific date
```

## What It Does

```
Standup Aggregation
────────────────────────────────────────────────────────────────
Aggregated: 5 team member standups
────────────────────────────────────────────────────────────────
```

## Where Output Goes

| Action | Target | Notes |
|--------|--------|-------|
| Summary | Console output | Team overview |
| Report | Optional file | Team standup summary |

## Example Output

```
Team Standup Summary: 2025-12-31
===============================================

TEAM MEMBERS (5/6 reported):

@John - Engineering
  Yesterday: Completed API integration
  Today: Starting frontend work
  Blockers: None

@Jane - Design
  Yesterday: Finished mockups
  Today: User testing
  Blockers: Waiting on feedback

@Bob - Backend
  Yesterday: Database optimization
  Today: Continue optimization
  Blockers: Need access to prod

BLOCKERS SUMMARY:
  1. @Bob needs prod access (owner: @DevOps)
  2. @Jane waiting on feedback (owner: @PM)

MISSING STANDUPS:
  @Alice - not submitted

TEAM FOCUS:
  Frontend: 2 people
  Backend: 2 people
  Design: 1 person

===============================================
```
