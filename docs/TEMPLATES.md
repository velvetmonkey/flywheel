# Template System Reference

Flywheel's template system allows you to create structured notes with variable interpolation using `{{variable}}` syntax.

---

## Quick Start

### Use a Built-in Template

```
/onboard-customer Acme Corp
```

This uses `templates/customer-onboarding.md` and replaces `{{customer}}` with "Acme Corp".

### Create a Custom Template

1. Create file in `templates/my-template.md`
2. Add `{{variables}}` where needed
3. Use in skills/agents

**Example**:

```markdown
---
type: meeting
date: {{date}}
---
# Meeting: {{title}}

**Attendees**: {{attendees}}
```

---

## Built-in Templates

Flywheel v1.8 includes 9 built-in templates:

| Template | Purpose | Key Variables | Used By |
|----------|---------|---------------|---------|
| `daily.md` | Daily journal note | `{{date}}` | Auto-created by hooks |
| `weekly.md` | Weekly summary | `{{week}}`, `{{start_date}}`, `{{end_date}}` | rollup-weekly-agent |
| `monthly.md` | Monthly summary | `{{month}}`, `{{month_name}}`, `{{year}}` | rollup-monthly-agent |
| `quarterly.md` | Quarterly review | `{{quarter}}`, `{{year}}` | rollup-quarterly-agent |
| `yearly.md` | Yearly review | `{{year}}` | rollup-yearly-agent |
| `meeting.md` | Meeting notes | `{{title}}`, `{{date}}`, `{{attendees}}` | action-extraction-agent |
| `standup.md` | Daily standup | `{{author}}`, `{{date}}` | standup-agent |
| `okr.md` | OKR tracking | `{{quarter}}`, `{{objective}}` | okr-review-agent |
| `customer-onboarding.md` | Onboarding checklist | `{{customer}}`, `{{date}}` | customer-onboarding-agent |

---

## Variable Syntax

### Simple Variables

```markdown
Hello {{name}}!
```

**Interpolation**:

```python
variables = {"name": "World"}
# Result: "Hello World!"
```

### Variables in Frontmatter

```yaml
---
type: meeting
date: {{date}}
customer: "{{customer}}"
---
```

**Interpolation**:

```python
variables = {"date": "2026-01-03", "customer": "Acme Corp"}
# Result:
# date: 2026-01-03
# customer: "Acme Corp"
```

**Note**: Always quote string variables in YAML frontmatter.

### Variables in Wikilinks

```markdown
Customer: [[{{customer}}]]
```

**Interpolation**:

```python
variables = {"customer": "Acme Corp"}
# Result: "Customer: [[Acme Corp]]"
```

### Nested Variables

```markdown
Host: {{config.server.host}}
```

**Interpolation**:

```python
variables = {
    "config": {
        "server": {
            "host": "localhost"
        }
    }
}
# Result: "Host: localhost"
```

---

## Built-in Template Details

### `daily.md`

**Purpose**: Daily journal note structure

**Variables**:
- `{{date}}` - YYYY-MM-DD format

**Template**:

```markdown
---
type: daily
date: {{date}}
---
# {{date}}

## Habits

- [ ] Walk
- [ ] Stretch
- [ ] Vitamins

## Food

-

## Tasks

- [ ]

## Log

-
```

**Used By**: Session-start hook (auto-creates if missing)

---

### `weekly.md`

**Purpose**: Weekly rollup summary

**Variables**:
- `{{week}}` - ISO week (YYYY-WXX)
- `{{start_date}}` - Week start (Monday)
- `{{end_date}}` - Week end (Sunday)
- `{{achievements}}` - Bullet list
- `{{habits_summary}}` - Completion rates
- `{{food_macros}}` - Total calories/macros

**Template**:

```markdown
---
type: weekly
week: {{week}}
start_date: {{start_date}}
end_date: {{end_date}}
---
# Week {{week}}

**Period**: {{start_date}} to {{end_date}}

## Achievements

{{achievements}}

## Habits

{{habits_summary}}

## Food Summary

{{food_macros}}

## Reflection

(To be filled)

## Next Week Goals

(To be filled)
```

**Used By**: rollup-weekly-agent

---

### `monthly.md`

**Purpose**: Monthly rollup summary

**Variables**:
- `{{month}}` - YYYY-MM
- `{{month_name}}` - Full month name
- `{{year}}` - Year
- `{{weeks_summary}}` - Week range
- `{{achievements}}` - Merged achievements
- `{{avg_habits}}` - Average habit %
- `{{total_calories}}` - Sum of weekly calories

**Template**:

