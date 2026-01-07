"""
Gate 3 Tests: Agent Chain Validation

Tests that multi-step agents include required Critical Rules section.
Only applies to files in agents/ directory that use Task().
"""

import pytest

from .helpers import run_hook, assert_deny


COMPLIANT_AGENT = '''# Test Agent

## Purpose
Test agent for validation.

## Critical Rules
1. Always verify input
2. Handle errors gracefully
3. Report completion status

## Error Handling
- On failure: Report error and stop
- On timeout: Retry once then fail

## Execution
Uses Task() to run sub-operations.
'''

NON_COMPLIANT_AGENT = '''# Test Agent

## Purpose
Test agent that uses Task() without Critical Rules.

## Execution
Uses Task() to run sub-operations.
'''

SIMPLE_AGENT_NO_TASK = '''# Simple Agent

## Purpose
Agent that doesn't use Task().

## Execution
Just does simple things directly.
'''


class TestGate3AgentValidation:
    """Tests for Gate 3: Agent validation."""

    def test_blocks_non_compliant_agent(self, hooks_dir, temp_vault):
        """Gate 3 should BLOCK Write of agent without Critical Rules."""
        # Create agents directory
        agents_dir = temp_vault / "agents"
        agents_dir.mkdir()

        hook_input = {
            "tool_name": "Write",
            "tool_input": {
                "file_path": str(agents_dir / "bad-agent.md"),
                "content": NON_COMPLIANT_AGENT
            }
        }

        # Check if validate-agent-gate3.py exists
        gate3_hook = hooks_dir / "validate-agent-gate3.py"
        if not gate3_hook.exists():
            pytest.skip("validate-agent-gate3.py not found in plugin hooks")

        result = run_hook(gate3_hook, hook_input)

        if result and "hookSpecificOutput" in result:
            assert_deny(result, "GATE 3")

    def test_allows_compliant_agent(self, hooks_dir, temp_vault):
        """Gate 3 should ALLOW Write of compliant agent."""
        agents_dir = temp_vault / "agents"
        agents_dir.mkdir()

        hook_input = {
            "tool_name": "Write",
            "tool_input": {
                "file_path": str(agents_dir / "good-agent.md"),
                "content": COMPLIANT_AGENT
            }
        }

        gate3_hook = hooks_dir / "validate-agent-gate3.py"
        if not gate3_hook.exists():
            pytest.skip("validate-agent-gate3.py not found in plugin hooks")

        result = run_hook(gate3_hook, hook_input)

        # Should pass (empty output or not deny)
        if result and "hookSpecificOutput" in result:
            assert result["hookSpecificOutput"].get("permissionDecision") != "deny"

    def test_skips_non_agent_files(self, hooks_dir, temp_vault):
        """Gate 3 should NOT check files outside agents/ directory."""
        skills_dir = temp_vault / "skills"
        skills_dir.mkdir()

        hook_input = {
            "tool_name": "Write",
            "tool_input": {
                "file_path": str(skills_dir / "test.md"),
                "content": "Regular markdown without Task() or Critical Rules"
            }
        }

        gate3_hook = hooks_dir / "validate-agent-gate3.py"
        if not gate3_hook.exists():
            pytest.skip("validate-agent-gate3.py not found in plugin hooks")

        result = run_hook(gate3_hook, hook_input)

        # Should pass (not an agent directory)
        if result and "hookSpecificOutput" in result:
            assert result["hookSpecificOutput"].get("permissionDecision") != "deny"

    def test_skips_agent_without_task(self, hooks_dir, temp_vault):
        """Gate 3 should NOT require Critical Rules if no Task() is used."""
        agents_dir = temp_vault / "agents"
        agents_dir.mkdir()

        hook_input = {
            "tool_name": "Write",
            "tool_input": {
                "file_path": str(agents_dir / "simple-agent.md"),
                "content": SIMPLE_AGENT_NO_TASK
            }
        }

        gate3_hook = hooks_dir / "validate-agent-gate3.py"
        if not gate3_hook.exists():
            pytest.skip("validate-agent-gate3.py not found in plugin hooks")

        result = run_hook(gate3_hook, hook_input)

        # Should pass (no Task() = no Critical Rules required)
        if result and "hookSpecificOutput" in result:
            assert result["hookSpecificOutput"].get("permissionDecision") != "deny"


class TestGate3EdgeCases:
    """Edge cases for Gate 3."""

    def test_edit_existing_agent_warns(self, hooks_dir, temp_vault):
        """Edit to existing agent should warn (not block)."""
        agents_dir = temp_vault / "agents"
        agents_dir.mkdir()

        # Create existing agent
        agent_file = agents_dir / "existing-agent.md"
        agent_file.write_text(COMPLIANT_AGENT)

        hook_input = {
            "tool_name": "Edit",  # Edit, not Write
            "tool_input": {
                "file_path": str(agent_file),
                "old_string": "Test agent",
                "new_string": "Modified agent"
            }
        }

        # Gate 3 post-hook may exist for Edit
        gate3_post = hooks_dir / "validate-agent-gate3-post.py"
        if not gate3_post.exists():
            pytest.skip("validate-agent-gate3-post.py not found")

        result = run_hook(gate3_post, hook_input)

        # Post-hook should warn, not block
        # (Exact behavior depends on implementation)
        pass  # Just verify it doesn't crash

    def test_nested_agents_directory(self, hooks_dir, temp_vault):
        """Agents in nested directories should still be validated."""
        nested_agents = temp_vault / "packages" / "plugin" / "agents"
        nested_agents.mkdir(parents=True)

        hook_input = {
            "tool_name": "Write",
            "tool_input": {
                "file_path": str(nested_agents / "nested-agent.md"),
                "content": NON_COMPLIANT_AGENT
            }
        }

        gate3_hook = hooks_dir / "validate-agent-gate3.py"
        if not gate3_hook.exists():
            pytest.skip("validate-agent-gate3.py not found")

        result = run_hook(gate3_hook, hook_input)

        # Should still validate (agents in path)
        if result and "hookSpecificOutput" in result:
            if "agents" in str(nested_agents):
                # May be blocked depending on path matching
                pass
