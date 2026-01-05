# Flywheel MCP Server

The intelligence layer of [Flywheel](https://github.com/bencassie/flywheel) — MCP tools for vault graph queries, wikilink services, and structure analysis.

[![npm](https://img.shields.io/npm/v/@bencassie/flywheel-mcp)](https://www.npmjs.com/package/@bencassie/flywheel-mcp)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![MCP](https://img.shields.io/badge/MCP-Compatible-blue)](https://modelcontextprotocol.io/)

## Installation

### Via `.mcp.json`

Add to your project's `.mcp.json` (in your vault root). **Zero-config** if `.mcp.json` is in your vault—no `PROJECT_PATH` needed:

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

> **Note**: Windows native requires `"command": "cmd", "args": ["/c", "npx", "-y", "@bencassie/flywheel-mcp"]`

<details>
<summary><strong>Advanced: Pointing to a different vault</strong></summary>

If `.mcp.json` is NOT in your vault, or you want to use a different vault, set `PROJECT_PATH`:

**Choose config based on where Claude Code runs, NOT where your vault is stored.**

<details>
<summary><strong>Linux / macOS</strong></summary>

```json
{
  "mcpServers": {
    "flywheel": {
      "command": "npx",
      "args": ["-y", "@bencassie/flywheel-mcp"],
      "env": {
        "PROJECT_PATH": "/path/to/your/vault"
      }
    }
  }
}
```

</details>

<details>
<summary><strong>WSL (Windows Subsystem for Linux)</strong></summary>

> ⚠️ **Common mistake**: Your vault may be on `C:\Users\...` (Windows filesystem), but if Claude Code runs in WSL, this is Linux—use `npx` directly, **not** `cmd /c`.

```json
{
  "mcpServers": {
    "flywheel": {
      "command": "npx",
      "args": ["-y", "@bencassie/flywheel-mcp"],
      "env": {
        "PROJECT_PATH": "/mnt/c/Users/yourname/path/to/vault"
      }
    }
  }
}
```

</details>

<details>
<summary><strong>Windows (native, not WSL)</strong></summary>

```json
{
  "mcpServers": {
    "flywheel": {
      "command": "cmd",
      "args": ["/c", "npx", "-y", "@bencassie/flywheel-mcp"],
      "env": {
        "PROJECT_PATH": "C:/Users/yourname/path/to/vault"
      }
    }
  }
}
```

</details>

#### Detecting Your Platform

Check the environment info shown at the start of your Claude Code session:

| `Platform:` value | Use config |
|-------------------|------------|
| `linux` | Linux (or WSL if your path starts with `/mnt/`) |
| `win32` | Windows |
| `darwin` | macOS |

</details>

### Via CLI

```bash
# Zero-config (run from vault directory)
claude mcp add flywheel -- npx -y @bencassie/flywheel-mcp

# With explicit vault path
claude mcp add flywheel --env PROJECT_PATH=/path/to/vault -- npx -y @bencassie/flywheel-mcp

# Windows (native) - with explicit path
claude mcp add flywheel --env PROJECT_PATH=C:/path/to/vault -- cmd /c npx -y @bencassie/flywheel-mcp
```

### Verify

```bash
claude mcp list  # Should show: flywheel ✓
```

## Tools

| Category | Examples |
|----------|----------|
| Graph | `get_backlinks`, `get_forward_links`, `find_orphan_notes`, `find_hub_notes` |
| Wikilinks | `suggest_wikilinks`, `find_broken_links` |
| Health | `get_vault_stats`, `get_folder_structure` |
| Query | `search_notes`, `get_recent_notes`, `get_stale_notes` |
| System | `refresh_index`, `get_all_entities` |
| Primitives | `list_notes`, `list_tags`, `list_folders`, `get_note_info` |
| Periodic | `get_periodic_note` |

[**Full tool reference →**](docs/tools-reference.md)

## Configuration

| Environment Variable | Required | Default | Description |
|---------------------|:--------:|---------|-------------|
| `PROJECT_PATH` | No | `cwd()` | Path to markdown vault directory |

**Zero-config**: If `PROJECT_PATH` is not set, the server uses the current working directory. When `.mcp.json` is in your vault root, this means no configuration needed—it just works.

The server scans the vault on startup and builds an in-memory index. No database required.

## Architecture

```
┌──────────┐        ┌────────────────────────────────┐
│          │        │           Flywheel             │
│  Vault   │  scan  │  ┌──────────────────────────┐  │
│  (.md)   │───────►│  │       VaultIndex         │  │
│          │        │  │  notes, backlinks,       │  │
└──────────┘        │  │  entities, tags          │  │
                    │  └────────────┬─────────────┘  │
                    │               ▼                │
                    │  ┌──────────────────────────┐  │
                    │  │       MCP Tools          │  │
                    │  └──────────────────────────┘  │
                    └───────────────┬────────────────┘
                                    │ MCP Protocol
                                    ▼
                            ┌──────────────┐
                            │ Claude Code  │
                            └──────────────┘
```

**Design decisions:**
- File-first: Parses markdown directly, no database
- Eager loading: Full index on startup (fine for <5000 notes)
- In-memory graph: <10ms query times
- Privacy by design: Returns structure/metadata, not content

## Performance

| Vault Size | Index Build | Query Time | Memory |
|------------|-------------|------------|--------|
| 100 notes | <200ms | <10ms | ~20MB |
| 500 notes | <500ms | <10ms | ~30MB |
| 1,500 notes | <2s | <10ms | ~50MB |
| 5,000 notes | <5s | <10ms | ~100MB |

## Error Handling

| Situation | Behavior |
|-----------|----------|
| Malformed YAML | Skipped, file treated as content |
| Binary files | Detected and skipped |
| Empty files | Indexed with no links/tags |
| Large files (>10MB) | Skipped with warning |
| Missing files | Graceful degradation |

## Development

```bash
# Install
npm install

# Run with vault
PROJECT_PATH=/path/to/vault npm run dev

# Build
npm run build

# Test
npm test

# Interactive inspector
npm run inspect
```

## License

Apache 2.0 — [Ben Cassie](https://github.com/bencassie)

## Links

- [Flywheel](https://github.com/bencassie/flywheel) — Main project
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Claude Code](https://claude.ai/code)
