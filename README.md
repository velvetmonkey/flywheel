# Flywheel - The Agentic Markdown Operating System

[![npm version](https://img.shields.io/npm/v/@bencassie/flywheel-mcp.svg)](https://www.npmjs.com/package/@bencassie/flywheel-mcp)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-blue.svg)](https://github.com/bencassie/flywheel)

**Vision**: Enable non-technical knowledge workers to build automated workflows using markdown files and agentic systems - the 2026 business automation stack.

**The pitch**: *"Starting a new business or project? Install Flywheel in Claude Code - it gives you the intelligence and workflows to run your business from day one."*

---

## See It In Action: The Rollup Workflow

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

[Shows generated summary preview]
```

**From scattered daily notes to structured insights—automatically.**

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

## Instant Logging: Capture Without Context Switching

```
You: "/log completed turbopump hot fire - nominal"

daily/2026-01-04.md
─────────────────────
## Log
- 14:32 completed turbopump hot fire - nominal   ← added
```

**One sentence → timestamped entry → today's daily note.**

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

Try Flywheel with real-world scenarios:

| Demo | You Are | Try Asking |
|------|---------|-----------|
| [Artemis Rocket](./demos/artemis-rocket/) | Chief Engineer, aerospace startup | "What's blocking propulsion?" |
| [Carter Strategy](./demos/carter-strategy/) | Solo consultant, 3 clients | "What's overdue this week?" |
| [Nexus Lab](./demos/nexus-lab/) | PhD researcher, protein folding | "How does AlphaFold connect to my experiment?" |
| [Startup Ops](./demos/startup-ops/) | Co-founder, pre-Series A SaaS | "Walk me through customer onboarding" |

```bash
cd demos/carter-strategy && say "setup flywheel"
```

---

## Documentation

| Getting Started | Reference | Patterns |
|-----------------|-----------|----------|
| [Installation](docs/GETTING_STARTED.md) | [MCP Tools](docs/MCP_REFERENCE.md) | [Agentic Patterns](docs/AGENTIC_PATTERNS.md) |
| [Tutorial](docs/TUTORIAL.md) | [Skills](docs/SKILLS_REFERENCE.md) | [Six Gates Safety](docs/SIX_GATES.md) |
| [Quickstart](docs/QUICKSTART.md) | [Agents](docs/AGENTS_REFERENCE.md) | [Architecture](docs/ARCHITECTURE.md) |

---

## Platform Support

- ✅ macOS / Linux / WSL / Windows

**[Platform Setup →](docs/GETTING_STARTED.md#platform-specific-notes)**

---

MIT License | [GitHub](https://github.com/bencassie/flywheel) | [Issues](https://github.com/bencassie/flywheel/issues)
