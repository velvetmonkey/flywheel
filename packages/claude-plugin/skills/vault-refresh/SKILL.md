---
name: vault-refresh
description: Rebuild the Flywheel vault index. Use after making changes in Obsidian.
auto_trigger: true
trigger_keywords:
  - "refresh vault"
  - "refresh index"
  - "rebuild index"
  - "refresh flywheel"
  - "update index"
allowed-tools: mcp__flywheel__refresh_index
---

# Vault Refresh

Rebuild the Flywheel MCP vault index.

## When to Use

- After adding/removing notes in Obsidian
- After editing frontmatter or links
- When vault queries return stale data
- After bulk operations on vault files

## Process

1. Call `mcp__flywheel__refresh_index`
2. Report results (notes indexed, duration)

## Expected Output

```
Flywheel - Index Refreshed

  Notes indexed: 245
  Entities indexed: 312
  Duration: 156ms
```

## Six Gates Compliance

| Gate | Implementation |
|------|----------------|
| 1-4 | N/A (read-only operation) |
| 5. Health Check | Uses MCP refresh_index |
| 6. Post Validation | Reports success/failure from tool response |

---

**Version:** 1.0.0 (Flywheel)
