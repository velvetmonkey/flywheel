# Demo 4: Startup Ops - AI-Managed Operations

> **Core Insight**: "AI handles ops, humans do strategy" - Automation first

## Scenario

**MetricFlow** is a B2B SaaS analytics platform for SMBs. Two co-founders (**Alex Chen** - CEO/Product, **Jamie Patel** - COO/Sales) are building toward Series A. They use Obsidian for operational knowledge management with clear zone separation:

- **Ops Zone** (`ops/`): AI-managed, high-frequency operational tasks
- **Product Zone** (`product/`): Human-reviewed strategic decisions
- **Finance Zone** (`finance/`): Mixed automation with human oversight
- **Time Notes** (`daily-notes/`, `weekly-notes/`): Automated rollups and handoffs

The vault demonstrates **4 key Flywheel features**:
1. **Bidirectional Bridge** (v1.1 roadmap priority) - Prose ↔ Frontmatter normalization
2. **Knowledge Handoff** - Zone-based automation (`automation: ai-managed` vs `human-review`)
3. **Schema Validation** - Intentional inconsistencies for demonstration
4. **Workflow Automation** - Playbook execution and recurring task templates

## Vault Structure

```
startup-ops/
├── README.md                               # This file
├── .obsidian/                              # Obsidian config
├── daily-notes/                            # 5 notes - Founder daily logs
│   ├── 2026-01-01.md                      # New Year planning
│   ├── 2026-01-02.md                      # Customer success (prose pattern)
│   ├── 2026-01-03.md                      # Target market decision
│   ├── 2026-01-06.md                      # Kickoff call (handoff trigger)
│   └── 2026-01-07.md                      # Investor call
├── weekly-notes/                           # 1 note - Weekly rollup
│   └── 2026-W01.md                        # Week 1 summary
├── ops/                                    # AI-MANAGED ZONE (11 notes)
│   ├── customers/
│   │   ├── DataDriven Co.md               # Active customer (prose patterns)
│   │   ├── GrowthStack.md                 # Trial customer
│   │   └── InsightHub.md                  # Churned (schema inconsistency)
│   ├── playbooks/
│   │   ├── Customer Onboarding.md         # Full playbook with checklists
│   │   ├── Support Escalation.md          # SOP template
│   │   ├── Weekly Metrics Review.md       # Rollup trigger
│   │   └── Investor Update.md             # Monthly template
│   ├── recurring/
│   │   ├── Monday Standup Prep.md         # Automated weekly prep
│   │   └── Friday Wrap-up.md              # EOW template
│   └── meetings/
│       ├── 2026-01-06 DataDriven Kickoff.md  # Meeting notes (prose patterns)
│       └── 2026-01-07 Investor Call.md       # Investor intro
├── product/                                # HUMAN STRATEGY ZONE (6 notes)
│   ├── roadmap/
│   │   ├── Q1 2026 Roadmap.md             # Strategic roadmap
│   │   └── Feature Priorities.md          # Product backlog
│   ├── decisions/
│   │   ├── DEC-001 Pricing Model.md       # Pricing decision (schema issue)
│   │   └── DEC-002 Target Market.md       # ICP decision (schema issue)
│   └── research/
│       ├── Competitor Analysis.md         # Market landscape
│       └── User Interview Synthesis.md    # Customer research (prose pattern)
├── team/                                   # 3 notes - People
│   ├── Alex Chen.md                       # Co-founder/CEO profile (hub)
│   ├── Jamie Patel.md                     # Co-founder/COO profile (hub)
│   └── Hiring Plan.md                     # Hiring roadmap
└── finance/                                # 3 notes - Financial tracking
    ├── MRR Tracker.md                     # Revenue tracking
    ├── Runway Calculator.md               # Burn rate analysis
    └── Investor Pipeline.md               # Fundraising tracker

Total: 30 notes
```

## Feature Showcase Patterns

### 1. Bidirectional Bridge (v1.1 Priority)

**Prose → Frontmatter Detection** (8 instances):

