# Carter Strategy

> Run a solo consulting practice with an AI back-office that never drops the ball.

---

**You are**: A solo strategy consultant

**Your situation**: You manage 3 clients, 4 active projects, $42K in pending invoices, and 15 open tasks. Your expertise is data strategy and API architecture. Your challenge is keeping everything organized without an assistant.

## Try it now

Ask Claude:

- "What's overdue this week?"
- "How much have I billed Acme Corp?"
- "Summarize my December"
- "What client work needs follow-up?"
- "Show me my active projects"

## What you'll discover

- See all your deadlines in one place - no more forgotten follow-ups
- Track client revenue and project budgets automatically
- Summarize your week or month instantly for planning

---

## How mutations work

When you ask Claude to make changes:

### Add a log entry

```
You: "/log finished Acme strategy deck"

┌─ MUTATION ───────────────────────────────────────┐
│ Reads:   ## Log section (35 tokens)              │
│ Appends: daily-notes/2026-01-04.md               │
└──────────────────────────────────────────────────┘

## Log
- 10:15 Morning review
- 14:32 finished Acme strategy deck                ← NEW
```

### Check what's overdue

```
You: "What's overdue this week?"

┌─ QUERY ──────────────────────────────────────────┐
│ Source: Task index (no file reads)               │
│ Tokens: ~60 vs ~2,000 without Flywheel           │
└──────────────────────────────────────────────────┘

Overdue Tasks (3):
- clients/acme.md: Follow up on proposal 📅 Jan 2
- projects/beta-api.md: Send status update 📅 Jan 3
- invoices/INV-042.md: Payment reminder 📅 Jan 3
```

### Do a rollup

```
You: "do a rollup"

┌─ CHAIN ──────────────────────────────────────────┐
│ Reads:   7 daily notes, ## Log sections          │
│          (~500 tokens vs ~5,000 full files)      │
│ Creates: weekly-notes/2026-W01.md                │
│ Appends: monthly-notes/2026-01.md                │
└──────────────────────────────────────────────────┘

### weekly-notes/2026-W01.md (created)
## Week 1 Summary
- Completed Acme strategy deck
- 3 client calls
- $12K invoiced
```

### Check client revenue

```
You: "How much have I billed Acme Corp?"

┌─ QUERY ──────────────────────────────────────────┐
│ Source: Graph index (frontmatter + links)        │
│ Tokens: ~40 vs ~1,200 without Flywheel           │
└──────────────────────────────────────────────────┘

Acme Corp Revenue
=================
Total Billed: $28,400
Paid: $16,200
Outstanding: $12,200

Projects:
- Data Strategy Phase 1: $16,200 (paid)
- API Architecture: $12,200 (pending)
```

---

*30 notes. Just start asking questions.*
