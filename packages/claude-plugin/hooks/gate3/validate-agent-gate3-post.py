#!/usr/bin/env python3
"""
Gate 3 Post-Edit Validator - Warns if Edit broke Gate 3 compliance.
Runs AFTER Edit operations on agent files.

This is a PROJECT-LEVEL hook that warns (but doesn't block) when an edit
may have broken Gate 3 compliance in an agent file.

Exit codes:
- 0: Always (warning only, never blocks)
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
        "Sequential execution": any(x in content.lower() for x in
            ["sequential", "wait for completion", "before calling next"]),
        "Error handling": "error" in content.lower(),
        "Verification output": ("✓" in content and "✗" in content) or
            ("completed" in content.lower() and "failed" in content.lower()),
    }

    for req, passed in checks.items():
        if not passed:
            missing.append(req)

    return missing


def main():
    try:
        hook_input = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    if hook_input.get('tool_name') != 'Edit':
        sys.exit(0)

    file_path = hook_input.get('tool_input', {}).get('file_path', '')
    if not is_agent_file(file_path):
        sys.exit(0)

    try:
        content = Path(file_path).read_text(encoding='utf-8')
    except (FileNotFoundError, PermissionError):
        sys.exit(0)

    if not is_multi_step_agent(content):
        sys.exit(0)

    missing = validate_gate3(content)
    if missing:
        print(f"\n⚠️  GATE 3 WARNING: Agent may be non-compliant after edit")
        print("-" * 60)
        print(f"File: {Path(file_path).name}")
        print("Missing requirements:")
        for m in missing:
            print(f"  ✗ {m}")
        print("-" * 60)
        print("Multi-step agents MUST include Gate 3 sections.")
        print("See: packages/claude-plugin/skills/_patterns/SIX_GATES.md\n")

    sys.exit(0)


if __name__ == '__main__':
    main()
