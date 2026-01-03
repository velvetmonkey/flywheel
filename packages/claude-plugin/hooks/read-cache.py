#!/usr/bin/env python3
"""
Read Cache Hook - Records Read operations for Gate 1 enforcement.

This PostToolUse hook runs after Read operations and caches the file paths
in a session-scoped file. This cache persists across context summarization,
allowing Gate 1 (pre-mutation-gate.py) to verify reads even after the
transcript is truncated.

Part of the Six Gates Safety Framework.

IMPORTANT: Uses file locking to handle parallel Read operations safely.
When Claude reads multiple files in parallel, each hook instance must
acquire a lock before modifying the cache.
"""

import json
import os
import sys
import time
from pathlib import Path

# Configure UTF-8 output for Windows console
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

# Session read cache - must match pre-mutation-gate.py
CACHE_DIR = Path(os.environ.get('CLAUDE_LOCAL_STATE_DIR', Path.home() / '.claude'))

# Cross-platform file locking
IS_WINDOWS = sys.platform == 'win32'

if IS_WINDOWS:
    import msvcrt

    def lock_file(f):
        """Acquire exclusive lock on file (Windows)."""
        msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, 1)

    def unlock_file(f):
        """Release lock on file (Windows)."""
        f.seek(0)
        msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
else:
    import fcntl

    def lock_file(f):
        """Acquire exclusive lock on file (Unix)."""
        fcntl.flock(f.fileno(), fcntl.LOCK_EX)

    def unlock_file(f):
        """Release lock on file (Unix)."""
        fcntl.flock(f.fileno(), fcntl.LOCK_UN)


def get_session_cache_path(session_id: str) -> Path:
    """Get the cache file path for this session."""
    cache_dir = CACHE_DIR / 'gate1-reads'
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir / f'{session_id}.json'


def get_lock_path(session_id: str) -> Path:
    """Get the lock file path for this session."""
    cache_dir = CACHE_DIR / 'gate1-reads'
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir / f'{session_id}.lock'


def record_read(session_id: str, file_path: str) -> None:
    """
    Record that a file was read in this session.

    Uses file locking to safely handle parallel Read operations.
    """
    if not session_id or not file_path:
        return

    normalized = str(Path(file_path).resolve())
    cache_path = get_session_cache_path(session_id)
    lock_path = get_lock_path(session_id)

    # Retry with backoff for lock acquisition
    max_retries = 5
    for attempt in range(max_retries):
        try:
            # Use a lock file to ensure atomic read-modify-write
            with open(lock_path, 'w') as lock_file:
                try:
                    lock_file(lock_file)

                    # Load existing reads while holding lock
                    reads = set()
                    if cache_path.exists():
                        try:
                            with open(cache_path, 'r', encoding='utf-8') as f:
                                reads = set(json.load(f))
                        except (json.JSONDecodeError, PermissionError, OSError):
                            pass

                    # Add new read
                    reads.add(normalized)

                    # Save while still holding lock
                    with open(cache_path, 'w', encoding='utf-8') as f:
                        json.dump(list(reads), f)

                    return  # Success

                finally:
                    try:
                        unlock_file(lock_file)
                    except (OSError, IOError):
                        pass

        except (PermissionError, OSError, IOError) as e:
            # Lock acquisition failed, retry with backoff
            if attempt < max_retries - 1:
                time.sleep(0.05 * (attempt + 1))  # 50ms, 100ms, 150ms, 200ms
            else:
                # Final attempt failed, try without lock (best effort)
                _record_read_no_lock(normalized, cache_path)


def _record_read_no_lock(normalized: str, cache_path: Path) -> None:
    """Fallback when locking fails - best effort, may lose writes in race."""
    try:
        reads = set()
        if cache_path.exists():
            try:
                with open(cache_path, 'r', encoding='utf-8') as f:
                    reads = set(json.load(f))
            except (json.JSONDecodeError, PermissionError, OSError):
                pass

        reads.add(normalized)

        with open(cache_path, 'w', encoding='utf-8') as f:
            json.dump(list(reads), f)
    except (PermissionError, OSError):
        pass


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
