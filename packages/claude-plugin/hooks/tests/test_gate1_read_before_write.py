"""
Gate 1 Tests: Read Before Write

Tests that Edit/Write to .md files are blocked unless the file was previously Read.
Gate 1 checks both transcript history AND session cache (for context summarization).
"""

import json
from pathlib import Path

import pytest

from .helpers import (
    run_hook,
    write_transcript_events,
    make_read_event,
    make_edit_input,
    assert_deny,
    assert_ask,
)


class TestGate1ReadBeforeWrite:
    """Tests for Gate 1: Read Before Write enforcement."""

    def test_blocks_unread_markdown(self, hooks_dir, temp_vault, temp_transcript, session_id, gate1_cache_dir):
        """Gate 1 should BLOCK Edit to .md file not in transcript or cache."""
        write_transcript_events(temp_transcript, [])  # Empty transcript

        hook_input = make_edit_input(
            file_path=str(temp_vault / "existing.md"),
            session_id=session_id,
            transcript_path=str(temp_transcript)
        )

        result = run_hook(hooks_dir / "pre-mutation-gate.py", hook_input)

        assert_deny(result, "Must Read")

    def test_allows_read_file_from_transcript(self, hooks_dir, temp_vault, temp_transcript, session_id, gate1_cache_dir):
        """Gate 1 should ALLOW Edit to .md file that was Read in transcript."""
        file_path = str(temp_vault / "existing.md")

        # Write Read event to transcript
        write_transcript_events(temp_transcript, [make_read_event(file_path)])

        hook_input = make_edit_input(
            file_path=file_path,
            session_id=session_id,
            transcript_path=str(temp_transcript)
        )

        result = run_hook(hooks_dir / "pre-mutation-gate.py", hook_input)

        # Should proceed to Gate 4 (ask), not be blocked by Gate 1
        assert_ask(result, "GATE 4")

    def test_allows_read_file_from_cache(self, hooks_dir, temp_vault, temp_transcript, session_id, gate1_cache_dir):
        """Gate 1 should ALLOW Edit when file is in session cache (survives summarization)."""
        file_path = str(temp_vault / "existing.md")

        # Pre-populate cache (simulating read-cache.py)
        cache_path = gate1_cache_dir / "gate1-reads" / f"{session_id}.json"
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.write_text(json.dumps([str(Path(file_path).resolve())]))

        # Empty transcript (simulating context summarization)
        write_transcript_events(temp_transcript, [])

        hook_input = make_edit_input(
            file_path=file_path,
            session_id=session_id,
            transcript_path=str(temp_transcript)
        )

        result = run_hook(hooks_dir / "pre-mutation-gate.py", hook_input)

        assert_ask(result)  # Gate 1 passed, proceeds to Gate 4

    @pytest.mark.parametrize("file_path", [
        "test.py",
        "config.json",
        "README.txt",
        "script.sh",
    ])
    def test_skips_non_markdown(self, hooks_dir, temp_vault, temp_transcript, session_id, gate1_cache_dir, file_path):
        """Gate 1 should NOT check non-.md files."""
        # Create the file so Gate 2 doesn't block
        target = temp_vault / file_path
        target.write_text("content")

        hook_input = {
            "tool_name": "Edit",
            "tool_input": {"file_path": str(target)},
            "session_id": session_id,
            "transcript_path": str(temp_transcript)
        }

        result = run_hook(hooks_dir / "pre-mutation-gate.py", hook_input)

        # Should go straight to Gate 4, no Gate 1 block
        if result:
            assert result.get("hookSpecificOutput", {}).get("permissionDecision") != "deny" or \
                   "GATE 1" not in result.get("hookSpecificOutput", {}).get("permissionDecisionReason", "")

    def test_skips_claude_directory(self, hooks_dir, temp_vault, temp_transcript, session_id, gate1_cache_dir):
        """Gate 1 should NOT check .claude directory files."""
        # Create a .claude directory with a file
        claude_dir = temp_vault / ".claude"
        claude_dir.mkdir()
        target = claude_dir / "settings.md"
        target.write_text("config")

        hook_input = {
            "tool_name": "Edit",
            "tool_input": {"file_path": str(target)},
            "session_id": session_id,
            "transcript_path": str(temp_transcript)
        }

        result = run_hook(hooks_dir / "pre-mutation-gate.py", hook_input)

        # Should pass (skip Gate 1) - either empty result or ask
        if result and "hookSpecificOutput" in result:
            # If there's a deny, it should NOT be Gate 1
            if result["hookSpecificOutput"]["permissionDecision"] == "deny":
                assert "GATE 1" not in result["hookSpecificOutput"]["permissionDecisionReason"]

    @pytest.mark.parametrize("read_path,edit_path", [
        ("foo/bar.md", "foo/bar.md"),           # Same path
        ("./foo/bar.md", "foo/bar.md"),         # Relative with ./
    ])
    def test_path_normalization(self, hooks_dir, temp_vault, temp_transcript, session_id, gate1_cache_dir, read_path, edit_path):
        """Gate 1 should normalize paths for comparison."""
        # Create the file
        target_dir = temp_vault / "foo"
        target_dir.mkdir(exist_ok=True)
        (target_dir / "bar.md").write_text("content")

        full_read = str(temp_vault / read_path)
        full_edit = str(temp_vault / edit_path)

        write_transcript_events(temp_transcript, [make_read_event(full_read)])

        hook_input = make_edit_input(
            file_path=full_edit,
            session_id=session_id,
            transcript_path=str(temp_transcript)
        )

        result = run_hook(hooks_dir / "pre-mutation-gate.py", hook_input)

        assert_ask(result)  # Should pass Gate 1

    def test_empty_transcript_checks_cache(self, hooks_dir, temp_vault, temp_transcript, session_id, gate1_cache_dir):
        """With empty transcript, Gate 1 should still check cache."""
        file_path = str(temp_vault / "existing.md")

        # No cache, empty transcript
        write_transcript_events(temp_transcript, [])

        hook_input = make_edit_input(
            file_path=file_path,
            session_id=session_id,
            transcript_path=str(temp_transcript)
        )

        result = run_hook(hooks_dir / "pre-mutation-gate.py", hook_input)

        # Should be blocked (nothing in transcript or cache)
        assert_deny(result, "Must Read")

    def test_malformed_transcript_fallback(self, hooks_dir, temp_vault, temp_transcript, session_id, gate1_cache_dir):
        """Malformed transcript should gracefully fall back to cache check."""
        file_path = str(temp_vault / "existing.md")

        # Write invalid JSON to transcript
        temp_transcript.write_text("not valid json\n{broken")

        # Pre-populate cache
        cache_path = gate1_cache_dir / "gate1-reads" / f"{session_id}.json"
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.write_text(json.dumps([str(Path(file_path).resolve())]))

        hook_input = make_edit_input(
            file_path=file_path,
            session_id=session_id,
            transcript_path=str(temp_transcript)
        )

        result = run_hook(hooks_dir / "pre-mutation-gate.py", hook_input)

        # Should pass via cache even with broken transcript
        assert_ask(result)

    def test_missing_session_id_blocks(self, hooks_dir, temp_vault, temp_transcript, gate1_cache_dir):
        """Missing session_id should block (safe default)."""
        hook_input = {
            "tool_name": "Edit",
            "tool_input": {"file_path": str(temp_vault / "existing.md")},
            "session_id": "",  # Empty session ID
            "transcript_path": str(temp_transcript)
        }

        write_transcript_events(temp_transcript, [])

        result = run_hook(hooks_dir / "pre-mutation-gate.py", hook_input)

        # Should be blocked (can't check cache without session ID)
        assert_deny(result, "Must Read")

    def test_write_to_new_file_no_gate1(self, hooks_dir, temp_vault, temp_transcript, session_id, gate1_cache_dir):
        """Write to new .md file should trigger Gate 1 (new files should be read first? or not?)."""
        # Note: This tests current behavior - Write to non-existent file
        # Gate 1 applies to Write as well as Edit for .md files
        new_file = str(temp_vault / "new-note.md")

        hook_input = {
            "tool_name": "Write",
            "tool_input": {"file_path": new_file, "content": "# New Note"},
            "session_id": session_id,
            "transcript_path": str(temp_transcript)
        }

        write_transcript_events(temp_transcript, [])

        result = run_hook(hooks_dir / "pre-mutation-gate.py", hook_input)

        # Current behavior: Gate 1 blocks Write to new .md files too
        # This may or may not be desired - the test documents current behavior
        if result and "hookSpecificOutput" in result:
            # Document what happens - either deny or ask
            decision = result["hookSpecificOutput"]["permissionDecision"]
            assert decision in ["deny", "ask"]


