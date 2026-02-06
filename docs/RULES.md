# Claude Code Rules for Obsidian Vaults

This guide explains how to configure Claude Code to work effectively with your Obsidian vault using rules and permissions.

## What Are Claude Code Rules?

Rules are markdown files in `.claude/rules/` that guide Claude's behavior when working with your vault. They define:

- **Formatting conventions** - How to structure notes, use wikilinks, format frontmatter
- **Naming patterns** - File naming conventions for different note types
- **Content guidelines** - Required sections, status values, linking practices

Rules are suggestions, not enforcement. Claude reads them and follows the conventions when creating or editing notes.

## Rule File Structure

Each rule file has YAML frontmatter and markdown content:

```markdown
---
paths: "invoices/**/*.md"
alwaysApply: false
---

# Invoice Format

## Naming Convention

`INV-YYYY-###.md` where ### is sequential...

## Required Frontmatter

\`\`\`yaml
type: invoice
client: "[[Client Name]]"
amount: 5000
status: pending
\`\`\`
```

### Frontmatter Fields

| Field | Description |
|-------|-------------|
| `paths` | Glob pattern for when this rule applies |
| `alwaysApply` | If `true`, rule applies to all files regardless of path |

## Permission Model

Permissions define what Claude **can** do. They're configured in `.claude/settings.json`:

```json
{
  "permissions": {
    "allow": [
      "Read(**/*)",
      "Edit(.claude/rules/**)",
      "Edit(CLAUDE.md)",
      "mcp__flywheel__*"
    ],
    "deny": [
      "Edit",
      "Write"
    ]
  }
}
```

### How Permissions Work

1. **Deny rules are checked first** - If something matches a deny rule, it's blocked
2. **Allow rules are exceptions** - Specific allows override general denies
3. **Order matters** - More specific patterns take precedence

### Common Permission Patterns

| Pattern | Effect |
|---------|--------|
| `Read(**/**)` | Can read any file |
| `Edit` | General edit permission (deny this for safety) |
| `Edit(.claude/rules/**)` | Can edit rule files specifically |
| `Write(CLAUDE.md)` | Can create/update CLAUDE.md |
| `mcp__flywheel__*` | Can use all Flywheel MCP tools |

## Rules vs Permissions

| Aspect | Permissions | Rules |
|--------|-------------|-------|
| **What it is** | Capability control | Convention guidance |
| **Enforcement** | Hard - Claude cannot bypass | Soft - Claude follows voluntarily |
| **Location** | `.claude/settings.json` | `.claude/rules/*.md` |
| **Purpose** | Security, safety | Consistency, quality |

**Example:**
- Permission: "Claude cannot edit files in `content/`"
- Rule: "When editing content, use this heading structure"

## The Self-Improving Feedback Loop

A key benefit of this architecture: **Claude can update its own rules based on your feedback**.

### How It Works

1. Claude helps you with a task
2. You provide feedback: "That's not how I format invoices"
3. Claude updates `.claude/rules/invoice-format.md` with the correction
4. Future interactions follow the improved rule
5. Over time, Claude becomes increasingly personalized

### What Makes This Safe

The permission model ensures Claude can only modify:
- `.claude/rules/**` - Its own instruction files
- `CLAUDE.md` - Project instructions

Claude **cannot** modify your actual vault content directly. This creates a safe sandbox for self-improvement.

## Demo Vaults

The `demos/` directory contains example vaults with working rules:

| Demo | Persona | Key Rules |
|------|---------|-----------|
| `carter-strategy` | Solo consultant | Invoice format, client notes |
| `artemis-rocket` | Rocket startup | Decision records, system notes |
| `nexus-lab` | PhD researcher | Experiment format, literature notes |
| `solo-operator` | Solopreneur | Content notes, automation playbooks |
| `startup-ops` | SaaS startup | Customer records, playbook format |

Each demo includes:
- `.claude/settings.json` - Permission configuration
- `.claude/rules/*.md` - Convention rules
- `CLAUDE.md` - Vault-specific instructions

## Getting Started

1. **Copy a demo's `.claude/` folder** to your vault as a starting point
2. **Customize rules** for your note types and conventions
3. **Adjust permissions** based on your comfort level
4. **Give feedback** when Claude does something differently than you'd like
5. **Watch rules evolve** as Claude learns your preferences

## Best Practices

### Rule Writing

- Be specific about formats with examples
- Include valid values for status/type fields
- Show frontmatter templates
- Explain the "why" not just the "what"

### Permission Configuration

- Start restrictive, allow more as needed
- Always allow `.claude/rules/**` editing for self-improvement
- Use Flywheel MCP tools instead of direct file writes
- Keep read access broad for context

### Feedback Loop

- Correct Claude in natural language
- Be specific: "Use 24-hour time in logs" not "Fix the time format"
- Check rule files periodically to see how they've evolved
