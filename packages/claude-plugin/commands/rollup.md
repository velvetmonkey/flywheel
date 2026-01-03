# /rollup - Execute Note Rollup Chain

Execute the complete rollup chain processing daily notes into weekly, monthly, quarterly, and yearly summaries.

## Usage

```
/rollup                    # Process last 2 months (default)
/rollup december           # Process specific month
/rollup 2025-Q4            # Process specific quarter
/rollup weekly only        # Just daily → weekly
```

## What It Does

```
Daily Notes                Weekly              Monthly            Yearly
───────────────────────────────────────────────────────────────────────────
Jan 1  ─┐
Jan 2  ─┼─► Week 1 ─┐
Jan 3  ─┤          │
...    ─┘          │
Jan 8  ─┐          ├─► January ─┐
Jan 9  ─┼─► Week 2 ─┤           │
...    ─┘          │           ├─► 2026 ─► Achievements.md
                   ...         │
                              ...
```

## Where Output Goes

| Level | Output Location | Detection Method |
|-------|-----------------|------------------|
| Weekly | `weekly-notes/YYYY-WXX.md` | MCP `detect_periodic_notes("weekly")` |
| Monthly | `monthly-notes/YYYY-MM.md` | MCP `detect_periodic_notes("monthly")` |
| Quarterly | `quarterly-notes/YYYY-QX.md` | MCP `detect_periodic_notes("quarterly")` |
| Yearly | `yearly-notes/YYYY.md` | MCP `detect_periodic_notes("yearly")` |
| Achievements | `Achievements.md` | Config `paths.achievements` |

## Process

1. **Confirm Scope** - User confirms what to process
2. **Launch Agent** - `rollup-agent` handles the chain
3. **Report Results** - Shows what was created/updated

## Example Output

```
Rollup Complete
===============

Processed: Last 2 months

✓ Daily → Weekly: 8 weekly summaries created
✓ Weekly → Monthly: 2 monthly summaries created
✓ Monthly → Quarterly: 1 quarterly summary updated
✓ Achievements: 3 new items extracted

Created files:
- weekly-notes/2026-W01.md
- weekly-notes/2026-W02.md
- monthly-notes/2026-01.md
- Achievements.md (updated)
```
