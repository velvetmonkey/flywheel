# Migration Guide: v1.23.x → v1.24.0

## Overview

Version 1.24.0 splits Flywheel into two focused plugins:

- **Flywheel Core** (this plugin): Infrastructure layer - MCP server, safety hooks, wikilink automation
- **Vault-Personal** (separate plugin): Workflow features - logging, rollups, task management, nutrition tracking

## What Changed

### Removed from Core

**Skills** (moved to vault-personal):
- `add-log` - Add entries to daily log
- `task-add` - Add tasks to daily notes
- `food` - Log meals with timestamps
- `food-macros` - Calculate daily nutrition totals
- `rollup` - Run complete rollup chain

**Agents** (moved to vault-personal):
- `rollup-agent` - Orchestrate rollup chain
- `rollup-weekly-agent` - Daily → Weekly aggregation
- `rollup-monthly-agent` - Weekly → Monthly aggregation
- `rollup-quarterly-agent` - Monthly → Quarterly aggregation
- `rollup-yearly-agent` - Quarterly → Yearly aggregation
- All other workflow agents

**Hooks** (moved to vault-personal):
- `achievement-detect.py` - Achievement detection from log entries

**Templates** (moved to vault-personal):
- `daily.md`, `weekly.md`, `monthly.md`, `quarterly.md`, `yearly.md`
- `customer-onboarding.md`, `meeting.md`, `standup.md`, `okr.md`

### What Remains in Core

**Core Skill**:
- `vault-tasks` - Extract and display tasks from vault

**Safety Infrastructure**:
- Six Gates safety framework (all 6 gates)
- Pre-mutation validation hooks
- Post-mutation verification hooks
- Agent chain validation

**Automation**:
- Wikilink automation (suggest-wikilinks.py)
- Obsidian syntax validation (validate-obsidian-syntax.py)
- Frontmatter automation

**MCP Server**:
- Full graph intelligence (unchanged)
- 50+ vault analysis tools
- Backlinks, orphans, hubs, clusters, etc.

## Breaking Changes

### 1. Skills Removed

**Before (v1.23.x)**:
```
User: "add log entry: fixed authentication bug"
Flywheel: ✓ Added to daily-notes/2026-01-25.md
```

**After (v1.24.0)**:
```
User: "add log entry: fixed authentication bug"
Flywheel: ❌ Skill not found (install vault-personal)
```

### 2. Templates Directory Gone

**Before (v1.23.x)**:
```
packages/claude-plugin/templates/
├── daily.md
├── weekly.md
└── monthly.md
```

**After (v1.24.0)**:
```
Templates directory removed (now in vault-personal)
```

### 3. Agents Not Available

**Before (v1.23.x)**:
```
User: "do a rollup"
Flywheel: ✓ Running rollup-agent...
```

**After (v1.24.0)**:
```
User: "do a rollup"
Flywheel: ❌ No rollup skill (install vault-personal)
```

### 4. Configuration Schema Changes

Configuration options for personal features are now marked with `[vault-personal feature]` but still accepted for backward compatibility.

## Migration Steps

### Option 1: I Need Personal Workflow Features

**Install vault-personal plugin**:

1. Add vault-personal to your Claude Code settings:
   ```json
   {
     "plugins": {
       "flywheel": {
         "source": "github:velvetmonkey/flywheel"
       },
       "vault-personal": {
         "source": "github:velvetmonkey/vault-personal"
       }
     }
   }
   ```

2. Your existing `.flywheel.json` config will work with both plugins.

3. Templates are now in vault-personal - copy them to your vault if needed.

4. All skills, agents, and achievement-detect hook are now in vault-personal.

### Option 2: I Only Need Core Infrastructure

**No action required**:

- Your `.flywheel.json` still works (personal config options ignored)
- MCP server unchanged
- Safety hooks unchanged
- Wikilink automation unchanged

