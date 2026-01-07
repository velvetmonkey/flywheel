# Building Custom Skills

Skills are markdown files that teach Claude how to execute workflows. No code required—just describe what should happen.

This guide walks through building a complete skill from scratch.

---

## What Is a Skill?

A skill is a single `SKILL.md` file containing:
1. **Frontmatter** - metadata, triggers, permissions
2. **Process** - step-by-step workflow
3. **Six Gates compliance** - safety checklist

When a user says something matching your skill's triggers, Claude follows your process.

---

## Skill Anatomy

```
packages/claude-plugin/skills/
├── your-skill-name/
│   └── SKILL.md          ← The skill definition
```

### SKILL.md Structure

```markdown
---
name: your-skill-name
description: One-line description shown to users
auto_trigger: true
trigger_keywords:
  - "first trigger phrase"
  - "second trigger phrase"
allowed-tools: Read, Edit, mcp__flywheel__search_notes
---

# Skill Title

Brief explanation of what this skill does.

## When to Use

Describe scenarios where this skill is helpful.

## Process

1. **First step**
   - Details about what to do
   - Sub-steps if needed

2. **Second step**
   - More details

3. **Verification**
   - How to confirm success

## Six Gates Compliance

| Gate | Implementation |
|------|----------------|
| 1. Read Before Write | [How this skill reads before writing] |
| 2. File Exists | [How this skill validates targets] |
| 3. Chain Validation | [N/A for single-step, or validation approach] |
| 4. Mutation Confirmation | [How user confirms changes] |
| 5. Health Check | [MCP connection verified] |
| 6. Post Validation | [How writes are verified] |
```

---

## Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Skill identifier (lowercase, hyphens) |
| `description` | Yes | One-line description |
| `auto_trigger` | No | `true` to match on keywords |
| `trigger_keywords` | No | Phrases that invoke the skill |
| `allowed-tools` | Yes | Tools this skill can use |

### allowed-tools Options

**Built-in tools:**
- `Read` - Read files
- `Edit` - Modify files
- `Write` - Create files
- `Task` - Spawn agents
- `Bash` - Shell commands

**MCP tools** (prefixed `mcp__flywheel__`):
- `mcp__flywheel__search_notes`
- `mcp__flywheel__get_backlinks`
- `mcp__flywheel__get_frontmatter_schema`
- See [MCP Reference](./MCP_REFERENCE.md) for full list

---

## Tutorial: Build a "Weekly Digest" Skill

Let's build a skill that creates a weekly digest from recent activity.

### Step 1: Create the Directory

```
packages/claude-plugin/skills/weekly-digest/
└── SKILL.md
```

### Step 2: Define Frontmatter

```yaml
---
name: weekly-digest
description: Generate a digest of vault activity from the past week
auto_trigger: true
trigger_keywords:
  - "weekly digest"
  - "what happened this week"
  - "week summary"
allowed-tools: Read, Write, mcp__flywheel__get_recent_notes, mcp__flywheel__get_activity_summary
---
```

**Key decisions:**
- `auto_trigger: true` - activates on matching phrases
- Four allowed tools: Read (for reading notes), Write (for creating digest), plus two MCP query tools

### Step 3: Write the Process

```markdown
# Weekly Digest

Generate a summary of vault activity from the past 7 days.

## When to Use

- End of week review
- Catching up after time away
- Preparing weekly status updates

## Process

1. **Query recent activity**
   - Use `get_activity_summary` for the past 7 days
   - Use `get_recent_notes` to list modified notes
   - Capture: note count, new notes, modified notes

2. **Categorize by folder**
   - Group notes by their parent folder
   - Identify most active areas

3. **Read key notes** (optional)
   - If fewer than 5 notes changed, read them
   - If many notes, read only titles/frontmatter

4. **Generate digest**
   - Summary paragraph
   - Activity by area
   - Key changes list
   - Suggestions for follow-up

5. **Present to user**
   - Display the digest in response
   - Optionally offer to save to a file

## Output Format

```markdown
## Weekly Digest: [Date Range]

