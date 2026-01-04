# Flywheel - The Agentic Markdown Operating System

[![npm version](https://img.shields.io/npm/v/@bencassie/flywheel-mcp.svg)](https://www.npmjs.com/package/@bencassie/flywheel-mcp)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-blue.svg)](https://github.com/bencassie/flywheel)

**A Claude Code + MCP plugin that gives AI deep knowledge of your vault using 200x fewer tokens.**

How it works:
- Builds a **header/note graph** from your markdown files
- AI queries the graph instead of reading every file
- Your knowledge stays local, private, and fast

Why this matters:
- **Cost**: 200x token reduction = 200x cheaper
- **Privacy**: Intelligence derived locally, not sent to cloud
- **Security**: No file contents in prompts unless needed
- **Speed**: Graph queries vs full-text search

---

## Graph Intelligence: Ask Anything About Your Vault

```
You: "What's blocking the propulsion milestone?"

Flywheel traverses your graph:
  Propulsion Milestone → depends on → Turbopump Test
  Turbopump Test → blocked by → Seal Supplier Delay
  Seal Supplier → contact → Marcus Chen

Claude: "The propulsion milestone is blocked by turbopump testing,
which is waiting on seals from Apex Materials. Marcus Chen is
tracking - last update was Jan 2."
```

**Your AI found the blocker in 3 hops. No manual search.**

---

## Action Logging: Decisions Become Searchable

```
You: "/log approved dual-sourcing with Precision Components"

daily/2026-01-04.md
─────────────────────
## Log
- 14:32 approved dual-sourcing with [[Precision Components]]
```

**Decision captured. Auto-linked. Searchable forever.**

---

## Path Finding: See How Concepts Connect

```
You: "how does the seal delay connect to our launch date?"

Flywheel traces the path:
  [[Seal Supplier Delay]]
    → blocks → [[Turbopump]]
    → required for → [[Engine Hot Fire Test 4]]
    → gates → [[Flight Readiness Review]]
    → determines → [[Launch Date]]
```

**5 hops. Critical path revealed.**

---

## Task Tracking: Find Overdue Across Linked Notes

```
You: "what's overdue for propulsion?"

Flywheel searches linked notes:
  ⚠️ Overdue (3):
    Turbopump.md:     - [ ] Review seal specs 📅 2026-01-02
    Risk-Register.md: - [ ] Update risk scores 📅 2026-01-03
    Test-Plan.md:     - [ ] Finalize Test 4 checklist 📅 2026-01-03

  All linked to [[Propulsion Milestone]].
```

**Not just "all overdue" — overdue for THIS project.**

---

## Schema Enforcement: Find Incomplete Notes

```
You: "check schema in systems/"

Flywheel infers conventions from 12 notes:
  Expected fields: type, status, owner (>90% have these)

  ⚠️ 2 notes incomplete:
    systems/avionics.md: missing 'owner'
    systems/thermal.md: missing 'status', 'owner'
```

**No config needed. Patterns detected automatically.**

---

## The Rollup Workflow: Daily → Weekly → Monthly

Your AI writes your weekly summary automatically:

```
You: "do a rollup of my notes"

Daily Notes                Weekly              Monthly            Yearly
───────────────────────────────────────────────────────────────────────────
Jan 1  ─┐
Jan 2  ─┼─► Week 1 ─┐
Jan 3  ─┤          │
...    ─┘          │
Jan 8  ─┐          ├─► January ─┐
Jan 9  ─┼─► Week 2 ─┤           │
...    ─┘          │           ├─► 2026 ─► Achievements.md
                   ...         │
                              ...

Claude: Processing rollup chain...
✓ Daily notes (Jan 1-7) → Weekly Summary
✓ Weekly notes (Dec) → Monthly Summary
✓ Achievements extracted → Achievements.md
```

**From scattered daily notes to structured insights—automatically.**

---

## Quick Start

### 1. Install

```bash
/plugin marketplace add bencassie/flywheel
/plugin install flywheel@bencassie-flywheel
```

### 2. Setup

Say: **"setup flywheel"** - Claude configures everything for your platform.

### 3. Try It

```
"check vault health"       → Comprehensive diagnostics
"find orphan notes"        → Disconnected notes needing links
"do a rollup"              → Daily → weekly → monthly
"/log fixed the bug"       → Timestamped entry
```

**[Full Installation Guide →](docs/GETTING_STARTED.md)**

---

## Demo Vaults

Try Flywheel with real-world scenarios (ordered by complexity):

| Demo | You Are | Try Asking |
|------|---------|-----------|
| [Carter Strategy](./demos/carter-strategy/) | Solo consultant, 3 clients | "What's overdue this week?" |
| [Artemis Rocket](./demos/artemis-rocket/) | Chief Engineer, aerospace startup | "What's blocking propulsion?" |
| [Startup Ops](./demos/startup-ops/) | Co-founder, pre-Series A SaaS | "Walk me through customer onboarding" |
| [Nexus Lab](./demos/nexus-lab/) | PhD researcher, protein folding | "How does AlphaFold connect to my experiment?" |

```bash
cd demos/carter-strategy
claude
/setup-flywheel
```

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

- ✅ macOS / Linux / WSL / Windows

**[Platform Setup →](docs/GETTING_STARTED.md#platform-specific-notes)**

---

MIT License | [GitHub](https://github.com/bencassie/flywheel) | [Issues](https://github.com/bencassie/flywheel/issues)
