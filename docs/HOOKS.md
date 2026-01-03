# Hook System Guide

Hooks are Python scripts that run automatically in response to Claude Code events, providing automation, validation, and quality assurance.

---

## Overview

**What are hooks?**

Hooks execute at specific lifecycle points:
- **SessionStart**: When Claude Code session begins
- **PreToolUse**: Before a tool executes (Read, Edit, Write, etc.)
- **PostToolUse**: After a tool executes

**Why hooks?**

- **Automation**: Auto-apply wikilinks, rebuild caches, validate syntax
- **Safety**: Enforce Six Gates (Read before Write, file exists, etc.)
- **Intelligence**: Detect achievements, suggest links, check health

---

## Built-in Hooks

Flywheel includes 8 hooks:

| Hook | Trigger | Purpose | Gate |
|------|---------|---------|------|
| `session-gate.py` | SessionStart | Verify MCP connection, PROJECT_PATH | Gate 5 |
| `session-start.py` | SessionStart | Validate daily note, rebuild wikilink cache, show briefing | - |
| `pre-mutation-gate.py` | PreToolUse (Edit/Write) | Enforce Gates 1, 2, 4 (Read before Write, file exists, confirmation) | Gates 1, 2, 4 |
| `read-cache.py` | PostToolUse (Read) | Track files read (for Gate 1 cache) | Gate 1 |
| `verify-mutation.py` | PostToolUse (Edit/Write) | Validate YAML frontmatter and wikilinks | Gate 6 |
| `syntax-validate.py` | PostToolUse (Edit/Write) | Warn about syntax issues (angle brackets, wrapped wikilinks) | - |
| `wikilink-suggest.py` | PostToolUse (Edit/Write) | Auto-apply `[[brackets]]` to recognized entities | - |
| `achievement-detect.py` | PostToolUse (Edit/Write) | Detect accomplishments, update Achievements.md | - |

---

## Hook Lifecycle

```
┌────────────────────────────────┐
│  SessionStart Event            │
│  ↓                              │
│  session-gate.py (Gate 5)      │
│  ↓                              │
│  session-start.py              │
└────────────────────────────────┘

┌────────────────────────────────┐
│  PreToolUse Event (Edit)       │
│  ↓                              │
│  pre-mutation-gate.py          │
│  ├─ Gate 1: Read before Write? │
│  ├─ Gate 2: File exists?       │
│  └─ Gate 4: Confirmation?      │
│  ↓                              │
│  [Allow/Deny/Ask decision]     │
└────────────────────────────────┘

┌────────────────────────────────┐
│  PostToolUse Event (Read)      │
│  ↓                              │
│  read-cache.py                 │
│  ↓                              │
│  [Cache file as "read"]        │
└────────────────────────────────┘

┌────────────────────────────────┐
│  PostToolUse Event (Edit)      │
│  ↓                              │
│  verify-mutation.py (Gate 6)   │
│  ↓                              │
│  syntax-validate.py            │
│  ↓                              │
│  wikilink-suggest.py           │
│  ↓                              │
│  achievement-detect.py         │
└────────────────────────────────┘
```

---

## Hook Details

### `session-gate.py` (Gate 5)

**Trigger**: SessionStart

**Purpose**: Verify MCP server health and PROJECT_PATH configuration

**Output**:

```
MCP Gate Check: ✓ PASS
  PROJECT_PATH: C:/Users/benca/obsidian/Ben
  Flywheel MCP: Connected

Action: Session ready
```

**or**

```
MCP Gate Check: WARNING
  PROJECT_PATH: (not set)

Issues detected:
  - PROJECT_PATH not set - MCP vault tools may not work

Action: Run mcp__flywheel__health_check to verify MCP is working.
```

**When it blocks**: Never blocks, only warns

---

### `session-start.py`

**Trigger**: SessionStart

**Purpose**:
1. Validate today's daily note exists
2. Rebuild wikilink entity cache
3. Show vault status briefing

**Output**:

```
Flywheel - Session started: 2026-01-03

Daily note: 2026-01-03.md exists
  Habits: 0/3 completed
  Food entries: 1
  Log entries: 82

Wikilink cache: 1183 entities
  Cache age: 0 hours (fresh)
```

