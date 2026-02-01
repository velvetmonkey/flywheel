> **Part of the Flywheel Suite:** This is the read-only graph intelligence server (the "Eyes"). See [Flywheel Crank](https://github.com/velvetmonkey/flywheel-crank) (the "Hands") for safe vault mutations with policies and auto-commit. Read [The Flywheel Platform](https://github.com/velvetmonkey/flywheel-crank/blob/main/docs/PLATFORM.md) for the full architecture.

<div align="center">
  <img src="header.png" alt="Flywheel" width="256"/>
</div>

# Flywheel

### Stop burning tokens. Start building agents.

[![npm version](https://img.shields.io/npm/v/@velvetmonkey/flywheel-mcp.svg)](https://www.npmjs.com/package/@velvetmonkey/flywheel-mcp)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache--2.0-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0)
[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-blue.svg)](https://github.com/velvetmonkey/flywheel)

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

### Finding Your Tasks

**Without Flywheel:** Claude reads through notes to find tasks—and re-reads them for follow-up queries.
**With Flywheel:** Queries the frontmatter index. Repeated lookups cost almost nothing.

```
You: Find all my tasks tagged #urgent across all notes

Claude: [uses get_all_tasks with filter]

Found 7 urgent tasks:
- [ ] Deploy API to prod #urgent (project-alpha.md, due tomorrow)
- [ ] Review security audit #urgent (security-notes.md, overdue)
- [ ] Call client about invoice #urgent (client-acme.md)
- [ ] Fix production bug #urgent (bug-tracker.md, due today)
...

3 are overdue - want me to prioritize them?
```

### Last-Minute Meeting Prep

**Without Flywheel:** Claude reads through files to gather context.
**With Flywheel:** Targeted queries return just what's needed—fast and token-efficient.

```
You: I have a client meeting in 10 minutes - show me everything about Acme Corp

Claude: [uses search_notes + get_backlinks]

Found 12 notes in 2 seconds:
- Client: Acme Corp.md (main hub, 8 backlinks)
- 2025-12-15 Acme Kickoff.md
- Acme Invoice #4521.md (pending payment)
- Acme Feature Requests.md (3 open items)
- 2026-01-20 Acme Standup.md (last meeting notes)
...

Want a quick summary before you join?
```

### Discovering Relationships

```
You: What connects my meeting notes to the Q4 strategy?

Claude: [uses get_shortest_path]

Found a 3-hop connection:
  Meeting Notes → [[Client Feedback]] → [[Product Roadmap]] → Q4 Strategy
```

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

## Docs

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
