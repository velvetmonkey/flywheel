# Flywheel Quickstart Guide

Get up and running with Flywheel in 5 minutes.

## Prerequisites

- Claude Code installed
- A markdown vault (Obsidian, plain folder, etc.)

## Installation

### 1. Configure MCP Server

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

**Windows:**
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

### 2. Install Plugin

In Claude Code:
```
/plugin marketplace add bencassie/flywheel
/plugin install flywheel@flywheel
```

### 3. Restart Claude Code

That's it!

## First Commands to Try

| Command | What it does |
|---------|--------------|
| `/onboard` | Guided introduction to your vault |
| `/vault-health` | Check vault health and get recommendations |
| `/vault-search <query>` | Search notes by title, tags, or content |
| `/auto-log <message>` | Add a timestamped log to today's daily note |

## Common Workflows

### Daily Note Workflow

```
/auto-log Finished implementing feature X
```
Adds a timestamped entry to your daily note.

```
/rollup daily
```
Roll up yesterday's logs into a summary.

### Knowledge Discovery

```
/vault-orphans
```
Find notes with no connections - prime candidates for linking.

```
/vault-hubs
```
Find your most connected notes - these are key concepts.

```
/vault-path [[Note A]] [[Note B]]
```
Find the shortest path between two notes.

### Schema Management

```
/vault-schema
```
See all frontmatter fields in use across your vault.

```
/vault-schema-check
```
Find inconsistencies (same field with different types).

```
/vault-field-values status
```
See all unique values for a specific field.

## Skill Categories

### Vault Health
- `/vault-health` - Comprehensive health check
- `/vault-orphans` - Notes with no backlinks
- `/vault-hubs` - Most connected notes
- `/vault-dead-ends` - Notes with backlinks but no outlinks

### Graph Queries
- `/vault-backlinks <note>` - What links to this note?
- `/vault-clusters` - Find note clusters
- `/vault-path <from> <to>` - Shortest path between notes
- `/vault-strength <note1> <note2>` - Connection strength

### Schema Tools
- `/vault-schema` - Analyze frontmatter usage
- `/vault-schema-check` - Find type inconsistencies
- `/vault-field-values <field>` - List all values

### Temporal
- `/vault-stale` - Find old notes that need updating
- `/vault-activity` - Recent activity summary
- `/vault-concurrent <note>` - Notes edited around same time

### Wikilinks
- `/vault-fix-links` - Find and fix broken links
- `/vault-suggest` - Suggest links for a note
- `/vault-unlinked-mentions` - Find unlinked mentions

### Tasks
- `/vault-tasks` - All tasks across vault
- `/vault-due` - Tasks with due dates
- `/task-add <note> <task>` - Add a task

### Automation
- `/auto-log <message>` - Add timestamped log entry
- `/rollup daily|weekly|monthly` - Roll up notes

## Next Steps

- Explore the [Demo Vaults](../demos/) for real-world examples
- Read the [Roadmap](./ROADMAP.md) for upcoming features
- Check the [Six Gates](../packages/claude-plugin/skills/_patterns/SIX_GATES.md) safety framework