**Side Effects**:
- Creates `.claude/wikilink-entities.json`
- Scans vault for all note titles and aliases
- Tracks daily note status

---

### `pre-mutation-gate.py` (Gates 1, 2, 4)

**Trigger**: PreToolUse (Edit, Write)

**Purpose**: Enforce safety gates before file mutations

**Gate 1: Read Before Write**

```
Decision: DENY
Reason: Must Read "example.md" before editing.

Files can only be edited after they've been read in this session.
Please use Read("example.md") first.
```

**Gate 2: File Exists**

```
Decision: DENY
Reason: File does not exist: "missing.md"

Cannot edit non-existent file. Use Write to create it.
```

**Gate 4: Mutation Confirmation**

```
Decision: ASK
Reason: Confirm bulk edit to 5 files?

Files to modify:
  - daily-notes/2026-01-01.md
  - daily-notes/2026-01-02.md
  - daily-notes/2026-01-03.md
  - daily-notes/2026-01-04.md
  - daily-notes/2026-01-05.md

Proceed? (yes/no)
```

**When it blocks**:
- Edit without prior Read (Gate 1)
- Edit non-existent file (Gate 2)
- Bulk mutations >5 files (Gate 4 - asks for confirmation)

---

### `read-cache.py` (Gate 1 Support)

**Trigger**: PostToolUse (Read)

**Purpose**: Track which files have been read this session

**Output**: (Silent - no visible output)

**Side Effects**:
- Appends file path to `.claude/read-cache/{session_id}.json`
- Used by `pre-mutation-gate.py` to validate Gate 1

**Cache Format**:

```json
{
  "session_id": "abc123",
  "files_read": [
    "daily-notes/2026-01-03.md",
    "projects/flywheel.md",
    "templates/meeting.md"
  ],
  "last_updated": "2026-01-03T19:10:00Z"
}
```

**Cache Lifespan**: Entire session (survives context summarization)

---

### `verify-mutation.py` (Gate 6)

**Trigger**: PostToolUse (Edit, Write)

**Purpose**: Validate YAML frontmatter and wikilink syntax after mutations

**Checks**:
1. YAML frontmatter is valid (can be parsed)
2. No corrupted wikilinks
3. No syntax errors

**Output** (if issues found):

```
⚠️ Gate 6 Warning: Potential syntax issues in "example.md"

Issues:
  - Invalid YAML frontmatter (line 3)
  - Unclosed wikilink: [[Example
  - Duplicate wikilink: [[Same]] [[Same]]

Please review and fix.
```

**When it blocks**: Never blocks, only warns

---

### `syntax-validate.py`

**Trigger**: PostToolUse (Edit, Write)

**Purpose**: Warn about common Obsidian syntax mistakes

**Checks**:

1. **Angle brackets in content** - Break wikilinks
   ```
   ⚠️ Angle brackets detected (line 15)

   Content: "Function signature: <T, U>"
   Issue: Angle brackets can break wikilink parsing

   Suggestion: Use code blocks or escape: \<T, U\>
   ```

2. **Wrapped wikilinks** - Break hyperlinks
   ```
   ⚠️ Wrapped wikilink detected (line 22)

   Content: "**[[Important Note]]**"
   Issue: Markdown formatting inside wikilinks breaks Obsidian links

   Suggestion: Move formatting outside: [[Important Note]] (bold)
   ```

3. **Wikilinks in YAML frontmatter** - Corrupt metadata
   ```
   ⚠️ Wikilink in frontmatter detected (line 4)

   Content: "related: [[Other Note]]"
   Issue: Wikilinks in YAML frontmatter corrupt metadata

   Suggestion: Use plain text: related: "Other Note"
   ```

**When it blocks**: Never blocks, only warns

---

### `wikilink-suggest.py`

**Trigger**: PostToolUse (Edit, Write)

**Purpose**: Auto-apply `[[brackets]]` to text matching known entities

**How it works**:

1. Reads `.claude/wikilink-entities.json` (entity cache)
2. Scans file content for matches
3. Wraps matches with `[[brackets]]`

**Example**:

