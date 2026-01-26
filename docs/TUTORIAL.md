# Flywheel Tutorial: 10 Minutes to Productivity

Get hands-on with Flywheel's MCP tools in 10 minutes.

---

## What You'll Learn

- Configure Flywheel MCP server
- Explore a knowledge graph
- Query your vault efficiently

---

## Part 1: Installation (2 min)

### Step 1: Create MCP Configuration

Add to `.mcp.json` in your vault root:

**Linux/macOS/WSL:**
```json
{
  "mcpServers": {
    "flywheel": {
      "command": "npx",
      "args": ["-y", "@bencassie/flywheel-mcp"]
    }
  }
}
```

**Windows (native):**
```json
{
  "mcpServers": {
    "flywheel": {
      "command": "cmd",
      "args": ["/c", "npx", "-y", "@bencassie/flywheel-mcp"]
    }
  }
}
```

### Step 2: Restart Claude Code

The MCP server loads on startup. After creating `.mcp.json`, restart Claude Code.

### Step 3: Verify Connection

Use the health check tool:

```
mcp__flywheel__health_check()
```

You should see vault stats including note count and link metrics.

---

## Part 2: Explore a Demo Vault (3 min)

Let's use the included demo vault to learn.

### Step 1: Open the Demo

```bash
cd demos/carter-strategy
```

Create `.mcp.json` with the configuration above, then restart Claude Code.

### Step 2: Check Vault Stats

```
mcp__flywheel__get_vault_stats()
```

You should see:
- Note count
- Total wikilinks
- Orphan notes
- Hub notes

### Step 3: Find Hub Notes

```
mcp__flywheel__find_hub_notes({ min_links: 5 })
```

Hub notes are your most connected knowledge - good entry points for understanding the vault.

### Step 4: Find Orphan Notes

```
mcp__flywheel__find_orphan_notes()
```

These are notes with no incoming links - they might need connections.

---

## Part 3: Graph Intelligence (3 min)

### Backlinks

```
mcp__flywheel__get_backlinks({ path: "Ben Carter" })
```

See all notes that reference Ben Carter.

### Path Finding

```
mcp__flywheel__get_link_path({ from: "Project Alpha", to: "Client ABC" })
```

Finds the shortest path of links between two notes.

### Common References

```
mcp__flywheel__get_common_neighbors({ note_a: "Sarah", note_b: "Mike" })
```

Find notes that multiple people or concepts reference together.

---

## Part 4: Schema Queries (2 min)

### Frontmatter Fields

```
mcp__flywheel__infer_folder_conventions({ folder: "projects" })
```

See all frontmatter fields used in a folder.

### Field Values

```
mcp__flywheel__get_field_values({ field: "status" })
```

See the vocabulary used across your vault.

### Filtered Search

```
mcp__flywheel__search_notes({ where: { "status": "blocked" } })
```

Query notes by frontmatter values.

---

## What's Next?

### On Your Own Vault

1. Navigate to your vault directory
2. Create `.mcp.json` with Flywheel config
3. Restart Claude Code
4. Run `mcp__flywheel__health_check()`

### Explore More Tools

| Tool | Purpose |
|------|---------|
| `get_recent_notes({ days: 7 })` | Notes modified this week |
| `get_stale_notes({ days: 30 })` | Important but neglected notes |
| `search_notes({ has_tag: "urgent" })` | Tag filtering |
| `search_notes({ folder: "meetings" })` | Folder filtering |

### Read More

- [ARCHITECTURE.md](ARCHITECTURE.md) - System design
- [MCP_REFERENCE.md](MCP_REFERENCE.md) - All 44 MCP tools

---

## Troubleshooting

### "MCP not connected"

1. Check `.mcp.json` exists in your vault root
2. Verify JSON syntax is valid
3. Restart Claude Code
4. Run `mcp__flywheel__health_check()`

### "Vault path not found"

Make sure you're in the correct directory. The working directory should be your vault root.

---

## Summary

In 10 minutes you learned to:

1. **Configure** - Add Flywheel to `.mcp.json`
2. **Verify** - Run `health_check()` to confirm connection
3. **Navigate** - Use `get_backlinks()`, `get_link_path()`, `get_common_neighbors()`
4. **Query** - Use `search_notes()`, `get_field_values()`, `infer_folder_conventions()`

Flywheel gives AI clients full intelligence over your markdown vault through 44 MCP tools.
