---
name: add-log
description: Auto-log entries to daily note. Triggers when user wants to log, record, or document their work. Detects "log", "captains log", "dictate", "record", "note this", "write this down", "document", "track this", "remember", "add to log", or similar logging intent.
auto_trigger: true
trigger_keywords:
  - "log"
  - "captains log"
  - "dictate"
  - "record"
  - "note this"
  - "write this down"
  - "document this"
  - "track this"
  - "remember this"
  - "add to log"
  - "add to my log"
  - "log this"
  - "record this"
  - "make a note"
  - "take note"
allowed-tools: Read, Edit
---

# Auto Log Entry

Automatically add a timestamped log entry to today's daily note when user wants to log their work.

## Trigger Detection

This skill activates when the user's prompt contains logging intent:
- "log" / "log this" / "add to log"
- "captains log"
- "dictate" / "record" / "record this"
- "note this" / "make a note" / "take note"
- "write this down" / "remember this"
- "document this" / "track this"

The text after the trigger word (or the context) becomes the log entry description.

## Examples

User prompts that trigger this skill:
- "log Fixed authentication bug"
- "captains log Meeting with product team"
- "dictate Deployed new feature to staging"
- "record Completed code review for PR #123"

## Process

1. **Extract log description**
   - Remove the trigger word from the start of the prompt
   - Use remaining text as the log description
   - Preserve any [[wikilinks]] in the description

2. **Get current time**
   - Parse from injected UserPromptSubmit hook context: "Time: HH:MM"
   - Extract: "HH:MM"
   - Format: HH:MM (24-hour format)
   - **IMPORTANT**: Do NOT use Bash or PowerShell commands. Time is provided by hook context.

3. **Construct daily note path**
   - Use today's date (YYYY-MM-DD format)
   - Path: `{paths.daily_notes}/YYYY-MM-DD.md` (from config)

4. **Read the daily note**
   - Find the Log section (from config `sections.log`, default: `## Log`)

5. **Add the log entry**
   - Format: `- HH:MM [log description]`
   - Add after the last log entry in the section
   - Use Edit tool to insert the new entry

6. **Confirm**
   - Display the added entry with timestamp and location

## Log Section Format

```markdown
## Log

- 13:54 Fixed authentication issue
- 15:34 Deployed to staging
- 16:03 Made significant progress with [[Project]]
```

## Critical Rules

- **Timestamp required**: Always include HH:MM format
- **Preserve structure**: Don't modify other sections
- **Bullet format**: Use `- HH:MM description` format
- **Today only**: Only add to current day's note
- **Wikilinks**: Preserve any [[wikilinks]] in the user's description
- **No empty logs**: If no description after trigger word, ask user what to log
- **Exact match**: Only trigger on prompts that START with trigger words (case-insensitive)

## Edge Cases

- If prompt is just "log" with no description, ask: "What would you like to log?"
- If daily note doesn't exist, create it using the template
- Preserve existing log formatting and order

## Configuration

This skill uses these config values:
- `paths.daily_notes`: Folder containing daily notes (default: "daily-notes")
- `sections.log`: Log section header (default: "## Log")
