# Rules (Manual Installation Required)

Claude Code plugins cannot bundle rules - they are project-level only. Copy these rules to your vault's `.claude/rules/` directory.

## Installation

```bash
# Create rules directory if it doesn't exist
mkdir -p /path/to/vault/.claude/rules

# Copy rule files (adjust paths for your system)
```

## Included Rules

### 1. obsidian-syntax.md

**Scope:** All markdown files (`**/*.md`)

Prevents common Obsidian-breaking syntax errors:
- **No angle brackets** - `ILogger<T>` breaks all wikilinks after it
- **No wrapped wikilinks** - `**[[Link]]**` breaks hyperlinks
- **No wikilinks in YAML** - Corrupts frontmatter parsing
- **Close code blocks** - Unclosed fences break rendering

```markdown
---
paths: "**/*.md"
alwaysApply: false
---

# Obsidian Markdown Syntax Rules
...
```

### 2. daily-notes.md

**Scope:** Daily notes folder (`daily-notes/**/*.md`)

Enforces daily note structure and formatting:
- Template-based creation (use `templates/daily.md`)
- Correct file naming (`YYYY-MM-DD.md`)
- Proper section structure (Habits, Food, Log)
- Log entries always appended chronologically
- Never use `---` or `## Heading` in Log section

```markdown
---
paths: "daily-notes/**/*.md"
alwaysApply: false
---

# Daily Notes Rules
...
```

### 3. folder-organization.md

**Scope:** All markdown files (`**/*.md`)

Enforces folder hierarchy:
- Protected folders (`personal/`, `work/`, `tech/`) require subfolders
- Periodic notes folders can contain files directly
- Configurable via `.obsidian-scribe.json`

```markdown
---
paths: "**/*.md"
alwaysApply: false
---

# Folder Organization Rules
...
```

### 4. platform-requirements.md

**Scope:** Global (no path restriction)

Documents platform-specific setup:
- WSL: Install `python-is-python3` package
- Windows: Ensure Python 3.8+ in PATH
- Path format differences between platforms

```markdown
# Platform Requirements
...
```

## Rule File Contents

<details>
<summary><strong>obsidian-syntax.md</strong> (click to expand)</summary>

```markdown
---
paths: "**/*.md"
alwaysApply: false
---

# Obsidian Markdown Syntax Rules

These rules apply when editing ANY markdown file in the vault.

## Wikilinks

- Use `[[wikilink]]` format for internal links
- Use `[[Page|Display Text]]` for aliased links

### CRITICAL - Never Wrap Wikilinks

NEVER wrap wikilinks with formatting characters:

WRONG:
**[[Link]]**
*[[Link]]*

CORRECT:
[[Link]]
**Text with [[Link]] inside**

## Angle Brackets

### CRITICAL - No Angle Brackets in Content

NEVER use angle brackets (< >) in Obsidian notes:

WRONG:
ILogger<T>
List<string>

CORRECT:
ILogger(T)
Use code blocks: `ILogger<T>`

## YAML Frontmatter

### CRITICAL - No Wikilinks in YAML Frontmatter

NEVER use wikilinks in YAML frontmatter keys or values.

## Code Blocks

### CRITICAL - Always Close Code Blocks

ALWAYS ensure fenced code blocks have matching opening and closing backticks.
```

</details>

<details>
<summary><strong>daily-notes.md</strong> (click to expand)</summary>

```markdown
---
paths: "daily-notes/**/*.md"
alwaysApply: false
---

# Daily Notes Rules

## File Structure

Daily notes follow this structure:
- Habits section with checkboxes
- Food section for nutrition tracking
- Log section for activities (append only, chronological)

## Naming Convention

- Format: `YYYY-MM-DD.md` (ISO date)
- Path: `daily-notes/YYYY-MM-DD.md`

## Log Section Rules

- ALWAYS append new entries to bottom
- NEVER use `---` or `## Heading` inside Log
- Keep as continuous bullet list
- Use sub-bullets for complex content
```

</details>

<details>
<summary><strong>folder-organization.md</strong> (click to expand)</summary>

```markdown
---
paths: "**/*.md"
alwaysApply: false
---

# Folder Organization Rules

## Protected Top-Level Folders

These folders MUST only contain subfolders, never direct files:
- personal/ → personal/goals/, personal/health/
- work/ → work/projects/, work/notes/
- tech/ → tech/frameworks/, tech/tools/

## Folders That Can Contain Files Directly

- daily-notes/
- weekly-notes/
- monthly-notes/
- quarterly-notes/
- yearly-notes/
- templates/
```

</details>

<details>
<summary><strong>platform-requirements.md</strong> (click to expand)</summary>

```markdown
# Platform Requirements

## WSL (Windows Subsystem for Linux)

Install Python symlink:
sudo apt install python-is-python3

## Windows

Ensure Python 3.8+ is installed and available as `python` in PATH.

## Cross-Platform

All hooks use `python` (not `python3`) for consistency.
The `${CLAUDE_PLUGIN_ROOT}` variable handles path differences.
```

</details>

## Why Rules Aren't Bundled

Claude Code's plugin architecture supports:
- Commands, Agents, Skills (bundled in plugins)
- Hooks, MCP servers (bundled in plugins)

But NOT:
- Rules (project-level only, in `.claude/rules/`)

Rules are auto-discovered from `.claude/rules/` at session start. They cannot be distributed via plugins because they're designed for project-specific customization.

## Customization

After copying to your vault, customize these rules:

1. **paths** - Adjust glob patterns to match your folder structure
2. **Protected folders** - Modify list in `folder-organization.md`
3. **Daily note sections** - Adjust to match your template

Rules with `paths:` frontmatter only apply when editing matching files.
Rules without `paths:` apply globally.
