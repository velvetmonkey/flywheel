> **Both Packages Required:** Flywheel (51 read-only tools) + [Flywheel-Crank](https://github.com/velvetmonkey/flywheel-crank) (11 mutation tools) work together. See the [Platform Installation Guide](docs/INSTALL.md) for your OS.

<div align="center">
  <img src="header.png" alt="Flywheel" width="256"/>
</div>

# Flywheel

### MCP server for markdown vault intelligence

[![MCP](https://img.shields.io/badge/MCP-Model%20Context%20Protocol-blueviolet.svg)](https://modelcontextprotocol.io/)
[![CI](https://github.com/velvetmonkey/flywheel/actions/workflows/ci.yml/badge.svg)](https://github.com/velvetmonkey/flywheel/actions/workflows/ci.yml)
[![npm version](https://img.shields.io/npm/v/@velvetmonkey/flywheel-mcp.svg)](https://www.npmjs.com/package/@velvetmonkey/flywheel-mcp)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache--2.0-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0)
[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-blue.svg)](https://github.com/velvetmonkey/flywheel)
[![Scale](https://img.shields.io/badge/scale-100k%20notes-brightgreen.svg)](./docs/SCALE_BENCHMARKS.md)

**Stop burning tokens. Start building agents.** Give Claude graph intelligence over your Obsidian vault without reading files.

## Verified Capabilities

✅ **100k Note Scale** - Index building and queries tested at 100,000 notes
✅ **51 Read-Only Tools** - Comprehensive graph intelligence without mutation risk
✅ **Cross-Platform** - Tested on Ubuntu, Windows, macOS (Intel + ARM)
✅ **Sub-Second Queries** - Graph traversal, backlinks, hub detection <100ms
✅ **Entity Detection** - Automatic extraction of people, projects, tech, acronyms

---

## See It Work

**Watch CI build a knowledge graph from scratch:**

[![Proof of Work](https://github.com/velvetmonkey/flywheel/actions/workflows/proof-of-work.yml/badge.svg)](https://github.com/velvetmonkey/flywheel/actions/workflows/proof-of-work.yml)

Every push:
1. Creates a vault from CSV seed data
2. Builds the entity index
3. Validates 100+ notes, 150+ wikilinks
4. Publishes metrics as artifacts

[View latest run →](https://github.com/velvetmonkey/flywheel/actions/workflows/proof-of-work.yml)

---

Claude reading files on every query? Those tokens add up fast.

Flywheel queries an in-memory index instead of reading files. Graph queries (backlinks, tags, tasks) return structured results without touching file content.

**The real win:** Your agents can now query your knowledge *hundreds of times* during long-running tasks without blowing up the context window.

---

## Quick Start

**Prerequisites:** Node.js 18+, Claude Code or MCP client, an Obsidian vault (or any markdown folder)

**1. Create `.mcp.json`** in your vault root:

```json
{
  "mcpServers": {
    "flywheel": {
      "command": "npx",
      "args": ["-y", "@velvetmonkey/flywheel-mcp"]
    }
  }
}
```

> **Windows:** Use `"command": "cmd", "args": ["/c", "npx", "-y", "@velvetmonkey/flywheel-mcp"]` with `"env": { "FLYWHEEL_WATCH_POLL": "true" }` for reliable file watching.
>
> **WSL:** Add `"env": { "FLYWHEEL_WATCH_POLL": "true" }` if your vault is on a Windows drive (`/mnt/c/...`). See [Configuration](docs/CONFIGURATION.md) for details.

**2. Restart Claude Code** and verify with `claude mcp list` — you should see `flywheel ✓`

That's it. Flywheel uses the current directory as your vault—no config needed.

See [Configuration](docs/CONFIGURATION.md) for environment variables, tool filtering, and platform setup.

---

## See It In Action

### Carter Consultancy: Meeting Prep in 30 Seconds

You're Carter, a solo consultant. Three active clients, $200K in annual revenue, and a meeting with Acme Corp in 10 minutes. You haven't looked at their file in weeks.

**The Prompt:**
```
You: What do I need to know about Acme Corp before this call?
```

**Claude Uses Flywheel:**
```
[search_notes: "Acme Corp"]
[get_backlinks: "clients/Acme Corp.md"]
[get_note_metadata: "clients/Acme Corp.md"]
```

**The Answer (2 seconds, ~200 tokens):**
```
Acme Corp - Quick Brief:
━━━━━━━━━━━━━━━━━━━━━━━━
Contact: Sarah Mitchell, VP Technology
Status: Active - Phase 2 of data migration

Current Project: [[Acme Data Migration]]
  Budget: $75,000 | Billed: $42,000
  Timeline: Oct 2025 - Mar 2026

Pending: [[INV-2025-048]] - $12,000 (December)
Opportunity: [[Acme Analytics Add-on]] - $35,000 proposal

Last touch: 2025-12-30
```

**Without Flywheel:** Claude reads 12 files (~6,000 tokens) to find this.
**With Flywheel:** Graph query returns structured data. 30× more efficient.

### Follow-Up: "What If They Go Amber?"

```
You: If Acme delays to Q3, what happens to my Q1 revenue?

Claude: [get_backlinks + frontmatter queries across projects/]

Impact Analysis:
━━━━━━━━━━━━━━━
If Acme Data Migration slips:
  - Q1 gap: $33,000 (remaining Acme budget)
  - Current Q1 pipeline: $42,000

Mitigation options:
  - [[Beta Corp Dashboard]] needs React help (understaffed)
  - [[Stacy Thompson]] at 40% utilization - available for reallocation

Your Q1 stays green if Beta Corp accelerates.
```

This is graph intelligence: backlinks, frontmatter queries, and relationship traversal—all without reading file contents.

### The Complete Picture

Flywheel gives you **eyes**: 51 read-only tools for querying your knowledge graph.

But reading isn't enough. When Carter finishes that call and needs to onboard a new project, update client files, and log the meeting—that's **writing**.

For mutations, see **[Flywheel-Crank](https://github.com/velvetmonkey/flywheel-crank)**: deterministic vault automation with auto-wikilinks, atomic commits, and policy-as-code.

**Eyes + Hands = Complete vault intelligence.**

---

## Try a Demo

5 production-ready vaults representing real knowledge work personas:

| Demo | Persona | Notes | Try Asking |
|------|---------|-------|------------|
| **[carter-strategy](demos/carter-strategy/)** | Solo Consultant | 32 | "How much have I billed Acme Corp?" |
| **[artemis-rocket](demos/artemis-rocket/)** | Aerospace Engineer | 65 | "What's blocking the propulsion milestone?" |
| **[startup-ops](demos/startup-ops/)** | SaaS Co-Founder | 31 | "Walk me through onboarding DataDriven" |
| **[nexus-lab](demos/nexus-lab/)** | PhD Researcher | 32 | "How does AlphaFold connect to my experiment?" |
| **[solo-operator](demos/solo-operator/)** | Content Creator | 19 | "What's my financial runway?" |

```bash
git clone https://github.com/velvetmonkey/flywheel.git
cd flywheel/demos/artemis-rocket && claude
```

---

## What This Unlocks

- **Graph intelligence** — backlinks, orphans, hubs, connection paths
- **Vault health monitoring** — find disconnected notes, stale hubs, broken links
- **Connection discovery** — "how does X relate to Y?" answered in milliseconds
- **Schema queries** on frontmatter without reading files
- **Agentic workflows** that query your knowledge hundreds of times without token bloat

---

## Why Markdown + Graph?

- **Git-native** — version-controlled knowledge
- **Plain text** — future-proof, zero lock-in
- **Privacy** — files stay local, only what you need gets sent
- **Editor-agnostic** — Obsidian, VSCode, Cursor, vim, whatever
- **AI-native** — 51 tools purpose-built for agent workflows

---

## Who Uses Flywheel?

**You might be:**

| Persona | Your Problem | Flywheel Gives You |
|---------|--------------|-------------------|
| 🧠 **PKM Practitioner** | Manual linking is tedious | Auto-wikilinks build connections as you write |
| 🤖 **Agent Builder** | AI burns tokens reading files | 51 graph queries, zero file reads |
| 🐵 **Chaos Monkey** | Markdown chaos, can't find anything | Structure emerges from motion |
| 💻 **Developer** | Code notes scattered across projects | Queryable second brain |
| 📊 **Knowledge Worker** | "Where's that decision from last month?" | Frontmatter + graph = instant retrieval |
| ✍️ **Writer/Researcher** | Missing connections between sources | Backlinks reveal unexpected paths |
| 👥 **Teams** | Shared vault coordination is messy | Multi-agent access to shared knowledge graph |
| 🎙️ **Voice-to-Vault** | Mobile capture lands in chaos | Whisper → Crank → auto-linked notes |

### Inspiration from Builders in Public

People doing interesting work with markdown knowledge bases:

- **Andy Matuschak** — [Evergreen notes](https://notes.andymatuschak.org/) on augmented cognition
- **Simon Willison** — [TIL](https://til.simonwillison.net/) public learning, Datasette creator
- **Maggie Appleton** — [Digital Gardeners](https://github.com/MaggieAppleton/digital-gardeners) community
- **Kepano** — [Obsidian Skills](https://github.com/kepano/obsidian-skills) for agent automation
- **Sonny Huynh** — [AI-Powered Second Brain](https://sonnyhuynhb.medium.com/i-built-an-ai-powered-second-brain-with-obsidian-claude-code-heres-how-b70e28100099) with Claude Code
- **MarkdownDB** — [Markdown as database](https://github.com/datopian/markdowndb) philosophy

### Get Involved

- [Star on GitHub](https://github.com/velvetmonkey/flywheel) — helps others discover the project
- [Report issues or share ideas](https://github.com/velvetmonkey/flywheel/issues) — bugs, features, workflow tips

---

## Prove It Yourself

Don't trust marketing. Run the tests:

```bash
# Clone the ecosystem
git clone https://github.com/velvetmonkey/flywheel
git clone https://github.com/velvetmonkey/flywheel-crank

# Run flywheel tests (395 tests - read tools, demos)
cd flywheel && npm install && npm test

# Run demo documentation tests
cd flywheel && npm run test:demos

# Run flywheel-crank tests (1,326 tests - mutations, scale, security)
cd ../flywheel-crank && npm install && npm test
```

**Total: 1,721 tests** proving the ecosystem works.

| Repo | Tests | Proves |
|------|-------|--------|
| **flywheel** | 395 | Graph queries, entity indexing, file watching |
| **flywheel-crank** | 1,326 | Mutations at scale, format preservation, security |

### Test Scripts

| Script | Purpose |
|--------|---------|
| `npm test` | Run all tests |
| `npm run test:demos` | Verify README examples against demo vaults |

---

## Docs

- **[Installation Guide](docs/INSTALL.md)** — Platform-specific setup (Windows, macOS, Linux, WSL)
- **[Configuration](docs/CONFIGURATION.md)** — Environment variables, tool presets, platform setup
- **[MCP Tools Reference](docs/MCP_REFERENCE.md)** — All 51 tools
- **[Query Guide](docs/QUERY_GUIDE.md)** — Patterns and examples
- **[How It Works](docs/HOW_IT_WORKS.md)** — Architecture and token savings
- **[Vault Health](docs/VAULT_HEALTH.md)** — Monitor and improve vault structure
- **[Performance](docs/PERFORMANCE.md)** — Benchmarks and optimization
- **[Privacy](docs/PRIVACY.md)** — Data handling and security
- **[Troubleshooting](docs/TROUBLESHOOTING.md)** — Common issues and fixes

---

macOS / Linux / WSL / Windows

Apache-2.0 License · [GitHub](https://github.com/velvetmonkey/flywheel) · [Issues](https://github.com/velvetmonkey/flywheel/issues)
