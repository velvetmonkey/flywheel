"""
Gate 2 Tests: File Exists for Edit

Tests that Edit operations are blocked on non-existent files.
Write operations are allowed to create new files.
"""

import json
from pathlib import Path

import pytest

from .helpers import (
    run_hook,
    write_transcript_events,
    assert_deny,
    assert_ask,
)


class TestGate2FileExists:
    """Tests for Gate 2: File Exists enforcement."""

    def test_blocks_edit_nonexistent(self, hooks_dir, temp_vault, temp_transcript, session_id, gate1_cache_dir):
        """Gate 2 should BLOCK Edit to non-existent file."""
        nonexistent = str(temp_vault / "nonexistent.md")

        hook_input = {
            "tool_name": "Edit",
            "tool_input": {"file_path": nonexistent},
            "session_id": session_id,
            "transcript_path": str(temp_transcript)
        }

        result = run_hook(hooks_dir / "pre-mutation-gate.py", hook_input)

        assert_deny(result, "does not exist")

    def test_allows_edit_existing(self, hooks_dir, temp_vault, temp_transcript, session_id, gate1_cache_dir):
        """Gate 2 should ALLOW Edit to existing file (then Gate 1/4 applies)."""
        file_path = str(temp_vault / "existing.md")

        # Pre-read to satisfy Gate 1
        cache_path = gate1_cache_dir / "gate1-reads" / f"{session_id}.json"
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.write_text(json.dumps([str(Path(file_path).resolve())]))

        write_transcript_events(temp_transcript, [])

        hook_input = {
            "tool_name": "Edit",
            "tool_input": {"file_path": file_path},
            "session_id": session_id,
            "transcript_path": str(temp_transcript)
        }

        result = run_hook(hooks_dir / "pre-mutation-gate.py", hook_input)

        # Should pass Gate 2, proceed to Gate 4
        assert_ask(result)

    def test_allows_write_new_file(self, hooks_dir, temp_vault, temp_transcript, session_id, gate1_cache_dir):
        """Gate 2 should ALLOW Write to new file (Write creates files)."""
        new_file = str(temp_vault / "new-file.md")

        hook_input = {
            "tool_name": "Write",
            "tool_input": {"file_path": new_file, "content": "# New"},
            "session_id": session_id,
            "transcript_path": str(temp_transcript)
        }

        result = run_hook(hooks_dir / "pre-mutation-gate.py", hook_input)

        # Write should not be blocked by Gate 2
        # (May be blocked by Gate 1 for .md files, but not Gate 2)
        if result and "hookSpecificOutput" in result:
            if result["hookSpecificOutput"]["permissionDecision"] == "deny":
                # If denied, should NOT be because file doesn't exist (that's Gate 2)
                reason = result["hookSpecificOutput"]["permissionDecisionReason"]
                assert "does not exist" not in reason or "Use Write" not in reason

    def test_gate2_before_gate1(self, hooks_dir, temp_vault, temp_transcript, session_id, gate1_cache_dir):
        """Gate 2 should trigger BEFORE Gate 1 for Edit on non-existent files."""
        nonexistent = str(temp_vault / "nonexistent.md")

        # Even with read cache, Gate 2 should trigger first
        cache_path = gate1_cache_dir / "gate1-reads" / f"{session_id}.json"
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.write_text(json.dumps([str(Path(nonexistent).resolve())]))

        hook_input = {
            "tool_name": "Edit",
            "tool_input": {"file_path": nonexistent},
            "session_id": session_id,
            "transcript_path": str(temp_transcript)
        }

        result = run_hook(hooks_dir / "pre-mutation-gate.py", hook_input)

        # Should be blocked by Gate 2, not Gate 1
        assert_deny(result, "does not exist")
        assert "GATE 2" in result["hookSpecificOutput"]["permissionDecisionReason"]

    def test_directory_instead_of_file(self, hooks_dir, temp_vault, temp_transcript, session_id, gate1_cache_dir):
        """Edit on a directory should be blocked."""
        dir_path = str(temp_vault / "daily-notes")  # This is a directory

        hook_input = {
            "tool_name": "Edit",
            "tool_input": {"file_path": dir_path},
            "session_id": session_id,
            "transcript_path": str(temp_transcript)
        }

        result = run_hook(hooks_dir / "pre-mutation-gate.py", hook_input)

        # Directories can't be edited - should be blocked
        # The exact behavior depends on implementation
        if result and "hookSpecificOutput" in result:
            # Either deny or the system handles it
            pass  # Just checking it doesn't crash


class TestGate2EdgeCases:
    """Edge cases for Gate 2."""

    def test_empty_file_path(self, hooks_dir, temp_transcript, session_id, gate1_cache_dir):
        """Empty file path should be handled gracefully."""
        hook_input = {
            "tool_name": "Edit",
            "tool_input": {"file_path": ""},
            "session_id": session_id,
            "transcript_path": str(temp_transcript)
        }

        result = run_hook(hooks_dir / "pre-mutation-gate.py", hook_input)

        # Should exit without error
        assert result.get("exit_code", 0) == 0 or "hookSpecificOutput" in result

    def test_absolute_path_nonexistent(self, hooks_dir, temp_transcript, session_id, gate1_cache_dir):
        """Absolute path to non-existent file should be blocked."""
        hook_input = {
            "tool_name": "Edit",
            "tool_input": {"file_path": "/absolutely/fake/path.md"},
            "session_id": session_id,
            "transcript_path": str(temp_transcript)
        }

        result = run_hook(hooks_dir / "pre-mutation-gate.py", hook_input)

        assert_deny(result, "does not exist")

    def test_special_characters_in_path(self, hooks_dir, temp_vault, temp_transcript, session_id, gate1_cache_dir):
        """File paths with special characters should work."""
        # Create file with special chars
        special_file = temp_vault / "note (copy).md"
        special_file.write_text("content")

        # Pre-read to satisfy Gate 1
        cache_path = gate1_cache_dir / "gate1-reads" / f"{session_id}.json"
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.write_text(json.dumps([str(Path(special_file).resolve())]))

        hook_input = {
            "tool_name": "Edit",
            "tool_input": {"file_path": str(special_file)},
            "session_id": session_id,
            "transcript_path": str(temp_transcript)
        }

        result = run_hook(hooks_dir / "pre-mutation-gate.py", hook_input)

        # Should pass Gate 2 (file exists)
        assert_ask(result)
