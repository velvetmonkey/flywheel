# /uninstall-flywheel - Complete Flywheel Removal

Removes Flywheel completely: both the Claude Code plugin and MCP server configuration.

## Usage

```
/uninstall-flywheel
```

## What It Does

```
┌─────────────────────────────────────────────────────────────────┐
│ Phase 1: Remove MCP Configuration                               │
│   - Check ~/.claude/settings.json for flywheel                  │
│   - Check .mcp.json for flywheel                                │
│   - Remove flywheel from mcpServers (preserve other servers)    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Phase 2: Uninstall Plugin                                       │
│   /plugin uninstall flywheel@bencassie-flywheel                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Phase 3: Cleanup                                                │
│   - Remove ~/.flywheel-update-check cache (if exists)           │
│   - Confirm removal complete                                    │
└─────────────────────────────────────────────────────────────────┘
```

## Where Changes Go

| Action | Target | Notes |
|--------|--------|-------|
| Remove MCP | `~/.claude/settings.json` | User-level config (if present) |
| Remove MCP | `.mcp.json` | Project-level config (if present) |
| Uninstall plugin | Claude Code plugins | Removes flywheel plugin |
| Remove cache | `~/.flywheel-update-check` | Update check cache |

## Configuration Layers

Flywheel may be configured at multiple levels. This command checks and removes from ALL:

| Layer | File | Scope |
|-------|------|-------|
| **User** | `~/.claude/settings.json` | All projects globally |
| **Project** | `.mcp.json` | This project only |

## Example Output

```
# Flywheel Uninstall

## Phase 1: MCP Configuration

Checking for Flywheel MCP config...

Found in:
- ~/.claude/settings.json (user-level)
- .mcp.json (project-level)

Remove Flywheel from both? (y/n)

[User confirms]

✓ Removed from ~/.claude/settings.json
✓ Removed from .mcp.json

## Phase 2: Plugin

Uninstalling plugin...

/plugin uninstall flywheel@bencassie-flywheel

✓ Plugin uninstalled

## Phase 3: Cleanup

✓ Removed ~/.flywheel-update-check cache

## Complete

Flywheel has been fully removed.

To reinstall later:
/plugin marketplace add bencassie/flywheel
/plugin install flywheel@bencassie-flywheel
```

## Reinstallation

If you want to reinstall Flywheel later:

```
/plugin marketplace add bencassie/flywheel
/plugin install flywheel@bencassie-flywheel
```

Then say "setup flywheel" to reconfigure the MCP server.

## Related Commands
- `/setup-flywheel` - Install and configure Flywheel
