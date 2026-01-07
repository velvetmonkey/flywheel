---
skill: onboard-customer
---

# /onboard-customer - Customer Onboarding Checklist

Generate a customer onboarding checklist from template.

## Usage

```
/onboard-customer "Acme Corp"  # New customer onboarding
```

## What It Does

```
Customer Onboarding
────────────────────────────────────────────────────────────────
Creating onboarding checklist for Acme Corp
────────────────────────────────────────────────────────────────
```

## Where Output Goes

| Action | Target | Notes |
|--------|--------|-------|
| Checklist | New note | Customer folder |
| Tasks | Checklist items | Trackable tasks |

## Example Output

```
Customer Onboarding: Acme Corp
===============================================

Created: customers/Acme Corp/Onboarding.md

ONBOARDING CHECKLIST:

## Week 1: Setup
- [ ] Create customer folder
- [ ] Initial discovery call
- [ ] Document requirements
- [ ] Setup access credentials

## Week 2: Implementation
- [ ] Configure environment
- [ ] Data migration
- [ ] Integration setup
- [ ] Initial training

## Week 3: Go-Live
- [ ] User acceptance testing
- [ ] Go-live support
- [ ] Documentation handoff
- [ ] Success metrics baseline

## Ongoing
- [ ] Weekly check-ins
- [ ] Monthly reviews
- [ ] Quarterly business reviews

CONTACTS:
  Primary: (add contact)
  Technical: (add contact)

===============================================
```
