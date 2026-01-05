# Flywheel Documentation

Your AI understands your knowledge graph. Ask questions. Run workflows.

**Installation**: [GETTING_STARTED](GETTING_STARTED.md) | **Demo Vaults**: [demos/](../demos/)

---

## Graph Intelligence

Ask natural language questions—Flywheel navigates your vault's connections to find answers.

### Example 1: Finding Blockers (artemis-rocket)

```
You: "What's blocking the propulsion milestone?"

Flywheel traverses:
  Propulsion Milestone → depends on → Turbopump Test
  Turbopump Test → blocked by → Seal Supplier Delay
  Seal Supplier → contact → Marcus Chen

Claude: "The propulsion milestone is blocked by turbopump testing,
which is waiting on seals from Apex Materials. Marcus Chen is
tracking - last update was Jan 2."
```

### Example 2: Aggregating Revenue (carter-strategy)

```
You: "How much have I billed Acme Corp?"

Flywheel aggregates:
  Acme Corp → has projects → [API Integration, Data Migration]
  API Integration → invoices → [$12,000 paid, $8,000 pending]
  Data Migration → invoices → [$15,000 paid]

Claude: "You've billed Acme Corp $35,000 total. $27,000 paid,
$8,000 pending from the API Integration project."
```

### Example 3: Tracing Research Chains (nexus-lab)

```
You: "How does AlphaFold connect to my docking experiment?"

Flywheel traces:
  AlphaFold Paper → method → Structure Prediction
  Structure Prediction → used in → Docking Experiment 3
  Docking Experiment 3 → builds on → Your Hypothesis

Claude: "AlphaFold's structure prediction method is the basis for
your Docking Experiment 3, which tests your protein binding hypothesis."
```

### Example 4: Following Playbooks (startup-ops)

```
You: "Walk me through onboarding DataDriven Co"

Flywheel retrieves:
  Onboarding Playbook → steps → [Welcome, Access, Training, Handoff]
  DataDriven Co → current step → Access Setup
  DataDriven Co → contact → Sarah Chen

Claude: "DataDriven Co is on step 2 (Access Setup). Next: send
credentials to Sarah Chen, then schedule training call."
```

### Example 5: Finding Decision Stakeholders (artemis-rocket)

```
You: "Who should review the avionics decision?"

Flywheel finds:
  Avionics Decision → affects → [Navigation, Comms, Power]
  Navigation → owner → Alex Kim
  Comms → owner → Jordan Lee
  Power → owner → Chris Park

Claude: "Alex Kim (Navigation), Jordan Lee (Comms), and Chris Park
(Power) should review—their systems are affected."
```

---

## Workflows & Mutators

Slash commands that modify your vault. Each shows: input → operation → output.

### /rollup — Aggregate Daily Notes

```
┌─ carter-strategy ────────────────────────────────────────────────┐
│                                                                   │
│  You: "/rollup"                                                   │
│                                                                   │
│  INPUT                     OPERATION                 OUTPUT       │
│  ──────────────────────────────────────────────────────────────  │
│  daily/2026-01-01.md  ─┐                                         │
│  daily/2026-01-02.md  ─┼─► Extract key points  ─► weekly/W01.md  │
│  daily/2026-01-03.md  ─┤   Preserve decisions                    │
│  ...                  ─┘   Link achievements                      │
│                                                                   │
│  OUTPUT: weekly/W01.md                                           │
│  WHY: Follows periodic-notes convention. Links back to dailies.  │
│  UPDATES: Regenerated on each rollup with new content.           │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘
```

### /log — Timestamped Entry

```
┌─ artemis-rocket ─────────────────────────────────────────────────┐
│                                                                   │
│  You: "/log completed turbopump hot fire - nominal"              │
│                                                                   │
│  INPUT             OPERATION               OUTPUT                 │
│  ──────────────────────────────────────────────────────────────  │
│  Your message ─► Append to ## Log   ─► daily/2026-01-04.md       │
│                  with timestamp            │                      │
│                                            ▼                      │
│                                   ## Log                          │
│                                   - 14:32 completed turbopump...  │
│                                                                   │
│  OUTPUT: Today's daily note under ## Log section                 │
│  WHY: Follows daily-note convention. Creates note if missing.    │
│  UPDATES: Appends only—never overwrites existing entries.        │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘
```

### /vault-fix-links — Repair Broken Wikilinks

```
┌─ nexus-lab ──────────────────────────────────────────────────────┐
│                                                                   │
│  You: "/vault-fix-links"                                                │
│                                                                   │
│  INPUT              OPERATION                  OUTPUT             │
│  ──────────────────────────────────────────────────────────────  │
│  Vault scan ─► Find [[Broken Link]]    ─► experiments/exp-07.md  │
│                Suggest [[AlphaFold]]        (link corrected)     │
│                ─────────────────────                              │
│                User confirms fix                                  │
│                                                                   │
│  OUTPUT: In-place edit to source file                            │
│  WHY: Fixes reference at point of use. Preserves git history.    │
│  UPDATES: One-time fix. Re-run to catch new broken links.        │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘
```

### /add-task — Task to Note

```
┌─ startup-ops ────────────────────────────────────────────────────┐
│                                                                   │
│  You: "/add-task customers/DataDriven.md Follow up on renewal"   │
│                                                                   │
│  INPUT              OPERATION                 OUTPUT              │
│  ──────────────────────────────────────────────────────────────  │
│  Note path    ─┐                                                 │
│  Task text    ─┼─► Append to ## Tasks ─► customers/DataDriven.md │
│  (due date)   ─┘   with checkbox             │                   │
│                                              ▼                    │
│                                     ## Tasks                      │
│                                     - [ ] Follow up on renewal    │
│                                                                   │
│  OUTPUT: Target note under ## Tasks section                      │
│  WHY: Tasks live with context. Creates section if missing.       │
│  UPDATES: Appends only—never removes existing tasks.             │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘
```

### /schema-apply — Enforce Folder Conventions

```
┌─ carter-strategy ────────────────────────────────────────────────┐
│                                                                   │
│  You: "/schema-apply projects/"                                   │
│                                                                   │
│  INPUT               OPERATION                   OUTPUT           │
│  ──────────────────────────────────────────────────────────────  │
│  projects/*.md ─► Infer folder schema       ─► projects/new.md   │
│                   (status, client, budget)       (frontmatter    │
│                   ─────────────────────           added)         │
│                   Add missing fields                              │
│                                                                   │
│  OUTPUT: In-place frontmatter addition                           │
│  WHY: Enforces consistency. Respects existing values.            │
│  UPDATES: Only adds missing fields. Never overwrites.            │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘
```

---

## For Developers

| Reference | Guide |
|-----------|-------|
| [MCP Tools](MCP_REFERENCE.md) | [Architecture](ARCHITECTURE.md) |
| [Skills](SKILLS_REFERENCE.md) | [Agentic Patterns](AGENTIC_PATTERNS.md) |
| [Agents](AGENTS_REFERENCE.md) | [Six Gates Safety](SIX_GATES.md) |

**Contributing**: See [CLAUDE.md](../CLAUDE.md) for development instructions.

---

**Version**: 1.10.5 | [Roadmap](ROADMAP.md) | [GitHub](https://github.com/bencassie/flywheel)