| File | Prose Pattern | Expected Frontmatter |
|------|---------------|----------------------|
| `ops/customers/DataDriven Co.md` | "Status: Active" | `status: active` |
| `ops/customers/DataDriven Co.md` | "MRR: $499" | `mrr: 499` |
| `ops/customers/DataDriven Co.md` | "Owner: [[Alex Chen]]" | `owner: "[[Alex Chen]]"` |
| `ops/meetings/2026-01-06 DataDriven Kickoff.md` | "Client: [[DataDriven Co]]" | `client: "[[DataDriven Co]]"` |
| `ops/meetings/2026-01-06 DataDriven Kickoff.md` | "Attendees: [[Alex Chen]], Sarah, Tom" | `attendees: ["[[Alex Chen]]", "Sarah Johnson", "Tom Wilson"]` |
| `daily-notes/2026-01-02.md` | "Customer: [[DataDriven Co]]" | `customer: "[[DataDriven Co]]"` |
| `product/research/User Interview Synthesis.md` | "Interviewee: [[DataDriven Co]]" | `interviewee: "[[DataDriven Co]]"` |
| `ops/recurring/Friday Wrap-up.md` | "Week: [[2026-W01]]" | `week: "[[2026-W01]]"` |

**Frontmatter → Wikilink Opportunities** (5 instances):

| File | Current Frontmatter | Should Be |
|------|---------------------|-----------|
| `ops/customers/GrowthStack.md` | `owner: "Jamie Patel"` | `owner: "[[Jamie Patel]]"` |
| `ops/customers/InsightHub.md` | `owner: "Alex Chen"` | `owner: "[[Alex Chen]]"` |
| `product/decisions/DEC-001 Pricing Model.md` | `stakeholder: "Alex Chen"` | `stakeholder: "[[Alex Chen]]"` |
| `product/decisions/DEC-002 Target Market.md` | `stakeholder: "Jamie Patel"` | `stakeholder: "[[Jamie Patel]]"` |
| `team/Hiring Plan.md` | `lead: "Jamie Patel"` | `lead: "[[Jamie Patel]]"` |

### 2. Knowledge Handoff (Zone Automation)

**AI-Managed Zone** (`automation: ai-managed`):
- `ops/playbooks/Customer Onboarding.md`
- `ops/playbooks/Support Escalation.md`
- `ops/playbooks/Weekly Metrics Review.md`
- `ops/playbooks/Investor Update.md`
- `ops/recurring/Monday Standup Prep.md`
- `finance/MRR Tracker.md`
- `finance/Runway Calculator.md`

**Human Strategy Zone** (`automation: human-review`):
- `product/roadmap/Q1 2026 Roadmap.md`
- `product/roadmap/Feature Priorities.md`
- `product/decisions/DEC-001 Pricing Model.md`
- `product/decisions/DEC-002 Target Market.md`

**Handoff Triggers**:
- `daily-notes/2026-01-06.md` → `automation: handoff-trigger` (Customer kickoff completed)

### 3. Schema Validation (Intentional Inconsistencies)

**Type Mismatches**:

| Field | File A | Type A | File B | Type B |
|-------|--------|--------|--------|--------|
| `priority` | DataDriven Co | (not set) | InsightHub | `"high"` (string) |
| `status` | DEC-001 | `"approved"` (string) | DEC-002 | `1` (number) |
| `stage` | Investor Pipeline | `2` (number) | Investor Pipeline table | `"seed"` (string) |
| `mrr` | DataDriven Co | (prose: $499) | GrowthStack | `0` (number) |
| `mrr` | InsightHub | `"$0"` (string with currency) | Others | number |

### 4. Workflow Automation

**Playbook Templates**:
- `ops/playbooks/Customer Onboarding.md` - Full onboarding checklist (Day 1, 2, 7, 14, 30)
- `ops/playbooks/Support Escalation.md` - P0-P3 severity levels with SLAs
- `ops/playbooks/Weekly Metrics Review.md` - Metrics review checklist
- `ops/playbooks/Investor Update.md` - Monthly email template

**Recurring Tasks**:
- `ops/recurring/Monday Standup Prep.md` - `schedule: "every Monday 8:00am"`
- `ops/recurring/Friday Wrap-up.md` - `schedule: "every Friday 4:00pm"`

**Rollup Patterns**:
- Daily notes (2026-01-01 through 2026-01-07) → Weekly summary (2026-W01)
- Weekly summaries → Monthly summaries (automation ready)

## Demo Scenarios

### Scenario 1: Bidirectional Bridge - Prose Pattern Detection

**Goal**: Detect prose patterns and promote to frontmatter

**Command**:
```bash
# Using Flywheel MCP skill
/flywheel:normalize-note "ops/customers/DataDriven Co.md"
```

**Expected Behavior**:
1. Skill reads note content
2. Detects prose patterns:
   - "Status: Active"
   - "MRR: $499"
   - "Owner: [[Alex Chen]]"
3. Suggests frontmatter additions:
   ```yaml
   status: active
   mrr: 499
   owner: "[[Alex Chen]]"
   ```
4. Optionally applies suggestions to note

