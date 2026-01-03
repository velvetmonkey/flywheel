---
name: setup-mcp
description: Configure Flywheel MCP server with correct platform detection and validate the connection
auto_trigger: true
trigger_keywords:
  - "setup mcp"
  - "configure mcp"
  - "fix mcp"
  - "mcp not working"
  - "flywheel not connecting"
  - "setup flywheel mcp"
  - "install mcp"
allowed-tools: Read, Write, mcp__flywheel__health_check
---

# Setup MCP

## Purpose
Configure the Flywheel MCP server correctly based on the user's platform and validate the connection works.

## Six Gates Compliance
- [x] Gate 1: Reads existing .mcp.json before writing
- [x] Gate 2: Creates new file if none exists, edits if present
- [x] Gate 3: N/A (single-step workflow)
- [x] Gate 4: Asks user to confirm before writing .mcp.json
- [x] Gate 5: Validates MCP health after setup
- [x] Gate 6: N/A (config file, not vault content)

## Process

### 1. Detect Platform (CRITICAL)

**Check the `Platform:` field in the environment info at the start of the session.**

| `Platform:` value | Runtime | Command | Path style |
|-------------------|---------|---------|------------|
| `linux` | Linux or WSL | `npx` | `/mnt/c/...` (WSL) or `/home/...` |
| `win32` | Native Windows | `cmd /c npx` | `C:/...` |
| `darwin` | macOS | `npx` | `/Users/...` |

**CRITICAL: NEVER infer platform from filesystem path.**
- `/mnt/c/Users/...` means WSL accessing Windows files → use `npx` (NOT `cmd /c`)
- The `Platform:` field is AUTHORITATIVE

### 2. Get Vault Path

Ask the user for their vault path if not obvious from the working directory.

For WSL users with vaults on Windows filesystem:
- Convert `C:\Users\name\vault` → `/mnt/c/Users/name/vault`

### 3. Generate .mcp.json

**For Linux / macOS / WSL (`Platform: linux` or `Platform: darwin`):**

```json
{
  "mcpServers": {
    "flywheel": {
      "command": "npx",
      "args": ["-y", "@bencassie/flywheel-mcp"],
      "env": {
        "PROJECT_PATH": "/path/to/vault"
      }
    }
  }
}
```

**For Windows (`Platform: win32`):**

```json
{
  "mcpServers": {
    "flywheel": {
      "command": "cmd",
      "args": ["/c", "npx", "-y", "@bencassie/flywheel-mcp"],
      "env": {
        "PROJECT_PATH": "C:/path/to/vault"
      }
    }
  }
}
```

### 4. Write Configuration

1. Check if `.mcp.json` exists in the project root
2. If exists, read it first (Gate 1)
3. Merge flywheel config with existing servers (don't overwrite other MCPs)
4. Show user the proposed config
5. Ask for confirmation (Gate 4)
6. Write the file

### 5. Validate Connection

After writing, tell the user:

```
## Next Steps

1. **Restart Claude Code** to load the new MCP configuration
2. After restart, run `/setup-mcp` again to validate the connection

Or if you have the MCP already loaded, I'll test it now...
```

If MCP is already available, call `mcp__flywheel__health_check()` to verify:

```
## Validation Result

✓ MCP server connected
✓ Vault accessible: /path/to/vault
✓ {N} notes indexed

Flywheel is ready! Try `/vault-health` for a full analysis.
```

If validation fails:

```
## Validation Failed

✗ MCP server not responding

This usually means:
1. Claude Code needs to restart to load the new config
2. The vault path is incorrect
3. npx is not available in PATH

Try:
1. Restart Claude Code
2. Run `/setup-mcp` again
```

## Error Handling

| Issue | Response |
|-------|----------|
| Can't determine platform | Ask user explicitly: "Are you on Windows, macOS, or Linux/WSL?" |
| Vault path doesn't exist | Warn user, suggest checking path |
| Existing .mcp.json has syntax errors | Show error, offer to create fresh config |
| MCP health check fails | Suggest restart, provide troubleshooting steps |

## Example Output

```
# MCP Setup

## Platform Detected
- Runtime: `linux` (WSL)
- Vault path: `/mnt/c/Users/benca/obsidian/Ben`

## Proposed Configuration

I'll add this to your `.mcp.json`:

```json
{
  "mcpServers": {
    "flywheel": {
      "command": "npx",
      "args": ["-y", "@bencassie/flywheel-mcp"],
      "env": {
        "PROJECT_PATH": "/mnt/c/Users/benca/obsidian/Ben"
      }
    }
  }
}
```

**Confirm?** (This will be merged with any existing MCP servers)
```

## Related Skills
- `/vault-health` - Full vault health check
- `/onboard` - Welcome and orientation
