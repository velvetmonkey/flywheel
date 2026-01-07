# Rollup Workflow Deep-Dive

The rollup workflow is Flywheel's flagship feature for automatically summarizing time-series notes into hierarchical summaries.

---

## Overview

```
Daily Notes (7 days)
    ↓ rollup-weekly-agent
Weekly Summary (1 note)
    ↓ rollup-monthly-agent
Monthly Summary (~4 weeks)
    ↓ rollup-quarterly-agent
Quarterly Summary (3 months)
    ↓ rollup-yearly-agent
Yearly Summary (4 quarters)
```

**Key Insight**: Each level aggregates from the level below, creating a lossy compression hierarchy that preserves signal while reducing noise.

---

## Quick Start

### Trigger Rollup

```bash
# Trigger from Claude Code
/rollup

# Or natural language
"summarize my notes"
"run the rollup chain"
"update my weekly summary"
```

### What Happens

1. **rollup-agent** (orchestrator) starts
2. Calculates date range (last 2 months)
3. Spawns **weekly-agent** for each ISO week
4. Each weekly agent:
   - Finds 7 daily notes for its week
   - Extracts habits, food, log entries
   - Writes `weekly-notes/YYYY-WXX.md`
5. Spawns **monthly-agent** for each month
6. Each monthly agent aggregates weekly notes
7. If quarter-end, spawns **quarterly-agent**
8. If year-end, spawns **yearly-agent**
9. Reports completion

---

## The Rollup Chain

### Level 1: Daily → Weekly

**Agent**: `rollup-weekly-agent`

**Input**: 7 daily notes (`daily-notes/YYYY-MM-DD.md`)

**Output**: 1 weekly summary (`weekly-notes/YYYY-WXX.md`)

**Process**:

```python
# 1. Calculate date range
start_date = get_week_start("2026-W01")  # 2025-12-29
end_date = get_week_end("2026-W01")      # 2026-01-04

# 2. Find daily notes
daily_notes = [
    "daily-notes/2025-12-29.md",
    "daily-notes/2025-12-30.md",
    # ... 7 total
]

# 3. Extract data from each daily note
for note in daily_notes:
    habits += extract_section(note, "## Habits")
    food += extract_section(note, "## Food")
    log += extract_section(note, "## Log")

# 4. Aggregate
habits_summary = calculate_completion_rate(habits)
food_summary = calculate_macros_total(food)
achievements = extract_significant_items(log)

# 5. Write weekly summary
write("weekly-notes/2026-W01.md", template)
```

**Extracted Data**:

| Section | Extraction Pattern | Output Format |
|---------|-------------------|---------------|
| **Habits** | `- [x] Walk` | `Walk: 6/7 (85.7%)` |
| **Food** | `- 09:00 Oatmeal (300cal, 10p, 50c, 5f)` | `Total: 14,000cal, 490p, 1400c, 420f` |
| **Log** | `- 10:00 Completed feature X` | Bullet list of achievements |

---

### Level 2: Weekly → Monthly

**Agent**: `rollup-monthly-agent`

**Input**: ~4 weekly summaries (`weekly-notes/YYYY-WXX.md`)

**Output**: 1 monthly summary (`monthly-notes/YYYY-MM.md`)

**Process**:

```python
# 1. Determine weeks in month
weeks = get_iso_weeks_for_month("2026-01")  # [2026-W01, W02, W03, W04, W05]

# 2. Read weekly summaries
weekly_notes = [
    "weekly-notes/2026-W01.md",
    "weekly-notes/2026-W02.md",
    # ... ~4-5 total
]

# 3. Aggregate weekly data
monthly_habits = average(weekly_habits)
monthly_macros = sum(weekly_macros)
monthly_achievements = merge(weekly_achievements)

# 4. Write monthly summary
write("monthly-notes/2026-01.md", template)
```

**Aggregation Rules**:

- **Habits**: Average completion rate across weeks
- **Food**: Sum total macros (calories, protein, carbs, fat)
- **Achievements**: Merge all weekly achievement lists
- **Themes**: Identify patterns across weeks

---

### Level 3: Monthly → Quarterly

**Agent**: `rollup-quarterly-agent`

**Input**: 3 monthly summaries (`monthly-notes/YYYY-MM.md`)

**Output**: 1 quarterly summary (`quarterly-notes/YYYY-QX.md`)

**Process**:

```python
# 1. Determine months in quarter
months = ["2026-01", "2026-02", "2026-03"]  # Q1

# 2. Read monthly summaries
monthly_notes = [
    "monthly-notes/2026-01.md",
    "monthly-notes/2026-02.md",
    "monthly-notes/2026-03.md"
]

# 3. Synthesize quarterly themes
big_achievements = extract_major_milestones(monthly_notes)
patterns = identify_quarterly_patterns(monthly_notes)

# 4. Write quarterly summary
write("quarterly-notes/2026-Q1.md", template)
```

**Synthesis Focus**:

- **Major Milestones**: Filter for significant achievements only
- **Patterns**: Recurring themes across 3 months
- **Trajectory**: Growth, decline, or stability in metrics
- **Strategic**: Tie to quarterly goals/OKRs if available

