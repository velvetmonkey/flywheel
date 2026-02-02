# Installation Guide

Platform-specific installation instructions for Flywheel.

---

## Prerequisites

- **Node.js 18+** — [Download](https://nodejs.org)
- **Claude Code** or another MCP client
- **Markdown vault** (Obsidian, plain folders, etc.)

---

## Both Packages Required

Flywheel provides **51 read-only tools** for querying your vault's graph, metadata, and structure.

For **write operations** (mutations, auto-wikilinks, policies), you also need:
- [Flywheel-Crank](https://github.com/velvetmonkey/flywheel-crank) — 11 mutation tools

Install both for the complete experience. See the platform sections below for combined configurations.

---

## macOS

macOS uses native FSEvents for file watching — no polling required.

### Configuration

Create `.mcp.json` in your vault root:

```json
{
  "mcpServers": {
    "flywheel": {
      "command": "npx",
      "args": ["-y", "@velvetmonkey/flywheel-mcp"]
    },
    "flywheel-crank": {
      "command": "npx",
      "args": ["-y", "@velvetmonkey/flywheel-crank"]
    }
  }
}
```

### Gatekeeper Note

On first run, macOS may block unsigned binaries. If you see security warnings:
1. Open **System Settings > Privacy & Security**
2. Click **Allow Anyway** for the blocked item
3. Restart Claude Code

### Tuning (Optional)

For large vaults (5,000+ notes), increase debounce to reduce rebuild frequency:

```json
{
  "mcpServers": {
    "flywheel": {
      "command": "npx",
      "args": ["-y", "@velvetmonkey/flywheel-mcp"],
      "env": {
        "FLYWHEEL_DEBOUNCE_MS": "1000",
        "FLYWHEEL_FLUSH_MS": "5000"
      }
    }
  }
}
```

**Recommended debounce:** 1000-5000ms for macOS (FSEvents is efficient, higher debounce reduces unnecessary rebuilds).

---

## Linux

Linux uses inotify for file watching — fast and efficient.

### Configuration

Create `.mcp.json` in your vault root:

```json
{
  "mcpServers": {
    "flywheel": {
      "command": "npx",
      "args": ["-y", "@velvetmonkey/flywheel-mcp"]
    },
    "flywheel-crank": {
      "command": "npx",
      "args": ["-y", "@velvetmonkey/flywheel-crank"]
    }
  }
}
```

### Check inotify Limits

Linux has a default limit on file watchers. Check your current limit:

```bash
cat /proc/sys/fs/inotify/max_user_watches
```

If your vault has more notes than this limit, increase it:

```bash
# Temporary (until reboot)
sudo sysctl fs.inotify.max_user_watches=524288

# Permanent (add to /etc/sysctl.conf)
echo "fs.inotify.max_user_watches=524288" | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

### Tuning (Optional)

Linux inotify is fast — you can use lower debounce values:

```json
{
  "mcpServers": {
    "flywheel": {
      "command": "npx",
      "args": ["-y", "@velvetmonkey/flywheel-mcp"],
      "env": {
        "FLYWHEEL_DEBOUNCE_MS": "300",
        "FLYWHEEL_FLUSH_MS": "1000"
      }
    }
  }
}
```

**Recommended debounce:** 300-1000ms for native Linux.

---

## Windows (Native)

Windows requires two adjustments:
1. **cmd /c wrapper** — npx must run through cmd
2. **Polling mode** — Native file watching is unreliable on Windows

### Configuration

Create `.mcp.json` in your vault root:

```json
{
  "mcpServers": {
    "flywheel": {
      "command": "cmd",
      "args": ["/c", "npx", "-y", "@velvetmonkey/flywheel-mcp"],
      "env": {
        "FLYWHEEL_WATCH_POLL": "true",
        "FLYWHEEL_POLL_INTERVAL": "10000"
      }
    },
    "flywheel-crank": {
      "command": "cmd",
      "args": ["/c", "npx", "-y", "@velvetmonkey/flywheel-crank"]
    }
  }
}
```

### Why Polling?

Windows native file watching (`ReadDirectoryChangesW`) has edge cases where changes aren't detected reliably. Polling mode ensures your index stays current.

**Poll interval:** 10000ms (10 seconds) balances responsiveness with CPU efficiency. Increase to 30000-60000ms if CPU usage is a concern.

### Path Format

Use Windows paths with backslashes (escaped in JSON):

```json
"env": {
  "PROJECT_PATH": "C:\\Users\\YourName\\Documents\\Vault"
}
```

Or forward slashes (also works):

```json
"env": {
  "PROJECT_PATH": "C:/Users/YourName/Documents/Vault"
}
```

---

## Windows (WSL)

WSL can run npx directly, but vaults on Windows drives (`/mnt/c/...`) require polling.

### If Vault is on Linux Filesystem

Native inotify works — no polling needed:

```json
{
  "mcpServers": {
    "flywheel": {
      "command": "npx",
      "args": ["-y", "@velvetmonkey/flywheel-mcp"]
    },
    "flywheel-crank": {
      "command": "npx",
      "args": ["-y", "@velvetmonkey/flywheel-crank"]
    }
  }
}
```

### If Vault is on Windows Drive (/mnt/c/...)

**Polling is required.** Linux inotify cannot detect changes across the WSL-Windows boundary:

```json
{
  "mcpServers": {
    "flywheel": {
      "command": "npx",
      "args": ["-y", "@velvetmonkey/flywheel-mcp"],
      "env": {
        "PROJECT_PATH": "/mnt/c/Users/YourName/Documents/Vault",
        "FLYWHEEL_WATCH_POLL": "true",
        "FLYWHEEL_POLL_INTERVAL": "10000"
      }
    },
    "flywheel-crank": {
      "command": "npx",
      "args": ["-y", "@velvetmonkey/flywheel-crank"],
      "env": {
        "PROJECT_PATH": "/mnt/c/Users/YourName/Documents/Vault"
      }
    }
  }
}
```

**Recommendation:** For best performance, keep your vault on the Linux filesystem (`~/vault`) rather than `/mnt/c/`.

### Tuning for WSL + Windows Drives

Higher debounce compensates for polling overhead:

| Setting | Recommended |
|---------|-------------|
| `FLYWHEEL_POLL_INTERVAL` | 10000-60000ms |
| `FLYWHEEL_DEBOUNCE_MS` | 5000-10000ms |

---

## Verify Installation

After configuration, verify everything works:

### 1. Check MCP Registration

```bash
claude mcp list
```

You should see:
```
flywheel ✓
flywheel-crank ✓
```

### 2. Test Vault Connection

Open Claude Code in your vault directory and ask:

```
What vault am I connected to?
```

Claude should respond with your vault name and note count.

### 3. Test File Watching

1. Modify a note in your vault (add a line)
2. Wait for the poll/watch interval
3. Ask Claude: "What changed recently in my vault?"

If Claude detects the change, file watching is working.

### 4. Health Check

Ask Claude to run the health check:

```
Run the health_check tool
```

This returns vault stats, index status, and any configuration issues.

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `flywheel ✗` in mcp list | Check `.mcp.json` is in vault root, not a subfolder |
| "No notes found" | Run `claude` from inside your vault directory |
| Windows: "spawn UNKNOWN" | Use `cmd /c npx` wrapper (see Windows section) |
| File changes not detected | Enable polling: `FLYWHEEL_WATCH_POLL=true` |
| High CPU on Windows | Increase `FLYWHEEL_POLL_INTERVAL` to 30000-60000 |
| Linux: "ENOSPC" error | Increase inotify limit (see Linux section) |

See [Troubleshooting](./TROUBLESHOOTING.md) for more solutions.

---

## Next Steps

- **[Configuration](./CONFIGURATION.md)** — Environment variables, tool presets, file watching tuning
- **[Query Guide](./QUERY_GUIDE.md)** — Patterns for effective vault queries
- **[MCP Reference](./MCP_REFERENCE.md)** — All 51 tools documented