```markdown
---
type: monthly
month: {{month}}
---
# {{month_name}} {{year}}

**Weeks**: {{weeks_summary}}

## Summary

## Achievements

{{achievements}}

## Metrics

- **Habits**: {{avg_habits}}
- **Total Calories**: {{total_calories}}

## Reflection

(To be filled)

## Next Month Goals

(To be filled)
```

**Used By**: rollup-monthly-agent

---

### `meeting.md`

**Purpose**: Meeting notes with action items

**Variables**:
- `{{title}}` - Meeting title
- `{{date}}` - Meeting date
- `{{attendees}}` - Comma-separated list (optional)

**Template**:

```markdown
---
type: meeting
date: {{date}}
attendees: []
tags:
  - meeting
---
# Meeting: {{title}}

**Date**: {{date}}
**Attendees**:

## Agenda

1.

## Discussion



## Action Items

- [ ]

## Decisions Made

-

## Next Steps

- **Next Meeting**:
- **Follow-ups**:
```

**Used By**: action-extraction-agent

---

### `standup.md`

**Purpose**: Daily standup format

**Variables**:
- `{{author}}` - Team member name
- `{{date}}` - Standup date

**Template**:

```markdown
---
type: standup
author: {{author}}
date: {{date}}
---
# {{author}} - Daily Standup

## Yesterday

-

## Today

-

## Blockers

-
```

**Used By**: standup-agent

---

### `okr.md`

**Purpose**: OKR tracking with scoring

**Variables**:
- `{{quarter}}` - YYYY-QX
- `{{year}}` - Year
- `{{objective}}` - High-level goal (optional)

**Template**:

```markdown
---
type: okr
quarter: {{quarter}}
---
# OKRs: {{quarter}}

## Objective 1: [Your Objective]

### Key Result 1: [Measurable outcome]

- **Baseline**: [Starting value]
- **Target**: [Goal value]
- **Current**: [Current value]
- **Score**: <!-- Calculated by agent -->

### Key Result 2: [Measurable outcome]

- **Baseline**:
- **Target**:
- **Current**:
- **Score**:

### Key Result 3: [Measurable outcome]

- **Baseline**:
- **Target**:
- **Current**:
- **Score**:

## Objective 2: [Your Objective]

...
```

**Used By**: okr-review-agent

---

### `customer-onboarding.md`

**Purpose**: Customer onboarding checklist

**Variables**:
- `{{customer}}` - Customer name
- `{{date}}` - Start date

**Template**:

```markdown
---
type: onboarding
customer: "{{customer}}"
status: in-progress
start_date: {{date}}
owner:
tags:
  - onboarding
  - customer
---
# Customer Onboarding: [[{{customer}}]]

## Overview

| Field | Value |
|-------|-------|
| Customer | [[{{customer}}]] |
| Start Date | {{date}} |
| Owner | |
| Target Completion | |
| Status | In Progress |

---

## Pre-Engagement

- [ ] Contract signed
- [ ] Initial payment received
- [ ] Access credentials shared
- [ ] Kickoff meeting scheduled
- [ ] Internal team briefed

---

## Discovery

- [ ] Requirements gathering complete
- [ ] Stakeholder interviews done
- [ ] Technical assessment complete
- [ ] Success criteria defined
- [ ] Timeline agreed

---

## Setup

- [ ] Development environment configured
- [ ] Access to customer systems
- [ ] Communication channels established
- [ ] Project tracking setup
- [ ] Documentation repository created

---

## Notes



---

## Related

- **Contract**:
- **Project**:
- **Key Contacts**:
```

**Used By**: customer-onboarding-agent

---

## Creating Custom Templates

### Step 1: Create Template File

Location: `templates/my-template.md`

```markdown
---
type: my-type
title: "{{title}}"
date: {{date}}
---
# {{title}}

## Section 1

{{content}}
```

### Step 2: Define Variables

Decide what variables your template needs:

- `{{title}}` - Note title
- `{{date}}` - Creation date
- `{{content}}` - Main content
- `{{author}}` - Author name
- etc.

### Step 3: Use in Agent/Skill

Reference template in agent prompt:

```markdown
## Phase 2: Create Note from Template

1. Read template: `templates/my-template.md`
2. Interpolate variables:
   - title: [extracted from user input]
   - date: [current date]
   - content: [generated content]
3. Write result to appropriate folder
```

---

## Variable Interpolation Rules

### Type Coercion

All variable values are converted to strings:

```python
variables = {
    "count": 42,           # Number
    "active": True,        # Boolean
    "price": 19.99,        # Float
    "name": "Product"      # String
}

# Results:
# {{count}} → "42"
# {{active}} → "True"
# {{price}} → "19.99"
# {{name}} → "Product"
```

