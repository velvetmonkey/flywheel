# Artemis Rocket

> Your AI knows your entire rocket program and can answer anything about it.

---

**You are**: Chief Engineer at a 15-person aerospace startup

**Your situation**: Building a small launch vehicle to deliver 250kg to orbit. You're 8 months in, between design reviews, running hot fire tests. 65 documents cover propulsion, avionics, structures, team, and decisions.

## Vault Map

```
┌─────────────────────────────────────────────────────────┐
│                    ARTEMIS ROCKET                       │
│                                                         │
│    ┌──────────────┐         ┌──────────────┐           │
│    │ Team Roster  │◄───────►│   Roadmap    │           │
│    └──────┬───────┘ staffs  └──────┬───────┘           │
│           │                        │ defines            │
│    owns   │    ┌───────────────────┘                   │
│           ▼    ▼                                        │
│    ┌─────────────────┐    ┌─────────────────┐          │
│    │   Propulsion    │───►│   Milestones    │          │
│    │     System      │    │                 │          │
│    └────────┬────────┘    └────────┬────────┘          │
│             │ depends-on           │ blocked-by        │
│             ▼                      ▼                   │
│    ┌─────────────────┐    ┌─────────────────┐          │
│    │   Decisions     │◄───│    Suppliers    │          │
│    │    (DR-###)     │    │                 │          │
│    └─────────────────┘    └─────────────────┘          │
└─────────────────────────────────────────────────────────┘
```

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

### Find all blockers

```
You: "What's blocking the launch?"

┌─ CHAIN ──────────────────────────────────────────┐
│ Queries: Milestones with status=blocked          │
│          Backlinks to find blocking dependencies │
│          Forward links to trace root causes      │
│          (~200 tokens vs ~5,000 full reads)      │
└──────────────────────────────────────────────────┘

Claude traces the dependency chain:
  [[Launch Milestone]] ← blocked by ← [[Propulsion Milestone]]
    ← blocked by ← [[Turbopump Test]] ← waiting on ← [[Seal Supplier]]

"Three blockers traced to root cause: Apex Materials seal delay (Jan 18 ETA)"
```

---

*65 notes. Just start asking questions.*

---

**Token savings:** Each note in this vault averages ~170 lines (~2,500 tokens).
With Flywheel, graph queries cost ~50-100 tokens instead of reading full files.
That's **25-50x savings** per query—enabling hundreds of queries in agentic workflows.