You can remove personal config options from `.flywheel.json` if desired:
```json
{
  "$schema": "./plugins/flywheel/config/config-schema.json",
  "vault_name": "My Vault",
  "paths": {
    "daily_notes": "daily-notes",
    "weekly_notes": "weekly-notes"
  },
  "folders": {
    "protected": ["personal", "work", "tech"]
  }
}
```

## Backward Compatibility

### What Still Works

✅ **Existing `.flywheel.json` configs** - All config options still accepted
✅ **MCP server** - No changes, all tools work identically
✅ **Core hooks** - All safety hooks unchanged
✅ **Wikilink automation** - No changes
✅ **Frontmatter automation** - No changes

### What Requires vault-personal

❌ **Personal workflow skills** - add-log, task-add, food, rollup
❌ **Workflow agents** - All rollup agents, review agents
❌ **Achievement detection** - achievement-detect hook
❌ **Templates** - Daily/weekly/monthly templates

## Configuration Schema

### Core Features (Flywheel)

```json
{
  "vault_name": "My Vault",
  "paths": {
    "daily_notes": "daily-notes",
    "weekly_notes": "weekly-notes",
    "monthly_notes": "monthly-notes",
    "quarterly_notes": "quarterly-notes",
    "yearly_notes": "yearly-notes"
  },
  "folders": {
    "protected": ["personal", "work", "tech"]
  }
}
```

### Personal Features (vault-personal)

```json
{
  "paths": {
    "achievements": "personal/goals/Achievements.md",
    "templates": "templates"
  },
  "habits": [
    { "name": "Walk", "tag": "#habit" },
    { "name": "Stretch", "tag": "#habit" }
  ],
  "sections": {
    "log": "Log",
    "food": "Food",
    "habits": "Habits"
  }
}
```

## Testing Your Migration

### Core Features Test

```bash
# Test MCP health
"check MCP health"

# Test wikilink automation
"suggest wikilinks for this note"

# Test vault intelligence
"find orphan notes"

# Test task extraction
"show me all tasks"
```

### Vault-Personal Features Test

```bash
# Test logging (requires vault-personal)
"add log entry: migration complete"

# Test rollup (requires vault-personal)
"do a rollup"

# Test food logging (requires vault-personal)
"I ate: breakfast - oatmeal"
```

## FAQ

**Q: Do I need both plugins?**
A: Only if you want personal workflow features. Core infrastructure works standalone.

**Q: Will my existing config break?**
A: No. All config options still work. Personal feature configs are just ignored if vault-personal isn't installed.

**Q: Can I keep using my templates?**
A: Yes, but they're now maintained in vault-personal. Copy them from vault-personal's templates directory.

**Q: What about my achievements file?**
A: It's unchanged. Achievement detection just requires vault-personal plugin now.

**Q: Is the MCP server affected?**
A: No. MCP server is unchanged and works identically.

**Q: What if I only want some personal features?**
A: Install vault-personal. You can ignore features you don't need.

## Troubleshooting

### "Skill not found" errors

**Symptom**: "add-log", "rollup", or "food" skills not working.

**Solution**: Install vault-personal plugin.

### Templates missing

**Symptom**: Template files gone from core plugin.

**Solution**: Get templates from vault-personal plugin.

### Achievement detection stopped

**Symptom**: Achievements.md not updating automatically.

**Solution**: Install vault-personal plugin (includes achievement-detect.py hook).

### Config warnings about personal features

**Symptom**: Warnings about unused config options.

**Solution**: Either install vault-personal or remove those config options from `.flywheel.json`.

## Support

- **Core issues**: [Flywheel GitHub](https://github.com/velvetmonkey/flywheel/issues)
- **Vault-personal issues**: [Vault-Personal GitHub](https://github.com/velvetmonkey/vault-personal/issues)
- **Documentation**: See `docs/` directory in each repository

## Version History

| Version | Changes |
|---------|---------|
| v1.23.1 | Last version with personal features in core |
| v1.24.0 | Personal features moved to vault-personal plugin |
