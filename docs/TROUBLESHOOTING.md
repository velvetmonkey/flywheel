# Flywheel Troubleshooting Guide

Common issues, root causes, and fixes for Flywheel MCP server.

---

## Table of Contents

- [Quick Diagnostics](#quick-diagnostics)
- [Index Issues](#index-issues)
- [File Watching Problems](#file-watching-problems)
- [Query Errors](#query-errors)
- [Performance Degradation](#performance-degradation)
- [Authentication & MCP Connection](#authentication--mcp-connection)
- [Platform-Specific Issues](#platform-specific-issues)
- [Debug Mode](#debug-mode)

---

## Quick Diagnostics

### Is Flywheel Running?

```bash
claude mcp list
```

Expected output:
```
flywheel ✓
```

If you see `flywheel ✗` or it's missing:
- Check `.mcp.json` syntax
- Verify Node.js 18+ installed: `node --version`
- Check Flywheel installation: `npx @velvetmonkey/flywheel-mcp --version`

### Health Check

Ask Claude:
```
Call health_check tool
```

Expected response:
```json
{
  "status": "healthy",
  "vault_path": "/path/to/vault",
  "notes_indexed": 1234,
  "index_age_seconds": 45
}
```

If status is not "healthy", see [Index Issues](#index-issues).

---

## Index Issues

### "Index is stale" / "Index out of date"

**Symptom:** Query results don't reflect recent changes.

**Cause:** File watcher missed an update, or index hasn't rescanned.

**Fix:**

1. **Force index rebuild:**
   ```
   Ask Claude: "Call rebuild_index tool"
   ```

2. **Check file watcher status:**
   - Look for "file watcher initialized" in server logs
   - Verify vault path is correct: `health_check` returns expected path

3. **Restart the MCP server:**
   - Exit Claude Code
   - Restart Claude Code
   - First query will trigger index build

**Prevention:**
- Keep vault size reasonable (see [Performance](#performance-degradation))
- Avoid operations that create/delete many files rapidly
- Use Flywheel Crank for mutations (auto-invalidates index)

---

### Index Corruption Recovery

**Symptom:** 
- Server crashes on startup
- `health_check` returns errors
- Queries fail with internal errors

**Error example:**
```
Error: ENOENT: no such file or directory
at Index.loadCache (/path/to/flywheel/index.js:123)
```

**Cause:** Cached index state doesn't match vault structure (files deleted outside Flywheel, vault moved, etc.)

**Recovery steps:**

1. **Delete cache files:**
   ```bash
   rm -rf /path/to/vault/.claude/wikilink-entities.json
   ```

2. **Restart server:**
   - Exit Claude Code
   - Restart Claude Code
   - Server will rebuild index from scratch

3. **Verify health:**
   ```
   Ask Claude: "Call health_check"
   ```

**If still failing:**
- Check vault path in `.mcp.json` or environment variable
- Verify vault directory exists and is readable
- Check for symlinks or mount issues (especially WSL/network drives)

---

### "No notes found" / Empty Index

**Symptom:** `get_vault_stats` shows `notes_indexed: 0`

**Causes:**

1. **Wrong vault path:**
   - Check `health_check` output
   - Verify `.mcp.json` working directory or `OBSIDIAN_VAULT_PATH` env var
   - Ensure path uses absolute paths or correct relative path

2. **No markdown files in vault:**
   - Flywheel only indexes `.md` files
   - Check `find /path/to/vault -name "*.md" | wc -l`

3. **File permissions:**
   - Ensure Flywheel can read vault files
   - Check `ls -la /path/to/vault` for permission issues

**Fix:**
```json
{
  "mcpServers": {
    "flywheel": {
      "command": "npx",
      "args": ["-y", "@velvetmonkey/flywheel-mcp"],
      "env": {
        "OBSIDIAN_VAULT_PATH": "/absolute/path/to/vault"
      }
    }
  }
}
```

---

## File Watching Problems

### Changes Not Detected

**Symptom:** Edit a file, but queries don't reflect the change.

**Debugging:**

1. **Check file watcher platform:**
   - macOS: Uses FSEvents (reliable)
   - Linux: Uses inotify (reliable)
   - Windows: Uses ReadDirectoryChangesW (can miss rapid changes)

2. **Test detection:**
   - Create a new file: `test-watch.md`
   - Call `get_recent_notes` with days: 1
   - Should appear in results within 1-2 seconds

**Workarounds:**

- Call `rebuild_index` after batch operations
- Restart server if stuck
- Use Crank for mutations (invalidates index automatically)

**Known issues:**

| Platform | Issue | Workaround |
|----------|-------|------------|
| WSL2 | Doesn't detect changes to `/mnt/c/` paths | Use Linux filesystem path |
| Network drives | Slow/missing events | Use local vault copy |
| Dropbox/Sync | Rapid changes confuse watcher | Pause sync during batch ops |

---

### File Watcher Crashes

**Error example:**
```
Error: ENOSPC: System limit for number of file watchers reached
```

**Cause:** Linux inotify limit exceeded (common with large vaults).

**Fix:**
```bash
# Check current limit
cat /proc/sys/fs/inotify/max_user_watches

# Increase limit (temporary)
sudo sysctl fs.inotify.max_user_watches=524288

# Permanent fix
echo "fs.inotify.max_user_watches=524288" | sudo tee -a /etc/sysctl.conf
```

**Alternative:** Disable file watching and rebuild manually:
```json
{
  "env": {
    "FLYWHEEL_WATCH": "false"
  }
}
```
(Requires manual `rebuild_index` calls after changes)

---

## Query Errors

### "Wikilink false positives" / "Entity not found"

**Symptom:** `[[Link Name]]` doesn't match expected note.

**Cause:** Multiple notes with similar names, or alias matching unexpected file.

**Example:**
```
Query: Get backlinks for [[John]]

Results include:
- john-smith.md (title: "John Smith")
- john-doe.md (title: "John Doe")  
- meeting-notes.md (contains: alias: ["John"])

All three match "John" - which one did you want?
```

**Solutions:**

1. **Use full title:**
   ```
   Get backlinks for [[John Smith]]
   ```

2. **Use file path:**
   ```
   Get section content from "people/john-smith.md"
   ```

3. **Check entity cache:**
   ```bash
   cat /path/to/vault/.claude/wikilink-entities.json
   ```
   Shows all entity→file mappings.

4. **Disambiguate aliases:**
   - Avoid generic aliases like "John" if multiple Johns exist
   - Use full names in aliases field

---

### Frontmatter Query Failures

**Error:**
```
Error: Field 'status' not found in schema
```

**Cause:** Queried frontmatter field doesn't exist in any indexed notes.

**Fix:**

1. **Check available fields:**
   ```
   Ask Claude: "What frontmatter fields exist in my vault?"
   Tool: get_vault_stats
   Look at: frontmatter_fields array
   ```

2. **Verify field spelling:**
   - Case-sensitive: `Status` ≠ `status`
   - Check for typos

3. **Check notes have frontmatter:**
   ```yaml
   ---
   status: active
   ---
   ```

---

### "Too many results" / Query Timeout

**Symptom:** Query hangs or returns "Result set too large"

**Cause:** Query matched too many notes (e.g., search for common word).

**Solutions:**

1. **Add filters:**
   ```
   Instead of: search_notes("meeting")
   Try: search_notes("meeting", folder: "2026/")
   ```

2. **Use more specific queries:**
   ```
   Instead of: search_notes("project")
   Try: query_notes(frontmatter: {project: "Alpha"})
   ```

3. **Limit results:**
   ```
   search_notes("term", limit: 10)
   ```

4. **Use graph queries instead of content search:**
   ```
   Instead of: Search all notes for "Project Alpha"
   Try: get_backlinks("Project Alpha")
   ```

---

## Performance Degradation

### Slow Index Builds

**Symptom:** Server takes >30s to start, or `rebuild_index` is slow.

**Benchmarks (validated via vault-core):**

| Vault Size | Expected Build Time | Notes |
|------------|-------------------|-------|
| 1,000 notes | <1s | Fast |
| 5,000 notes | ~5s | Fast |
| 10,000 notes | ~10s | Good |
| 50,000 notes | ~15s | Good |
| 100,000 notes | <30s | Validated threshold |

**Optimization tips:**

1. **Exclude folders:**
   ```json
   {
     "env": {
       "FLYWHEEL_EXCLUDE_PATTERNS": "archive/,templates/,attachments/"
     }
   }
   ```

2. **Use SSD storage:**
   - Avoid network drives
   - Avoid spinning disks
   - WSL: Use native Linux filesystem

3. **Reduce vault size:**
   - Archive old notes
   - Split vaults by topic/year
   - Move attachments outside vault

---

### High Memory Usage

**Symptom:** Server uses >500MB RAM.

**Cause:** Large vault, many entities cached, or memory leak.

**Expected memory usage (validated via vault-core benchmarks):**

| Vault Size | Expected RAM |
|------------|-------------|
| 1,000 notes | ~100 MB |
| 5,000 notes | ~200 MB |
| 10,000 notes | ~400 MB |
| 50,000 notes | ~800 MB |
| 100,000 notes | ~1.5 GB |

**Mitigation:**

1. **Restart server:**
   - Memory is released
   - Index rebuilds from disk

2. **Reduce cache size:**
   - TODO: Add cache size config option

3. **Split vault:**
   - Multiple smaller vaults use less memory each

---

### Slow Queries

**Symptom:** Individual queries take >5 seconds.

**Causes:**

1. **Content search on large vault:**
   - `search_notes` scans file contents
   - Solution: Use graph queries instead

2. **Complex graph queries:**
   - `get_shortest_path` with deep graphs
   - `find_hub_notes` with thousands of backlinks
   - Solution: Add limits, filter by folder

3. **Disk I/O bottleneck:**
   - Network drive
   - Spinning disk
   - Solution: Move vault to SSD

**Debug:**
- Enable debug logging (see [Debug Mode](#debug-mode))
- Check which tool calls are slow
- Optimize query patterns

---

## Authentication & MCP Connection

### "MCP server not found"

**Error:**
```
Error: Unable to connect to MCP server 'flywheel'
```

**Causes & fixes:**

1. **`.mcp.json` not found:**
   - Must be in vault root (where you run `claude`)
   - Or in `~/.config/claude/` for global config

2. **Invalid JSON syntax:**
   ```bash
   cat .mcp.json | jq .
   # Should pretty-print JSON. If error, fix syntax.
   ```

3. **Wrong command:**
   - macOS/Linux: `"command": "npx"`
   - Windows: `"command": "cmd"` with `"/c"` arg

4. **npx not in PATH:**
   ```bash
   which npx
   # Should show path. If not, install Node.js.
   ```

---

### "Permission denied"

**Error:**
```
Error: spawn npx EACCES
```

**Fix:**
```bash
chmod +x $(which npx)
```

Or reinstall Node.js with proper permissions.

---

### MCP Protocol Errors

**Error:**
```
Error: Invalid MCP response: Expected JSON-RPC 2.0 format
```

**Causes:**

1. **Version mismatch:**
   - Update Flywheel: `npx @velvetmonkey/flywheel-mcp@latest`
   - Update Claude Code

2. **Corrupted installation:**
   ```bash
   npm cache clean --force
   npx @velvetmonkey/flywheel-mcp@latest
   ```

3. **Conflicting MCP servers:**
   - Check other servers in `.mcp.json`
   - Disable others to isolate issue

---

## Platform-Specific Issues

### Windows

**WSL Path Issues:**

❌ **Won't work:**
```json
{
  "env": {
    "OBSIDIAN_VAULT_PATH": "/mnt/c/Users/You/Documents/Vault"
  }
}
```
File watching doesn't work on `/mnt/c/` paths in WSL.

✅ **Use native Linux path:**
```json
{
  "env": {
    "OBSIDIAN_VAULT_PATH": "/home/you/vault"
  }
}
```

**Command syntax:**
```json
{
  "command": "cmd",
  "args": ["/c", "npx", "-y", "@velvetmonkey/flywheel-mcp"]
}
```

---

### macOS

**Gatekeeper blocking npx:**

**Error:** "npx cannot be opened because the developer cannot be verified"

**Fix:**
```bash
xattr -d com.apple.quarantine $(which npx)
```

---

### Linux

**inotify limits:** See [File Watcher Crashes](#file-watcher-crashes)

**Permission errors:** Ensure user has read access to vault.

---

## Debug Mode

### Enable Logging

**Method 1: Environment variable**
```json
{
  "env": {
    "DEBUG": "flywheel:*"
  }
}
```

**Method 2: Log to file**
```json
{
  "env": {
    "FLYWHEEL_LOG_FILE": "/tmp/flywheel.log"
  }
}
```

### What to look for

**Successful startup:**
```
flywheel:index Scanning vault: /path/to/vault
flywheel:index Found 1234 markdown files
flywheel:index Building entity cache...
flywheel:index Indexed 1234 notes in 3.2s
flywheel:watch File watcher initialized
flywheel:mcp Server ready
```

**Index issues:**
```
flywheel:index Error reading file: /path/to/note.md
flywheel:index ENOENT: File not found
```

**Query performance:**
```
flywheel:query search_notes("term") started
flywheel:query Matched 45 notes in 234ms
flywheel:query Returning 10 results
```

---

## Getting Help

### Before reporting issues

1. **Run diagnostics:**
   - `health_check` output
   - `get_vault_stats` output
   - Vault size (`find /vault -name "*.md" | wc -l`)
   - Platform (OS, Node.js version, Claude Code version)

2. **Enable debug logging**

3. **Try minimal reproduction:**
   - Create small test vault
   - Does issue reproduce?
   - Helps isolate cause

### Report to:

- GitHub Issues: https://github.com/velvetmonkey/flywheel/issues
- Include: Debug logs, vault stats, error messages
- Exclude: Sensitive vault contents

---

## See Also

- [Performance Benchmarks](./PERFORMANCE.md) - Expected speeds
- [Configuration](./CONFIGURATION.md) - Tuning options
- [Architecture](./ARCHITECTURE.md) - How indexing works
- [Limitations](./LIMITATIONS.md) - Known edge cases
