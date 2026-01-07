"""
Tests for Gate 5: MCP Health Check (session-gate.py)

Gate 5 checks MCP availability at session start:
- Verifies PROJECT_PATH is set
- Checks if vault path exists and is accessible
- Warns if no .md files found
- Suggests running health_check

This is a "soft" gate - it warns but doesn't block.
"""

import os
from pathlib import Path

import pytest

from .helpers import run_hook


class TestGate5HealthCheck:
    """Gate 5: MCP connection verification at session start."""

    def test_returns_ok_with_valid_vault(self, hooks_dir, temp_vault, monkeypatch):
        """Gate 5 should return OK status when PROJECT_PATH points to valid vault."""
        monkeypatch.setenv("PROJECT_PATH", str(temp_vault))

        hook_input = {"hook_event_name": "SessionStart"}
        result = run_hook(hooks_dir / "session-gate.py", hook_input)

        assert "hookSpecificOutput" in result
        context = result["hookSpecificOutput"].get("additionalContext", "")
        assert "OK" in context or "ok" in context.lower()
        assert str(temp_vault) in context or "Vault path" in context

    def test_warns_without_project_path(self, hooks_dir, monkeypatch):
        """Gate 5 should warn when PROJECT_PATH is not set."""
        monkeypatch.delenv("PROJECT_PATH", raising=False)

        hook_input = {"hook_event_name": "SessionStart"}
        result = run_hook(hooks_dir / "session-gate.py", hook_input)

        assert "hookSpecificOutput" in result
        context = result["hookSpecificOutput"].get("additionalContext", "")
        assert "WARNING" in context or "not set" in context.lower()

    def test_errors_when_path_does_not_exist(self, hooks_dir, tmp_path, monkeypatch):
        """Gate 5 should error when PROJECT_PATH doesn't exist."""
        fake_path = tmp_path / "nonexistent-vault"
        monkeypatch.setenv("PROJECT_PATH", str(fake_path))

        hook_input = {"hook_event_name": "SessionStart"}
        result = run_hook(hooks_dir / "session-gate.py", hook_input)

        assert "hookSpecificOutput" in result
        context = result["hookSpecificOutput"].get("additionalContext", "")
        assert "ERROR" in context or "does not exist" in context.lower()

    def test_errors_when_path_is_file(self, hooks_dir, tmp_path, monkeypatch):
        """Gate 5 should error when PROJECT_PATH is a file, not directory."""
        file_path = tmp_path / "file.txt"
        file_path.write_text("content")
        monkeypatch.setenv("PROJECT_PATH", str(file_path))

        hook_input = {"hook_event_name": "SessionStart"}
        result = run_hook(hooks_dir / "session-gate.py", hook_input)

        assert "hookSpecificOutput" in result
        context = result["hookSpecificOutput"].get("additionalContext", "")
        assert "ERROR" in context or "not a directory" in context.lower()

    def test_warns_when_no_markdown_files(self, hooks_dir, tmp_path, monkeypatch):
        """Gate 5 should warn when vault has no .md files."""
        empty_vault = tmp_path / "empty-vault"
        empty_vault.mkdir()
        (empty_vault / "readme.txt").write_text("Not a markdown file")
        monkeypatch.setenv("PROJECT_PATH", str(empty_vault))

        hook_input = {"hook_event_name": "SessionStart"}
        result = run_hook(hooks_dir / "session-gate.py", hook_input)

        assert "hookSpecificOutput" in result
        context = result["hookSpecificOutput"].get("additionalContext", "")
        assert "WARNING" in context or "No .md files" in context

    def test_suggests_health_check(self, hooks_dir, temp_vault, monkeypatch):
        """Gate 5 should suggest running health_check."""
        monkeypatch.setenv("PROJECT_PATH", str(temp_vault))

        hook_input = {"hook_event_name": "SessionStart"}
        result = run_hook(hooks_dir / "session-gate.py", hook_input)

        assert "hookSpecificOutput" in result
        context = result["hookSpecificOutput"].get("additionalContext", "")
        assert "health" in context.lower()

    def test_does_not_block(self, hooks_dir, monkeypatch):
        """Gate 5 is a soft gate - it should never block, only warn."""
        # Even with an invalid setup, should return context, not deny
        monkeypatch.delenv("PROJECT_PATH", raising=False)

        hook_input = {"hook_event_name": "SessionStart"}
        result = run_hook(hooks_dir / "session-gate.py", hook_input)

        # Should NOT have a deny decision
        if "hookSpecificOutput" in result:
            assert result["hookSpecificOutput"].get("permissionDecision") != "deny"

    def test_handles_invalid_input_gracefully(self, hooks_dir, temp_vault, monkeypatch):
        """Gate 5 should handle missing/invalid input gracefully."""
        monkeypatch.setenv("PROJECT_PATH", str(temp_vault))

        # Empty input
        result = run_hook(hooks_dir / "session-gate.py", {})

        # Should not crash, may return empty or valid response
        assert result.get("exit_code", 0) == 0 or "hookSpecificOutput" in result
