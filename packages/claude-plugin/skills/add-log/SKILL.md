---
name: add-log
description: Add timestamped log entry to daily note when user wants to log their work
auto_trigger: true
trigger_keywords:
  - "add log entry"
  - "log entry"
  - "log to daily"
  - "add to log"
  - "add to my log"
  - "captains log"
  - "log this to daily"
  - "record to daily"
  - "write this down"
  - "document this"
allowed-tools: Read, Edit
---

# Auto Log Entry

Automatically add a timestamped log entry to today's daily note when user wants to log their work.

## Where Does Output Go?

```
┌─────────────────────────────────────────────────────┐
│ INPUT:  "add log entry: Fixed the bug"              │
│                                                     │
│ OUTPUT: daily-notes/2026-01-03.md                   │
│         └─► ## Log section (appended)               │
│             └─► - 14:32 Fixed the bug               │
└─────────────────────────────────────────────────────┘

How location is determined:
1. MCP detect_periodic_notes("daily") → finds daily notes folder
2. Today's date → 2026-01-03.md
3. sections.log (default: "Log") → finds ## Log heading
4. Appends after last log entry
```

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
   - **Check Edit result** - if blocked or failed:
     - Inform user: "Edit was blocked or failed. Please confirm the mutation or add manually."
     - Do NOT proceed to confirmation

6. **Verify the write succeeded**
   - Re-read the daily note file
   - Search for the newly added log entry (the exact description + timestamp)
   - If NOT found: Alert user "Log write failed - please add manually: `- HH:MM [description]`"
   - If found: Proceed to confirmation

7. **Confirm** (only if Step 6 succeeded)
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

## Six Gates Compliance

| Gate | Implementation |
|------|----------------|
| 1. Read Before Write | Reads daily note before adding entry (step 4) |
| 2. File Exists | Validates daily note exists; creates if missing |
| 3. Chain Validation | N/A (single operation) |
| 4. Mutation Confirmation | Entry shown to user before write |
| 5. Health Check | Uses vault config infrastructure |
| 6. Post Validation | **Re-reads file and verifies entry was written** (step 6) |

## Configuration

This skill uses these config values:
- `paths.daily_notes`: Folder containing daily notes (default: "daily-notes")
- `sections.log`: Log section header text (default: "Log")

**Note**: Section matching is case-insensitive and level-agnostic. "Log" matches `# Log`, `## Log`, `### LOG`, etc.
