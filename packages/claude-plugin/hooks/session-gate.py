#!/usr/bin/env python3
"""
Session Gate hook - MCP health reminder at session start.
Part of the Six Gates Safety Framework (Gate 5: MCP Connection Verification).

Note: Hooks can't call MCP tools directly. This hook just outputs a reminder
for Claude to run health_check. MCP validates its own config from .mcp.json.

Runs at SessionStart, before other session hooks.
"""
import json
import sys

# Configure UTF-8 output for Windows console
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass


def check_mcp_health():
    """
    Note: Since hooks run as standalone Python scripts, we can't directly
    call MCP tools. We just remind Claude to run health_check if needed.

    MCP gets its vault path from .mcp.json config, not environment variables,
    so we can't validate MCP configuration from here.
    """
    return {'status': 'ok'}


def main():
    try:
        # Hooks can't call MCP directly - just output a minimal reminder
        # MCP validates its own config from .mcp.json
        context = "Tip: Run mcp__flywheel__health_check for MCP status."

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
