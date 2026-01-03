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
│   └── artemis-rocket/      # First demo: aerospace startup
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

Provides automated workflows:
- Core: `auto-log`, `task-add`, `rollup`
- Vault health: `vault-health`, `vault-orphans`, `vault-hubs`, `vault-fix-links`
- Graph queries: `vault-backlinks`, `vault-clusters`, `vault-gaps`
- Schema tools: `frontmatter-validate`, `normalize-note`, `promote-to-frontmatter`

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

| Demo | Replaces | Key Insight |
|------|----------|-------------|
| **Artemis Rocket** | 200-person aerospace corp | Engineering at 10x efficiency |
| **Consulting Firm** | Partner-heavy firm | One person = 5-person team |
| **Startup Ops** | Founders doing everything | AI handles ops, humans do strategy |
| **Research Lab** | Manual literature review | 100 papers/week processed |

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

## Development Status

**v1.0** (In Progress):
- ✅ MCP server with graph intelligence
- ✅ Periodic note detection (zero-config)
- 🔄 Artemis Rocket demo vault
- ⏳ Bidirectional bridge (frontmatter ↔ wikilinks)

**v1.1** (Planned):
- Bidirectional translation tools
- Rich frontmatter queries
- Schema validation and suggestions

See [Roadmap](./docs/ROADMAP.md) for details.

## Contributing

Flywheel is open source and welcomes contributions. See [CONTRIBUTING.md](./CONTRIBUTING.md).

## License

MIT - see [LICENSE](./LICENSE)

## Links

- Documentation: [./docs](./docs/)
- MCP Server: [./packages/mcp-server](./packages/mcp-server/)
- Claude Plugin: [./packages/claude-plugin](./packages/claude-plugin/)
- Demo Vaults: [./demos](./demos/)
