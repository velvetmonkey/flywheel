# Flywheel Tutorial: 10 Minutes to Productivity

Get hands-on with Flywheel's core features in 10 minutes.

---

## What You'll Learn

- Install and configure Flywheel
- Explore a knowledge graph
- Run your first rollup
- Understand natural language skill invocation

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

### Step 2: Check Vault Health

Say: **"check vault health"**

This runs a comprehensive analysis:
- Graph statistics (links, orphans, hubs)
- Schema analysis (frontmatter patterns)
- Issues and recommendations

### Step 3: Find Hub Notes

Say: **"show hub notes"**

Hub notes are your most connected knowledge - good entry points for understanding the vault.

---

## Part 3: Graph Intelligence (2 min)

### Backlinks

Say: **"show backlinks for Ben Carter"**

See all notes that reference Ben Carter.

### Orphan Notes

Say: **"find orphan notes"**

These are notes with no incoming links - they might need connections.

### Path Finding

Say: **"how do Project Alpha and Client ABC connect?"**

Finds the shortest path of links between two notes.

---

## Part 4: Your First Rollup (3 min)

The rollup feature aggregates scattered daily notes into structured summaries.

### How Rollup Works

```
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
```

### Run the Rollup

Say: **"do a rollup"**

Claude will:
1. Ask to confirm scope (default: last 2 months)
2. Process daily notes → weekly summaries
3. Process weekly → monthly → quarterly → yearly
4. Extract achievements

### See the Results

Check the generated summary files:
- `weekly-notes/YYYY-WXX.md`
- `monthly-notes/YYYY-MM.md`
- `Achievements.md`

---

## What's Next?

### On Your Own Vault

```bash
cd /path/to/your/vault
# Say: "setup flywheel"
```

### Explore More Skills

All skills are triggered by natural language:

| Say This | What Happens |
|----------|--------------|
| "add log entry: finished feature X" | Appends to today's daily note |
| "find broken links" | Scans for dead wikilinks |
| "extract actions from meeting" | Pulls action items from meeting notes |
| "review my OKRs" | Score quarterly objectives |

### Read More

- [AGENTIC_PATTERNS.md](AGENTIC_PATTERNS.md) - Understand how Flywheel makes AI reliable
- [ARCHITECTURE.md](ARCHITECTURE.md) - System design deep dive
- [SKILLS_REFERENCE.md](SKILLS_REFERENCE.md) - All 49 skills

---

## Troubleshooting

### "MCP not connected"

1. Check `.mcp.json` exists in your vault root
2. Restart Claude Code
3. Say "setup flywheel" again

### "Vault path not found"

Make sure you're in the correct directory. The working directory should be your vault root.

### "No daily notes found"

Flywheel auto-detects your daily notes folder. If you use a non-standard structure, check that you have files matching `YYYY-MM-DD.md` pattern.

---

## Summary

In 10 minutes you learned to:

1. **Install** - `claude plugin install flywheel@flywheel`
2. **Setup** - Say "setup flywheel"
3. **Explore** - "check vault health", "find orphan notes"
4. **Rollup** - "do a rollup" to aggregate notes
5. **Navigate** - "what links to X", "how do A and B connect"

Flywheel gives your AI full intelligence over your knowledge graph - just describe what you want in natural language.
