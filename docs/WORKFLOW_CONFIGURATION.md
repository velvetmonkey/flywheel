# Workflow Configuration Guide

This guide explains how to configure Flywheel workflows using `.flywheel.json` in your vault root.

---

## Quick Start

Create `.flywheel.json` in your vault root:

```json
{
  "vault_name": "My Vault",
  "paths": {
    "daily_notes": "daily-notes",
    "weekly_notes": "weekly-notes",
    "templates": "templates"
  }
}
```

That's it! Flywheel will use these paths for all workflows.

---

## Complete Schema

```json
{
  "vault_name": "string (optional)",
  "paths": {
    "daily_notes": "string (required)",
    "weekly_notes": "string (optional)",
    "monthly_notes": "string (optional)",
    "quarterly_notes": "string (optional)",
    "yearly_notes": "string (optional)",
    "templates": "string (optional)",
    "achievements": "string (optional)"
  },
  "sections": {
    "log": "string (optional)",
    "food": "string (optional)",
    "tasks": "string (optional)",
    "habits": "string (optional)"
  },
  "habits": ["string", ...] (optional),
  "folders": {
    "protected": ["string", ...] (optional),
    "require_subfolders": ["string", ...] (optional),
    "allow_direct_files": ["string", ...] (optional)
  }
}
```

---

## Configuration Options

### `vault_name` (optional)

Display name for your vault, used in reports and summaries.

**Example:**
```json
{
  "vault_name": "Ben's Knowledge Base"
}
```

---

### `paths` (object)

File system paths for periodic notes and special files.

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `daily_notes` | string | ✅ Yes | - | Folder for daily notes (YYYY-MM-DD.md) |
| `weekly_notes` | string | No | `weekly-notes` | Folder for weekly summaries (YYYY-WXX.md) |
| `monthly_notes` | string | No | `monthly-notes` | Folder for monthly summaries (YYYY-MM.md) |
| `quarterly_notes` | string | No | `quarterly-notes` | Folder for quarterly summaries (YYYY-QX.md) |
| `yearly_notes` | string | No | `yearly-notes` | Folder for yearly summaries (YYYY.md) |
| `templates` | string | No | `templates` | Folder for note templates |
| `achievements` | string | No | `Achievements.md` | Path to achievements file (created at vault root if missing) |

**Example:**
```json
{
  "paths": {
    "daily_notes": "journal/daily",
    "weekly_notes": "journal/weekly",
    "monthly_notes": "journal/monthly",
    "templates": "templates",
    "achievements": "goals/achievements.md"
  }
}
```

**Path Format:**
- Relative paths from vault root (no leading `/`)
- Use forward slashes even on Windows
- Folders don't need trailing slashes

---

### `sections` (object)

Section header TEXT for structured sections in notes. Use text only (no `#` prefix) - matching is case-insensitive and level-agnostic.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `log` | string | `Log` | Section for timestamped log entries |
| `food` | string | `Food` | Section for food tracking |
| `tasks` | string | `Tasks` | Section for checkbox tasks |
| `habits` | string | `Habits` | Section for habit tracking |

**Example:**
```json
{
  "sections": {
    "log": "Daily Log",
    "food": "Food Diary",
    "tasks": "Action Items",
    "habits": "Daily Habits"
  }
}
```

**Section Format:**
- Use TEXT ONLY (no `#` or `##` prefix)
- Matching is case-insensitive (`Log` matches `## Log`, `# LOG`, `### log`)
- Matching is level-agnostic (any heading level works)

---

### `habits` (array)

List of habits to track in daily notes.

**Example:**
```json
{
  "habits": ["Walk", "Stretch", "Vitamins", "Meditate", "Journal"]
}
```

**Usage:**
- Used by `/auto-log` skill to validate habit entries
- Used by rollup agents to calculate habit completion rates
- Format: Simple strings (no checkboxes or metadata)

---

### `folders` (object)

Folder organization rules and protections.

| Field | Type | Description |
|-------|------|-------------|
| `protected` | string[] | Folders that should never be modified |
| `require_subfolders` | string[] | Folders that must contain subfolders (not direct files) |
| `allow_direct_files` | string[] | Folders explicitly allowed to contain files |

**Example:**
```json
{
  "folders": {
    "protected": [".obsidian", ".git", ".claude"],
    "require_subfolders": ["personal", "work", "tech"],
    "allow_direct_files": ["templates", "daily-notes"]
  }
}
```

