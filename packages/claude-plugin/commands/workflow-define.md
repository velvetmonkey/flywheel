---
skill: workflow-define
---

# /workflow-define - Define Custom Workflows

Create a custom workflow definition for your vault.

## Usage

```
/workflow-define "Code Review"  # Create new workflow
```

## What It Does

```
Workflow Definition
────────────────────────────────────────────────────────────────
Creating workflow template: Code Review
────────────────────────────────────────────────────────────────
```

## Where Output Goes

| Action | Target | Notes |
|--------|--------|-------|
| Template | workflows/ folder | Workflow definition |
| Trigger | Natural language | Keyword activation |

## Example Output

```
Workflow Definition: Code Review
===============================================

Created: workflows/code-review.md

WORKFLOW TEMPLATE:

---
name: code-review
description: Code review workflow for PRs
trigger_keywords:
  - "code review"
  - "review PR"
  - "review code"
---

# Code Review Workflow

## Checklist
- [ ] Read PR description
- [ ] Check code style
- [ ] Verify tests pass
- [ ] Review security implications
- [ ] Check performance impact
- [ ] Approve or request changes

## Output
- Review comment on PR
- Log entry in daily note

-------------------------------------------------

USAGE:
  Say "code review for PR #123" to trigger

CUSTOMIZATION:
  Edit workflows/code-review.md to modify steps

===============================================
```