### Missing Variables

If a variable is undefined:

```python
template = "Hello {{name}}, your score is {{score}}"
variables = {"name": "Alice"}  # score missing

# Result: "Hello Alice, your score is "
# Missing variables become empty strings
```

### Nested Path Resolution

Access nested values using dot notation:

```python
variables = {
    "user": {
        "profile": {
            "name": "Alice",
            "email": "alice@example.com"
        }
    }
}

# {{user.profile.name}} → "Alice"
# {{user.profile.email}} → "alice@example.com"
```

### Special Characters

Template values can include special characters:

```python
variables = {
    "text": "Hello & goodbye, [[link]] here"
}

# {{text}} → "Hello & goodbye, [[link]] here"
# No escaping needed
```

---

## Template Best Practices

### 1. Use Meaningful Variable Names

**Good**:
```markdown
Date: {{meeting_date}}
Customer: {{customer_name}}
```

**Bad**:
```markdown
Date: {{d}}
Customer: {{c}}
```

### 2. Quote Variables in YAML

Always quote string variables in frontmatter:

**Good**:
```yaml
---
customer: "{{customer}}"
title: "{{title}}"
---
```

**Bad**:
```yaml
---
customer: {{customer}}  # May break YAML parsing
---
```

### 3. Provide Default Structure

Templates should have a complete structure even without variables:

**Good**:
```markdown
## Section 1

{{content}}

## Section 2

(To be filled)
```

**Bad**:
```markdown
{{everything}}
```

### 4. Document Variables

Add a comment block documenting expected variables:

```markdown
<!--
Variables:
- title: Meeting title
- date: YYYY-MM-DD format
- attendees: Comma-separated names
-->

---
type: meeting
date: {{date}}
---
# {{title}}
```

### 5. Use Templates Folder

Keep all templates in `templates/` directory:

```
vault/
  templates/
    daily.md
    weekly.md
    meeting.md
    my-custom-template.md
```

Configure path in `.flywheel.json`:

```json
{
  "paths": {
    "templates": "templates"
  }
}
```

---

## Template Validation

### Validate Before Use

Check template before interpolation:

```python
def validate_template(template: str, required_vars: list) -> bool:
    """Ensure all required variables are in template."""
    for var in required_vars:
        pattern = f"{{{{{var}}}}}"
        if pattern not in template:
            print(f"Missing required variable: {var}")
            return False
    return True

# Example
template = read("templates/meeting.md")
required = ["title", "date"]
if validate_template(template, required):
    result = interpolate_template(template, variables)
```

### Validate After Interpolation

Ensure no variables were missed:

```python
import re

def check_unresolved_variables(text: str) -> list:
    """Find any {{variables}} that weren't replaced."""
    pattern = r'\{\{(\w+(?:\.\w+)*)\}\}'
    return re.findall(pattern, text)

# Example
result = interpolate_template(template, variables)
unresolved = check_unresolved_variables(result)
if unresolved:
    print(f"Warning: Unresolved variables: {unresolved}")
```

---

## Troubleshooting

### Issue: "Template not found"

**Cause**: Template doesn't exist at expected path

**Fix**:

1. Check `.flywheel.json` → `paths.templates`
2. Verify template file exists: `templates/my-template.md`
3. Ensure file name matches exactly (case-sensitive)

### Issue: "Variable not replaced"

**Cause**: Variable name mismatch or syntax error

**Fix**:

1. Check variable name matches exactly: `{{customer}}` not `{{Customer}}`
2. Ensure proper syntax: `{{var}}` not `{var}` or `{{var}}`
3. Verify variable is in variables dict

### Issue: "YAML frontmatter broken"

**Cause**: Unquoted string variable in YAML

**Fix**:

```yaml
# BAD
customer: {{customer}}  # Can break if customer name has special chars

# GOOD
customer: "{{customer}}"  # Always quote
```

### Issue: "Nested variable not working"

**Cause**: Dot notation not supported by interpolation function

**Fix**:

Ensure your interpolation function handles nested paths:

```python
# Should support this:
{{user.profile.name}}

# Not just this:
{{user}}
```

---

## See Also

- [WORKFLOW_CONFIGURATION.md](./WORKFLOW_CONFIGURATION.md) - Configure templates path
- [ROLLUP_WORKFLOW.md](./ROLLUP_WORKFLOW.md) - How rollup uses templates
- [AGENTS_REFERENCE.md](./AGENTS_REFERENCE.md) - Agents that use templates
- [test_template_interpolation.py](../packages/claude-plugin/hooks/tests/test_template_interpolation.py) - Template interpolation tests
