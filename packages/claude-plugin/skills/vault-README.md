# Vault Intelligence Suite

**Comprehensive Vault Analysis & Maintenance Skills**

These skills require the [smoking-mirror MCP server](https://github.com/coddingtonbear/obsidian-mcp) for Obsidian vault intelligence.

---

## Overview

This suite provides:
- **Vault Health**: Diagnostics, broken link detection, maintenance
- **Graph Intelligence**: Backlinks, hubs, clusters, orphans
- **Content Discovery**: Search, related notes, knowledge gaps
- **Automation**: Scheduled maintenance, auto-linking, insights

---

## Available Skills

### Core Skills (P0 - Essential)

| Skill | Trigger | Purpose |
|-------|---------|---------|
| **health** | "vault health", "health report" | Quick vault diagnostics |
| **fix-links** | "fix links", "broken links" | Preview and repair broken links |
| **backlinks** | "backlinks", "who links here" | Show note connections |

### Discovery Skills (P1 - Exploration)

| Skill | Trigger | Purpose |
|-------|---------|---------|
| **orphans** | "orphan notes", "disconnected" | Find isolated notes |
| **hubs** | "hub notes", "most connected" | Find highly connected notes |
| **search** | "vault search", "find notes with" | Advanced queries |
| **suggest** | "suggest links", "wikilink suggestions" | Suggest links for current note |

### Analysis Skills (P2 - Deep Insights)

| Skill | Trigger | Purpose |
|-------|---------|---------|
| **bidirectional** | "bidirectional links", "one-way" | Find asymmetric links |
| **clusters** | "clusters", "communities" | Find knowledge groups |
| **dead-ends** | "dead ends", "endpoint notes" | Notes with no outgoing links |
| **related** | "related notes", "similar to" | Find similar notes |
| **gaps** | "knowledge gaps", "content gaps" | Find missing topics |
| **stale** | "stale notes", "old notes" | Find neglected notes |
| **link-density** | "link density", "link analysis" | Analyze link patterns |
| **folder-health** | "folder health", "vault organization" | Analyze folder structure |

---

## Requirements

These skills require the **smoking-mirror MCP** server to be configured:

```json
{
  "mcpServers": {
    "smoking-mirror": {
      "command": "cmd",
      "args": ["/c", "npx", "-y", "@anthropic/smoking-mirror-mcp"],
      "env": {
        "OBSIDIAN_VAULT_PATH": "C:/path/to/your/vault"
      }
    }
  }
}
```

---

## Visual Identity

All vault skills use consistent output branding:

```
Vault Health Report
═══════════════════════════════════════════════

[Content]

═══════════════════════════════════════════════
```

---

## Quick Start

### Check Vault Health
```
User: "vault health"
→ Shows diagnostics, broken links, orphans, top hubs
```

### Fix Broken Links
```
User: "fix broken links"
→ Preview broken links
→ Spawn autonomous repair agent
```

### Find Connections
```
User: "backlinks for MyProject"
→ Shows all notes linking to/from MyProject
```

---

**Version:** 1.0.0
