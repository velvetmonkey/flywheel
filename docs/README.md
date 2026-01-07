# Flywheel Documentation

Query your markdown vault. Run workflows. Build your own skills.

**[Getting Started](GETTING_STARTED.md)** | **[Query Guide](QUERY_GUIDE.md)** | **[Demo Vaults](../demos/)**

---

## 1. Query Your Vault

Ask questions—Flywheel queries the graph index, not your files.

### Graph Intelligence

```
"What's blocking the propulsion milestone?"

Flywheel traverses:
  Propulsion Milestone → depends on → Turbopump Test
  Turbopump Test → blocked by → Seal Supplier Delay

Answer in ~50 tokens (vs 5,000+ reading files)
```

### Temporal Queries

```
"What changed in the last 7 days?"
"Find stale notes—important but neglected"
"Show notes edited around the same time as [[This Note]]"
```

### Schema Queries

```
"What fields exist in projects/?"
"Find notes where status is 'blocked'"
"Show all unique client values"
```

**[Full Query Guide →](QUERY_GUIDE.md)**

---

## 2. Pre-Built Commands

50+ workflow commands for common operations.

### Daily Operations

| Command | What It Does |
|---------|--------------|
| `/log fixed the bug` | Timestamped entry in daily note |
| `/rollup` | Daily → weekly → monthly summaries |
| `/vault-tasks` | Show all open tasks |

### Vault Maintenance

| Command | What It Does |
|---------|--------------|
| `/vault-health` | Full diagnostics |
| `/vault-orphans` | Notes with no connections |
| `/vault-fix-links` | Find and repair broken links |

### Reviews

| Command | What It Does |
|---------|--------------|
| `/weekly-review` | Generate weekly summary |
| `/extract-actions` | Pull action items from notes |

**[Full Command Reference →](SKILLS_REFERENCE.md)**

---

## 3. Build Your Own Skills

Skills are markdown files. No code required.

```markdown
# SKILL.md

---
name: weekly-digest
description: Generate weekly vault summary
trigger_keywords:
  - "weekly digest"
allowed-tools: Read, mcp__flywheel__get_recent_notes
---

## Process
1. Query recent activity
2. Group by folder
3. Generate summary
```

When you say "weekly digest", Claude follows your process.

**[Building Skills Guide →](BUILDING_SKILLS.md)**

---

## Documentation Index

### Getting Started
- **[Quick Start](GETTING_STARTED.md)** — Install, setup, first queries
- **[Query Guide](QUERY_GUIDE.md)** — Graph, temporal, schema queries

### Reference
- **[MCP Tools](MCP_REFERENCE.md)** — All 44 query tools
- **[Skills Reference](SKILLS_REFERENCE.md)** — 50+ pre-built commands
- **[Agents Reference](AGENTS_REFERENCE.md)** — Multi-step workflows

### Building
- **[Building Skills](BUILDING_SKILLS.md)** — Create custom workflows
- **[Architecture](ARCHITECTURE.md)** — System design
- **[Six Gates](SIX_GATES.md)** — Safety framework

### Advanced
- **[Agentic Patterns](AGENTIC_PATTERNS.md)** — Reliable AI workflows
- **[Workflow Configuration](WORKFLOW_CONFIGURATION.md)** — Customize rollups
- **[Templates](TEMPLATES.md)** — Note templates

---

## Demo Examples

See query patterns in action:

| Demo | Ask This |
|------|----------|
| [carter-strategy](../demos/carter-strategy/) | "How much have I billed Acme Corp?" |
| [startup-ops](../demos/startup-ops/) | "Walk me through onboarding DataDriven" |
| [artemis-rocket](../demos/artemis-rocket/) | "Who should review the avionics decision?" |
| [nexus-lab](../demos/nexus-lab/) | "How does AlphaFold connect to my experiment?" |

---

**[GitHub](https://github.com/bencassie/flywheel)** | **[Roadmap](ROADMAP.md)**