### Summary
[1-2 sentence overview]

### Activity by Area
- **projects/**: 5 notes modified
- **meetings/**: 3 new notes
- **daily-notes/**: 7 entries

### Key Changes
- [[Project Alpha]] - status changed to "review"
- [[Q1 Planning]] - new note created
- [[Client Meeting]] - action items added

### Suggested Follow-ups
- Review stale notes in projects/
- Process action items from meetings
```

## Six Gates Compliance

| Gate | Implementation |
|------|----------------|
| 1. Read Before Write | Queries index and optionally reads notes before generating |
| 2. File Exists | N/A - creates new file or displays only |
| 3. Chain Validation | Single-step workflow |
| 4. Mutation Confirmation | Digest shown before any file write |
| 5. Health Check | MCP tools verify vault access |
| 6. Post Validation | If saved, re-read file to confirm |
```

### Step 4: Full SKILL.md

```markdown
---
name: weekly-digest
description: Generate a digest of vault activity from the past week
auto_trigger: true
trigger_keywords:
  - "weekly digest"
  - "what happened this week"
  - "week summary"
  - "weekly summary"
allowed-tools: Read, Write, mcp__flywheel__get_recent_notes, mcp__flywheel__get_activity_summary
---

# Weekly Digest

Generate a summary of vault activity from the past 7 days.

## When to Use

- End of week review
- Catching up after time away
- Preparing weekly status updates

## Process

1. **Query recent activity**
   - Use `get_activity_summary` for the past 7 days
   - Use `get_recent_notes` to list modified notes
   - Note: These are READ-ONLY queries, no file access needed

2. **Categorize by folder**
   - Group returned notes by parent folder
   - Count new vs modified

3. **Identify highlights**
   - Notes with most backlinks (high importance)
   - Notes with frontmatter changes (status updates)
   - New notes (fresh content)

4. **Generate digest**
   - Create markdown summary
   - Include activity breakdown
   - List key changes
   - Suggest follow-up actions

5. **Present options**
   - Display digest to user
   - Offer: "Save to weekly-notes/?"
   - If user confirms, write to file

## Output Format

```
## Weekly Digest: Jan 1-7, 2026

### Summary
Active week with 23 notes touched across 4 areas.

### Activity
| Folder | New | Modified |
|--------|-----|----------|
| projects/ | 2 | 8 |
| meetings/ | 3 | 1 |
| daily-notes/ | 7 | 0 |
| clients/ | 0 | 2 |

### Highlights
- [[Project Alpha]] moved to review
- New meeting notes from client calls
- 3 tasks completed in daily notes

### Follow-up
- 2 stale notes in projects/ need review
- Action items pending from [[Client Meeting]]
```

## Six Gates Compliance

| Gate | Implementation |
|------|----------------|
| 1. Read Before Write | Queries return metadata only; reads notes only if needed for detail |
| 2. File Exists | Creating new file; checks weekly-notes/ folder exists |
| 3. Chain Validation | Single workflow, no agent delegation |
| 4. Mutation Confirmation | Shows digest and asks before saving |
| 5. Health Check | MCP queries verify vault access on first call |
| 6. Post Validation | If saved, re-reads file to confirm content |
```

---

## Three Skill Types

### 1. Read-Only Skills

Query and display information. No file modifications.

```yaml
allowed-tools: mcp__flywheel__search_notes, mcp__flywheel__get_backlinks
```

**Six Gates:** Gates 1, 2, 4, 6 are N/A (no mutations).

### 2. Mutation Skills

Modify files in the vault.

```yaml
allowed-tools: Read, Edit, mcp__flywheel__search_notes
```

**Six Gates:** All six gates must be addressed.

### 3. Delegation Skills

Spawn agents for complex workflows.

```yaml
allowed-tools: Task
```

**Six Gates:** Gate 3 (Chain Validation) is critical.

---

## Six Gates Deep Dive

Every skill must address all six gates. Here's what each means:

### Gate 1: Read Before Write

**Rule:** Never modify a file without reading it first.

```markdown
## Process
1. **Read target file**
   - Use Read tool to get current content
   - Understand existing structure

2. **Plan modification**
   - Based on current content, determine changes

3. **Execute modification**
   - Use Edit tool with specific old_string/new_string
```

**Compliance statement:**
> Gate 1: Reads [target file] before any modification to understand current state.

### Gate 2: File Exists

**Rule:** Validate that target files exist before operating.

```markdown
## Process
1. **Verify target exists**
   - Check if file path is valid
   - If missing: warn user or create with confirmation
```

**Compliance statement:**
> Gate 2: Validates target file exists; if missing, asks user before creating.

### Gate 3: Chain Validation

**Rule:** For multi-step workflows, verify each step before proceeding.

```markdown
## Process
1. **Step one**
   - Execute action
   - **Verify:** Check result before continuing

2. **Step two** (only if step one succeeded)
   - Execute next action
```

**Compliance statement:**
> Gate 3: Each step verifies success before proceeding to next step.

For single-step skills:
> Gate 3: N/A - single operation, no chain.

### Gate 4: Mutation Confirmation

**Rule:** Show changes to user before writing.

```markdown
## Process
1. **Prepare changes**
   - Generate new content

2. **Show preview**
   - Display what will be written
   - Ask: "Apply these changes?"

3. **Execute on confirmation**
   - Only proceed if user confirms
```

**Compliance statement:**
> Gate 4: Displays preview of changes and waits for user confirmation.

### Gate 5: Health Check

**Rule:** Verify MCP connection and vault access.

```markdown
## Process
1. **Verify vault access**
   - First MCP call confirms connection
   - If fails, inform user
```

**Compliance statement:**
> Gate 5: Initial MCP query verifies vault is accessible.

### Gate 6: Post-Execution Validation

**Rule:** After writing, verify the change was applied.

```markdown
## Process
1. **Write changes**
   - Use Edit or Write tool

2. **Verify write**
   - Re-read the file
   - Confirm changes are present
   - Report success or failure
```

**Compliance statement:**
> Gate 6: Re-reads file after write to confirm changes were applied.

---

## Validation

Before committing, validate your skill:

```bash
npm run validate:skills
```

This checks:
- Frontmatter format
- Required sections present
- Six Gates compliance table
- Valid tool names

---

## Best Practices

### Trigger Keywords
- Use natural phrases users would say
- Include variations ("weekly digest", "week summary", "this week's activity")
- Avoid overlapping with existing skills

### Process Steps
- Number each step
- Include verification after mutations
- Keep steps atomic and clear

### Tools
- Request minimum permissions needed
- Prefer MCP queries over file reads
- Use Read/Edit over Write when modifying existing files

### Six Gates
- Every gate needs an entry, even if "N/A"
- Be specific about implementation
- Include which step implements each gate

---

## Examples to Study

| Skill | Type | Key Pattern |
|-------|------|-------------|
| `add-log` | Mutation | Simple file append |
| `vault-health` | Read-only | Query + analysis |
| `extract-actions` | Delegation | Spawns agent |
| `normalize-note` | Mutation | Complex multi-step |
| `weekly-review` | Delegation | Agent workflow |

Browse existing skills in `packages/claude-plugin/skills/` for patterns.

---

## Checklist

Before submitting a new skill:

- [ ] Created `packages/claude-plugin/skills/skill-name/SKILL.md`
- [ ] Frontmatter includes: name, description, allowed-tools
- [ ] Trigger keywords defined (if auto_trigger)
- [ ] Process section with numbered steps
- [ ] Six Gates compliance table completed
- [ ] Ran `npm run validate:skills`
- [ ] Tested by invoking `/skill-name` or trigger phrase
