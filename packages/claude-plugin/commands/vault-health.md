---
skill: check-health
---

# /vault-health - Vault Diagnostics

Comprehensive vault health check with diagnostics and recommendations.

## Usage

```
/vault-health                  # Full vault health report
```

## What It Does

```
Vault Analysis
────────────────────────────────────────────────────────────────
Total Notes: 1,000     Total Links: 15,000     Orphans: 100
Broken Links: 200      Avg Links/Note: 15.0    Health: 85%
────────────────────────────────────────────────────────────────
```

## Where Output Goes

| Action | Target | Notes |
|--------|--------|-------|
| Report | Console output | Health report with scores |
| Recommendations | Console output | Suggested next steps |

## Process

1. **Analyze** - Get vault stats from MCP
2. **Score** - Calculate health score (0-100%)
3. **Report** - Show issues and recommendations
4. **Suggest** - Link to relevant fix commands

## Example Output

```
Vault Health Report
===============================================

Overview:
  Total Notes: 1,000
  Total Links: 15,000
  Average Links/Note: 15.0

Issues Found:
  Broken Links: 200 (1.3% of all links)
  Orphan Notes: 100 (10% of all notes)

Top Hubs:
  1. [[Project A]] - 150 backlinks
  2. [[Technology X]] - 120 backlinks
  3. [[Daily Workflow]] - 100 backlinks

Vault Health Score: 85% (Good)

Recommendations:
  Run /fix-links to repair broken links
  Review /orphans to connect isolated notes

===============================================
```
