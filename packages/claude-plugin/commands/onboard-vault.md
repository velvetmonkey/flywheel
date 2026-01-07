---
skill: onboard-vault
---

# /onboard-vault - Welcome & Getting Started

Welcome new users with vault overview and guided first steps.

## Usage

```
/onboard-vault              # Get started with Flywheel
```

## What It Does

```
Welcome to Flywheel
────────────────────────────────────────────────────────────────
Notes: 500     Links: 3,000     Tags: 150     Health: 85%
────────────────────────────────────────────────────────────────
```

## Where Output Goes

| Action | Target | Notes |
|--------|--------|-------|
| Overview | Console output | Vault stats and hub notes |
| Suggestions | Console output | Recommended next commands |

## Process

1. **Health Check** - Verify MCP connection
2. **Stats** - Get vault overview
3. **Hubs** - Find most connected notes
4. **Guide** - Suggest next steps based on vault state

## Example Output

```
Welcome to Flywheel!
===============================================

Your Vault at a Glance:
  Notes: 500
  Links: 3,000
  Tags: 150
  Folders: 25

Your Hub Notes (Most Connected):
  1. [[Projects]] - 45 connections
  2. [[People]] - 38 connections
  3. [[Daily Notes]] - 32 connections

Suggested Next Steps:
  /vault-health     - Deep health analysis
  /vault-orphans    - Find disconnected notes
  /vault-search     - Search your vault

===============================================
```
