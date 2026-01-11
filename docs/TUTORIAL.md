# Flywheel Tutorial: 10 Minutes to Productivity

Get hands-on with Flywheel's core features in 10 minutes.

---

## What You'll Learn

- Install and configure Flywheel
- Explore a knowledge graph
- Query your vault efficiently

---

## Part 1: Installation (2 min)

### Step 1: Install the Plugin

```bash
/plugin marketplace add bencassie/flywheel
/plugin install flywheel@bencassie-flywheel
```

### Step 2: Setup Flywheel

Just say: **"setup flywheel"**

Claude will:
1. Detect your platform (Windows/macOS/Linux/WSL)
2. Generate the correct `.mcp.json` configuration
3. Ask you to confirm before writing
4. Validate the MCP connection
5. Show your vault stats

### Step 3: Restart if Needed

If the MCP wasn't already loaded, you'll need to restart Claude Code. After restart, say "setup flywheel" again to see your vault stats.

---

## Part 2: Explore a Demo Vault (3 min)

Let's use the included demo vault to learn.

### Step 1: Open the Demo

```bash
cd demos/carter-strategy
```

Then say: **"setup flywheel"**

You should see:
```
## Flywheel Connected!

### Your Vault
- **Notes**: 30 markdown files
- **Wikilinks**: 87 connections
- **Orphans**: 3 unlinked notes
- **Hub notes**: 2 highly connected
```

### Step 2: Find Hub Notes

Say: **"show hub notes"**

Hub notes are your most connected knowledge - good entry points for understanding the vault.

### Step 3: Find Orphan Notes

Say: **"find orphan notes"**

These are notes with no incoming links - they might need connections.

---

## Part 3: Graph Intelligence (3 min)

### Backlinks

Say: **"show backlinks for Ben Carter"**

See all notes that reference Ben Carter.

### Path Finding

Say: **"how do Project Alpha and Client ABC connect?"**

Finds the shortest path of links between two notes.

### Common References

Say: **"what do Sarah and Mike both link to?"**

Find notes that multiple people or concepts reference together.

---

## Part 4: Schema Queries (2 min)

### Frontmatter Fields

Say: **"what fields exist in projects/"**

See all frontmatter fields used in a folder.

### Field Values

Say: **"show all unique values for status"**

See the vocabulary used across your vault.

### Filtered Search

Say: **"find notes where status is blocked"**

Query notes by frontmatter values.

---

## What's Next?

### On Your Own Vault

```bash
cd /path/to/your/vault
# Say: "setup flywheel"
```

### Explore More Queries

| Say This | What Happens |
|----------|--------------|
| "show notes modified this week" | Temporal query |
| "find stale important notes" | High-connection, old modification |
| "find notes tagged #urgent" | Tag filtering |
| "list notes in meetings/" | Folder filtering |

### Read More

- [QUERY_GUIDE.md](QUERY_GUIDE.md) - Complete query reference
- [MCP_REFERENCE.md](MCP_REFERENCE.md) - All 40+ MCP tools

---

## Troubleshooting

### "MCP not connected"

1. Check `.mcp.json` exists in your vault root
2. Restart Claude Code
3. Say "setup flywheel" again

### "Vault path not found"

Make sure you're in the correct directory. The working directory should be your vault root.

---

## Summary

In 10 minutes you learned to:

1. **Install** - `/plugin install flywheel@bencassie-flywheel`
2. **Setup** - Say "setup flywheel"
3. **Navigate** - "what links to X", "how do A and B connect"
4. **Query** - Graph, temporal, and schema queries

Flywheel gives your AI full intelligence over your knowledge graph - just describe what you want in natural language.
