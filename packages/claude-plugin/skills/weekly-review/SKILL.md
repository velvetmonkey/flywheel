---
name: weekly-review
description: Comprehensive weekly review with rollup, reflection, wins/challenges, and next week planning
auto_trigger: true
trigger_keywords:
  - weekly review
  - review my week
  - week in review
  - reflect on week
  - end of week review
  - how was my week
  - weekly reflection
  - week summary
allowed-tools: Task, Read, Edit, mcp__flywheel__get_recent_notes, mcp__flywheel__get_all_tasks, mcp__flywheel__search_notes
---

# Weekly Review

Run a comprehensive weekly review that goes beyond data rollup to include reflection, wins/challenges identification, and next week planning.

## Trigger Detection

Activate when user:
- Wants to review their week
- Asks for weekly reflection
- Needs end-of-week summary with planning

## Examples

- "Run my weekly review"
- "Review my week"
- "How was my week?"
- "Weekly reflection for 2026-W01"
- "End of week review"

## Process

1. **Determine Week**
   - If week specified (e.g., "2026-W01"), use it
   - Otherwise, use current ISO week

2. **Delegate to Agent**
   ```
   Task(
       subagent_type="weekly-review-agent",
       description="Run weekly review",
       prompt="Run comprehensive weekly review for [week]. Include rollup, wins/challenges, goal progress, and next week planning."
   )
   ```

3. **Present Results**
   - Show review summary
   - Highlight key wins and challenges
   - Present next week focus areas

4. **Verify Agent Results** (Gate 6)
   - If agent reports success: Re-read the weekly review note to verify content was written
   - If blocked or failed: Inform user "Weekly review failed - please complete manually"
   - If succeeded: Only report success if verification confirms review content present
   - If not found: Alert user that review may not have been written correctly

## Difference from /run-rollup

| Aspect | /run-rollup | /weekly-review |
|--------|-------------|----------------|
| Purpose | Data aggregation | Reflection + planning |
| Output | Stats, habits, logs | Insights, wins, goals |
| Automation | Fully automated | Guided reflection |
| Next steps | None | Next week planning |

## Six Gates Compliance

| Gate | Status | Notes |
|------|--------|-------|
| 1. Read Before Write | Via Agent | Agent reads daily notes before rollup |
| 2. File Exists Check | Via Agent | Agent validates notes exist |
| 3. Chain Validation | ✓ | Sequential: delegate → verify |
| 4. Mutation Confirm | Via Agent | Agent confirms before writes |
| 5. MCP Health | Via Agent | Agent validates MCP connection |
| 6. Post Validation | ✓ | Re-read note to verify review written (step 4) |
