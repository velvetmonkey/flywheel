#!/usr/bin/env python3
"""
SessionStart hook - Minimal output for fast startup.
Just tells Claude what tools are available.
"""
import json
import sys
from pathlib import Path

# Configure UTF-8 output for Windows console
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass


def get_current_version():
    """Read current version from plugin.json."""
    try:
        plugin_json = Path(__file__).parent.parent / '.claude-plugin' / 'plugin.json'
        if plugin_json.exists():
            data = json.loads(plugin_json.read_text(encoding='utf-8'))
            return data.get('version', '0.0.0')
    except Exception:
        pass
    return '0.0.0'


def main():
    try:
        version = get_current_version()

        # Minimal session message - just plugin info and tool list
        context = f"""Flywheel v{version} - Markdown Operating System

MCP tools for vault intelligence:
- Graph: get_backlinks, get_forward_links, find_hub_notes, find_orphan_notes, get_link_path
- Query: search_notes, find_sections, get_recent_notes, get_stale_notes
- Schema: get_frontmatter_schema, validate_frontmatter, infer_folder_conventions
- Tasks: get_all_tasks, get_tasks_with_due_dates
- Structure: get_note_structure, get_headings, get_section_content

Run health_check for vault status."""

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
        print(f"[flywheel] Session start error: {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()
