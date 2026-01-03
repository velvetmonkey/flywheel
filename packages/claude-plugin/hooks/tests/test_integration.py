"""
Integration Tests: Cross-Gate Scenarios

Tests that verify multiple gates work together correctly.
Simulates realistic usage flows.
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


class TestIntegrationFlows:
    """Tests for realistic multi-gate flows."""

    def test_full_edit_flow_via_cache(self, hooks_dir, temp_vault, temp_transcript, session_id, gate1_cache_dir):
        """Full flow: Read caches file, Edit allowed."""
        file_path = str(temp_vault / "existing.md")

        # Step 1: Read (triggers read-cache.py)
        read_input = {
            "tool_name": "Read",
            "tool_input": {"file_path": file_path},
            "session_id": session_id
        }
        run_hook(hooks_dir / "read-cache.py", read_input)

        # Step 2: Edit (triggers pre-mutation-gate.py)
        write_transcript_events(temp_transcript, [])  # Empty transcript

        edit_input = make_edit_input(
            file_path=file_path,
            session_id=session_id,
            transcript_path=str(temp_transcript)
        )
        result = run_hook(hooks_dir / "pre-mutation-gate.py", edit_input)

        # Should pass Gates 1-3, get Gate 4 ask
        assert_ask(result, "GATE 4")

    def test_full_edit_flow_via_transcript(self, hooks_dir, temp_vault, temp_transcript, session_id, gate1_cache_dir):
        """Full flow: Read in transcript, Edit allowed."""
        file_path = str(temp_vault / "existing.md")

        # Write Read event to transcript (no cache)
        write_transcript_events(temp_transcript, [make_read_event(file_path)])

        edit_input = make_edit_input(
            file_path=file_path,
            session_id=session_id,
            transcript_path=str(temp_transcript)
        )
        result = run_hook(hooks_dir / "pre-mutation-gate.py", edit_input)

        assert_ask(result, "GATE 4")

    def test_context_summarization_scenario(self, hooks_dir, temp_vault, temp_transcript, session_id, gate1_cache_dir):
        """Read survives context summarization via cache."""
        file_path = str(temp_vault / "existing.md")

        # Step 1: Read (caches file)
        read_input = {
            "tool_name": "Read",
            "tool_input": {"file_path": file_path},
            "session_id": session_id
        }
        run_hook(hooks_dir / "read-cache.py", read_input)

        # Step 2: Simulate context summarization (empty transcript)
        write_transcript_events(temp_transcript, [])

        # Step 3: Edit (should pass via cache)
        edit_input = make_edit_input(
            file_path=file_path,
            session_id=session_id,
            transcript_path=str(temp_transcript)
        )
        result = run_hook(hooks_dir / "pre-mutation-gate.py", edit_input)

        # Gate 1 should pass (cache), proceed to Gate 4
        assert_ask(result)

    def test_edit_without_read_blocked(self, hooks_dir, temp_vault, temp_transcript, session_id, gate1_cache_dir):
        """Edit without Read should be blocked by Gate 1."""
        file_path = str(temp_vault / "existing.md")

        # No read cache, empty transcript
        write_transcript_events(temp_transcript, [])

        edit_input = make_edit_input(
            file_path=file_path,
            session_id=session_id,
            transcript_path=str(temp_transcript)
        )
        result = run_hook(hooks_dir / "pre-mutation-gate.py", edit_input)

        assert_deny(result, "Must Read")

    def test_edit_nonexistent_blocked_by_gate2(self, hooks_dir, temp_vault, temp_transcript, session_id, gate1_cache_dir):
        """Edit non-existent file blocked by Gate 2 (before Gate 1)."""
        nonexistent = str(temp_vault / "nonexistent.md")

        edit_input = make_edit_input(
            file_path=nonexistent,
            session_id=session_id,
            transcript_path=str(temp_transcript)
        )
        result = run_hook(hooks_dir / "pre-mutation-gate.py", edit_input)

        assert_deny(result, "does not exist")
        assert "GATE 2" in result["hookSpecificOutput"]["permissionDecisionReason"]

    def test_multiple_files_workflow(self, hooks_dir, temp_vault, temp_transcript, session_id, gate1_cache_dir):
        """Read and edit multiple files in sequence."""
        file1 = str(temp_vault / "existing.md")
        file2 = str(temp_vault / "daily-notes" / "2026-01-03.md")

        # Read both files
        run_hook(hooks_dir / "read-cache.py", {
            "tool_name": "Read",
            "tool_input": {"file_path": file1},
            "session_id": session_id
        })
        run_hook(hooks_dir / "read-cache.py", {
            "tool_name": "Read",
            "tool_input": {"file_path": file2},
            "session_id": session_id
        })

        write_transcript_events(temp_transcript, [])

        # Edit first file
        result1 = run_hook(hooks_dir / "pre-mutation-gate.py", make_edit_input(
            file_path=file1,
            session_id=session_id,
            transcript_path=str(temp_transcript)
        ))
        assert_ask(result1)

        # Edit second file
        result2 = run_hook(hooks_dir / "pre-mutation-gate.py", make_edit_input(
            file_path=file2,
            session_id=session_id,
            transcript_path=str(temp_transcript)
        ))
        assert_ask(result2)

    def test_mixed_transcript_and_cache(self, hooks_dir, temp_vault, temp_transcript, session_id, gate1_cache_dir):
        """Some files in transcript, some in cache only."""
        file1 = str(temp_vault / "existing.md")
        file2 = str(temp_vault / "daily-notes" / "2026-01-03.md")

        # File 1: in cache only
        run_hook(hooks_dir / "read-cache.py", {
            "tool_name": "Read",
            "tool_input": {"file_path": file1},
            "session_id": session_id
        })

        # File 2: in transcript only
        write_transcript_events(temp_transcript, [make_read_event(file2)])

        # Both should be editable
        result1 = run_hook(hooks_dir / "pre-mutation-gate.py", make_edit_input(
            file_path=file1,
            session_id=session_id,
            transcript_path=str(temp_transcript)
        ))
        assert_ask(result1)

        result2 = run_hook(hooks_dir / "pre-mutation-gate.py", make_edit_input(
            file_path=file2,
            session_id=session_id,
            transcript_path=str(temp_transcript)
        ))
        assert_ask(result2)


class TestGateOrdering:
    """Tests that verify gates execute in correct order."""

    def test_gate2_before_gate1_for_edit(self, hooks_dir, temp_vault, temp_transcript, session_id, gate1_cache_dir):
        """Gate 2 (file exists) should trigger before Gate 1 (read before write)."""
        nonexistent = str(temp_vault / "nonexistent.md")

        # Even if we "read" a non-existent file (put in cache), Gate 2 should block
        cache_path = gate1_cache_dir / "gate1-reads" / f"{session_id}.json"
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.write_text(json.dumps([str(Path(nonexistent).resolve())]))

        result = run_hook(hooks_dir / "pre-mutation-gate.py", make_edit_input(
            file_path=nonexistent,
            session_id=session_id,
            transcript_path=str(temp_transcript)
        ))

        # Should be blocked by Gate 2, not pass to Gate 1/4
        assert_deny(result, "does not exist")

    def test_gate4_after_gate1_for_valid_edit(self, hooks_dir, temp_vault, temp_transcript, session_id, gate1_cache_dir):
        """Gate 4 should trigger after Gate 1 passes."""
        file_path = str(temp_vault / "existing.md")

        # Pre-read to pass Gate 1
        run_hook(hooks_dir / "read-cache.py", {
            "tool_name": "Read",
            "tool_input": {"file_path": file_path},
            "session_id": session_id
        })

        write_transcript_events(temp_transcript, [])

        result = run_hook(hooks_dir / "pre-mutation-gate.py", make_edit_input(
            file_path=file_path,
            session_id=session_id,
            transcript_path=str(temp_transcript)
        ))

        # Should get Gate 4 prompt (not blocked by Gate 1)
        assert_ask(result, "GATE 4")


class TestSessionIsolation:
    """Tests that sessions are properly isolated."""

    def test_different_sessions_isolated(self, hooks_dir, temp_vault, temp_transcript, gate1_cache_dir):
        """Different sessions should have isolated caches."""
        file_path = str(temp_vault / "existing.md")
        session1 = "test-session-1"
        session2 = "test-session-2"

        # Read in session 1
        run_hook(hooks_dir / "read-cache.py", {
            "tool_name": "Read",
            "tool_input": {"file_path": file_path},
            "session_id": session1
        })

        write_transcript_events(temp_transcript, [])

        # Session 1 can edit
        result1 = run_hook(hooks_dir / "pre-mutation-gate.py", make_edit_input(
            file_path=file_path,
            session_id=session1,
            transcript_path=str(temp_transcript)
        ))
        assert_ask(result1)

        # Session 2 cannot edit (no read in that session)
        result2 = run_hook(hooks_dir / "pre-mutation-gate.py", make_edit_input(
            file_path=file_path,
            session_id=session2,
            transcript_path=str(temp_transcript)
        ))
        assert_deny(result2, "Must Read")
