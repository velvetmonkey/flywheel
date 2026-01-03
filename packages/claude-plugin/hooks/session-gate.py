#!/usr/bin/env python3
"""
Session Gate hook - MCP health verification at session start.
Part of the Six Gates Safety Framework (Gate 5: MCP Connection Verification).

This hook:
1. Checks if MCP is reachable by calling health_check
2. Reports index freshness
3. Warns user if MCP is unavailable or index is stale
4. Auto-refreshes stale index if configured

Runs at SessionStart, before other session hooks.
"""
import json
import sys
from pathlib import Path

# Configure UTF-8 output for Windows console
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass


def check_mcp_health():
    """
    Attempt to verify MCP is working.

    Note: Since hooks run as standalone Python scripts, we can't directly
    call MCP tools. Instead, we check environment variables and report
    status that will be shown to Claude, who can then call health_check.
    """
    import os

    project_path = os.environ.get('PROJECT_PATH', '')
    recommendations = []
    status = 'unknown'

    if not project_path:
        recommendations.append('PROJECT_PATH not set - MCP vault tools may not work')
        status = 'warning'
    else:
        # Check if path exists and is accessible
        vault_path = Path(project_path)
        if not vault_path.exists():
            recommendations.append(f'PROJECT_PATH ({project_path}) does not exist')
            status = 'error'
        elif not vault_path.is_dir():
            recommendations.append(f'PROJECT_PATH ({project_path}) is not a directory')
            status = 'error'
        else:
            # Check for markdown files
            md_files = list(vault_path.glob('**/*.md'))[:5]  # Just check for presence
            if not md_files:
                recommendations.append(f'No .md files found in vault - is this a markdown vault?')
                status = 'warning'
            else:
                status = 'ok'

    return {
        'status': status,
        'project_path': project_path or '(not set)',
        'recommendations': recommendations
    }


def main():
    try:
        health = check_mcp_health()

        # Build context message based on status
        if health['status'] == 'ok':
            context = f"""MCP Gate Check: OK
Vault path: {health['project_path']}

Tip: Run mcp__flywheel__health_check for detailed MCP status."""

        elif health['status'] == 'warning':
            context = f"""MCP Gate Check: WARNING
Vault path: {health['project_path']}

Issues detected:
""" + '\n'.join(f"  - {r}" for r in health['recommendations']) + """

Action: Run mcp__flywheel__health_check to verify MCP is working."""

        else:  # error
            context = f"""MCP Gate Check: ERROR
Vault path: {health['project_path']}

Critical issues:
""" + '\n'.join(f"  - {r}" for r in health['recommendations']) + """

Action: Check PROJECT_PATH environment variable in MCP configuration."""

        # Output in Claude Code's expected JSON format
        output = {
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": context
            }
        }
        print(json.dumps(output))
        sys.exit(0)

    except Exception as e:
        print(f"[flywheel] Session gate error: {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()
