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

## Mutations

When you ask Claude to make changes, here's what happens:

### Add a standup note

```
You: "/log turbopump test successful - 98% efficiency"

→ Modifies: daily-notes/2026-01-04.md

## Log
- 09:15 Team sync
- 14:47 turbopump test successful - 98% efficiency   ← ADDED
```

### Create a decision record

```
You: "record decision: switching to titanium valves"

→ Creates: decisions/DR-015-titanium-valves.md

# DR-015: Titanium Valves
Date: 2026-01-04
Status: Approved
Context: [[Turbopump Test Results]]
```

---

*65 notes. Just start asking questions.*
