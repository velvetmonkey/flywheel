#!/usr/bin/env python3
"""
SessionStart hook - Shows today's daily note status and recent achievements.
Runs when Claude Code session starts.

Delegates wikilink cache rebuild to wikilink-cache.py (SRP).
"""
import json
import sys
import subprocess
from datetime import datetime
from pathlib import Path

# Configure UTF-8 output for Windows console
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

# Add parent directory to path for config import
sys.path.insert(0, str(Path(__file__).parent.parent))
from config.loader import load_config, get_path


def get_vault_path():
    """Get the vault path from current working directory."""
    return Path.cwd()


def get_daily_note_status(config: dict):
    """Check today's daily note and extract key info."""
    vault_path = get_vault_path()
    today = datetime.now().strftime("%Y-%m-%d")
    daily_notes_folder = config['paths']['daily_notes']
    daily_note_path = vault_path / daily_notes_folder / f"{today}.md"

    if not daily_note_path.exists():
        return f"Daily note: {today}.md does not exist yet"

    try:
        content = daily_note_path.read_text(encoding='utf-8')
        lines = content.split('\n')

        # Count habits completed
        habits_done = sum(1 for line in lines if line.strip().startswith('- [x]') and '#habit' in line)
        habits_total = sum(1 for line in lines if '#habit' in line and ('- [x]' in line or '- [ ]' in line))

        # Check if food section has entries
        food_header = config['sections']['food']
        food_entries = 0
        in_food = False
        for line in lines:
            if line.strip() == food_header:
                in_food = True
            elif line.startswith('#') and in_food:
                break
            elif in_food and line.strip().startswith('-') and line.strip() != '-':
                food_entries += 1

        # Check log entries
        log_header = config['sections']['log']
        log_entries = 0
        in_log = False
        for line in lines:
            if line.strip() == log_header:
                in_log = True
            elif line.startswith('#') and in_log:
                break
            elif in_log and line.strip().startswith('-') and line.strip() != '-':
                log_entries += 1

        status = f"Daily note: {today}.md exists"
        status += f"\n  Habits: {habits_done}/{habits_total} completed"
        status += f"\n  Food entries: {food_entries}"
        status += f"\n  Log entries: {log_entries}"

        return status
    except Exception as e:
        return f"Daily note: {today}.md (error reading: {e})"


def get_recent_achievements(config: dict):
    """Get the 5 most recent achievements."""
    vault_path = get_vault_path()
    achievements_path = vault_path / config['paths']['achievements']

    if not achievements_path.exists():
        return "No achievements file found"

    try:
        content = achievements_path.read_text(encoding='utf-8')
        lines = content.split('\n')

        # Find achievement lines (bullets under date headers)
        achievements = []
        current_date = None

        for line in lines:
            if line.startswith('## '):
                current_date = line[3:].strip()
            elif line.strip().startswith('-') and current_date:
                achievements.append(f"{current_date}: {line.strip()[2:]}")

        if not achievements:
            return "No achievements recorded yet"

        # Get last 5
        recent = achievements[-5:]
        return "Recent achievements:\n  " + "\n  ".join(recent)
    except Exception as e:
        return f"Error reading achievements: {e}"


def rebuild_wikilink_cache():
    """Delegate to wikilink-cache.py for cache rebuild (SRP)."""
    vault_path = get_vault_path()
    cache_script = Path(__file__).parent / 'wikilink-cache.py'

    try:
        result = subprocess.run(
            [sys.executable, str(cache_script)],
            cwd=str(vault_path),
            capture_output=True,
            text=True,
            timeout=60
        )
        # Return stdout which contains the status message
        return result.stdout.strip() if result.stdout else "Wikilink cache: rebuilt"
    except subprocess.TimeoutExpired:
        return "Wikilink cache: timeout"
    except Exception as e:
        return f"Wikilink cache: error - {e}"


def main():
    try:
        config = load_config()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")

        daily_status = get_daily_note_status(config)
        achievements = get_recent_achievements(config)
        cache_status = rebuild_wikilink_cache()

        # Build context string
        context = f"""Flywheel - Session started: {current_time}

{daily_status}
{cache_status}

{achievements}"""

        # Output in Claude Code's expected JSON format
        output = {
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": context
            }
        }
        print(json.dumps(output))

        sys.exit(0)

    except FileNotFoundError as e:
        print(f"[flywheel] Session start: Config file not found. Create .flywheel.json in vault root.", file=sys.stderr)
        sys.exit(0)
    except PermissionError as e:
        print(f"[flywheel] Session start: Permission denied - {e.filename}", file=sys.stderr)
        sys.exit(0)
    except ModuleNotFoundError as e:
        print(f"[flywheel] Session start: Missing module - {e.name}. Check plugin installation.", file=sys.stderr)
        sys.exit(0)
    except json.JSONDecodeError as e:
        print(f"[flywheel] Session start: Invalid JSON in config - {e.msg} at line {e.lineno}", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        print(f"[flywheel] Session start error: {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()
