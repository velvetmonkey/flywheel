# Flywheel - What if your notes could run your business?

[![npm version](https://img.shields.io/npm/v/@bencassie/flywheel-mcp.svg)](https://www.npmjs.com/package/@bencassie/flywheel-mcp)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-blue.svg)](https://github.com/bencassie/flywheel)

**Claude Code + Flywheel plugin.**

---

## How It Works

```
┌─────────────────────────────────────────┐
│  YOU (thinking, deciding, creating)     │
├─────────────────────────────────────────┤
│  CLAUDE CODE (AI co-processor)          │  ← THE PRODUCT
│  - Spins off the monotony               │
│  - Gives you the good stuff             │
│  - Handles ops while you create         │
├─────────────────────────────────────────┤
│  FLYWHEEL (graph intelligence)          │  ← Makes Claude smarter
│  - 40+ management tools                 │
│  - Auto-curation hooks                  │
│  - Token-efficient queries              │
├─────────────────────────────────────────┤
│  YOUR VAULT (plain markdown)            │
│  - Edit with any tool you want          │
│  - Obsidian, VSCode, vim, whatever      │
│  - Git-versioned, future-proof          │
└─────────────────────────────────────────┘
```

You're a solo operator — consultant, founder, freelancer, creator.
Your notes ARE your business. Claude Code is your AI co-processor.

Flywheel gives Claude graph intelligence about your vault:
- AI understands how your notes connect (no manual tagging)
- Log your work once, AI keeps everything updated
- Daily notes roll up into weekly → monthly → quarterly summaries
- Track projects, clients, revenue — all in plain text

No SaaS lock-in. No code. Just you + Claude + markdown.

---

## The Flywheel Loop: Your Notes Get Smarter

Most note-taking: you write, you organize, you forget.

With Flywheel, your knowledge base **improves itself**:

```
┌────────────────────────────────────────────────────────────────┐
│                     THE FLYWHEEL LOOP                          │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  WIKILINKS ←──────────────────────────────→ FRONTMATTER        │
│  [[Acme Corp]]                              status: active     │
│  [[Sarah Chen]]                             contact: Sarah     │
│                                             rate: $250/hr      │
│         ↑                                          ↑           │
│         │         AUTO-CURATION HOOKS              │           │
│         │    ┌──────────────────────────┐          │           │
│         └────│ wikilink-auto.py         │──────────┘           │
│              │ frontmatter-auto.py      │                      │
│              └──────────────────────────┘                      │
│                         ↓                                      │
│         After every Edit/Write, hooks auto-apply:              │
│         ✓ Wikilinks to known entities                          │
│         ✓ Frontmatter from folder patterns                     │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

**How it works:**

1. **You write naturally — AI adds links automatically**
   - Mention "Acme Corp" in your daily note
   - Flywheel detects it matches an existing note
   - `✓ Auto-Applied 3 Wikilinks` — done, no prompts needed

2. **AI learns your patterns**
   - Scans clients/ folder: 90% have `status`, `contact`, `rate`
   - New client note missing fields
   - `✓ Auto-Added frontmatter: status: active` — high-confidence fields applied

3. **Inconsistencies caught on `/review`**
   - Frontmatter says `status: active`
   - Prose says "project wrapped up last month"
   - Run `/review` → Claude finds mismatches, you decide which is correct

4. **Each interaction improves the next**
   - More links → better graph queries
   - Consistent frontmatter → better pattern detection
   - Clean data → smarter AI suggestions

**This is the flywheel effect.** Not just storage — a self-curating system.

---

**The Graph Index**

At startup, Flywheel builds an in-memory graph of your notes.
When you ask questions, AI queries the index — not the files.

**Why this matters:**

| Without Flywheel | With Flywheel |
|------------------|---------------|
| AI reads 50 files to find 3 relevant ones | AI queries the graph directly |
| ~50,000 tokens consumed | ~500 tokens consumed |
| Slow, expensive, context overload | Fast, cheap, precise |

For mutations (logging, rollups), Flywheel reads only the **sections** it needs:
- Full file stays on disk (privacy preserved)
- Only relevant content goes to AI (tokens saved)
- You get both: local data + smart AI

---

## Graph Queries: How Claude Knows What's Blocking You

**This works because your notes have structured frontmatter:**
```yaml
# Course Launch Plan.md
---
status: blocked
blocked_by: "[[Payment Setup]]"
---
```

```
You: "What's blocking the course launch?"

┌─ QUERY ──────────────────────────────────────────┐
│ Source:  Graph index (no file reads)             │
│ Tokens:  ~50 vs ~3,000                           │
└──────────────────────────────────────────────────┘

Claude traces the graph (not files):
  1. [[Course Launch Plan]] → frontmatter: status: blocked
  2. [[Course Launch Plan]] → frontmatter: blocked_by: [[Payment Setup]]
  3. [[Payment Setup]] → frontmatter: status: waiting
  4. [[Payment Setup]] → frontmatter: waiting_on: [[Bank Verification]]
  5. [[Bank Verification]] → frontmatter: submitted: 2026-01-03

No files read. Just index lookups on:
- 3 note titles (from index)
- 5 frontmatter fields (from index)
- 2 wikilink relationships (from index)

Claude: "The course launch is blocked by bank verification
for Stripe. You submitted Jan 3 — should clear in 2-3 days.
Once verified, payment setup takes ~1 hour, then you're live."
```

**With Flywheel: 50 tokens, instant. Without: 1,500+ tokens, 30+ seconds.**

**Note:** Frontmatter is optional but powerful. Even without it, wikilinks create a graph that Claude can traverse.

---

## The Rollup Workflow: Daily → Weekly → Monthly

**What are periodic notes?**
In personal knowledge management, people keep daily/weekly/monthly notes.
But this is also **how businesses should track progress**:

- **Daily**: What happened today? Decisions, calls, wins, blockers
- **Weekly**: What did we accomplish? What's carrying over?
- **Monthly**: Are we on track? What patterns emerge?
- **Quarterly**: Strategic review. Goals vs reality.

Most businesses track this in scattered tools (Slack, email, spreadsheets).
With Flywheel, it's **one folder of markdown** — and AI aggregates it automatically.

```
You: "do a rollup"

┌─ CHAIN ──────────────────────────────────────────┐
│ Reads:   7 daily notes, ## Log sections          │
│          (~700 tokens vs ~7,000 full files)      │
│ Creates: weekly/2026-W01.md                      │
│ Appends: monthly/2026-01.md                      │
│ Appends: quarterly/2026-Q1.md                    │
│ Appends: Achievements.md                         │
└──────────────────────────────────────────────────┘

### weekly/2026-W01.md (created)
## Week 1 Summary
- Finalized Stripe integration for course payments
- Newsletter hit 3,000 subscribers (up 200)
- Consulting: closed $2,400 in new work

## Achievements
- First week with $1K+ passive revenue

### monthly/2026-01.md (appended)
## Week 1
[Summary linked here]
```

**You can still edit these files.** Rollup aggregates — it doesn't lock you out.

---

## Capture Context: Log What You Learned

You spent 20 minutes researching payment processors with Claude.
One command captures everything:

```
You: "log our findings on payment options"

┌─ MUTATION ───────────────────────────────────────┐
│ Context: Prior conversation (summarized by AI)   │
│ Reads:   ## Log section (42 tokens)              │
│ Appends: daily/2026-01-07.md                     │
└──────────────────────────────────────────────────┘

## Log
- 09:15 Morning review
- 10:47 **Payment processor research**                    ← NEW
  Compared Stripe vs Square vs PayPal for course sales.
  Stripe wins: 2.9% + $0.30, instant payouts, better API.
  Setting up this week.
  See also: [[Revenue Tracker]], [[Course Launch Plan]]
```

**20 minutes of conversation → one structured entry. Claude did the summarizing.**

---

## Entity Extraction: AI Links For You

Claude identifies entities from context and creates wikilinks automatically:

```
You: "log the client call"

┌─ MUTATION ───────────────────────────────────────┐
│ Context: Prior conversation about Acme Corp call │
│ Reads:   ## Log section (38 tokens)              │
│ Appends: daily/2026-01-07.md                     │
│ Entities: [[Acme Corp]], [[Sarah Chen]], [[Q1 Proposal]]
└──────────────────────────────────────────────────┘

## Log
- 14:22 **Client call: [[Acme Corp]]**                    ← NEW
  Met with [[Sarah Chen]] (VP Ops). They want to expand
  the [[Q1 Proposal]] scope to include API integration.
  Budget approved: $15K additional. Timeline: 3 weeks.
  Action: Send revised SOW by Friday.
```

**Claude extracted 3 entities from the conversation and linked them automatically.**

---

## MCP Cross-Talk: Log + Calendar in One Command

With Google Calendar MCP connected, Claude can log AND create a reminder:

```
You: "log this and remind me to follow up Friday"

┌─ CHAIN ──────────────────────────────────────────┐
│ Context: Prior conversation about proposal       │
│ Reads:   ## Log section (38 tokens)              │
│ Appends: daily/2026-01-07.md                     │
│ Creates: Google Calendar event (via calendar MCP)│
└──────────────────────────────────────────────────┘

## Log
- 14:22 **Proposal sent to [[Acme Corp]]**               ← NEW
  Revised SOW with API scope ($15K). Sarah reviewing.
  Follow-up: Friday 10am

Calendar event created:
   "Follow up: Acme Corp proposal"
   Friday, Jan 10, 2026 at 10:00 AM
```

**One command: logged the context, linked entities, AND created a calendar reminder.**

---

## Voice → Research → Report → Log

The most powerful pattern: speak a request, get research done, report written, and logged:

```
[You're at your desk with a headset. Hands busy with coffee. Speaking to Claude.]

You: "Research the best email automation tools for course creators,
     write me a report, and log it in my daily note"

┌─ CHAIN ──────────────────────────────────────────┐
│ Step 1: Web research (via Claude)                │
│ Step 2: Creates: reports/email-automation.md     │
│ Step 3: Reads: ## Log section (38 tokens)        │
│ Step 4: Appends: daily/2026-01-07.md             │
│ Writes: 2 files                                  │
└──────────────────────────────────────────────────┘

### reports/email-automation.md (created)
---
type: research-report
topic: email automation for course creators
date: 2026-01-07
---

# Email Automation Tools for Course Creators

| Tool | Price | Best For | Course Integration |
|------|-------|----------|-------------------|
| ConvertKit | $29/mo | Creators | Native |
| Mailchimp | Free tier | Starting out | Zapier |
| ActiveCampaign | $49/mo | Advanced automation | API |

Recommendation: ConvertKit for course creators.

### daily/2026-01-07.md (appended)
## Log
- 10:30 **Email automation research** → [[reports/email-automation]]  ← NEW
  Compared ConvertKit, Mailchimp, ActiveCampaign.
  ConvertKit recommended. Next: free trial signup.
```

**One voice command: research done, report created, daily log updated.**

---

## Quick Start

### 1. Install

```bash
/plugin marketplace add bencassie/flywheel
/plugin install flywheel@bencassie-flywheel
```

### 2. Setup

```
/setup-flywheel
```

Claude configures everything for your platform.

### 3. Try It

```
"check vault health"       → Comprehensive diagnostics
"find orphan notes"        → Disconnected notes needing links
"do a rollup"              → Daily → weekly → monthly
"/log fixed the bug"       → Timestamped entry
```

**[Full Installation Guide →](docs/GETTING_STARTED.md)**

---

## See It In Action

Pick your business. Start asking questions.

| You Are | Demo | AI Handles |
|---------|------|------------|
| **Content creator** | [Solo Operator](./demos/solo-operator/) | Newsletter, course sales, consulting |
| **Consultant** | [Carter Strategy](./demos/carter-strategy/) | Clients, invoices, deliverables |
| **Startup founder** | [Startup Ops](./demos/startup-ops/) | Onboarding, metrics, playbooks |
| **Researcher** | [Nexus Lab](./demos/nexus-lab/) | Literature, experiments, citations |
| **Technical lead** | [Artemis Rocket](./demos/artemis-rocket/) | Systems, decisions, blockers |

```bash
cd demos/solo-operator
claude
/setup-flywheel
```

---

## Why Flywheel Is Different

Most AI tools read your files, dump them into context, and hope for the best.
Flywheel is architecturally different:

### 1. Graph-First, Not File-First
At startup, Flywheel builds an **in-memory graph** of your notes:
- Titles, links, frontmatter, tags — all indexed
- AI queries relationships, not raw text
- Result: 50-200 tokens instead of 5,000-50,000

### 2. Your Files Stay on Your Disk
For mutations (logging, rollups), Flywheel reads **only the sections it needs**:
- Full file stays on disk — never sent to AI unless necessary
- Only `## Log` or `## Tasks` content goes over the wire
- Privacy by architecture, not by policy

### 3. 10-200x Token Savings (Real Numbers)
| Operation | Without Flywheel | With Flywheel | Savings |
|-----------|------------------|---------------|---------|
| "What's blocking X?" | ~5,000 tokens | ~50 tokens | 100x |
| "/log research findings" | ~800 tokens | ~42 tokens | 19x |
| "do a rollup" (7 days) | ~7,000 tokens | ~700 tokens | 10x |

### 4. MCP Protocol = Claude-Native
Flywheel uses the Model Context Protocol (MCP), so Claude:
- Sees 40+ specialized tools automatically
- Chooses the right tool for each query
- No prompting or configuration needed

**You just ask questions. Claude uses the graph.**

### 5. Git-Native: Your Business History, Versioned
Every markdown file is just a file. Use Git to:
- Track every decision, every change, every rollback
- See what changed last quarter vs this quarter
- Collaborate with partners via branches and PRs
- Never lose context — your history is your history

**Your business has version control. Most SaaS tools don't.**

### 6. Plain Text = Future-Proof
Notion can change their API. Salesforce can sunset features. Your markdown?
- Works in any editor (Obsidian, VSCode, vim, Notepad)
- No export needed — it's already in the universal format
- Migrate to any system, anytime
- Your grandkids could read these files

**No lock-in. No migration. Just files.**

### 7. Extensible: Make It Yours
Flywheel is a framework, not a finished product:
- **Skills**: Add `/invoice` or `/standup` commands for your workflow
- **Agents**: Multi-step automations that chain operations
- **Hooks**: Trigger actions on file changes or commands
- **MCP Tools**: Extend the graph intelligence

**Start simple. Grow into automation.**

---

## Documentation

| Doc | What It Covers |
|-----|----------------|
| **[Getting Started](docs/GETTING_STARTED.md)** | Installation, platform setup, first commands |
| **[MCP Tools](docs/MCP_REFERENCE.md)** | All 40+ graph query tools |
| **[Skills](docs/SKILLS_REFERENCE.md)** | Slash commands like `/log`, `/rollup`, `/vault-health` |
| **[Agentic Patterns](docs/AGENTIC_PATTERNS.md)** | How Flywheel makes AI workflows reliable |
| **[Six Gates](docs/SIX_GATES.md)** | Safety framework for mutations |

---

## Platform Support

- macOS / Linux / WSL / Windows

**[Platform Setup →](docs/GETTING_STARTED.md#platform-specific-notes)**

---

Apache 2.0 License | [GitHub](https://github.com/bencassie/flywheel) | [Issues](https://github.com/bencassie/flywheel/issues)
