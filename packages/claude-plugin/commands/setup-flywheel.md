# /setup-flywheel - Configure and Onboard to Flywheel

Complete Flywheel setup in one command: configure MCP, validate connection, and see your vault stats.

## Usage

```
/setup-flywheel
```

## What It Does

```
┌─────────────────────────────────────────────────────────────────┐
│ Phase 1: Platform Detection                                     │
│   Platform: win32 → cmd /c npx                                  │
│   Platform: linux → npx (including WSL)                         │
│   Platform: darwin → npx                                        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Phase 2: Generate .mcp.json                                     │
│   - Detect or ask for vault path                                │
│   - Merge with existing MCP servers                             │
│   - User confirms before write                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Phase 3: Validate Connection                                    │
│   mcp__flywheel__health_check()                                │
│   - If fail → restart instructions                              │
│   - If pass → continue to Phase 4                               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Phase 4: Vault Onboarding                                       │
│   mcp__flywheel__get_vault_stats()                             │
│   - Note count, link density                                    │
│   - Folder structure                                            │
│   - Suggested next steps                                        │
└─────────────────────────────────────────────────────────────────┘
```

## Where Output Goes

| Action | Target | Notes |
|--------|--------|-------|
| MCP Config | `.mcp.json` in project root | Merged with existing servers |
| Validation | Console output | Health check results |
| Stats | Console output | Vault statistics |

## Platform Detection (CRITICAL)

The `Platform:` field in environment info is **authoritative**:

| `Platform:` value | Command | Path style |
|-------------------|---------|------------|
| `linux` | `npx` | `/mnt/c/...` (WSL) or `/home/...` |
| `win32` | `cmd /c npx` | `C:/...` |
| `darwin` | `npx` | `/Users/...` |

**NEVER infer platform from filesystem path.** `/mnt/c/...` means WSL (use `npx`, NOT `cmd /c`).

## Example Output

```
# Flywheel Setup

## Phase 1: Platform Detected
- Runtime: `win32` (Native Windows)
- Command: `cmd /c npx`

## Phase 2: Configuration
Vault path: C:/Users/benca/obsidian/Ben

I'll add this to your `.mcp.json`:

{
  "mcpServers": {
    "flywheel": {
      "command": "cmd",
      "args": ["/c", "npx", "-y", "@bencassie/flywheel-mcp"],
      "env": {
        "PROJECT_PATH": "C:/Users/benca/obsidian/Ben"
      }
    }
  }
}

**Confirm?** (This will be merged with any existing MCP servers)

[User confirms]

## Phase 3: Validating...
✓ MCP server connected
✓ Vault accessible

## Phase 4: Your Vault

Notes: 147 | Links: 523 | Orphans: 12

Folder structure:
├── daily-notes/ (89)
├── projects/ (32)
└── ...

### Next Steps
- "check vault health" - Full analysis
- "find orphan notes" - Unlinked content
- "do a rollup" - Aggregate your notes
```

## Related Commands
- `/rollup` - Aggregate notes
- `/fix-links` - Repair broken wikilinks
- `/normalize` - Harmonize frontmatter and wikilinks
