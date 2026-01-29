# Artemis Rocket

> Your AI knows your entire rocket program and can answer anything about it.

---

**You are**: Chief Engineer at a 15-person aerospace startup

**Your situation**: Building a small launch vehicle to deliver 250kg to orbit. You're 8 months in, between design reviews, running hot fire tests. 65 documents cover propulsion, avionics, structures, team, and decisions.

## Try it now

Ask Claude:

- "What's the status of the propulsion system?"
- "What's causing the turbopump delay?"
- "Show me today's standup notes"
- "Who's responsible for avionics?"
- "What decisions led to our engine design?"

## What you'll discover

- Ask about any system and get instant context from connected documents
- Find what needs attention: disconnected notes, broken links, stale docs
- Add to your daily standup with a single sentence

---

## How mutations work

When you ask Claude to make changes:

### Add a standup note

```
You: "/log turbopump test successful - 98% efficiency"

┌─ MUTATION ───────────────────────────────────────┐
│ Reads:   ## Log section (42 tokens)              │
│ Appends: daily-notes/2026-01-04.md               │
└──────────────────────────────────────────────────┘

## Log
- 09:15 Team sync
- 14:47 turbopump test successful - 98% efficiency ← NEW
```

### Trace a blocker

```
You: "What's blocking propulsion?"

┌─ QUERY ──────────────────────────────────────────┐
│ Source: Graph index (no file reads)              │
│ Tokens: ~50 vs ~3,000 without Flywheel           │
└──────────────────────────────────────────────────┘

Claude traces the graph:
  [[Propulsion Milestone]] → blocked by → [[Turbopump Test]]
  [[Turbopump Test]] → waiting on → [[Seal Supplier]]
  [[Seal Supplier]] → status: delayed, ETA: Jan 18

Claude: "Propulsion is blocked by the turbopump test,
which is waiting on seals from Apex Materials.
Current ETA is Jan 18 - 14 days out."
```

### Create a decision record

```
You: "record decision: switching to titanium valves"

┌─ MUTATION ───────────────────────────────────────┐
│ Reads:   decisions/ folder conventions           │
│ Creates: decisions/DR-015-titanium-valves.md     │
└──────────────────────────────────────────────────┘

# DR-015: Titanium Valves
---
date: 2026-01-04
status: approved
context: "[[Turbopump Test Results]]"
---

Decision: Switching to titanium valves for improved
temperature tolerance based on hot fire results.
```

### Do a rollup

```
You: "do a rollup"

┌─ CHAIN ──────────────────────────────────────────┐
│ Reads:   7 daily notes, ## Log sections          │
│          (~700 tokens vs ~7,000 full files)      │
│ Creates: weekly-notes/2026-W01.md                │
│ Appends: Achievements.md                         │
└──────────────────────────────────────────────────┘

### weekly-notes/2026-W01.md (created)
## Week 1 Summary
- Turbopump hot fire: 98% efficiency achieved
- Seal supplier delay: pushed to Jan 18
- Decision: switching to titanium valves (DR-015)

## Achievements
- First successful turbopump hot fire test         ← NEW
```

---

*65 notes. Just start asking questions.*
