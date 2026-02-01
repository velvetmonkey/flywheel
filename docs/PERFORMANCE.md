# Flywheel Performance Guide

Benchmarks, optimization tips, and scaling characteristics.

---

## Table of Contents

- [Performance Summary](#performance-summary)
- [Benchmark Methodology](#benchmark-methodology)
- [Index Build Performance](#index-build-performance)
- [Query Performance](#query-performance)
- [Memory Usage](#memory-usage)
- [Scaling Characteristics](#scaling-characteristics)
- [Breaking Points & Limitations](#breaking-points--limitations)
- [Optimization Tips](#optimization-tips)

---

## Performance Summary

**Token Savings (Realistic Estimates)**

*These estimates assume Claude would read 10-30 relevant files without Flywheel, not the entire vault.*

| Operation | Without Flywheel | With Flywheel | Savings |
|-----------|-----------------|---------------|---------|
| Find backlinks | Read ~10-20 files to find mentions (~5,000 tokens) | Index query (~150 tokens) | ~30x |
| Tasks by due date | Read ~10-30 notes with tasks (~8,000 tokens) | Frontmatter query (~300 tokens) | ~25x |
| Notes by tag | Read ~10-20 tagged files (~5,000 tokens) | Tag index (~150 tokens) | ~30x |
| Content search | Read matching files (~3,000 tokens) | Find files + still read them (~2,500 tokens) | ~1.2x |

**Important:** Content searches don't save much—Claude still needs to read file contents. The big wins are structure queries that avoid file reads entirely.

**Token efficiency = Cost efficiency:**
- Fewer tokens → cheaper API costs
- Fewer tokens → faster responses
- Fewer tokens → more queries per context window

---

## Benchmark Methodology

### Test Environment

**TODO: Actual benchmarks required. Marking estimates below.**

Estimated based on:
- Apple M1 MacBook Pro (16GB RAM)
- SSD storage
- Node.js 20.x
- Vault on local filesystem (not network drive)

All timing numbers below are **estimates** pending proper benchmarking.

### Benchmark Vaults

Test vault characteristics:

| Size | Notes | Total Size | Avg Note Size | Links/Note | Tags/Note |
|------|-------|-----------|--------------|------------|-----------|
| Small | 1,000 | ~10 MB | 10 KB | 5 | 2 |
| Medium | 5,000 | ~50 MB | 10 KB | 8 | 3 |
| Large | 10,000 | ~100 MB | 10 KB | 10 | 3 |
| XL | 50,000 | ~500 MB | 10 KB | 12 | 4 |

---

## Index Build Performance

### Initial Index Build

Time to build index from scratch (cold start):

| Vault Size | Est. Build Time | Est. Memory Used | Notes/Second |
|------------|----------------|-----------------|--------------|
| 1,000 notes | ~2-5s | ~50-80 MB | ~300/s |
| 5,000 notes | ~10-20s | ~150-200 MB | ~300/s |
| 10,000 notes | ~30-60s | ~300-400 MB | ~200/s |
| 50,000 notes | ~3-5 min | ~1-2 GB | ~200/s |

**Factors affecting speed:**
- Disk speed (SSD vs HDD)
- Note complexity (lots of links/frontmatter)
- CPU (single-threaded indexing)

### Incremental Updates (File Watching)

When a file changes, Flywheel re-indexes just that file:

| Operation | Est. Time | Impact |
|-----------|-----------|--------|
| Single note edit | <100ms | Instant |
| Create new note | <100ms | Instant |
| Delete note | <50ms | Instant |
| Rename note | ~200ms | Re-index backlinks |

**Why it's fast:** Only changed files are re-parsed. Index structure is in-memory.

---

## Query Performance

### Graph Queries

Fast queries (hit index only, no file I/O):

| Query Type | Est. Time | Scales With |
|------------|-----------|-------------|
| `get_backlinks` | <10ms | # of backlinks |
| `get_forward_links` | <5ms | # of links in note |
| `find_hub_notes` | 10-50ms | Vault size |
| `find_orphan_notes` | 10-50ms | Vault size |
| `get_shortest_path` | 10-100ms | Graph connectivity |

**Characteristics:**
- O(1) for direct lookups (backlinks, forward links)
- O(n) for full-vault scans (hub notes, orphans)
- O(n log n) for shortest path (graph traversal)

### Frontmatter Queries

Medium queries (index + minimal parsing):

| Query Type | Est. Time | Scales With |
|------------|-----------|-------------|
| `query_notes` (frontmatter filter) | 10-100ms | # matching notes |
| `get_notes_by_tag` | 10-50ms | # tagged notes |
| `get_tasks_with_due_dates` | 20-100ms | # tasks |

**Why fast:** Frontmatter is cached in index. No full file read.

### Content Search

Content search queries with FTS5 full-text search:

| Query Type | Est. Time | Scales With |
|------------|-----------|-------------|
| `full_text_search` (FTS5) | 10-50ms | Index size |
| `search_notes` (frontmatter) | 10-100ms | # matching notes |
| `get_section_content` | 50-200ms | File size |

**FTS5 Performance:**
- Index builds on first search or manual trigger
- Subsequent searches are sub-100ms (SQLite FTS5)
- Supports stemming, phrases, boolean operators
- Index stored in `.claude/vault-search.db`

**Why FTS5 is fast:** SQLite FTS5 uses inverted indexes. Query time is O(log n) not O(n).

**Optimization:** Use FTS5 for content search, graph queries for relationships.

---

### Real-World Query Comparison

**Scenario:** "Find all notes about Project Alpha"

**Method 1: Content search (slow)**
```
search_notes("Project Alpha")
→ Reads 10,000 notes to find matches
→ ~500ms, ~100,000 tokens processed
```

**Method 2: Graph query (fast)**
```
get_backlinks("Project Alpha")
→ Index lookup only
→ ~10ms, ~50 tokens returned
```

**Graph queries skip file reading.** The backlink lookup returns structured results in ~10ms without reading any files from disk.

---

## Memory Usage

### Baseline Memory

Flywheel server (idle):

| Vault Size | Est. RAM Usage |
|------------|---------------|
| 1,000 notes | ~50-80 MB |
| 5,000 notes | ~150-250 MB |
| 10,000 notes | ~300-500 MB |
| 50,000 notes | ~1-2 GB |

**What's in memory:**
- Index structure (links, tags, frontmatter)
- Entity cache (wikilink mapping)
- File watcher state
- MCP server overhead

### Memory Growth

**Linear scaling:** Memory usage grows roughly linearly with vault size.

**Rule of thumb:** ~10-20 KB RAM per note.

**Factors increasing memory:**
- Many links per note
- Large frontmatter
- Many tags
- Deep folder structure

---

### Memory Optimization

**If running low on RAM:**

1. **Exclude folders:**
   ```json
   {
     "env": {
       "FLYWHEEL_EXCLUDE_PATTERNS": "archive/,attachments/"
     }
   }
   ```
   Reduces indexed notes → less memory.

2. **Restart server periodically:**
   - Clears any memory leaks
   - Rebuilds index from scratch

3. **Split vault:**
   - Multiple smaller vaults use less memory each
   - Trade-off: Can't query across vaults

---

## Scaling Characteristics

### Small Vaults (1-5k notes)

**Performance:** Excellent
- Index builds in seconds
- All queries <50ms
- Negligible memory usage
- No optimization needed

**Use case:** Personal knowledge management, small teams

---

### Medium Vaults (5-15k notes)

**Performance:** Very Good
- Index builds in 30-60s
- Graph queries <100ms
- Content search ~200-500ms
- Moderate memory (~500MB)

**Optimization tips:**
- Exclude archive folders
- Use graph queries over content search
- Consider SSD if on HDD

**Use case:** Power users, researchers, small company wikis

---

### Large Vaults (15-50k notes)

**Performance:** Good (with tuning)
- Index builds in 1-5 min
- Graph queries <200ms
- Content search 500ms-2s
- High memory (1-2GB)

**Optimization required:**
- Exclude non-essential folders
- Use targeted queries (filter by folder/tag)
- Increase Node.js heap size if needed:
  ```json
  {
    "env": {
      "NODE_OPTIONS": "--max-old-space-size=4096"
    }
  }
  ```

**Use case:** Large company wikis, extensive research databases

---

### Very Large Vaults (50k+ notes)

**Performance:** TODO: Needs testing

**Expected issues:**
- Long index build times (>5 min)
- High memory usage (>2GB)
- Slower queries on full-vault operations
- File watcher may struggle with many concurrent changes

**Recommendations:**
- **Split vault** into multiple smaller vaults by topic/year
- Use aggressive folder exclusions
- Consider dedicated machine for Flywheel server
- **May hit breaking points** - see below

---

## Breaking Points & Limitations

### Theoretical Limits

**TODO: Requires stress testing**

Estimated breaking points:

| Limit | Est. Threshold | Symptom |
|-------|---------------|---------|
| Max notes | ~100,000 | Index build >10 min, high memory |
| Max links/note | ~500 | Slow graph queries |
| Max file size | ~10 MB/note | Slow content reads |
| Max backlinks/note | ~1,000 | Slow backlink queries |
| Max frontmatter fields | ~100 | Slow frontmatter parsing |

**Real-world usage:** Most vaults stay well below these limits.

---

### Known Bottlenecks

1. **Index build is single-threaded**
   - Can't use multiple CPU cores
   - Limited by single-core speed

2. **File watching on large vaults**
   - OS limits on inotify watchers (Linux)
   - Performance degrades with 50k+ files

3. **FTS5 index requires rebuild**
   - Index auto-rebuilds when stale (>1 hour)
   - Manual rebuild available via `rebuild_search_index`
   - Index stored locally in `.claude/vault-search.db`

4. **Memory growth**
   - All index data kept in RAM
   - No disk-based index (by design - speed)

---

### What Flywheel Does NOT Optimize

**Semantic search:**
- Flywheel has no embeddings or vector search
- Can't find "similar notes" conceptually
- Use OpenAI embeddings separately if needed

**Complex regex:**
- Basic text search only
- No advanced query languages (SQL, GraphQL)

**Cross-vault queries:**
- Each Flywheel instance = one vault
- Can't query across multiple vaults

See [Limitations](./LIMITATIONS.md) for full details.

---

## Optimization Tips

### 1. Use Graph Queries Over Content Search

❌ **Slow:**
```
"Search all my notes for mentions of Project Alpha"
→ search_notes("Project Alpha")
→ Reads thousands of files
```

✅ **Fast:**
```
"What links to Project Alpha?"
→ get_backlinks("Project Alpha")
→ Index lookup only
```

**Result:** Graph queries return in milliseconds without reading file content.

---

### 2. Filter Queries Aggressively

❌ **Slow:**
```
get_all_tasks()
→ Returns every task in vault (could be thousands)
```

✅ **Fast:**
```
get_tasks_with_due_dates(
  after: "2026-01-29",
  before: "2026-02-05"
)
→ Returns only tasks due this week
```

**Result:** Faster response, fewer tokens, more relevant results.

---

### 3. Exclude Irrelevant Folders

```json
{
  "env": {
    "FLYWHEEL_EXCLUDE_PATTERNS": "archive/,templates/,attachments/,_private/"
  }
}
```

**Benefits:**
- Faster index builds
- Less memory usage
- Cleaner query results (no archive spam)

---

### 4. Use SSD Storage

**Impact:** 3-5x faster index builds on SSD vs HDD.

**Avoid:**
- Network drives (10-100x slower)
- Cloud sync folders during indexing (file lock delays)
- WSL `/mnt/c/` paths (slow on Windows)

---

### 5. Limit Result Sets

```
search_notes("term", limit: 10)
```

Instead of returning 1,000 matches, return top 10.

**Benefits:**
- Faster query
- Fewer tokens
- Easier for Claude to process

---

### 6. Restart Server Periodically

If running 24/7, restart weekly:
```
ctrl+c (in Claude Code)
Restart Claude Code
```

**Why:** Clears memory leaks, rebuilds index cleanly.

---

### 7. Tune Node.js Heap

For large vaults:
```json
{
  "env": {
    "NODE_OPTIONS": "--max-old-space-size=4096"
  }
}
```

Allows Node.js to use up to 4GB RAM (default is ~1.5GB).

---

## Comparing to Alternatives

### vs. Reading Files Directly (Claude Code's Edit tool)

| Operation | File Reading | Flywheel | Speedup |
|-----------|-------------|----------|---------|
| Find backlinks | Read ~10-20 files | Index query | ~30x |
| Count notes | `ls` + count | `get_vault_stats` | ~10x |
| Find tasks | Read ~10-30 files | Frontmatter query | ~25x |

**When file reading is better:**
- Need full file content
- One-time operation
- Small vault (<100 notes)

**When Flywheel is better:**
- Repeated queries
- Graph operations
- Large vaults

---

### vs. Dataview (Obsidian plugin)

| Aspect | Dataview | Flywheel |
|--------|----------|----------|
| **Speed** | Fast (in-app) | Fast (MCP) |
| **Context** | Obsidian UI | AI agents |
| **Token cost** | N/A | Low (~50 tokens/query) |
| **Query language** | DQL (custom) | Natural language (Claude) |

**Flywheel advantage:** Works outside Obsidian, AI-native.

**Dataview advantage:** Richer query language, UI integration.

See [Comparison Guide](./COMPARISON.md) for full breakdown.

---

## Monitoring Performance

### Manual Timing

Use `health_check` to see index age:
```json
{
  "status": "healthy",
  "index_age_seconds": 45
}
```

If `index_age_seconds` > 60, index may be stale (file watching issue).

### Debug Logging

```json
{
  "env": {
    "DEBUG": "flywheel:performance"
  }
}
```

Shows query timing:
```
flywheel:performance search_notes took 234ms
flywheel:performance get_backlinks took 12ms
```

---

## Summary

**Flywheel's performance sweet spot:**
- Vaults: 1,000 - 10,000 notes
- Queries: Graph operations, frontmatter filters
- Hardware: SSD, 8GB+ RAM

**Key insight:** Flywheel trades memory for speed. Graph queries (~30x faster) avoid file I/O entirely. Content searches still need file reads.

**When to optimize:** If queries take >500ms, or index build >5 min, see [Optimization Tips](#optimization-tips).

**When Flywheel isn't enough:** See [Limitations](./LIMITATIONS.md) for alternative approaches.

---

## See Also

- [Troubleshooting](./TROUBLESHOOTING.md) - Performance degradation issues
- [Configuration](./CONFIGURATION.md) - Tuning options
- [Limitations](./LIMITATIONS.md) - Scaling boundaries
- [Architecture](./ARCHITECTURE.md) - Why it's fast
