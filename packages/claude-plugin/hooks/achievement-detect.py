#!/usr/bin/env python3
"""
Achievement Detector Hook

Runs after Edit operations on daily notes to detect accomplishments
that should be added to Achievements file.

This hook uses the shared achievement_detector library module for detection logic.
The same logic is used by the achievement-extraction-agent for manual extraction.

Exit codes:
- 0: Always (informational only, never blocks)
"""

import json
import sys
from pathlib import Path

# Configure UTF-8 output for Windows console
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

# Add parent directory to path for config import
sys.path.insert(0, str(Path(__file__).parent.parent))
from config.loader import load_config

# Import shared achievement detection library
sys.path.insert(0, str(Path(__file__).parent))
from lib.achievement_detector import (
    check_for_achievements,
    write_achievements_to_file
)


def main():
    try:
        # Read hook input from stdin
        hook_input = json.load(sys.stdin)

        # Only run on Edit/Write operations
        tool_name = hook_input.get('tool_name', '')
        if tool_name not in ['Edit', 'Write']:
            sys.exit(0)

        # Get the file path from tool input
        tool_input = hook_input.get('tool_input', {})
        file_path = tool_input.get('file_path', '')

        # Load config
        config = load_config()
        daily_notes_folder = config['paths']['daily_notes']

        # Only check daily notes
        if daily_notes_folder not in file_path or not file_path.endswith('.md'):
            sys.exit(0)

        # Check if file exists
        path = Path(file_path)
        if not path.exists():
            sys.exit(0)

        # Read file content
        content = path.read_text(encoding='utf-8')

        # Check for achievements using shared library
        achievements = check_for_achievements(content, config)

        if achievements:
            # Get vault root
            vault_path = path
            while vault_path.parent != vault_path:
                if (vault_path / '.obsidian').exists() or (vault_path / '.claude').exists():
                    break
                vault_path = vault_path.parent

            # Get achievements file path from config
            achievements_file = vault_path / config['paths']['achievements']

            if achievements_file.exists():
                # Write achievements using shared library (no limit - log everything)
                num_written = write_achievements_to_file(
                    achievements,
                    achievements_file,
                    max_achievements=1000
                )

                if num_written > 0:
                    print(f"\n✓ Auto-Added {num_written} Achievements")
                    print("-" * 50)
                    for a in achievements[:num_written]:
                        print(f"  • {a['line'][:80]}{'...' if len(a['line']) > 80 else ''}")
                    print("-" * 50)
                    print("")
            else:
                # Fallback: just notify
                print(f"\n🏆 Achievement Detected (Achievements file not found)")
                print("-" * 50)
                for a in achievements[:3]:
                    print(f"  • {a['line'][:80]}{'...' if len(a['line']) > 80 else ''}")
                print("-" * 50)
                print("")

        sys.exit(0)

    except json.JSONDecodeError:
        sys.exit(0)
    except FileNotFoundError as e:
        print(f"[obsidian-scribe] Achievement detector: File not found - {e.filename}", file=sys.stderr)
        sys.exit(0)
    except PermissionError as e:
        print(f"[obsidian-scribe] Achievement detector: Permission denied - {e.filename}", file=sys.stderr)
        sys.exit(0)
    except ModuleNotFoundError as e:
        print(f"[obsidian-scribe] Achievement detector: Missing module - {e.name}. Check plugin installation.", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        print(f"[obsidian-scribe] Achievement detector error: {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(0)


if __name__ == '__main__':
    main()
