---
name: obsidian-scribe-rollup
description: Execute the complete rollup chain processing daily notes into weekly, monthly, quarterly, and yearly summaries, then updating achievements. Triggers when user mentions "rollup", "summarize notes", "weekly summary", "monthly summary", "process my notes", "update achievements", or wants to aggregate their work logs.
auto_trigger: true
trigger_keywords:
  - "rollup"
  - "do rollup"
  - "run rollup"
  - "process rollup"
  - "summarize my notes"
  - "weekly summary"
  - "monthly summary"
  - "quarterly summary"
  - "yearly summary"
  - "update achievements"
  - "process my daily notes"
  - "aggregate my logs"
  - "compile my work"
allowed-tools: Task
---

# Rollup Chain Processor

Execute the complete note summarization chain: daily → weekly → monthly → quarterly → yearly → achievements.

## When This Skill Activates

This skill triggers when you say:
- "Do rollup"
- "Run the rollup chain"
- "Summarize my notes"
- "Create weekly summary"
- "Update my achievements"
- "Process my daily notes"
- "Compile this month's work"

## Your Task

When user requests rollup processing:

### 1. Confirm Scope

Ask if needed:
- "Process last 2 months?" (default)
- Or specific timeframe: "Process December only"
- Or specific level: "Just weekly summaries"

### 2. Execute Rollup Agent

Launch the appropriate rollup agent to process the chain:

```javascript
Task({
  subagent_type: "obsidian-scribe-rollup-agent",
  description: "Process rollup chain",
  prompt: "Execute the complete rollup chain for the last 2 months"
})
```

### 3. Monitor Progress

The rollup agent will:
1. Process daily notes → weekly summaries
2. Process weekly summaries → monthly summaries
3. Process monthly summaries → quarterly summaries
4. Process quarterly summaries → yearly summaries
5. Extract achievements and update Achievements file

### 4. Confirm Results

After rollup completes, tell the user:
- ✅ What was processed
- 📊 How many notes were summarized
- 🏆 What achievements were extracted
- 📁 Which files were updated

## What Gets Rolled Up

### Daily Notes → Weekly Summary
- Log entries
- Accomplishments
- Habits completed
- Food tracking
- Work done

### Weekly → Monthly
- Key achievements
- Projects worked on
- Patterns and trends
- Important events

### Monthly → Quarterly
- Major milestones
- Quarter achievements
- Growth areas
- Strategic progress

### Quarterly → Yearly
- Annual achievements
- Yearly themes
- Big picture wins
- Personal growth

### → Achievements File
- Notable accomplishments
- Skills developed
- Projects completed
- Career milestones

## Examples

**User says**: "Run rollup"

**You do**:
1. Confirm: "I'll process the rollup chain for the last 2 months. This will update weekly, monthly, quarterly, and yearly summaries, plus achievements. Proceed?"
2. Launch rollup agent
3. Monitor progress
4. Report results

**User says**: "Summarize December"

**You do**:
1. Clarify: "Process December daily notes into weekly and monthly summaries?"
2. Launch rollup agent with December scope
3. Report results

**User says**: "Update my achievements"

**You do**:
1. Confirm: "I'll run the full rollup chain to extract achievements from your recent work. Last 2 months?"
2. Process rollup
3. Report achievements found

## Critical Rules

- ✅ **Ask before processing**: Confirm scope with user
- ✅ **Use rollup agents**: Always delegate to specialized agents
- ✅ **Report progress**: Keep user informed
- ✅ **Preserve existing**: Don't overwrite, only add new summaries
- ✅ **Extract intelligently**: Only log genuine achievements
- ✅ **Maintain format**: Follow established summary formats

## Scope Options

User can request:
- **Default**: Last 2 months (daily→weekly→monthly→quarterly→yearly→achievements)
- **Specific month**: "December" (daily→weekly→monthly)
- **Specific level**: "Just weekly" (daily→weekly only)
- **Full year**: "All of 2025" (entire year rollup)

Always clarify scope if ambiguous.

## Configuration

This skill uses these config values:
- `paths.daily_notes`: Daily notes folder
- `paths.weekly_notes`: Weekly notes folder
- `paths.monthly_notes`: Monthly notes folder
- `paths.quarterly_notes`: Quarterly notes folder
- `paths.yearly_notes`: Yearly notes folder
- `paths.achievements`: Achievements file path