**Verification**:
- Frontmatter added to top of file
- Prose patterns remain in body (or removed if instructed)
- Wikilinks preserved in frontmatter values

### Scenario 2: Bidirectional Bridge - Wikilinkify Frontmatter

**Goal**: Convert frontmatter strings to wikilinks

**Command**:
```bash
# Using Flywheel MCP skill
/flywheel:wikilinkify-frontmatter "ops/customers/GrowthStack.md"
```

**Expected Behavior**:
1. Skill reads frontmatter
2. Detects string value `owner: "Jamie Patel"`
3. Checks if "Jamie Patel" is a known entity (note title or alias)
4. Converts to wikilink: `owner: "[[Jamie Patel]]"`

**Verification**:
- Run on all 5 files with frontmatter→wikilink opportunities
- Verify backlink created from GrowthStack → Jamie Patel
- Check that non-entity strings remain unchanged

### Scenario 3: Knowledge Handoff - Query by Automation Zone

**Goal**: Find all AI-managed operational notes vs human-reviewed strategy notes

**Command**:
```bash
# Using Flywheel MCP
mcp__flywheel__search_notes({
  where: { automation: "ai-managed" }
})

mcp__flywheel__search_notes({
  where: { automation: "human-review" }
})
```

**Expected Results**:
- **AI-managed**: 7 notes (4 playbooks, 1 recurring, 2 finance)
- **Human-review**: 4 notes (2 roadmap, 2 decisions)

**Use Case**: Automation orchestration - route notes to appropriate workflows based on `automation` field

### Scenario 4: Schema Validation - Find Inconsistencies

**Goal**: Detect type mismatches in frontmatter fields

**Command**:
```bash
# Using Flywheel MCP
mcp__flywheel__find_frontmatter_inconsistencies()

# Or get field values to spot issues
mcp__flywheel__get_field_values({ field: "status" })
mcp__flywheel__get_field_values({ field: "priority" })
mcp__flywheel__get_field_values({ field: "mrr" })
```

**Expected Results**:
- **status** field: `["approved", 1]` (string + number)
- **priority** field: `["high"]` (only string, but missing in other notes)
- **mrr** field: `[499, 0, "$0"]` (number, number, string with currency)
- **stage** field: `[2, "seed"]` (number + string)

**Use Case**: Vault health check - identify fields needing normalization

### Scenario 5: Workflow Automation - Playbook Execution

**Goal**: Execute Customer Onboarding playbook for new customer

**Command**:
```bash
# Using Flywheel skill
/flywheel:vault-section "ops/playbooks/Customer Onboarding.md" "## Day 1"

# Get tasks from playbook
mcp__flywheel__get_tasks_from_note({
  path: "ops/playbooks/Customer Onboarding.md"
})
```

**Expected Behavior**:
1. Extract Day 1 section content
2. Return checklist:
   - [ ] Send welcome email
   - [ ] Schedule kickoff call
   - [ ] Prepare demo environment
   - [ ] Review Customer Onboarding playbook
3. Show automation marker: `automation: ai-managed`

**Use Case**: AI agent can read playbook, execute steps, track completion

### Scenario 6: Combined - Startup Health Check

**Goal**: Full vault intelligence for weekly ops review

**Commands**:
```bash
# 1. Get vault stats
mcp__flywheel__get_vault_stats()

# 2. Find orphans (disconnected knowledge)
mcp__flywheel__find_orphan_notes()

# 3. Find hubs (key concepts)
mcp__flywheel__find_hub_notes({ min_links: 5 })

# 4. Get stale notes (important but neglected)
mcp__flywheel__get_stale_notes({ days: 30, min_backlinks: 3 })

# 5. Find schema issues
mcp__flywheel__find_frontmatter_inconsistencies()

# 6. Get recent activity
mcp__flywheel__get_activity_summary({ days: 7 })
```

**Expected Intelligence**:
- **Orphans**: None expected (all notes well-connected)
- **Hubs**: Alex Chen, Jamie Patel, DataDriven Co, Customer Onboarding
- **Stale**: Check if any research/decision notes untouched >30 days
- **Schema issues**: 4 field inconsistencies (status, priority, mrr, stage)
- **Activity**: 5 daily notes, 1 weekly note, multiple edits in Week 1

**Use Case**: Weekly ops review - surface areas needing attention

## Key Insights Embedded in Vault

### Customer Insights (from User Interview Synthesis)
- **Spreadsheet breaking point**: 50-100 employees
- **$1K/mo threshold**: Manager-level buying without approval
- **Alerts are table stakes**: 8/12 interviews mentioned need
- **Mobile myth**: Everyone wants, nobody uses
- **Fast time-to-value**: 30 min to "aha moment" = conversion

