# Flywheel - The Agentic Markdown Operating System

**Vision**: Enable non-technical knowledge workers to build automated workflows using markdown files and agentic systems - the 2026 business automation stack.

**The pitch**: *"Starting a new business or project? Install Flywheel in Claude Code - it gives you the intelligence and workflows to run your business from day one."*

## What is Flywheel?

Flywheel is an AI-native business operating system built on plain markdown files. It combines:

- **Graph Intelligence** (MCP server) - AI understands your knowledge graph
- **Workflow Automation** (Claude plugin) - AI handles repetitive tasks
- **Demo Vaults** - Ready-to-use templates for common workflows

### The Dual Paradigm

Flywheel supports BOTH knowledge management philosophies:

**Graph-Native** (Obsidian, Roam users):
- Wikilinks for organic relationships
- Emergent structure through connections
- **Plus**: Get queryability and structure when you need it

**Schema-Native** (VSCode, Cursor users):
- YAML frontmatter for typed data
- Explicit schemas and validation
- **Plus**: Get graph traversal and relationship intelligence

**The unique value**: Same markdown file works for both. Users don't choose - they fluidly move between paradigms.

## Architecture

```
flywheel/
├── packages/
│   ├── mcp-server/          # Graph + schema intelligence
│   └── claude-plugin/       # Workflows and automation
├── demos/
│   ├── artemis-rocket/      # Demo 1: Aerospace startup
│   ├── carter-strategy/     # Demo 2: Management consulting
│   ├── nexus-lab/           # Demo 3: Research lab
│   └── startup-ops/         # Demo 4: B2B SaaS startup (NEW)
└── docs/                    # Self-documenting vault
```

### MCP Server (Graph Intelligence)

Provides vault navigation and intelligence:
- Graph queries (backlinks, hubs, clusters, orphans)
- Temporal analysis (recent, stale, concurrent notes)
- Structure inspection (headings, sections, tasks)
- Wikilink services (suggestions, validation, broken link detection)
- Frontmatter intelligence (schema, queries, validation)
- Periodic note detection (zero-config)

### Claude Plugin (Workflow Automation)

Provides 30+ automated workflows via slash commands:
- **Core**: `/auto-log`, `/task-add`, `/rollup`
- **Health**: `/vault-health`, `/vault-orphans`, `/vault-hubs`, `/vault-dead-ends`
- **Graph**: `/vault-backlinks`, `/vault-clusters`, `/vault-path`, `/vault-strength`
- **Schema**: `/vault-schema`, `/vault-schema-check`, `/vault-field-values`
- **Links**: `/vault-fix-links`, `/vault-suggest`, `/vault-unlinked-mentions`

## The Bidirectional Bridge

**Key insight**: Wikilinks and frontmatter are two representations of the SAME information.

Flywheel automatically translates between them:

**Prose → Frontmatter** (add structure):
```markdown
Client: [[Acme Corp]]
Status: Active

↓ Flywheel suggests

---
type: project
client: [[Acme Corp]]
status: active
---
```

**Frontmatter → Wikilinks** (add traversability):
```yaml
---
attendees: ["Ben Carter", "John Smith"]
---

↓ Flywheel suggests

---
attendees:
  - [[Ben Carter]]
  - [[John Smith]]
---
```

**Result**: Same data, queryable AND traversable.

## Installation

### 1. Configure Flywheel MCP Server

Add to your `.mcp.json` (project) or `~/.claude.json` (user):

**macOS/Linux/WSL:**
```json
{
  "mcpServers": {
    "flywheel": {
      "command": "npx",
      "args": ["-y", "@bencassie/flywheel-mcp"],
      "env": { "PROJECT_PATH": "/path/to/your/vault" }
    }
  }
}
```

**Windows (requires `cmd /c` wrapper):**
```json
{
  "mcpServers": {
    "flywheel": {
      "command": "cmd",
      "args": ["/c", "npx", "-y", "@bencassie/flywheel-mcp"],
      "env": { "PROJECT_PATH": "C:/path/to/your/vault" }
    }
  }
}
```

### 2. Install the Claude Code Plugin

In Claude Code, run:
```
/plugin marketplace add bencassie/flywheel
/plugin install flywheel@flywheel
```

### 3. Restart Claude Code

That's it! Skills like `/vault-health` and `/auto-log` are now available.

See [packages/claude-plugin/INSTALLATION.md](packages/claude-plugin/INSTALLATION.md) for detailed platform-specific instructions.

## Demo Vaults

Each demo shows how AI + markdown replace traditional business software:

| Demo | Replaces | Key Insight | Status |
|------|----------|-------------|--------|
| **[Artemis Rocket](./demos/artemis-rocket)** | 200-person aerospace corp | Engineering at 10x efficiency | ✅ Complete |
| **[Carter Strategy](./demos/carter-strategy)** | Partner-heavy consultancy | One person = 5-person team | ✅ Complete |
| **[Nexus Lab](./demos/nexus-lab)** | Research lab | 100 papers/week processed | ✅ Complete |
| **[Startup Ops](./demos/startup-ops)** | B2B SaaS founders | AI handles ops, humans do strategy | ✅ Complete |

### Startup Ops Demo (New!)

**Scenario**: Two co-founders (Alex & Jamie) building "MetricFlow" - a B2B SaaS analytics platform. 30 notes showing operational automation with zone separation:

- **Ops Zone** (`ops/`) - AI-managed playbooks, customer records, recurring tasks
- **Product Zone** (`product/`) - Human-reviewed roadmap and strategic decisions
- **Finance Zone** (`finance/`) - Mixed automation for MRR tracking and fundraising

