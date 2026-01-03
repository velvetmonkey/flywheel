#!/usr/bin/env python3
"""
Read Cache Hook - Records Read operations for Gate 1 enforcement.

This PostToolUse hook runs after Read operations and caches the file paths
in a session-scoped file. This cache persists across context summarization,
allowing Gate 1 (pre-mutation-gate.py) to verify reads even after the
transcript is truncated.

Part of the Six Gates Safety Framework.
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

# Session read cache - must match pre-mutation-gate.py
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


def save_session_reads(session_id: str, reads: set) -> None:
    """Save the set of read file paths for this session."""
    if not session_id:
        return
    cache_path = get_session_cache_path(session_id)
    try:
        with open(cache_path, 'w', encoding='utf-8') as f:
            json.dump(list(reads), f)
    except (PermissionError, OSError):
        pass


def record_read(session_id: str, file_path: str) -> None:
    """Record that a file was read in this session."""
    if not session_id or not file_path:
        return
    reads = load_session_reads(session_id)
    normalized = str(Path(file_path).resolve())
    reads.add(normalized)
    save_session_reads(session_id, reads)


def main():
    try:
        hook_input = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    # Only process successful Read operations
    tool_name = hook_input.get('tool_name', '')
    if tool_name != 'Read':
        sys.exit(0)

    # Get the file path that was read
    file_path = hook_input.get('tool_input', {}).get('file_path', '')
    if not file_path:
        sys.exit(0)

    # Only cache markdown files (matches Gate 1 scope)
    if not file_path.endswith('.md'):
        sys.exit(0)

    # Skip .claude directory
    if '.claude' in file_path:
        sys.exit(0)

    # Record the read in the session cache
    session_id = hook_input.get('session_id', '')
    record_read(session_id, file_path)

    sys.exit(0)


if __name__ == '__main__':
    main()