**Before**:
```
Met with John Smith to discuss Flywheel roadmap.
```

**After** (if "John Smith" and "Flywheel" are note titles):
```
Met with [[John Smith]] to discuss [[Flywheel]] roadmap.
```

**Protected Zones** (never wikilinked):
- YAML frontmatter
- Code blocks (``` and \`)
- Existing wikilinks
- Markdown links
- URLs
- Hashtags
- HTML tags
- Obsidian comments (%% ... %%)
- Math expressions ($ ... $)

**Output**:

```
✓ Applied 3 wikilinks to "example.md"
  - John Smith (line 5)
  - Flywheel (line 5)
  - Claude Code (line 12)
```

---

### `achievement-detect.py`

**Trigger**: PostToolUse (Edit, Write)

**Purpose**: Detect significant accomplishments and update Achievements.md

**Detection Patterns**:

1. **Action verbs**: completed, delivered, shipped, launched, deployed, finished
2. **Impact markers**: successfully, critical, major, significant
3. **Graph signals**: New hub notes, orphan reduction, broken link repairs

**Example**:

**Daily Log Entry**:
```
## Log

- 10:00 Completed authentication refactor
- 14:00 Successfully deployed v2.1.0 to production
- 16:00 Fixed critical bug in payment flow
```

**Achievement Detected**:
```
✓ Achievement detected in "daily-notes/2026-01-03.md"
  - Completed authentication refactor
  - Successfully deployed v2.1.0 to production
  - Fixed critical bug in payment flow

Updated: personal/goals/Achievements.md
```

**Achievements.md Format**:

```markdown
# Achievements

## 2026

- **2026-01-03**: Completed authentication refactor
- **2026-01-03**: Successfully deployed v2.1.0 to production
- **2026-01-03**: Fixed critical bug in payment flow
```

---

## Hook Configuration

### Location

Hooks are defined in `hooks/hooks.json`:

```json
{
  "hooks": [
    {
      "name": "session-gate",
      "type": "command",
      "trigger": "SessionStart",
      "command": "python \"${CLAUDE_PLUGIN_ROOT}/hooks/session-gate.py\""
    },
    {
      "name": "pre-mutation-gate",
      "type": "command",
      "trigger": "PreToolUse",
      "command": "python \"${CLAUDE_PLUGIN_ROOT}/hooks/pre-mutation-gate.py\"",
      "toolPattern": "Edit|Write"
    }
  ]
}
```

### Environment Variables

Available in hook execution:

| Variable | Description | Example |
|----------|-------------|---------|
| `CLAUDE_PLUGIN_ROOT` | Path to plugin directory | `/home/user/.claude/plugins/marketplaces/flywheel` |
| `CLAUDE_LOCAL_STATE_DIR` | Claude state directory | `/home/user/.claude` |
| `PROJECT_PATH` | Vault path (from MCP config) | `/home/user/obsidian/vault` |

---

## Writing Custom Hooks

### Step 1: Create Hook Script

Location: `hooks/my-hook.py`

```python
#!/usr/bin/env python3
"""
My Custom Hook

Description: What this hook does
Trigger: When it runs
"""

import json
import sys

def main():
    # Read hook input from stdin
    hook_input = json.loads(sys.stdin.read())

    # Extract relevant data
    tool_name = hook_input.get("tool_name")
    tool_input = hook_input.get("tool_input", {})
    file_path = tool_input.get("file_path")

    # Your hook logic here
    if tool_name == "Edit":
        # Do something before Edit
        pass

    # Return decision (for PreToolUse hooks)
    decision = {
        "hookSpecificOutput": {
            "permissionDecision": "allow"  # or "deny" or "ask"
        }
    }

    print(json.dumps(decision))

if __name__ == "__main__":
    main()
```

### Step 2: Register Hook

Add to `hooks/hooks.json`:

```json
{
  "name": "my-hook",
  "type": "command",
  "trigger": "PreToolUse",
  "command": "python \"${CLAUDE_PLUGIN_ROOT}/hooks/my-hook.py\"",
  "toolPattern": "Edit|Write"
}
```

### Step 3: Test Hook

```bash
cd hooks
pytest tests/test_my_hook.py
```

---

## Hook Input Format

### SessionStart Hook

```json
{
  "trigger": "SessionStart",
  "session_id": "abc123",
  "timestamp": "2026-01-03T19:10:00Z"
}
```

### PreToolUse Hook

```json
{
  "trigger": "PreToolUse",
  "tool_name": "Edit",
  "tool_input": {
    "file_path": "daily-notes/2026-01-03.md",
    "old_string": "hello",
    "new_string": "world"
  },
  "session_id": "abc123",
  "transcript_path": "/home/user/.claude/transcripts/abc123.jsonl"
}
```

### PostToolUse Hook

```json
{
  "trigger": "PostToolUse",
  "tool_name": "Read",
  "tool_input": {
    "file_path": "daily-notes/2026-01-03.md"
  },
  "tool_output": {
    "content": "# 2026-01-03\n\n## Log\n- Task completed"
  },
  "session_id": "abc123"
}
```

---

## Hook Output Format

### Permission Decision (PreToolUse)

**Allow**:
```json
{
  "hookSpecificOutput": {
    "permissionDecision": "allow"
  }
}
```

**Deny**:
```json
{
  "hookSpecificOutput": {
    "permissionDecision": "deny",
    "permissionDecisionReason": "Must Read file before editing."
  }
}
```

**Ask**:
```json
{
  "hookSpecificOutput": {
    "permissionDecision": "ask",
    "permissionDecisionReason": "Confirm bulk edit to 5 files?",
    "confirmationPrompt": "Proceed? (yes/no)"
  }
}
```

### Informational Output (PostToolUse)

```json
{
  "hookSpecificOutput": {
    "message": "✓ Applied 3 wikilinks",
    "details": ["John Smith", "Flywheel", "Claude Code"]
  }
}
```

---

## Debugging Hooks

### Check Debug Logs

**WSL**:
```bash
cat ~/.claude/debug/(session-id).txt | grep -A 5 "hook"
```

**Windows**:
```powershell
Get-Content $env:USERPROFILE\.claude\debug\(session-id).txt | Select-String "hook" -Context 5
```

### Key Log Patterns

**Hook loaded**:
```
Registered 8 hooks from 1 plugins
  - session-gate (SessionStart)
  - pre-mutation-gate (PreToolUse: Edit|Write)
  ...
```

**Hook executed**:
```
[Hook] pre-mutation-gate triggered for Edit
[Hook] Decision: allow
```

**Hook failed**:
```
[Hook] pre-mutation-gate failed: Python not found
[Hook] Stderr: /usr/bin/python3: No such file or directory
```

### Test Hook Manually

```bash
cd hooks

# Create test input
echo '{"tool_name": "Edit", "tool_input": {"file_path": "test.md"}}' | \
  python pre-mutation-gate.py
```

---

## Troubleshooting

### Issue: "Hook not firing"

**Cause**: Hook not registered or trigger mismatch

**Fix**:

1. Check `hooks/hooks.json` - is hook listed?
2. Verify trigger matches: `SessionStart`, `PreToolUse`, `PostToolUse`
3. Check toolPattern (if PreToolUse): `Edit|Write|Read`
4. Restart Claude Code session

### Issue: "Python not found"

**Cause**: Python not in PATH or wrong command

**Fix**:

WSL:
```bash
sudo apt install python-is-python3
```

Windows: Ensure Python installed and in PATH

### Issue: "Hook blocks all edits"

**Cause**: pre-mutation-gate.py denying operations

**Fix**:

1. Check if files were Read first (Gate 1)
2. Verify files exist (Gate 2)
3. Check debug logs for denial reason

### Issue: "Wikilinks not auto-applying"

**Cause**: Entity cache stale or missing

**Fix**:

```bash
# Rebuild cache manually
/rebuild-cache

# Or restart session (cache rebuilds on SessionStart)
```

---

## See Also

- [SIX_GATES.md](./SIX_GATES.md) - Six Gates framework that hooks enforce
- [WORKFLOW_CONFIGURATION.md](./WORKFLOW_CONFIGURATION.md) - Configure protected folders
- [test_gate*.py](../packages/claude-plugin/hooks/tests/) - Hook test suite