**Features Showcased**:
1. **Bidirectional Bridge** - Prose patterns ↔ Frontmatter (8 instances)
2. **Knowledge Handoff** - Zone-based automation (`ai-managed` vs `human-review`)
3. **Schema Validation** - Intentional type inconsistencies for demonstration
4. **Workflow Automation** - Playbook execution and recurring task templates

**Try it**: `cd demos/startup-ops && cat README.md`

## Why Flywheel?

**vs Notion**: You own your data (plain markdown, Git-friendly)
**vs Salesforce**: No vendor lock-in, AI has direct access
**vs Obsidian alone**: Add AI-powered workflows and automation
**vs VSCode alone**: Add graph intelligence and relationship traversal

**The unlock**: Plain text markdown becomes a queryable, executable, automatable platform for running businesses.

## Technical Stack

```
Markdown Files (plain text, Git-friendly)
    ↓
MCP Server (graph + schema intelligence)
    ↓
Claude Code / LLM (agentic automation)
    ↓
Any Editor (Obsidian, VSCode, Cursor, CLI)
```

Not tied to any specific UI - works everywhere.

## Six Gates Safety Framework

All Flywheel extensions observe the **Six Gates** - mandatory safety checks:

| Gate | Purpose | Enforcement |
|------|---------|-------------|
| **1. Read Before Write** | Read state before mutation | BLOCKS via hook |
| **2. File Exists for Edit** | Validate targets exist | BLOCKS via hook |
| **3. Agent Chain Validation** | Verify each multi-step step | BLOCKS via hook |
| **4. Mutation Confirmation** | User confirms writes | BLOCKS via hook |
| **5. MCP Health Check** | Verify MCP on session start | Warns |
| **6. Post-Write Validation** | Verify writes succeeded | Warns |

See [SIX_GATES.md](./packages/claude-plugin/skills/_patterns/SIX_GATES.md) for full specification.

## Development Status

**Current: v1.6.2** | **Next: v1.7.0 Advanced Schema Intelligence**

### What's New in v1.6.x

**v1.6.2 - Six Gates REAL Enforcement** (Latest)
- Gates 1, 2, 4 now BLOCK unsafe operations via `pre-mutation-gate.py`
- Gate 3 (Agent Chain Validation) enforced at project level
- All 8 agents now Gate 3 compliant
- Shared hooks architecture for enforcement

**v1.6.1 - Six Gates Safety Framework**
- Mandatory safety framework for all Flywheel extensions
- `session-gate.py` - MCP health verification on session start
- `verify-mutation.py` - Post-write YAML/wikilink validation
- Two-level hook architecture (plugin + project level)

**v1.6.0 - Bidirectional Bridge**
- `detect_prose_patterns` - Find "Key: [[Value]]" patterns in prose
- `suggest_frontmatter_from_prose` - Recommend YAML from detected patterns
- `suggest_wikilinks_in_frontmatter` - Find strings that could be wikilinks
- `validate_cross_layer` - Check frontmatter ↔ wikilink consistency
- `/normalize-note`, `/promote-to-frontmatter`, `/wikilinkify-frontmatter` skills

### ✅ v1.0-1.5 Foundation (Complete)
- MCP server with 40+ graph intelligence tools
- Claude plugin with 30+ vault skills
- Zero-config periodic note detection
- 4 demo vaults: Artemis Rocket, Carter Strategy, Nexus Lab, Startup Ops
- Marketplace-based plugin installation
- Cross-platform support (macOS, Linux, Windows, WSL)

### Skills Available
- **Vault Health**: `/vault-health`, `/vault-orphans`, `/vault-hubs`, `/vault-dead-ends`
- **Graph Queries**: `/vault-backlinks`, `/vault-clusters`, `/vault-path`, `/vault-strength`
- **Schema Tools**: `/vault-schema`, `/vault-schema-check`, `/vault-field-values`
- **Temporal**: `/vault-stale`, `/vault-activity`, `/vault-concurrent`
- **Wikilinks**: `/vault-fix-links`, `/vault-suggest`, `/vault-unlinked-mentions`
- **Tasks**: `/vault-tasks`, `/vault-due`, `/task-add`
- **Automation**: `/auto-log`, `/rollup` (daily/weekly/monthly/quarterly/yearly)

### Agents
- Rollup agents (daily → weekly → monthly → quarterly → yearly)
- Achievement extraction agent
- Schema enforcer agent
- Relationship explorer agent

### Roadmap

**v1.7.0 - Advanced Schema Intelligence** (Next)
- `validate_frontmatter(path, schema)` - Validate against schema
- `find_incomplete_notes(type, required_fields)` - Find notes missing fields
- `compute_frontmatter(path, fields)` - Auto-compute derived fields
- `rename_field(old, new, scope)` - Bulk rename frontmatter fields
- Schema inheritance and composition

**v1.8.0 - Workflow Templates**
- Pre-built workflow templates for common business processes
- Workflow editor and customization
- Trigger-based automation

**v2.0 - Enterprise Features**
- Multi-vault support
- Team collaboration primitives
- Audit logging and compliance

## Contributing

Flywheel is open source and welcomes contributions. See [CONTRIBUTING.md](./CONTRIBUTING.md).

## License

MIT - see [LICENSE](./LICENSE)

## Links

- Documentation: [./docs](./docs/)
- MCP Server: [./packages/mcp-server](./packages/mcp-server/)
- Claude Plugin: [./packages/claude-plugin](./packages/claude-plugin/)
- Demo Vaults: [./demos](./demos/)
