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

## What is Flywheel?

Flywheel is an AI-native business operating system built on plain markdown files. It combines:

- **Graph Intelligence** (MCP server) - AI understands your knowledge graph
- **Workflow Automation** (Claude plugin) - AI handles repetitive tasks
- **Safety Framework** - Six enforced gates make AI workflows reliable
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

---

## Quick Start

### 1. Install Plugin

```bash
/plugin marketplace add bencassie/flywheel
/plugin install flywheel@bencassie-flywheel
```

### Updating

Plugins don't auto-update. To get the latest version:

```bash
/plugin update flywheel@bencassie-flywheel
```

### 2. Setup & Onboard

Just say: **"setup flywheel"**

Claude will:
- Detect your platform (Linux/WSL/Windows/macOS)
- Configure `.mcp.json` correctly
- Validate the MCP connection
- Show your vault stats and next steps

### 3. Explore

Skills are triggered by natural language - just describe what you want:

```
"check vault health"     → Deep analysis with recommendations
"find orphan notes"      → Disconnected notes needing links
"do a rollup"            → Aggregate your notes automatically
"add log entry: fixed bug" → Append timestamped entry to daily note
```

### Try with a Demo Vault

```bash
cd demos/carter-strategy
# Then say: "setup flywheel"
```

**[Full Installation Guide →](docs/GETTING_STARTED.md)**

> **Note**: Skills are triggered by natural language, not slash commands.
> Just describe what you want - Claude matches your intent to the right skill.

---

## Why Flywheel?

### vs File-Centric Tools

**Before (Naive Approach)**:
```
Search: Grep everything
  Result: 47 files
  Read: All matches
  Tokens: 50,000+
  Time: 10+ minutes
```

**After (Graph-First with Flywheel)**:
```
Search: Semantic queries
  Result: 3 core notes + 12 refs
  Read: Only core (surgical)
  Tokens: ~5,000
  Time: 30 seconds
```

**10x token reduction. 20x faster. Full relationship context.**

### vs Other Tools

- **vs Notion**: You own your data (plain markdown, Git-friendly)
- **vs Salesforce**: No vendor lock-in, AI has direct access
- **vs Obsidian alone**: Add AI-powered workflows and automation
- **vs VSCode alone**: Add graph intelligence and relationship traversal

**The unlock**: Plain text markdown becomes a queryable, executable, automatable platform for running businesses.

---

## Key Features

### 1. Graph Intelligence (40+ MCP Tools)

Navigate your vault by relationships, not files:

```bash
get_backlinks({ path: "Project.md" })     # Who references this?
find_hub_notes({ min_links: 5 })          # Key concepts
search_notes({ has_tag: "active" })       # Semantic search
get_link_path({ from: "A.md", to: "B.md" }) # How do they connect?
```

**[Full Tool Reference →](docs/MCP_REFERENCE.md)** (coming soon)

### 2. Workflow Automation (33 Skills)

Automate repetitive tasks:

```bash
/vault-health        # Comprehensive diagnostics
/auto-log "entry"    # Timestamped daily notes
/rollup              # Daily → weekly → monthly
/vault-fix-links     # Fix broken wikilinks
```

**[Full Skill Reference →](docs/SKILLS_REFERENCE.md)** (coming soon)

### 3. Six Gates Safety Framework

**The Problem**: AI can corrupt files, skip steps, fail silently.

**The Solution**: Six enforced safety gates:

| Gate | Purpose | Enforces |
|------|---------|----------|
| 1. Read Before Write | Read state before mutation | ✓ BLOCKS |
| 2. File Exists Check | Validate Edit targets exist | ✓ BLOCKS |
| 3. Chain Validation | Verify multi-step operations | ✓ BLOCKS |
| 4. Mutation Confirm | User confirms writes | ✓ BLOCKS |
| 5. MCP Health Check | Verify MCP on session start | ⚠ WARNS |
| 6. Post-Write Verify | Validate writes succeeded | ⚠ WARNS |

**[Learn the Patterns →](docs/AGENTIC_PATTERNS.md)**

### 4. Bidirectional Bridge

**Key insight**: Wikilinks and frontmatter are two representations of the SAME information.

```markdown
# Prose → Frontmatter (add structure)
Client: [[Acme Corp]]
Status: Active

↓ Flywheel suggests

---
type: project
client: [[Acme Corp]]
status: active
---
```

