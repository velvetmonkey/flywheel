#!/usr/bin/env python3
"""
SessionStart hook - Shows today's daily note status and recent achievements.
Runs when Claude Code session starts.

Delegates wikilink cache rebuild to wikilink-cache.py (SRP).
"""
import json
import sys
import subprocess
import urllib.request
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


def check_for_updates():
    """Check GitHub for newer version. Returns update message or empty string."""
    current_version = get_current_version()

    # Cache file to avoid checking every session (check once per day)
    cache_file = Path.home() / '.flywheel-update-check'

    try:
        # Check cache first
        if cache_file.exists():
            mtime = datetime.fromtimestamp(cache_file.stat().st_mtime)
            if (datetime.now() - mtime).total_seconds() < 86400:  # 24 hours
                cached = cache_file.read_text(encoding='utf-8').strip()
                if cached and cached != current_version:
                    return format_update_message(current_version, cached)
                return ""

        # Fetch latest release from GitHub
        url = "https://api.github.com/repos/bencassie/flywheel/releases/latest"
        req = urllib.request.Request(url, headers={'User-Agent': 'flywheel-plugin'})
        with urllib.request.urlopen(req, timeout=3) as response:
            data = json.loads(response.read().decode('utf-8'))
            latest = data.get('tag_name', '').lstrip('v')

        # Cache the result
        try:
            cache_file.write_text(latest, encoding='utf-8')
        except Exception:
            pass  # Cache write failed, continue anyway

        # Compare versions
        if latest and latest != current_version:
            return format_update_message(current_version, latest)
        return ""

    except Exception:
        # Network error, rate limit, timeout - silently fail
        return ""


def format_update_message(current_version, latest_version):
    """Format the update notification box."""
    cmd = "/plugin update flywheel@bencassie-flywheel"
    url = "https://github.com/bencassie/flywheel/releases"

    return f"""
╔════════════════════════════════════════════════════════════════╗
║  Flywheel v{latest_version} available (you have v{current_version})
║
║  To update, copy and paste this command:
║  {cmd}
║
║  What's new: {url}
╚════════════════════════════════════════════════════════════════╝
"""


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

        # Check for updates (silent fail if network issues)
        update_notice = check_for_updates()

        # Build context string with available skills for plugin discovery
        context = f"""{update_notice}Flywheel - Session started: {current_time}

{daily_status}
{cache_status}

{achievements}

Available Flywheel skills (say these naturally):
- "setup flywheel" - Configure MCP, validate connection, see vault stats
- "check vault health" - Comprehensive diagnostics and recommendations
- "find orphan notes" - Disconnected notes needing links
- "show hub notes" - Your most connected knowledge
- "do a rollup" - Aggregate daily notes into weekly/monthly summaries
- "add log entry: [message]" - Append timestamped entry to daily note
- "find broken links" - Detect and repair dead wikilinks
- "what links to [note]" - Show backlinks for a note"""

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
