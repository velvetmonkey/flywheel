# Solo Operator

> Run your one-person business with an AI chief of staff.

---

**You are**: Jordan, a solopreneur running a content business

**Your situation**: You make ~$8K/month from:
- **Newsletter**: "AI Tools Weekly" (2,800 subscribers, 2x/week)
- **Digital product**: AI Automation Course ($297)
- **Consulting**: $300/hour for AI workflow design

Your challenge: doing everything yourself. Claude Code is your chief of staff - it handles ops, tracking, and automation while you focus on creating.

---

## Try it now

Open this vault with Flywheel MCP connected, then ask Claude:

```
"Run my morning standup"
"How's revenue this month?"
"What content is due this week?"
"Show me subscriber growth"
"Do rollup"
```

---

## What you'll discover

- **Automation handles daily ops** - standup, tracking, alerts
- **Track multiple revenue streams** in one place
- **Connect content calendar** to actual writing workflow
- **Watch the rollup chain** turn daily logs into achievements

---

## Quick Setup

### 1. Configure MCP

Create `.mcp.json` in this folder with your platform config:

**Windows (PowerShell/cmd)**:
```json
{
  "mcpServers": {
    "flywheel": {
      "command": "cmd",
      "args": ["/c", "npx", "-y", "flywheel-mcp@latest"],
      "env": {
        "OBSIDIAN_VAULT_PATH": "C:/Users/YOU/path/to/solo-operator"
      }
    }
  }
}
```

**macOS/Linux**:
```json
{
  "mcpServers": {
    "flywheel": {
      "command": "npx",
      "args": ["-y", "flywheel-mcp@latest"],
      "env": {
        "OBSIDIAN_VAULT_PATH": "/path/to/solo-operator"
      }
    }
  }
}
```

### 2. Open in Claude Code

```bash
cd demos/solo-operator
claude
```

### 3. Start operating

Try: "Run my morning standup"

---

## How mutations work

When you ask Claude to make changes:

### Run morning standup

```
You: "Run my morning standup"

┌─ CHAIN ──────────────────────────────────────────┐
│ Reads: yesterday's daily note, Revenue Tracker,  │
│        Content Calendar (~150 tokens)            │
│ Writes: daily-notes/2026-01-07.md               │
└──────────────────────────────────────────────────┘

## Standup (auto-generated 9:00am)

**Yesterday:**
- Newsletter sent: "AI Tools Weekly" (42% open rate)
- Course sales: 1 ($297)

**Today:**
- Draft next newsletter (due Thu)
- Follow up with consulting lead

**Alerts:**
- [!] Subscriber growth slowed                     ← NEW
```

### Add a log entry

```
You: "log sent newsletter, 42% open rate"

┌─ MUTATION ───────────────────────────────────────┐
│ Reads:   ## Log section (38 tokens)              │
│ Appends: daily-notes/2026-01-07.md               │
└──────────────────────────────────────────────────┘

## Log
- 09:00 Morning review
- 10:30 sent newsletter, 42% open rate             ← NEW
```

### Check revenue

```
You: "How's revenue this month?"

┌─ QUERY ──────────────────────────────────────────┐
│ Source: Graph index (no file reads)              │
│ Tokens: ~50 vs ~800 full file                    │
└──────────────────────────────────────────────────┘

Revenue Dashboard (January 2026)
================================
Newsletter Sponsors: $500/mo
Course Sales: $1,188 (4 sales)
Consulting: $1,200 (4 hours)
--------------------------------
Total MTD: $2,888
Target: $8,000
Progress: 36% (on track)
```

### Do a rollup

```
You: "do a rollup"

┌─ CHAIN ──────────────────────────────────────────┐
│ Reads:   7 daily notes, ## Log sections          │
│          (~700 tokens vs ~7,000 full files)      │
│ Creates: weekly-notes/2026-W01.md                │
│ Appends: monthly-notes/2026-01.md                │
│ Appends: Achievements.md                         │
└──────────────────────────────────────────────────┘

### weekly-notes/2026-W01.md (created)
## Week 1 Summary
- Sent 2 newsletters (avg 40% open rate)
- Course sales: $891 (3 sales)
- Consulting: 6 hours billed

## Achievements
- First week with 3+ course sales                  ← NEW
```

---

## Vault structure

```
solo-operator/
├── daily-notes/        # Daily operations log
├── weekly-notes/       # AI-generated weekly summaries
├── content/            # Newsletter and content calendar
├── products/           # Course and consulting tracking
├── ops/                # Revenue and subscriber metrics
├── automations/        # Playbooks for recurring workflows
├── Reference.md        # Personal context for AI
├── Achievements.md     # Rolling log of wins
└── .claude/            # Custom commands and config
```

---

## The pattern

This vault demonstrates the "AI-first operator" pattern:

1. **Reference.md** gives Claude context about you
2. **Daily notes** capture everything with `## Log`
3. **Tracker notes** aggregate data with queryable frontmatter
4. **Automation notes** define recurring workflows
5. **`.claude/commands/`** provides quick triggers

The result: Claude operates as your chief of staff, handling the operational overhead while you focus on creating value.

---

*22 notes. Just start asking questions.*
