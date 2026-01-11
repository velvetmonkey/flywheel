# Gate 3 Enforcement Hooks

These hooks enforce Gate 3 (Agent Chain Validation) when developing Flywheel agents.

## Setup

Copy or merge into your `.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "python packages/claude-plugin/hooks/gate3/validate-agent-gate3.py",
            "timeout": 5000
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit",
        "hooks": [
          {
            "type": "command",
            "command": "python packages/claude-plugin/hooks/gate3/validate-agent-gate3-post.py"
          }
        ]
      }
    ]
  }
}
```

## What They Do

- **validate-agent-gate3.py** (PreToolUse): BLOCKS writing new agent files that don't have Gate 3 compliance sections
- **validate-agent-gate3-post.py** (PostToolUse): WARNS after editing agent files if Gate 3 sections are removed

## Gate 3 Requirements

Multi-step agents (those containing `Task()` calls) must have:

1. `## Critical Rules` section
2. Sequential execution documentation
3. Error handling strategy
4. Verification output (✓/✗ symbols)

See `packages/claude-plugin/skills/_patterns/SIX_GATES.md` for full specification.
