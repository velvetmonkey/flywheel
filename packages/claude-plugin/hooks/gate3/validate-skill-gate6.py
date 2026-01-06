#!/usr/bin/env python3
"""
Gate 6 Skill Validator Hook - Enforces Gate 6 when writing skill files.
Runs BEFORE Write operations on packages/claude-plugin/skills/**/SKILL.md

BLOCKS the write if a mutation skill is missing verification requirements.

This is a PROJECT-LEVEL hook (in .claude/hooks/) that only applies to
the Flywheel development repo, not to vaults that install the plugin.

Exit codes:
- 0: Always (decision communicated via JSON output)
"""

import json
import sys
from pathlib import Path

# Configure UTF-8 output for Windows console
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass


def is_skill_file(file_path: str) -> bool:
    """Check if this is a SKILL.md file (not a pattern/template)."""
    return ('skills/' in file_path and
            file_path.endswith('SKILL.md') and
            '_patterns/' not in file_path and
            '_templates/' not in file_path)


def uses_mutation_tools(content: str) -> bool:
    """Check if skill uses Edit or Write tools."""
    # Check allowed-tools frontmatter and process steps
    return ('Edit' in content or 'Write' in content)


def validate_skill_gate6(content: str) -> list:
    """Validate Gate 6 requirements. Returns list of missing requirements."""
    missing = []

    # Skills that use Edit/Write MUST have verification
    if not uses_mutation_tools(content):
        return []  # No verification needed for read-only skills

    content_lower = content.lower()

    checks = {
        "Verify step after Edit/Write": any(x in content_lower for x in
            ["verify", "re-read", "confirm written", "check result", "verification"]),
        "Error handling for blocked/failed Edit": any(x in content_lower for x in
            ["if failed", "if blocked", "edit fails", "write fails",
             "blocked or failed", "failed or blocked"]),
        "Success/failure output distinction": any(x in content_lower for x in
            ["if found", "if not found", "if succeeded", "if failed",
             "only if step", "only if verification"]),
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
    if tool_name not in ('Write', 'Edit'):
        sys.exit(0)  # Only validate Write/Edit

    file_path = hook_input.get('tool_input', {}).get('file_path', '')
    if not is_skill_file(file_path):
        sys.exit(0)

    content = hook_input.get('tool_input', {}).get('content', '')

    # For Edit operations, we may not have full content - allow through
    if tool_name == 'Edit' and not content:
        sys.exit(0)

    if not content:
        sys.exit(0)

    # Validate Gate 6 requirements
    missing = validate_skill_gate6(content)

    if missing:
        missing_list = '\n'.join(f'  ✗ {m}' for m in missing)
        output = {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": f"""GATE 6 BLOCKED: Skill with Edit/Write missing verification:

{missing_list}

Skills that call Edit or Write MUST include:
1. A verification step that re-reads the file
2. Error handling if Edit/Write is blocked or fails
3. Distinct output for success vs failure (only confirm if verified)

See: packages/claude-plugin/skills/_patterns/SIX_GATES.md"""
            }
        }
        print(json.dumps(output))
        sys.exit(0)

    # All checks passed
    sys.exit(0)


if __name__ == '__main__':
    main()
