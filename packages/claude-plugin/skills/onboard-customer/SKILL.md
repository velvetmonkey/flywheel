---
name: onboard-customer
description: Create customer onboarding checklist from template with customer details
auto_trigger: true
trigger_keywords:
  - "onboard customer"
  - "onboard new customer"
  - "create customer onboarding"
  - "customer onboarding checklist"
  - "new customer setup"
  - "new client setup"
  - "client onboarding checklist"
  - "start customer onboarding"
allowed-tools: Task, Read, Write, mcp__flywheel__get_note_metadata, mcp__flywheel__search_notes, mcp__flywheel__get_folder_structure
---

# Onboard Customer

Create a new customer onboarding checklist from template, with customer details pre-filled.

## Trigger Detection

Activate when user:
- Has a new customer to onboard
- Needs to create an onboarding checklist
- Wants to start customer setup process

## Examples

- "Onboard Acme Corp"
- "New customer: TechStart Inc"
- "Create onboarding checklist for Big Enterprise"
- "Start onboarding for [[New Client]]"

## Process

1. **Parse Customer Name**
   - Extract customer name from request
   - If unclear, ask for confirmation

2. **Delegate to Agent**
   ```
   Task(
       subagent_type="customer-onboarding-agent",
       description="Onboard customer",
       prompt="Create onboarding checklist for [Customer Name]"
   )
   ```

3. **Confirm Creation**
   - Show created note path
   - Link to related resources

4. **Verify Creation** (Gate 6)
   - If agent reports success: Re-read the onboarding note to verify it was created
   - If blocked or failed: Inform user "Onboarding creation failed - please create manually"
   - If succeeded: Only report success if verification confirms note exists
   - If not found: Alert user that note may not have been created correctly

## Customization

The onboarding template can be customized:
- Edit `templates/customer-onboarding.md` for your workflow
- Add/remove checklist phases
- Include company-specific steps

## Six Gates Compliance

| Gate | Status | Notes |
|------|--------|-------|
| 1. Read Before Write | Via Agent | Agent reads template first |
| 2. File Exists Check | Via Agent | Agent checks template exists |
| 3. Chain Validation | ✓ | Sequential: delegate → verify |
| 4. Mutation Confirm | Via Agent | User confirms before creation |
| 5. MCP Health | Via Agent | Agent validates MCP connection |
| 6. Post Validation | ✓ | Re-read note to verify creation succeeded (step 4) |
