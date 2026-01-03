---
name: onboard-vault
description: Welcome new users with vault health check, stats overview, and suggested next steps
auto_trigger: true
trigger_keywords:
  - "onboard"
  - "getting started"
  - "hello flywheel"
  - "what can you do"
  - "introduction"
  - "first steps"
  - "help me get started"
  - "show me around"
allowed-tools: mcp__flywheel__health_check, mcp__flywheel__get_vault_stats, mcp__flywheel__find_hub_notes
---

# Vault Onboarding

## Purpose
Welcome new users to Flywheel and provide a guided introduction to their vault.

## Six Gates Compliance
- [x] Gate 1: Read-only skill (no mutations)
- [x] Gate 2: N/A (no file operations)
- [x] Gate 3: N/A (single-step workflow)
- [x] Gate 4: N/A (no mutations)
- [x] Gate 5: Calls health_check first
- [x] Gate 6: N/A (no mutations)

## Process

### 1. Check MCP Health
Call `mcp__flywheel__health_check()` first to ensure vault is accessible.

If health check fails or shows degraded status, warn user and suggest running `mcp__flywheel__refresh_index()`.

### 2. Get Vault Overview
Call `mcp__flywheel__get_vault_stats()` to get:
- Total notes, links, tags
- Folder distribution
- Link density metrics

### 3. Find Key Notes
Call `mcp__flywheel__find_hub_notes(min_links=3, limit=5)` to show the most connected notes.

### 4. Present Welcome Message

Format output as:

```
# Welcome to Flywheel!

## Your Vault at a Glance

| Metric | Count |
|--------|-------|
| Notes | {count} |
| Links | {count} |
| Tags | {count} |
| Folders | {count} |

## Your Hub Notes (Most Connected)

These are your most interconnected notes:

1. [[Note Name]] - {X} connections
2. [[Note Name]] - {X} connections
3. [[Note Name]] - {X} connections
...

## Suggested Next Steps

Based on your vault, try these commands:

| Command | What it does |
|---------|--------------|
| `/vault-health` | Deep health analysis with recommendations |
| `/vault-orphans` | Find disconnected notes to integrate |
| `/vault-search <query>` | Search your vault by title, tags, or frontmatter |
| `/auto-log <message>` | Add a timestamped log entry to today's daily note |

## Learn More

- See `docs/QUICKSTART.md` for a getting started guide
- See `docs/ROADMAP.md` for upcoming features
- Run `/vault-health` for a comprehensive health check
```

## Customization

Adjust suggestions based on vault state:
- If orphan count > 10: Emphasize `/vault-orphans`
- If no daily notes detected: Skip `/auto-log` suggestion
- If link density < 1.0: Suggest building more connections

## Related Skills
- `/vault-health` - Detailed health analysis
- `/vault-stats` - Full statistics
- `/vault-orphans` - Find disconnected notes
