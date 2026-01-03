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
| 1. Read Before Write | N/A | Agent handles |
| 2. File Exists Check | N/A | Agent validates |
| 3. Chain Validation | N/A | Single delegation |
| 4. Mutation Confirm | N/A | Agent confirms |
| 5. MCP Health | N/A | Agent checks |
| 6. Post Validation | N/A | Agent verifies |
