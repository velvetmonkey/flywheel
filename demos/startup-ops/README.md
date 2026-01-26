# Startup Ops

> Let AI handle operations while you focus on building the product.

---

**You are**: Co-founder of MetricFlow, a B2B SaaS analytics startup

**Your situation**: Pre-Series A with 3 customers and 2 co-founders doing everything. You need to run ops (onboarding, support, metrics, investor updates) without hiring yet. You've got playbooks, customer records, and decisions scattered across 30 notes.

## Try it now

Ask Claude:

- "Walk me through onboarding a new customer"
- "What's our current MRR?"
- "What decisions need my review this week?"
- "Show me the support escalation process"
- "Summarize what happened with DataDriven Co"

## What you'll discover

- Run operational playbooks step-by-step with AI guidance
- Keep customer, product, and finance information connected
- Separate routine ops from strategic decisions that need your brain

---

## How mutations work

When you ask Claude to make changes:

### Log a customer interaction

```
You: "/log call with DataDriven - they want API access"

┌─ MUTATION ───────────────────────────────────────┐
│ Reads:   ## Log section (38 tokens)              │
│ Appends: daily-notes/2026-01-04.md               │
└──────────────────────────────────────────────────┘

## Log
- 10:00 Standup with Sarah
- 11:30 call with DataDriven - they want API access ← NEW
```

### Check MRR

```
You: "What's our current MRR?"

┌─ QUERY ──────────────────────────────────────────┐
│ Source: Graph index (customer frontmatter)       │
│ Tokens: ~40 vs ~1,500 without Flywheel           │
└──────────────────────────────────────────────────┘

MRR Dashboard
=============
Active Customers: 3
Total MRR: $4,200/mo

Breakdown:
- DataDriven Co: $1,500/mo (pilot → paid)
- TechStart Inc: $1,200/mo (annual contract)
- Metrics Plus: $1,500/mo (monthly)

Pipeline: $3,800/mo (2 in trial)
```

### Update customer record

```
You: "update DataDriven status to pilot"

┌─ MUTATION ───────────────────────────────────────┐
│ Reads:   customers/datadriven-co.md frontmatter  │
│ Modifies: customers/datadriven-co.md             │
└──────────────────────────────────────────────────┘

---
status: pilot                                      ← CHANGED from 'lead'
last_contact: 2026-01-04
mrr: 1500
---
```

### Run a playbook

```
You: "Walk me through onboarding a new customer"

┌─ QUERY ──────────────────────────────────────────┐
│ Source: playbooks/customer-onboarding.md         │
│ Tokens: ~200 (playbook only)                     │
└──────────────────────────────────────────────────┘

Customer Onboarding Playbook
============================

Step 1: Create customer record
  → /create customer [name]

Step 2: Schedule kickoff call
  → Check calendar availability

Step 3: Send welcome email
  → Template: templates/welcome-email.md

Step 4: Set up their workspace
  → Provision API keys
  → Create Slack channel

Step 5: Log completion
  → /log onboarded [customer name]

Ready to start? Tell me the customer name.
```

---

*30 notes. Just start asking questions.*
