# Vault Health Guide

Monitor and improve the structural health of your knowledge graph.

---

## Why Vault Health Matters

Most file-based tools treat your vault as a filesystem. Flywheel treats it as a **knowledge graph**. This means you can measure and improve how well your notes connect.

A healthy vault has:
- **Few orphans** — most notes have at least one backlink
- **Active hubs** — central notes that are kept up-to-date
- **Good flow** — ideas connect outward, not just inward
- **No broken links** — every `[[wikilink]]` resolves to a real note

---

## Health Metrics

| Metric | What It Reveals | Why It Matters |
|--------|-----------------|----------------|
| **Orphan notes** | Notes with zero backlinks | Disconnected knowledge that needs integration |
| **Hub notes** | Notes with 10+ connections | Your vault's knowledge centers — keep them current |
| **Dead ends** | Notes linked TO but linking to nothing | Information sinks that should connect outward |
| **Stale hubs** | Important notes not updated recently | Critical knowledge drifting out of date |
| **Broken links** | Wikilinks pointing to non-existent notes | References that need to be fixed or created |

---

## Running a Health Check

Ask Claude to assess your vault:

```
You: Is my vault healthy?

Claude: Let me check the key metrics.
[uses get_orphan_notes, get_hub_notes, get_dead_ends]

Your vault has 847 notes:
- 12 orphan notes (no backlinks) - consider linking these
- 8 hub notes (10+ connections) - your knowledge centers
- 3 stale hubs not updated in 30+ days - may need attention

Would you like me to list the orphans?
```

### Quick Health Commands

| Ask Claude | What It Does |
|------------|--------------|
| "Find orphan notes" | Lists notes with zero backlinks |
| "Show hub notes" | Lists your most-connected notes (10+ links) |
| "Find dead ends" | Notes that receive links but don't link out |
| "Check for stale hubs" | Hub notes not updated in 30+ days |
| "Find broken links" | Wikilinks pointing to non-existent notes |
| "Suggest wikilinks" | Unlinked mentions that could become links |

---

## Fixing Common Issues

### Orphan Notes

**Problem:** Notes with zero backlinks are disconnected from your knowledge graph.

**Solution:**
1. Ask Claude: "Find orphan notes"
2. Review each one — is it worth keeping?
3. Link it from a relevant note, or
4. Delete it if it's no longer useful

```
You: Show me orphan notes in projects/

Claude: [uses find_orphan_notes]

Found 4 orphan notes in projects/:
- projects/old-idea.md - created 6 months ago, never linked
- projects/brainstorm-notes.md - has content but no connections
- projects/temp.md - looks like scratch notes
- projects/q2-planning.md - should probably link to quarterly-goals.md

Want me to suggest where to link these?
```

### Stale Hubs

**Problem:** Your most important notes haven't been updated recently.

**Solution:**
1. Ask Claude: "Find stale hub notes"
2. Review each hub — is the information current?
3. Update outdated sections
4. Add new links to recent related notes

```
You: Which of my hub notes are stale?

Claude: [uses find_hub_notes, filters by modification date]

3 hub notes haven't been updated in 30+ days:

- Team Roster.md (23 backlinks, last updated 45 days ago)
  → May be missing new team members

- Architecture Overview.md (18 backlinks, last updated 38 days ago)
  → Referenced by many docs, might have outdated info

- Q4 Goals.md (15 backlinks, last updated 62 days ago)
  → Quarter is over, needs update or archiving

Want me to show what's linking to these?
```

### Dead Ends

**Problem:** Notes that receive many links but don't link to anything else create information sinks.

**Solution:**
1. Ask Claude: "Find dead end notes"
2. Add outgoing links to related concepts
3. Consider if the note should be a hub or remain terminal

```
You: Find dead ends with more than 5 backlinks

Claude: [uses find_dead_ends]

Found 2 high-traffic dead ends:

- glossary/API.md (12 backlinks, 0 forward links)
  → Definition note - dead end is intentional

- concepts/authentication.md (8 backlinks, 0 forward links)
  → Should probably link to implementation notes

The glossary entry is fine as a terminal node.
The concepts note could benefit from connecting to your auth-related project notes.
```

### Broken Links

**Problem:** Wikilinks pointing to notes that don't exist.

**Solution:**
1. Ask Claude: "Find broken links"
2. Create the missing note, or
3. Fix the wikilink to point to the correct note

```
You: Are there any broken links?

Claude: [uses find_broken_links]

Found 3 broken wikilinks:

- meetings/2026-01-15.md links to [[John Smith]] (doesn't exist)
  → Did you mean [[John Smithson]]?

- projects/api-v2.md links to [[API Spec v2]] (doesn't exist)
  → Note was renamed to [[API Specification v2]]

- notes/ideas.md links to [[DELETEME]] (doesn't exist)
  → Looks like a cleanup artifact

Want me to suggest fixes?
```

---

## Health Monitoring Workflow

For ongoing vault health, establish a regular review:

### Weekly (5 minutes)
- "Show me new orphan notes" — integrate recent additions
- "Any new broken links?" — catch issues early

### Monthly (15 minutes)
- "Run a full health check" — get all metrics
- "Which hubs are stale?" — keep centers current
- "Find notes I haven't touched in 60 days" — review or archive

### Quarterly (30 minutes)
- "Analyze vault growth patterns" — see how your knowledge is evolving
- "Find clusters of related notes" — identify emerging topics
- "What's my most connected note?" — understand your knowledge centers

---

## What Other MCPs Don't Have

Generic file MCPs can read and write files. **Only Flywheel understands:**

- The **link structure** between your notes
- Which notes are **orphaned** vs **well-connected**
- How ideas **flow** through your vault via wikilinks
- When your **knowledge graph is degrading** (stale hubs, broken links)

This is the difference between a filesystem and a **second brain**.

---

## Related Docs

- **[MCP Tools Reference](MCP_REFERENCE.md)** — All health-related tools
- **[Query Guide](QUERY_GUIDE.md)** — More query patterns
- **[How It Works](HOW_IT_WORKS.md)** — Understanding the graph index
