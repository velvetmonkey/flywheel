"""
Shared test utilities for Six Gates hook testing.

This module provides:
- run_hook(): Execute hooks as subprocess with JSON stdin/stdout
- write_transcript_events(): Create mock transcript files
- Helper functions for creating hook inputs
- Assertion helpers for checking hook decisions
"""

import json
import os
import subprocess
from pathlib import Path


def run_hook(hook_path: Path, hook_input: dict, timeout: int = 5, env: dict = None) -> dict:
    """
    Run a hook script with given input and return parsed output.

    Args:
        hook_path: Path to the Python hook script
        hook_input: Dictionary to pass as JSON on stdin
        timeout: Maximum seconds to wait
        env: Additional environment variables

    Returns:
        Parsed JSON output from the hook, or dict with exit_code/stderr on failure
    """
    # Build environment
    run_env = os.environ.copy()
    if env:
        run_env.update(env)

    # Try python3 first, fall back to python on Windows
    for python_cmd in ["python3", "python"]:
        try:
            result = subprocess.run(
                [python_cmd, str(hook_path)],
                input=json.dumps(hook_input),
                capture_output=True,
                text=True,
                timeout=timeout,
                env=run_env
            )
            break
        except FileNotFoundError:
            continue
    else:
        return {"exit_code": 1, "stderr": "Python not found"}

    if result.returncode != 0:
        return {"exit_code": result.returncode, "stderr": result.stderr}

    if result.stdout.strip():
        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError:
            return {"exit_code": 0, "stdout": result.stdout, "parse_error": True}
    return {}


def write_transcript_events(transcript_path: Path, events: list):
    """
    Write JSON lines transcript file.

    Args:
        transcript_path: Path to write the transcript
        events: List of event dictionaries to write as JSON lines
    """
    with open(transcript_path, "w", encoding="utf-8") as f:
        for event in events:
            f.write(json.dumps(event) + "\n")


def make_read_event(file_path: str) -> dict:
    """Create a Read tool_use event for transcripts."""
    return {
        "type": "tool_use",
        "name": "Read",
        "input": {"file_path": file_path}
    }


def make_edit_input(file_path: str, session_id: str, transcript_path: str = "") -> dict:
    """Create standard Edit hook input."""
    return {
        "tool_name": "Edit",
        "tool_input": {"file_path": file_path},
        "session_id": session_id,
        "transcript_path": transcript_path
    }


def make_write_input(file_path: str, content: str = "", session_id: str = "") -> dict:
    """Create standard Write hook input."""
    return {
        "tool_name": "Write",
        "tool_input": {"file_path": file_path, "content": content},
        "session_id": session_id
    }


def assert_deny(result: dict, reason_contains: str = None):
    """Assert that hook result is a deny decision."""
    assert "hookSpecificOutput" in result, f"Expected hookSpecificOutput, got: {result}"
    assert result["hookSpecificOutput"]["permissionDecision"] == "deny", \
        f"Expected deny, got: {result['hookSpecificOutput']}"
    if reason_contains:
        assert reason_contains in result["hookSpecificOutput"]["permissionDecisionReason"], \
            f"Expected '{reason_contains}' in reason: {result['hookSpecificOutput']['permissionDecisionReason']}"


def assert_ask(result: dict, reason_contains: str = None):
    """Assert that hook result is an ask decision."""
    assert "hookSpecificOutput" in result, f"Expected hookSpecificOutput, got: {result}"
    assert result["hookSpecificOutput"]["permissionDecision"] == "ask", \
        f"Expected ask, got: {result['hookSpecificOutput']}"
    if reason_contains:
        assert reason_contains in result["hookSpecificOutput"]["permissionDecisionReason"], \
            f"Expected '{reason_contains}' in reason: {result['hookSpecificOutput']['permissionDecisionReason']}"


def assert_allow_or_empty(result: dict):
    """Assert that hook result allows the operation (allow or empty output)."""
    if not result:
        return  # Empty output means allow
    if "hookSpecificOutput" in result:
        decision = result["hookSpecificOutput"].get("permissionDecision")
        assert decision in ["allow", None], f"Expected allow or none, got: {decision}"
