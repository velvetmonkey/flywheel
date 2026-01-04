# Flywheel Demo Vaults

> See Flywheel in action with real-world scenarios

## 60-Second Demo (Any Vault)

```bash
# Step 1: Navigate to demo
cd flywheel/demos/artemis-rocket  # or carter-strategy, nexus-lab, startup-ops

# Step 2: Configure MCP (add to .mcp.json)
{
  "mcpServers": {
    "flywheel": {
      "command": "npx",
      "args": ["-y", "@bencassie/flywheel-mcp"],
      "env": { "PROJECT_PATH": "." }
    }
  }
}

# Step 3: Try it (in Claude Code)
/vault-health
```

**That's it**. You now have full vault intelligence.

---

## Choose Your Demo

| Demo | Domain | Notes | Focus | Time | README |
|------|--------|-------|-------|------|--------|
| **[Artemis Rocket](#artemis-rocket)** | Aerospace startup | 65 | Graph patterns, vault health | 5 min | [View](./artemis-rocket/README.md) |
| **[Carter Strategy](#carter-strategy)** | Solo consultant | 30 | Tasks, schema, rollups | 5 min | [View](./carter-strategy/README.md) |
| **[Nexus Lab](#nexus-lab)** | Research lab | 30 | Relationships, citations | 5 min | [View](./nexus-lab/README.md) |
| **[Startup Ops](#startup-ops)** | B2B SaaS startup | 30 | Bidirectional bridge, zones | 5 min | [View](./startup-ops/README.md) |

---

## Artemis Rocket - Aerospace Startup

**Scenario**: 8-person aerospace startup building rocket engines. 65 notes with realistic complexity.

### What It Demonstrates
- **Graph patterns**: Hubs, orphans, clusters, broken links
- **Vault health**: Intentional issues for fixing
- **Team collaboration**: Engineering, business, R&D notes

### Try These Commands

```bash
# Get vault overview
/vault-health
# Expected: 65 notes, 300+ links, 4 orphans, 3 broken links

# Find disconnected knowledge
/vault-orphans
# Expected: 4 intentional orphans to discover

# Fix broken wikilinks
/vault-fix-links
# Expected: 3 broken links with fuzzy-match suggestions

# Add to daily standup
/auto-log "Reviewed propulsion system design"
# Expected: Timestamped entry in today's daily note

# Find key concepts (hubs)
/vault-hubs
# Expected: "Propulsion", "Testing", key team members
```

### Best For
- Understanding graph intelligence
- Learning vault maintenance workflows
- Team project organization

[Full Details →](./artemis-rocket/README.md)

---

## Carter Strategy - Solo Consultant

**Scenario**: Independent strategy consultant managing client projects, tasks, and knowledge. 30 notes.

### What It Demonstrates
- **Task management**: 15 tasks with due dates
- **Frontmatter schema**: 12+ fields (project, client, status)
- **Rollup workflows**: Daily → weekly → monthly aggregation
- **Stale note detection**: Important but neglected notes

### Try These Commands

```bash
# Get upcoming tasks
/vault-due
# Expected: 3 overdue, 2 this week, 5 upcoming

# Find important but neglected notes
/vault-stale
# Expected: Client projects untouched >30 days

# See all frontmatter fields
/vault-schema
# Expected: 12+ fields (project, client, status, priority, etc.)

# Run daily → monthly rollup
/rollup
# Expected: Weekly summaries created, monthly aggregated

# Find schema inconsistencies
/vault-schema-check
# Expected: Type mismatches (e.g., priority: string vs number)
```

### Best For
- Task and project management
- Frontmatter-heavy workflows
- Solo practice organization

[Full Details →](./carter-strategy/README.md)

---

## Nexus Lab - Research Lab

**Scenario**: University research lab studying protein folding. 30 notes with citation chains.

### What It Demonstrates
- **Relationship intelligence**: Citation networks, knowledge paths
- **Temporal analysis**: Concurrent edits, activity clusters
- **Connection strength**: How related are two notes?
- **Knowledge gaps**: What's mentioned but not documented?

### Try These Commands

```bash
# How do two topics connect?
get_link_path({ from: "AlphaFold.md", to: "Docking Simulations.md" })
# Expected: AlphaFold → Protein Structure → Docking (3 hops)

# Find knowledge clusters
/vault-clusters
# Expected: 3 clusters (Methods, Results, Literature)

# What's commonly referenced?
get_common_neighbors({ note_a: "AlphaFold.md", note_b: "Rosetta.md" })
# Expected: "Protein Structure Prediction.md"

# Find knowledge sources (literature notes)
find_sources()
# Expected: Papers with no backlinks (pure references)

# Find knowledge sinks (project notes)
find_dead_ends()
# Expected: Projects that reference but aren't referenced
```

### Best For
- Research and academic use
- Citation network analysis
- Understanding knowledge relationships

[Full Details →](./nexus-lab/README.md)

---

## Startup Ops - B2B SaaS Startup

**Scenario**: MetricFlow SaaS startup managing operations. 30 notes with zone-based automation.

### What It Demonstrates
- **Bidirectional Bridge**: Prose → frontmatter detection
- **Wikilinkification**: Convert strings to `[[wikilinks]]`
- **Automation zones**: `ai-managed` vs `human-review` notes
- **Schema validation**: Intentional inconsistencies for demo

### Try These Commands

```bash
# Detect prose patterns (Key: [[Value]])
/normalize-note "ops/customers/DataDriven Co.md"
# Expected: Detects "Status: Active", "MRR: $499", suggests frontmatter

# Convert strings to wikilinks
/wikilinkify-frontmatter "ops/customers/GrowthStack.md"
# Expected: owner: "Jamie Patel" → owner: "[[Jamie Patel]]"

# Query by automation zone
search_notes({ where: { automation: "ai-managed" } })
# Expected: 7 notes (playbooks, finance tracking)

search_notes({ where: { automation: "human-review" } })
# Expected: 4 notes (product roadmap, strategic decisions)

# Find schema inconsistencies
/vault-schema-check
# Expected: 4 fields with type mismatches (status, priority, mrr, stage)
```

### Best For
- Startup operations
- AI/human workflow separation
- Frontmatter normalization

[Full Details →](./startup-ops/README.md)

---

## Demo Comparison Matrix

| Aspect | Artemis | Carter | Nexus | Startup Ops |
|--------|---------|--------|-------|-------------|
| **Scale** | 65 notes | 30 notes | 30 notes | 30 notes |
| **Graph Type** | Clusters | Star topology | Citation chains | Zones |
| **Frontmatter** | Light (4-5 fields) | Heavy (12+ fields) | Medium (6-8) | Mixed |
| **Primary Focus** | Health, orphans | Tasks, schema | Relationships | Bidirectional bridge |
| **Complexity** | High (realistic) | Medium | Medium | Medium |
| **Best For** | Teams | Solo | Research | Startups |
| **Key Feature** | Vault maintenance | Task management | Graph intelligence | Prose normalization |

---

## Common Workflows (All Demos)

### Vault Intelligence

```bash
# Comprehensive health check
/vault-health
# Stats, orphans, hubs, broken links, stale notes

# Find disconnected notes
/vault-orphans

# Find highly connected notes (key concepts)
/vault-hubs

# Get vault statistics
get_vault_stats()
```

### Graph Navigation

```bash
# Who links to this note?
get_backlinks({ path: "note.md" })

# What does this note link to?
get_forward_links({ path: "note.md" })

# Shortest path between notes
get_link_path({ from: "A.md", to: "B.md" })

# Notes that reference each other
find_bidirectional_links()
```

### Search & Discovery

```bash
# Find notes by tag
search_notes({ has_tag: "project" })

# Find by frontmatter
search_notes({ where: { status: "active" } })

# Recent activity
get_recent_notes({ days: 7 })

# Important but neglected
get_stale_notes({ days: 30, min_backlinks: 3 })
```

### Tasks

```bash
# All tasks
/vault-tasks

# Tasks with due dates
/vault-due

# Add task
/task-add "Review Q1 goals by 2026-01-15"
```

---

## Installation

### Prerequisites
- **Flywheel MCP**: `npm install -g @bencassie/flywheel-mcp` (or use `npx`)
- **Flywheel Plugin** (optional, for skills): Install via Claude Code marketplace
- **Claude Code**: v0.2.0+ recommended

### Quick Setup

1. **Clone this repo** (or download demo folder):
   ```bash
   git clone https://github.com/bencassie/flywheel.git
   cd flywheel/demos/artemis-rocket  # or any demo
   ```

2. **Configure MCP**:
   Add to your `.mcp.json` (in project or global):
   ```json
   {
     "mcpServers": {
       "flywheel": {
         "command": "npx",
         "args": ["-y", "@bencassie/flywheel-mcp"],
         "env": {
           "PROJECT_PATH": "."
         }
       }
     }
   }
   ```

3. **Verify**:
   ```bash
   # In Claude Code
   get_vault_stats()
   # Should return vault statistics
   ```

4. **Install Plugin** (optional, for `/skills`):
   ```bash
   /plugin marketplace add bencassie/flywheel
   /plugin install flywheel@bencassie-flywheel
   ```

---

## What's Next?

- **Learn patterns**: [../docs/AGENTIC_PATTERNS.md](../docs/AGENTIC_PATTERNS.md) - How Flywheel makes AI reliable
- **Get started**: [../docs/GETTING_STARTED.md](../docs/GETTING_STARTED.md) - Install on your vault
- **Tool reference**: [../docs/MCP_REFERENCE.md](../docs/MCP_REFERENCE.md) - All 40+ MCP tools
- **Skill reference**: [../docs/SKILLS_REFERENCE.md](../docs/SKILLS_REFERENCE.md) - All 33 skills

---

## Troubleshooting

### "Tool not found"
MCP server not connected. Check `.mcp.json` configuration and restart Claude Code.

### "File not found"
Ensure `PROJECT_PATH` in `.mcp.json` points to the demo directory.

### Skills not working
Install Flywheel plugin: `/plugin install flywheel@bencassie-flywheel`

### Windows: "Connection closed"
Wrap `npx` with `cmd /c`:
```json
{
  "command": "cmd",
  "args": ["/c", "npx", "-y", "@bencassie/flywheel-mcp"]
}
```

More help: [../docs/TROUBLESHOOTING.md](../docs/TROUBLESHOOTING.md) (coming soon)

---

**Demo Status**: ✅ All 4 demos ready
**Last Updated**: 2026-01-03
**Flywheel Version**: 1.6.2