```yaml
# Frontmatter → Wikilinks (add traversability)
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

---

## Demo Vaults

Try Flywheel with 4 real-world scenarios:

| Demo | Domain | Notes | Focus | README |
|------|--------|-------|-------|--------|
| **Artemis Rocket** | Aerospace startup | 65 | Graph patterns, vault health | [View](./demos/artemis-rocket/README.md) |
| **Carter Strategy** | Solo consultant | 30 | Tasks, schema, rollups | [View](./demos/carter-strategy/README.md) |
| **Nexus Lab** | Research lab | 30 | Relationships, citations | [View](./demos/nexus-lab/README.md) |
| **Startup Ops** | B2B SaaS startup | 30 | Bidirectional bridge, zones | [View](./demos/startup-ops/README.md) |

**[Try a Demo →](demos/README.md)**

---

## Documentation

| Topic | Link |
|-------|------|
| **Getting Started** | [30-second installation](docs/GETTING_STARTED.md) |
| **Agentic Patterns** | [How Flywheel makes AI reliable](docs/AGENTIC_PATTERNS.md) |
| **MCP Reference** | [All 40+ tools](docs/MCP_REFERENCE.md) (coming soon) |
| **Skills Reference** | [All 33 skills](docs/SKILLS_REFERENCE.md) (coming soon) |
| **Six Gates Safety** | [Enforced safety framework](docs/SIX_GATES.md) (coming soon) |
| **Architecture** | [System design](docs/ARCHITECTURE.md) (coming soon) |
| **Troubleshooting** | [Common issues](docs/TROUBLESHOOTING.md) (coming soon) |
| **Roadmap** | [Version history & future plans](docs/ROADMAP.md) |
| **Demo Vaults** | [Try it risk-free](demos/README.md) |

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Claude Code                           │
│  ┌───────────────────┬─────────────────────────────┐    │
│  │  Skills           │  Agents                     │    │
│  │  /vault-health    │  rollup-agent               │    │
│  │  /auto-log        │  achievement-agent          │    │
│  └────────┬──────────┴──────────┬──────────────────┘    │
└───────────┼─────────────────────┼──────────────────────┘
            │                     │
┌───────────▼─────────────────────▼──────────────────────┐
│               Flywheel MCP Server                      │
│  ┌────────────────────────────────────────────────┐    │
│  │  Graph Tools  │  Query Tools  │  Schema Tools  │    │
│  │  backlinks    │  search       │  validate      │    │
│  └────────────────────────────────────────────────┘    │
└───────────────────────────┬────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│              Markdown Vault                            │
│  .md files + wikilinks + YAML frontmatter              │
└────────────────────────────────────────────────────────┘
```

**Not tied to any specific UI** - works with Obsidian, VSCode, Cursor, or CLI.

---

## Development Status

**Current**: v1.10.0 - Update Notifications
**Next**: v2.0 - Enterprise Features

### Recent Updates

**v1.10.0** (2026-01-03)
- Update notifications on session start when new version available
- Copy-paste ready update command in notification box
- Daily check with local caching (no spam)

**v1.9.0** (2026-01-03)
- New `setup-flywheel` skill with 4-phase onboarding flow
- TUTORIAL.md and ARCHITECTURE.md documentation
- Multi-word trigger keywords (prevents false positives)
- "Where Does Output Go?" sections for mutation skills
- Section matching now case-insensitive and level-agnostic
- Slash commands for mutations (`/rollup`, `/fix-links`, `/normalize`)

**v1.8.0** (2026-01-03)
- 6 new skills: `/extract-actions`, `/weekly-review`, `/standup-rollup`, `/okr-review`, `/onboard-customer`, `/workflow-define`
- 5 new Gate 3 compliant agents for workflow automation
- 4 new templates: meeting, standup, OKR, customer onboarding

**v1.7.4** (2026-01-03)
- Fixed read-cache locking bug for parallel Reads
- Added Six Gates test suite

**v1.6.2** (2026-01-03)
- Gates 1, 2, 4 now BLOCK unsafe operations
- Gate 3 enforced at project level for agent compliance

**[Full Version History →](docs/ROADMAP.md)**

### Roadmap

**v2.0** - Enterprise Features
- Multi-vault support
- Team collaboration
- Audit logging

**[Detailed Roadmap →](docs/ROADMAP.md)**

---

## Platform Support

- ✅ macOS (native)
- ✅ Linux (native)
- ✅ Windows (requires `cmd /c` wrapper)
- ✅ WSL (requires `python-is-python3`)

**[Platform-Specific Setup →](docs/GETTING_STARTED.md#platform-specific-notes)**

---

## Contributing

Flywheel is open source and welcomes contributions:

- Report bugs: [GitHub Issues](https://github.com/bencassie/flywheel/issues)
- Suggest features: [GitHub Discussions](https://github.com/bencassie/flywheel/discussions)
- Contribute code: [CONTRIBUTING.md](./CONTRIBUTING.md)

---

## License

MIT - see [LICENSE](./LICENSE)

---

## Project Structure

```
flywheel/
├── packages/
│   ├── mcp-server/          # Graph + schema intelligence
│   └── claude-plugin/       # Workflows and automation
├── demos/
│   ├── artemis-rocket/      # Aerospace startup (65 notes)
│   ├── carter-strategy/     # Solo consultant (30 notes)
│   ├── nexus-lab/           # Research lab (30 notes)
│   └── startup-ops/         # B2B SaaS (30 notes)
└── docs/                    # Documentation
```

---

**Ready to get started?** → [Installation Guide](docs/GETTING_STARTED.md)

**Want to try it first?** → [Demo Vaults](demos/README.md)

**Learn the patterns?** → [Agentic Design](docs/AGENTIC_PATTERNS.md)