---

### Level 4: Quarterly → Yearly

**Agent**: `rollup-yearly-agent`

**Input**: 4 quarterly summaries (`quarterly-notes/YYYY-QX.md`)

**Output**: 1 yearly summary (`yearly-notes/YYYY.md`)

**Process**:

```python
# 1. Read all quarterly summaries
quarters = [
    "quarterly-notes/2026-Q1.md",
    "quarterly-notes/2026-Q2.md",
    "quarterly-notes/2026-Q3.md",
    "quarterly-notes/2026-Q4.md"
]

# 2. Extract year-level insights
top_achievements = rank_by_impact(all_achievements)
year_patterns = identify_annual_patterns(quarters)
growth_metrics = calculate_year_over_year(quarters)

# 3. Write yearly summary
write("yearly-notes/2026.md", template)
```

**Yearly Focus**:

- **Top 10 Achievements**: Most impactful accomplishments
- **Annual Patterns**: What defined the year
- **Growth Metrics**: Quantitative progress
- **Reflection**: Lessons learned, what to change

---

## Date Range Calculation

Rollup uses ISO 8601 week numbers for consistency.

### ISO Week Rules

- Week starts on Monday
- Week 1 is the week with January 4th
- Weeks span Sunday → Saturday (ISO: Monday → Sunday)

**Example**:

```
2025-12-29 (Monday) → 2026-W01
2025-12-30 (Tuesday) → 2026-W01
2025-12-31 (Wednesday) → 2026-W01
2026-01-01 (Thursday) → 2026-W01
2026-01-02 (Friday) → 2026-W01
2026-01-03 (Saturday) → 2026-W01
2026-01-04 (Sunday) → 2026-W01
```

**Why ISO Weeks Matter**:

- Consistent week boundaries across years
- Avoids partial weeks at year boundaries
- Matches international standards

### Python Date Calculation

```python
from datetime import datetime, timedelta

def get_week_start(iso_week: str) -> str:
    """Convert ISO week to start date (Monday)."""
    year, week = iso_week.split("-W")
    jan4 = datetime(int(year), 1, 4)
    week1_monday = jan4 - timedelta(days=jan4.weekday())
    target_monday = week1_monday + timedelta(weeks=int(week) - 1)
    return target_monday.strftime("%Y-%m-%d")

def get_week_end(iso_week: str) -> str:
    """Convert ISO week to end date (Sunday)."""
    start = get_week_start(iso_week)
    end = datetime.strptime(start, "%Y-%m-%d") + timedelta(days=6)
    return end.strftime("%Y-%m-%d")
```

---

## Template Customization

### Weekly Template

Default: `templates/weekly.md`

```markdown
---
type: weekly
week: {{week}}
start_date: {{start_date}}
end_date: {{end_date}}
---
# Week {{week}}

## Achievements

{{achievements}}

## Habits

{{habits_summary}}

## Food Summary

{{food_macros}}

## Reflection

(To be filled manually)

## Next Week Goals

(To be filled manually)
```

**Variables Available**:

- `{{week}}` - ISO week number (e.g., `2026-W01`)
- `{{start_date}}` - Week start (Monday)
- `{{end_date}}` - Week end (Sunday)
- `{{achievements}}` - Bullet list from daily logs
- `{{habits_summary}}` - Completion rates
- `{{food_macros}}` - Total calories/protein/carbs/fat

### Monthly Template

Default: `templates/monthly.md`

```markdown
---
type: monthly
month: {{month}}
---
# {{month_name}} {{year}}

## Summary

{{weeks_summary}}

## Achievements

{{achievements}}

## Metrics

- **Habits**: {{avg_habits}}
- **Total Calories**: {{total_calories}}

## Reflection

(To be filled manually)
```

**Variables Available**:

- `{{month}}` - YYYY-MM format
- `{{month_name}}` - Full month name (January)
- `{{year}}` - Year (2026)
- `{{weeks_summary}}` - Summary of included weeks
- `{{achievements}}` - Merged from weekly notes
- `{{avg_habits}}` - Average habit completion
- `{{total_calories}}` - Sum of weekly totals

---

## Extraction Patterns

### Habits Extraction

**Pattern**: Look for checkbox lists under `## Habits`

```markdown
## Habits

- [x] Walk
- [ ] Stretch
- [x] Vitamins
```

**Extraction**:

```python
habits = {
    "Walk": True,
    "Stretch": False,
    "Vitamins": True
}

# Weekly aggregation
weekly_habits = {
    "Walk": 6/7,  # 85.7%
    "Stretch": 3/7,  # 42.9%
    "Vitamins": 7/7  # 100%
}
```

### Food Extraction

**Pattern**: Look for timestamped food entries under `## Food`

```markdown
## Food

- 09:00 Oatmeal (300cal, 10p, 50c, 5f)
- 12:00 Chicken salad (450cal, 35p, 20c, 20f)
- 18:00 Salmon (500cal, 40p, 10c, 25f)
```

**Extraction**:

