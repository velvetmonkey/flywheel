# Flywheel Documentation

Query your markdown vault like a database.

**[Getting Started](GETTING_STARTED.md)** | **[Query Guide](QUERY_GUIDE.md)** | **[Demo Vaults](../demos/)**

---

## Query Your Vault

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

## Documentation Index

### Getting Started
- **[Quick Start](GETTING_STARTED.md)** — Install, setup, first queries
- **[Tutorial](TUTORIAL.md)** — 10-minute hands-on guide
- **[Query Guide](QUERY_GUIDE.md)** — Graph, temporal, schema queries

### Reference
- **[MCP Tools](MCP_REFERENCE.md)** — All 40+ query tools

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

**[GitHub](https://github.com/bencassie/flywheel)**
