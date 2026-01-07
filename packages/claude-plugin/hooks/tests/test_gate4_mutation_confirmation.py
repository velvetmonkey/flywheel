"""
Gate 4 Tests: Mutation Confirmation

Tests that Edit/Write operations prompt for user confirmation.
Uses "ask" permission decision (can be bypassed by permissions.allow config).
"""

import json
from pathlib import Path

import pytest

from .helpers import run_hook, write_transcript_events, assert_ask


class TestGate4MutationConfirmation:
    """Tests for Gate 4: Mutation confirmation prompt."""

    def test_asks_for_markdown_edit(self, hooks_dir, temp_vault, temp_transcript, session_id, gate1_cache_dir):
        """Gate 4 should ASK user to confirm Edit."""
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

        assert_ask(result, "GATE 4")

    def test_includes_filename_in_prompt(self, hooks_dir, temp_vault, temp_transcript, session_id, gate1_cache_dir):
        """Gate 4 prompt should include the filename."""
        file_path = str(temp_vault / "existing.md")

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

        assert "existing.md" in result["hookSpecificOutput"]["permissionDecisionReason"]

    def test_includes_tool_name_in_prompt(self, hooks_dir, temp_vault, temp_transcript, session_id, gate1_cache_dir):
        """Gate 4 prompt should include the tool name (Edit/Write)."""
        file_path = str(temp_vault / "existing.md")

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

        assert "Edit" in result["hookSpecificOutput"]["permissionDecisionReason"]

    def test_asks_for_write(self, hooks_dir, temp_vault, temp_transcript, session_id, gate1_cache_dir):
        """Gate 4 should ASK for Write operations too."""
        # Create a file first
        file_path = str(temp_vault / "to-overwrite.md")
        Path(file_path).write_text("original content")

        # Pre-read to satisfy Gate 1
        cache_path = gate1_cache_dir / "gate1-reads" / f"{session_id}.json"
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.write_text(json.dumps([str(Path(file_path).resolve())]))

        write_transcript_events(temp_transcript, [])

        hook_input = {
            "tool_name": "Write",
            "tool_input": {"file_path": file_path, "content": "new content"},
            "session_id": session_id,
            "transcript_path": str(temp_transcript)
        }

        result = run_hook(hooks_dir / "pre-mutation-gate.py", hook_input)

        # Should ask for confirmation
        assert_ask(result, "GATE 4")

    def test_asks_for_non_markdown(self, hooks_dir, temp_vault, temp_transcript, session_id, gate1_cache_dir):
        """Gate 4 should also prompt for non-.md files (even though Gate 1 skips them)."""
        py_file = temp_vault / "script.py"
        py_file.write_text("print('hello')")

        hook_input = {
            "tool_name": "Edit",
            "tool_input": {"file_path": str(py_file)},
            "session_id": session_id,
            "transcript_path": str(temp_transcript)
        }

        result = run_hook(hooks_dir / "pre-mutation-gate.py", hook_input)

        # Should reach Gate 4 (Gate 1 skips non-.md)
        if result and "hookSpecificOutput" in result:
            assert result["hookSpecificOutput"]["permissionDecision"] == "ask"


class TestGate4PermissionDecision:
    """Tests for the ask permission decision behavior."""

    def test_ask_decision_format(self, hooks_dir, temp_vault, temp_transcript, session_id, gate1_cache_dir):
        """Verify the ask decision has correct JSON format."""
        file_path = str(temp_vault / "existing.md")

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

        # Verify structure
        assert "hookSpecificOutput" in result
        output = result["hookSpecificOutput"]
        assert "hookEventName" in output
        assert output["hookEventName"] == "PreToolUse"
        assert "permissionDecision" in output
        assert output["permissionDecision"] == "ask"
        assert "permissionDecisionReason" in output