```python
import re

pattern = r'\((\d+)cal, (\d+)p, (\d+)c, (\d+)f\)'
daily_total = {
    "calories": 0,
    "protein": 0,
    "carbs": 0,
    "fat": 0
}

for entry in food_entries:
    match = re.search(pattern, entry)
    if match:
        daily_total["calories"] += int(match.group(1))
        daily_total["protein"] += int(match.group(2))
        daily_total["carbs"] += int(match.group(3))
        daily_total["fat"] += int(match.group(4))
```

### Log Achievements Extraction

**Pattern**: Timestamped entries under `## Log`

```markdown
## Log

- 10:00 Completed authentication refactor
- 14:00 Fixed critical bug in payment flow
- 16:00 Deployed v2.1.0 to production
```

**Extraction**:

```python
# Filter for significant achievements
keywords = ["completed", "finished", "deployed", "launched", "delivered", "shipped"]

achievements = [
    entry for entry in log_entries
    if any(keyword in entry.lower() for keyword in keywords)
]
```

---

## Handling Missing Notes

### Partial Weeks

If some daily notes are missing:

1. ✅ **Proceed** with available notes
2. ⚠️ **Warn** user about missing notes
3. 📊 **Calculate** metrics only from available data
4. 📝 **Note** coverage in summary (e.g., "5/7 days tracked")

**Example Warning**:

```
⚠️ Week 2026-W01: Only 5/7 daily notes found
Missing: 2025-12-29, 2025-12-30
Rollup will proceed with available notes.
```

### Empty Sections

If a daily note exists but a section is empty:

1. ✅ **Skip** that section for that day
2. 📊 **Aggregate** only from notes with data
3. 📝 **Note** partial data in summary

**Example**:

```markdown
## Habits

Walk: 4/7 (57.1%)
- Note: Only 4 days tracked habits
```

---

## Troubleshooting

### Issue: "No daily notes found for week 2026-W01"

**Cause**: Daily notes don't match expected path pattern

**Fix**:

1. Check `.flywheel.json` → `paths.daily_notes`
2. Verify daily notes use `YYYY-MM-DD.md` format
3. Ensure notes are in correct folder

**Example**:

```json
{
  "paths": {
    "daily_notes": "journal/daily"  // Check this matches actual folder
  }
}
```

### Issue: "Weekly summary has no content"

**Cause**: Daily notes don't have required sections

**Fix**:

1. Check `.flywheel.json` → `sections`
2. Ensure daily notes have `## Habits`, `## Food`, `## Log` sections
3. Verify section headings match exactly (case-sensitive)

### Issue: "Date parsing failed"

**Cause**: ISO week calculation error (rare)

**Fix**:

1. Verify week number is valid (W01-W53)
2. Check year boundary cases (Dec 29 → Jan 4)
3. Report bug if ISO week calculation is incorrect

### Issue: "Food macros showing zero"

**Cause**: Food entries don't match expected format

**Fix**:

Ensure food entries use this exact format:

```markdown
- HH:MM Food name (XXXcal, XXp, XXc, XXf)
```

**Valid**:
- `09:00 Oatmeal (300cal, 10p, 50c, 5f)` ✅

**Invalid**:
- `Oatmeal (300 calories)` ❌ (missing timestamp, wrong format)
- `09:00 Oatmeal 300cal` ❌ (missing parentheses)

---

## Advanced: Customizing Extraction

### Custom Section Patterns

Override default sections in `.flywheel.json`:

```json
{
  "sections": {
    "log": "## Daily Updates",
    "exercise": "## Workout",
    "mood": "## Mood Tracker"
  }
}
```

Then modify templates to use these sections.

### Custom Aggregation Logic

For advanced users: Modify agent prompts in `agents/rollup/weekly-agent.md`:

```markdown
## Phase 3: Extract Data

Instead of default habit tracking, extract custom metrics:

- **Exercise Minutes**: Sum from ## Workout section
- **Mood Score**: Average from ## Mood Tracker (1-10 scale)
```

---

## Performance

Rollup chain is optimized for speed:

| Level | Input Notes | Processing Time |
|-------|-------------|-----------------|
| Weekly | 7 daily notes | ~5 seconds |
| Monthly | 4-5 weekly notes | ~3 seconds |
| Quarterly | 3 monthly notes | ~2 seconds |
| Yearly | 4 quarterly notes | ~2 seconds |
| **Total Chain** | **~60 daily notes** | **~15 seconds** |

**Optimization Techniques**:

1. **Parallel Reads**: Read all daily notes simultaneously (not sequential)
2. **Surgical Extraction**: Use `get_section_content()` instead of reading entire files
3. **MCP Queries**: Use Flywheel MCP for metadata (skip full file reads)
4. **Caching**: Wikilink entity cache rebuilt once per session

---

## See Also

- [WORKFLOW_CONFIGURATION.md](./WORKFLOW_CONFIGURATION.md) - Configure paths and sections
- [TEMPLATES.md](./TEMPLATES.md) - Customize rollup templates
- [SIX_GATES.md](./SIX_GATES.md) - How rollup chain respects gates
- [AGENTS_REFERENCE.md](./AGENTS_REFERENCE.md) - Rollup agent details