**Behavior:**
- **Protected**: Hooks will deny writes to these folders
- **Require subfolders**: Notes must be in subfolders (e.g., `personal/health/note.md`, not `personal/note.md`)
- **Allow direct files**: Overrides `require_subfolders` for specific folders

---

## Configuration Examples

### Example 1: Personal Vault

```json
{
  "vault_name": "Personal Knowledge Base",
  "paths": {
    "daily_notes": "daily",
    "weekly_notes": "weekly",
    "monthly_notes": "monthly",
    "templates": "templates",
    "achievements": "goals/achievements.md"
  },
  "sections": {
    "log": "Log",
    "food": "Food",
    "habits": "Habits"
  },
  "habits": ["Walk", "Stretch", "Vitamins"],
  "folders": {
    "protected": [".obsidian", ".git"],
    "require_subfolders": ["personal", "work"],
    "allow_direct_files": ["daily", "weekly", "monthly", "templates"]
  }
}
```

**Use case**: Individual journaling with health tracking

---

### Example 2: Team Vault

```json
{
  "vault_name": "Acme Corp Team Vault",
  "paths": {
    "daily_notes": "standups/daily",
    "weekly_notes": "summaries/weekly",
    "templates": "templates"
  },
  "sections": {
    "log": "Updates",
    "tasks": "Action Items"
  },
  "folders": {
    "protected": [".obsidian", ".git", "clients"],
    "require_subfolders": ["projects", "meetings"],
    "allow_direct_files": ["standups", "summaries", "templates"]
  }
}
```

**Use case**: Team collaboration with standup tracking

---

### Example 3: Research Vault

```json
{
  "vault_name": "Research Notes",
  "paths": {
    "daily_notes": "logs",
    "templates": "templates"
  },
  "sections": {
    "log": "Research Log",
    "tasks": "Experiments"
  },
  "folders": {
    "protected": [".obsidian", ".git", "data"],
    "require_subfolders": ["papers", "experiments"],
    "allow_direct_files": ["logs", "templates"]
  }
}
```

**Use case**: Academic research with experiment tracking

---

## Validation

Flywheel validates your configuration at runtime. Common errors:

| Error | Cause | Fix |
|-------|-------|-----|
| `Missing daily_notes path` | No `paths.daily_notes` defined | Add `"daily_notes": "folder-name"` |
| `Path does not exist: X` | Folder doesn't exist in vault | Create folder or fix path |
| `Section not found: X` | Section header text not in note | Check spelling matches your notes |
| `Protected folder: X` | Attempt to write to protected folder | Remove from `protected` list |

---

## Default Behavior

If `.flywheel.json` is missing or incomplete, Flywheel uses these defaults:

```json
{
  "vault_name": "Vault",
  "paths": {
    "daily_notes": "daily-notes",
    "weekly_notes": "weekly-notes",
    "monthly_notes": "monthly-notes",
    "quarterly_notes": "quarterly-notes",
    "yearly_notes": "yearly-notes",
    "templates": "templates",
    "achievements": "Achievements.md"
  },
  "sections": {
    "log": "Log",
    "food": "Food",
    "tasks": "Tasks",
    "habits": "Habits"
  },
  "habits": [],
  "folders": {
    "protected": [".obsidian", ".git", ".claude"],
    "require_subfolders": [],
    "allow_direct_files": []
  }
}
```

---

## Advanced: Dynamic Configuration

For vault-specific customization, you can override config in individual notes using frontmatter:

```yaml
---
type: daily
config_override:
  sections:
    log: "## Daily Updates"
---
```

**Note**: This is an advanced feature. Most users should use `.flywheel.json`.

---

## Configuration Generator

Don't want to write JSON by hand? Use the interactive config generator:

```bash
flywheel init --interactive
```

Or use the upcoming v1.9 feature:

```
/generate-config
```

This will:
1. Scan your vault for existing note patterns
2. Detect folder structure
3. Suggest optimal configuration
4. Create `.flywheel.json` for you

---

## See Also

- [ROLLUP_WORKFLOW.md](./ROLLUP_WORKFLOW.md) - How rollup chain uses paths
- [TEMPLATES.md](./TEMPLATES.md) - How templates use paths
- [SIX_GATES.md](./SIX_GATES.md) - How folder protection works
