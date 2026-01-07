"""
Read Cache Tests

Tests for read-cache.py PostToolUse hook that persists Read operations
to enable Gate 1 enforcement across context summarization.
"""

import json
from pathlib import Path

import pytest

from .helpers import run_hook


class TestReadCache:
    """Tests for the read-cache.py hook."""

    def test_caches_markdown_reads(self, hooks_dir, temp_vault, session_id, gate1_cache_dir):
        """read-cache.py should cache .md file reads."""
        file_path = str(temp_vault / "existing.md")

        hook_input = {
            "tool_name": "Read",
            "tool_input": {"file_path": file_path},
            "session_id": session_id
        }

        run_hook(hooks_dir / "read-cache.py", hook_input)

        # Check cache was written
        cache_path = gate1_cache_dir / "gate1-reads" / f"{session_id}.json"
        assert cache_path.exists(), "Cache file should be created"

        cached = json.loads(cache_path.read_text())
        resolved_path = str(Path(file_path).resolve())
        assert resolved_path in cached, f"Expected {resolved_path} in cache: {cached}"

    def test_skips_non_markdown(self, hooks_dir, temp_vault, session_id, gate1_cache_dir):
        """read-cache.py should NOT cache non-.md files."""
        # Create a .py file
        py_file = temp_vault / "script.py"
        py_file.write_text("print('hello')")

        hook_input = {
            "tool_name": "Read",
            "tool_input": {"file_path": str(py_file)},
            "session_id": session_id
        }

        run_hook(hooks_dir / "read-cache.py", hook_input)

        cache_path = gate1_cache_dir / "gate1-reads" / f"{session_id}.json"

        if cache_path.exists():
            cached = json.loads(cache_path.read_text())
            assert "script.py" not in str(cached), "Non-.md files should not be cached"
        # If cache doesn't exist, that's also correct

    def test_skips_claude_directory(self, hooks_dir, temp_vault, session_id, gate1_cache_dir):
        """read-cache.py should NOT cache .claude directory files."""
        # Create .claude directory file
        claude_dir = temp_vault / ".claude"
        claude_dir.mkdir()
        settings = claude_dir / "settings.md"
        settings.write_text("config")

        hook_input = {
            "tool_name": "Read",
            "tool_input": {"file_path": str(settings)},
            "session_id": session_id
        }

        run_hook(hooks_dir / "read-cache.py", hook_input)

        cache_path = gate1_cache_dir / "gate1-reads" / f"{session_id}.json"

        if cache_path.exists():
            cached = json.loads(cache_path.read_text())
            assert ".claude" not in str(cached), ".claude files should not be cached"

    def test_accumulates_reads(self, hooks_dir, temp_vault, session_id, gate1_cache_dir):
        """Multiple reads should accumulate in cache."""
        file1 = str(temp_vault / "existing.md")
        file2 = str(temp_vault / "daily-notes" / "2026-01-03.md")

        # Read first file
        run_hook(hooks_dir / "read-cache.py", {
            "tool_name": "Read",
            "tool_input": {"file_path": file1},
            "session_id": session_id
        })

        # Read second file
        run_hook(hooks_dir / "read-cache.py", {
            "tool_name": "Read",
            "tool_input": {"file_path": file2},
            "session_id": session_id
        })

        cache_path = gate1_cache_dir / "gate1-reads" / f"{session_id}.json"
        assert cache_path.exists()

        cached = json.loads(cache_path.read_text())

        # Both files should be in cache
        assert len(cached) == 2, f"Expected 2 files in cache, got {len(cached)}"
        assert str(Path(file1).resolve()) in cached
        assert str(Path(file2).resolve()) in cached

    def test_handles_missing_session_id(self, hooks_dir, temp_vault, gate1_cache_dir):
        """Missing session_id should gracefully skip caching."""
        hook_input = {
            "tool_name": "Read",
            "tool_input": {"file_path": str(temp_vault / "existing.md")},
            "session_id": ""  # Empty session ID
        }

        # Should not raise an error
        result = run_hook(hooks_dir / "read-cache.py", hook_input)

        # Should exit cleanly (exit code 0)
        assert result.get("exit_code", 0) == 0 or not result

    def test_handles_missing_file_path(self, hooks_dir, session_id, gate1_cache_dir):
        """Missing file_path should gracefully skip."""
        hook_input = {
            "tool_name": "Read",
            "tool_input": {},  # No file_path
            "session_id": session_id
        }

        result = run_hook(hooks_dir / "read-cache.py", hook_input)

        # Should exit cleanly
        assert result.get("exit_code", 0) == 0 or not result

    def test_skips_non_read_tools(self, hooks_dir, temp_vault, session_id, gate1_cache_dir):
        """Only Read tool should be cached."""
        hook_input = {
            "tool_name": "Edit",  # Not Read
            "tool_input": {"file_path": str(temp_vault / "existing.md")},
            "session_id": session_id
        }

        run_hook(hooks_dir / "read-cache.py", hook_input)

        cache_path = gate1_cache_dir / "gate1-reads" / f"{session_id}.json"

        # Cache should not be created for non-Read tools
        if cache_path.exists():
            cached = json.loads(cache_path.read_text())
            assert len(cached) == 0, "Edit tool should not create cache entries"

    def test_deduplicates_reads(self, hooks_dir, temp_vault, session_id, gate1_cache_dir):
        """Reading same file multiple times should not duplicate in cache."""
        file_path = str(temp_vault / "existing.md")

        # Read same file three times
        for _ in range(3):
            run_hook(hooks_dir / "read-cache.py", {
                "tool_name": "Read",
                "tool_input": {"file_path": file_path},
                "session_id": session_id
            })

        cache_path = gate1_cache_dir / "gate1-reads" / f"{session_id}.json"
        cached = json.loads(cache_path.read_text())

        # Should only have one entry (set behavior)
        assert len(cached) == 1, f"Expected 1 entry, got {len(cached)}: {cached}"

    def test_different_sessions_isolated(self, hooks_dir, temp_vault, gate1_cache_dir):
        """Different sessions should have isolated caches."""
        file_path = str(temp_vault / "existing.md")
        session1 = "test-session-1"
        session2 = "test-session-2"

        # Read in session 1
        run_hook(hooks_dir / "read-cache.py", {
            "tool_name": "Read",
            "tool_input": {"file_path": file_path},
            "session_id": session1
        }, env={"CLAUDE_LOCAL_STATE_DIR": str(gate1_cache_dir)})

        # Session 2 should have empty cache
        cache2_path = gate1_cache_dir / "gate1-reads" / f"{session2}.json"
        assert not cache2_path.exists(), "Session 2 should not have cache from session 1"

        # Session 1 should have the read
        cache1_path = gate1_cache_dir / "gate1-reads" / f"{session1}.json"
        assert cache1_path.exists()
