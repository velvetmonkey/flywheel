---
name: extract-actions
description: Extract action items from meeting notes into structured tasks
auto_trigger: true
trigger_keywords:
  - extract actions
  - pull action items
  - get todos from meeting
  - meeting actions
  - action items from
  - tasks from meeting
  - what are the action items
  - find action items
allowed-tools: Task, Read, Edit, mcp__flywheel__get_tasks_from_note, mcp__flywheel__search_notes, mcp__flywheel__get_note_metadata
---

# Extract Actions

Extract action items from meeting notes, including natural language action items that aren't in checkbox format.

## Trigger Detection

Activate when user:
- Asks to extract actions from a meeting
- Wants to find action items in notes
- Needs to pull tasks from meeting discussions

## Examples

- "Extract actions from today's standup"
- "What are the action items from the sprint planning meeting?"
- "Pull tasks from meetings/2026-01-03 Client Call.md"
- "Find action items in my last meeting"

## Process

1. **Identify Meeting Note**
   - If path provided, use it directly
   - If not, search for recent meeting notes
   - Ask user to confirm which meeting

2. **Delegate to Agent**
   ```
   Task(
       subagent_type="action-extraction-agent",
       description="Extract action items from meeting",
       prompt="Extract all action items from [meeting path]. Include both checkbox tasks and natural language action items."
   )
   ```

3. **Present Results**
   - Show extracted actions with owners and due dates
   - Offer to create tasks in daily notes (optional)

4. **Verify Agent Results**
   - If agent reports success: Re-read the meeting note to verify actions were extracted
   - If blocked or failed: Inform user "Action extraction failed - please extract manually"
   - If succeeded: Only report success if extraction was verified
   - If not found: Alert user that actions may not have been extracted correctly

## Six Gates Compliance

| Gate | Status | Notes |
|------|--------|-------|
| 1. Read Before Write | Via Agent | Agent reads meeting note before extraction |
| 2. File Exists Check | Via Agent | Agent validates meeting note exists |
| 3. Chain Validation | ✓ | Sequential: identify → delegate → verify |
| 4. Mutation Confirm | Via Agent | Agent confirms before any writes |
| 5. MCP Health | Via Agent | Agent validates MCP connection |
| 6. Post Validation | ✓ | Re-read note to verify extraction succeeded |