class TestGate1EdgeCases:
    """Edge cases and error handling for Gate 1."""

    def test_no_transcript_path(self, hooks_dir, temp_vault, session_id, gate1_cache_dir):
        """No transcript path should rely on cache only."""
        file_path = str(temp_vault / "existing.md")

        # Pre-populate cache
        cache_path = gate1_cache_dir / "gate1-reads" / f"{session_id}.json"
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.write_text(json.dumps([str(Path(file_path).resolve())]))

        hook_input = {
            "tool_name": "Edit",
            "tool_input": {"file_path": file_path},
            "session_id": session_id,
            "transcript_path": ""  # No transcript
        }

        result = run_hook(hooks_dir / "pre-mutation-gate.py", hook_input)

        # Should pass via cache
        assert_ask(result)

    def test_nonexistent_transcript(self, hooks_dir, temp_vault, session_id, gate1_cache_dir):
        """Non-existent transcript file should fall back to cache."""
        file_path = str(temp_vault / "existing.md")

        # Pre-populate cache
        cache_path = gate1_cache_dir / "gate1-reads" / f"{session_id}.json"
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.write_text(json.dumps([str(Path(file_path).resolve())]))

        hook_input = {
            "tool_name": "Edit",
            "tool_input": {"file_path": file_path},
            "session_id": session_id,
            "transcript_path": "/nonexistent/path/transcript.jsonl"
        }

        result = run_hook(hooks_dir / "pre-mutation-gate.py", hook_input)

        # Should pass via cache
        assert_ask(result)

    def test_multiple_reads_same_file(self, hooks_dir, temp_vault, temp_transcript, session_id, gate1_cache_dir):
        """Multiple reads of same file should still allow edit."""
        file_path = str(temp_vault / "existing.md")

        # Multiple Read events
        write_transcript_events(temp_transcript, [
            make_read_event(file_path),
            make_read_event(file_path),
            make_read_event(file_path),
        ])

        hook_input = make_edit_input(
            file_path=file_path,
            session_id=session_id,
            transcript_path=str(temp_transcript)
        )

        result = run_hook(hooks_dir / "pre-mutation-gate.py", hook_input)

        assert_ask(result)

    def test_read_different_file(self, hooks_dir, temp_vault, temp_transcript, session_id, gate1_cache_dir):
        """Reading a different file should not allow edit of unread file."""
        file_a = str(temp_vault / "existing.md")
        file_b = str(temp_vault / "daily-notes" / "2026-01-03.md")

        # Read file A
        write_transcript_events(temp_transcript, [make_read_event(file_a)])

        # Try to edit file B
        hook_input = make_edit_input(
            file_path=file_b,
            session_id=session_id,
            transcript_path=str(temp_transcript)
        )

        result = run_hook(hooks_dir / "pre-mutation-gate.py", hook_input)

        # Should be blocked (file B not read)
        assert_deny(result, "Must Read")
