#!/usr/bin/env python3
"""
Gate 3 Agent Validator Hook - Enforces Gate 3 when writing agent files.
Runs BEFORE Write operations on packages/claude-plugin/agents/**/*.md

BLOCKS the write if multi-step agent is missing Gate 3 requirements.

This is a PROJECT-LEVEL hook (in .claude/hooks/) that only applies to
the Flywheel development repo, not to vaults that install the plugin.

Exit codes:
- 0: Always (decision communicated via JSON output)
"""

import json
import sys
import re
from pathlib import Path

# Configure UTF-8 output for Windows console
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass


def is_agent_file(file_path: str) -> bool:
    """Check if this is an agent file (not a template)."""
    return ('agents/' in file_path and
            file_path.endswith('.md') and
            '_templates/' not in file_path)


def is_multi_step_agent(content: str) -> bool:
    """Check if agent calls Task() - making it multi-step."""
    return bool(re.search(r'Task\s*\(', content))


def validate_gate3(content: str) -> list:
    """Validate Gate 3 requirements. Returns list of missing requirements."""
    missing = []

    checks = {
        "## Critical Rules section": "## Critical Rules" in content,
        "Sequential execution (wait for completion)": any(x in content.lower() for x in
            ["sequential", "wait for completion", "before calling next", "before proceeding"]),
        "Error handling strategy": "error" in content.lower() and
            any(x in content.lower() for x in ["handling", "continue", "fail"]),
        "Verification output (✓/✗ or completed/failed)":
            ("✓" in content and "✗" in content) or
            ("completed" in content.lower() and "failed" in content.lower()),
    }

    for requirement, passed in checks.items():
        if not passed:
            missing.append(requirement)

    return missing


def main():
    try:
        hook_input = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    tool_name = hook_input.get('tool_name', '')
    if tool_name != 'Write':
        sys.exit(0)  # Only validate Write (new files)

    file_path = hook_input.get('tool_input', {}).get('file_path', '')
    if not is_agent_file(file_path):
        sys.exit(0)

    content = hook_input.get('tool_input', {}).get('content', '')
    if not content:
        sys.exit(0)

    # Only enforce Gate 3 for multi-step agents
    if not is_multi_step_agent(content):
        sys.exit(0)

    # Validate Gate 3 requirements
    missing = validate_gate3(content)

    if missing:
        missing_list = '\n'.join(f'  ✗ {m}' for m in missing)
        output = {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": f"""GATE 3 BLOCKED: Multi-step agent missing requirements:

{missing_list}

Multi-step agents (containing Task() calls) MUST include:
1. "## Critical Rules" section with sequential execution
2. Error handling strategy (continue on failure, report all)
3. Verification output showing ✓/✗ for each step

See: packages/claude-plugin/skills/_patterns/SIX_GATES.md"""
            }
        }
        print(json.dumps(output))
        sys.exit(0)

    # All checks passed
    sys.exit(0)


if __name__ == '__main__':
    main()