### Strategic Decisions
- **DEC-001 Pricing**: $499 Professional (unlimited users, 1M rows), $1,999 Enterprise
- **DEC-002 Target Market**: 50-200 employees, (1M rows, $5M-$50M revenue
  - Anti-ICP: <20 employees (too small), )500 employees (need enterprise features), >5M rows (performance issues)

### Competitive Position
- **vs Tableau**: 10x faster setup, 1/2 the price
- **vs PowerBI**: Better UX, not locked to Microsoft ecosystem
- **vs Looker**: No-code, fraction of cost, SMB-focused
- **vs Metabase**: Fully managed, better features, proper support

### Automation Patterns
- **Playbooks**: Checklists with prerequisites, steps, outputs
- **Recurring tasks**: Schedule-based automation (Monday prep, Friday wrap-up)
- **Handoff triggers**: Daily notes signal milestone completion for automation
- **Zone separation**: Ops (AI), Product (Human), Finance (Mixed)

## Testing Checklist

### Bidirectional Bridge
- [ ] Detect 8 prose patterns across 4 files
- [ ] Promote prose to frontmatter (at least 1 file)
- [ ] Convert 5 frontmatter strings to wikilinks
- [ ] Verify backlinks created after wikilinkification

### Knowledge Handoff
- [ ] Query notes by `automation: ai-managed` (expect 7)
- [ ] Query notes by `automation: human-review` (expect 4)
- [ ] Identify handoff trigger in daily-notes/2026-01-06.md
- [ ] Extract playbook section content

### Schema Validation
- [ ] Find 4 field type inconsistencies
- [ ] Get unique values for `status`, `priority`, `mrr`, `stage` fields
- [ ] Generate schema health report

### Workflow Automation
- [ ] Extract Customer Onboarding playbook tasks
- [ ] Read Monday Standup Prep template
- [ ] Verify recurring task schedules
- [ ] Check weekly note rollup from daily notes

### Vault Intelligence
- [ ] Get vault stats (30 notes, 3 folders, X backlinks)
- [ ] Find hub notes (expect Alex Chen, Jamie Patel, DataDriven Co)
- [ ] Get activity summary (Week 1 edits)
- [ ] No orphans expected (all notes connected)

## Usage

### Prerequisites
- Flywheel MCP server installed and configured
- Flywheel plugin installed (for skills)
- Obsidian (optional, for viewing)

### Running Demos

**Option 1: Manual Testing**
```bash
# Navigate to demo directory
cd /path/to/flywheel/demos/startup-ops

# Configure MCP to point to this vault
# In your .mcp.json or equivalent:
{
  "mcpServers": {
    "flywheel": {
      "command": "npx",
      "args": ["-y", "@bencassie/flywheel-mcp"],
      "env": {
        "PROJECT_PATH": "/path/to/flywheel/demos/startup-ops"
      }
    }
  }
}

# Run any of the scenario commands above
```

**Option 2: Automated Test Suite** (future)
```bash
# Run all demo scenarios with expected outputs
npm run demo:startup-ops
```

## Notes

### Design Decisions
- **30 notes**: Enough complexity to show patterns, not overwhelming
- **Intentional issues**: Schema inconsistencies are deliberate for demo purposes
- **Real startup patterns**: Based on actual B2B SaaS startup operations
- **Zone separation**: Reflects real AI/human division of labor

### Patterns to Highlight
1. **Prose detection**: Most valuable for quick manual notes (meetings, daily logs)
2. **Wikilinkification**: Converts strings to graph entities (relationships visible)
3. **Automation zones**: Shows how to route tasks to AI vs human review
4. **Schema validation**: Vault health check for data quality
5. **Playbook execution**: Structured workflows for repeated processes

### Future Enhancements
- [ ] Add more daily notes (full month)
- [ ] Create monthly rollup (2026-01.md)
- [ ] Add engineering notes (for Alex's product work)
- [ ] Include customer support tickets (ops automation)
- [ ] Add fundraising deck drafts (versioning)

## Credits

**Scenario Design**: Based on real B2B SaaS startup operations
**Vault Structure**: Inspired by operational knowledge bases at 10-50 person startups
**Automation Patterns**: Reflects v1.1 Flywheel roadmap priorities (Bidirectional Bridge focus)

---

**Demo Status**: ✅ Complete - 30 notes, 4 features, 6 scenarios
**Last Updated**: 2026-01-03
**Maintainer**: Flywheel project
