#!/usr/bin/env python3
"""
Pre-Mutation Gate - Six Gates Enforcement (Gates 1, 2, 4)
Runs BEFORE Edit/Write to BLOCK unsafe operations.

Gate 1: Read Before Write - Block if file not read first
Gate 2: File Exists for Edit - Block Edit on non-existent files
Gate 4: Mutation Confirmation - Ask user to confirm

Exit codes:
- 0: Always (decision communicated via JSON output)

Session Read Cache:
Gate 1 uses transcript to find prior Read events, but transcript is lost
when context is summarized. To fix this, we also maintain a session-scoped
cache file that persists reads across summarization.
"""

import json
import os
import sys
from pathlib import Path

# Configure UTF-8 output for Windows console
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

# Session read cache - persists across context summarization
# Uses session_id from hook input to scope the cache
CACHE_DIR = Path(os.environ.get('CLAUDE_LOCAL_STATE_DIR', Path.home() / '.claude'))


def get_session_cache_path(session_id: str) -> Path:
    """Get the cache file path for this session."""
    cache_dir = CACHE_DIR / 'gate1-reads'
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir / f'{session_id}.json'


def load_session_reads(session_id: str) -> set:
    """Load the set of read file paths for this session."""
    if not session_id:
        return set()
    cache_path = get_session_cache_path(session_id)
    try:
        if cache_path.exists():
            with open(cache_path, 'r', encoding='utf-8') as f:
                return set(json.load(f))
    except (json.JSONDecodeError, PermissionError, OSError):
        pass
    return set()


def has_session_read(session_id: str, file_path: str) -> bool:
    """Check if file was read in this session (from cache)."""
    if not session_id:
        return False
    reads = load_session_reads(session_id)
    normalized = str(Path(file_path).resolve())
    return normalized in reads


def load_transcript(transcript_path):
    """Parse conversation history to find prior tool uses."""
    events = []
    try:
        with open(transcript_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    events.append(json.loads(line))
    except (FileNotFoundError, json.JSONDecodeError, PermissionError):
        return []
    return events


def has_prior_read(events, file_path):
    """Check if file was Read in this session."""
    # Normalize the file path for comparison
    normalized_target = Path(file_path).resolve()

    for event in events:
        # Check for tool_use events with Read tool
        if event.get('type') == 'tool_use' and event.get('name') == 'Read':
            event_path = event.get('input', {}).get('file_path', '')
            if event_path:
                try:
                    normalized_event = Path(event_path).resolve()
                    if normalized_event == normalized_target:
                        return True
                except (ValueError, OSError):
                    # Path normalization failed, try string comparison
                    if event_path == file_path:
                        return True
    return False


def main():
    try:
        hook_input = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)  # Invalid input, don't block

    tool_name = hook_input.get('tool_name', '')
    if tool_name not in ['Write', 'Edit']:
        sys.exit(0)  # Only gate mutations

    file_path = hook_input.get('tool_input', {}).get('file_path', '')
    if not file_path:
        sys.exit(0)

    # Skip .claude directory (internal files)
    if '.claude' in file_path:
        sys.exit(0)

    # Skip non-markdown files for Gate 1 (read-before-write)
    # But still apply Gate 2 and 4 to all files
    is_markdown = file_path.endswith('.md')

    # GATE 2: Edit requires file exists
    if tool_name == 'Edit':
        if not Path(file_path).exists():
            output = {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": f"GATE 2 BLOCKED: File does not exist: {file_path}. Use Write to create new files."
                }
            }
            print(json.dumps(output))
            sys.exit(0)

    # GATE 1: Read before write (for .md files only)
    # For Write: only require read if file ALREADY EXISTS (overwriting)
    # For Edit: always require read (Gate 2 already ensures file exists)
    file_exists = Path(file_path).exists()

    if is_markdown and (tool_name == 'Edit' or (tool_name == 'Write' and file_exists)):
        session_id = hook_input.get('session_id', '')
        transcript_path = hook_input.get('transcript_path', '')

        # Check BOTH transcript AND session cache (cache survives context summarization)
        found_in_transcript = False
        found_in_cache = has_session_read(session_id, file_path)

        if transcript_path:
            events = load_transcript(transcript_path)
            found_in_transcript = has_prior_read(events, file_path)

        if not found_in_transcript and not found_in_cache:
            action = "overwriting" if tool_name == 'Write' else "editing"
            output = {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": f"GATE 1 BLOCKED: Must Read '{Path(file_path).name}' before {action}. This prevents overwriting content you haven't reviewed."
                }
            }
            print(json.dumps(output))
            sys.exit(0)

    # GATE 4: Confirmation for mutations
    # Use "ask" to prompt user (respects permissions.allow if configured)
    output = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "ask",
            "permissionDecisionReason": f"GATE 4: Confirm {tool_name} to {Path(file_path).name}?"
        }
    }
    print(json.dumps(output))
    sys.exit(0)


if __name__ == '__main__':
    main()
