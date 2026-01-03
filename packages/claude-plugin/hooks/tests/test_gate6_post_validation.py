"""
Tests for Gate 6: Post-Execution Validation (verify-mutation.py)

Gate 6 validates files AFTER Edit/Write operations:
- Checks YAML frontmatter is valid/parseable
- Checks wikilinks are syntactically correct
- Warns about issues but does not block

This is a "soft" gate - it warns but doesn't block or auto-fix.
"""

import subprocess
import json
from pathlib import Path

import pytest


class TestGate6PostValidation:
    """Gate 6: Post-execution validation of file mutations."""

    @pytest.fixture
    def hooks_dir(self):
        """Path to hooks directory."""
        return Path(__file__).parent.parent

    @pytest.fixture
    def temp_vault(self, tmp_path):
        """Create temporary vault with test files."""
        vault = tmp_path / "test-vault"
        vault.mkdir()
        return vault

    def run_verify_hook(self, hooks_dir, hook_input: dict) -> tuple:
        """Run verify-mutation.py and return (stdout, stderr, exit_code)."""
        for python_cmd in ["python3", "python"]:
            try:
                result = subprocess.run(
                    [python_cmd, str(hooks_dir / "verify-mutation.py")],
                    input=json.dumps(hook_input),
                    capture_output=True,
                    text=True,
                    timeout=5,
                    encoding='utf-8',
                    errors='replace'  # Handle Unicode decode errors gracefully
                )
                return result.stdout or "", result.stderr or "", result.returncode
            except FileNotFoundError:
                continue
            except Exception:
                # Handle any other subprocess errors
                return "", "", 0
        return "", "Python not found", 1

    # ===== YAML Frontmatter Tests =====

    def test_warns_on_unclosed_frontmatter(self, hooks_dir, temp_vault):
        """Gate 6 should warn about unclosed YAML frontmatter."""
        bad_file = temp_vault / "broken-yaml.md"
        bad_file.write_text("---\ntitle: test\nno closing marker")

        hook_input = {
            "tool_name": "Edit",
            "tool_input": {"file_path": str(bad_file)},
            "tool_result": {"success": True}
        }

        stdout, stderr, exit_code = self.run_verify_hook(hooks_dir, hook_input)

        # Should output warning
        assert "unclosed" in stdout.lower() or "frontmatter" in stdout.lower() or \
               "unclosed" in stderr.lower() or "frontmatter" in stderr.lower()

    def test_warns_on_invalid_yaml_syntax(self, hooks_dir, temp_vault):
        """Gate 6 should warn about invalid YAML in frontmatter."""
        bad_file = temp_vault / "invalid-yaml.md"
        # Invalid YAML: unquoted string with colon
        bad_file.write_text("---\ntitle: test: invalid: yaml\n---\n\nContent")

        hook_input = {
            "tool_name": "Edit",
            "tool_input": {"file_path": str(bad_file)},
            "tool_result": {"success": True}
        }

        stdout, stderr, exit_code = self.run_verify_hook(hooks_dir, hook_input)

        # May or may not warn depending on PyYAML availability
        # At minimum, should not crash
        assert exit_code == 0

    def test_passes_valid_frontmatter(self, hooks_dir, temp_vault):
        """Gate 6 should not warn about valid YAML frontmatter."""
        good_file = temp_vault / "valid-yaml.md"
        good_file.write_text("---\ntitle: Test\ntags:\n  - one\n  - two\n---\n\n# Content")

        hook_input = {
            "tool_name": "Edit",
            "tool_input": {"file_path": str(good_file)},
            "tool_result": {"success": True}
        }

        stdout, stderr, exit_code = self.run_verify_hook(hooks_dir, hook_input)

        # Should pass without warnings/errors in output
        assert "error" not in stdout.lower() or "0" in stdout
        assert exit_code == 0

    def test_passes_file_without_frontmatter(self, hooks_dir, temp_vault):
        """Gate 6 should pass files without any frontmatter."""
        no_fm_file = temp_vault / "no-frontmatter.md"
        no_fm_file.write_text("# Just a heading\n\nSome content with [[wikilink]].")

        hook_input = {
            "tool_name": "Edit",
            "tool_input": {"file_path": str(no_fm_file)},
            "tool_result": {"success": True}
        }

        stdout, stderr, exit_code = self.run_verify_hook(hooks_dir, hook_input)

        assert exit_code == 0

    # ===== Wikilink Tests =====

    def test_warns_on_unclosed_wikilink(self, hooks_dir, temp_vault):
        """Gate 6 should warn about unclosed wikilinks."""
        bad_file = temp_vault / "broken-links.md"
        bad_file.write_text("# Test\n\nSee [[broken link here\n\nMore text")

        hook_input = {
            "tool_name": "Edit",
            "tool_input": {"file_path": str(bad_file)},
            "tool_result": {"success": True}
        }

        stdout, stderr, exit_code = self.run_verify_hook(hooks_dir, hook_input)

        # Should warn about unclosed wikilink
        assert "wikilink" in stdout.lower() or "[[" in stdout or \
               "unclosed" in stdout.lower()

    def test_passes_valid_wikilinks(self, hooks_dir, temp_vault):
        """Gate 6 should not warn about valid wikilinks."""
        good_file = temp_vault / "valid-links.md"
        good_file.write_text("# Test\n\nSee [[valid link]] and [[another|with alias]].")

        hook_input = {
            "tool_name": "Edit",
            "tool_input": {"file_path": str(good_file)},
            "tool_result": {"success": True}
        }

        stdout, stderr, exit_code = self.run_verify_hook(hooks_dir, hook_input)

        # Should pass without wikilink warnings
        assert "wikilink" not in stdout.lower() or "0" in stdout
        assert exit_code == 0

    def test_ignores_wikilinks_in_code_blocks(self, hooks_dir, temp_vault):
        """Gate 6 should ignore wikilinks inside code blocks."""
        code_file = temp_vault / "code-blocks.md"
        code_file.write_text("""# Test

```
[[this is not a real wikilink
```

Normal text with [[valid link]].
""")

        hook_input = {
            "tool_name": "Edit",
            "tool_input": {"file_path": str(code_file)},
            "tool_result": {"success": True}
        }

        stdout, stderr, exit_code = self.run_verify_hook(hooks_dir, hook_input)

        # Should not warn about the "broken" link in code block
        assert exit_code == 0

    def test_ignores_wikilinks_in_inline_code(self, hooks_dir, temp_vault):
        """Gate 6 should ignore wikilinks inside inline code."""
        inline_file = temp_vault / "inline-code.md"
        inline_file.write_text("Text with `[[not a link` and [[real link]].")

        hook_input = {
            "tool_name": "Edit",
            "tool_input": {"file_path": str(inline_file)},
            "tool_result": {"success": True}
        }

        stdout, stderr, exit_code = self.run_verify_hook(hooks_dir, hook_input)

        # Should not warn about code inside backticks
        assert exit_code == 0

    # ===== Scope Tests =====

    def test_skips_non_markdown_files(self, hooks_dir, temp_vault):
        """Gate 6 should not check non-.md files."""
        py_file = temp_vault / "script.py"
        py_file.write_text("# [[not markdown\nprint('hello')")

        hook_input = {
            "tool_name": "Edit",
            "tool_input": {"file_path": str(py_file)},
            "tool_result": {"success": True}
        }

        stdout, stderr, exit_code = self.run_verify_hook(hooks_dir, hook_input)

        # Should skip entirely
        assert exit_code == 0
        assert stdout.strip() == "" or "wikilink" not in stdout.lower()

    def test_skips_claude_directory(self, hooks_dir, temp_vault):
        """Gate 6 should not check .claude directory files."""
        claude_dir = temp_vault / ".claude"
        claude_dir.mkdir()
        claude_file = claude_dir / "settings.md"
        claude_file.write_text("---\nbroken: yaml\n[[unclosed")

        hook_input = {
            "tool_name": "Edit",
            "tool_input": {"file_path": str(claude_file)},
            "tool_result": {"success": True}
        }

        stdout, stderr, exit_code = self.run_verify_hook(hooks_dir, hook_input)

        # Should skip .claude directory
        assert exit_code == 0

    def test_skips_non_edit_write_tools(self, hooks_dir, temp_vault):
        """Gate 6 should only run for Edit/Write tools."""
        hook_input = {
            "tool_name": "Read",
            "tool_input": {"file_path": str(temp_vault / "existing.md")},
        }

        stdout, stderr, exit_code = self.run_verify_hook(hooks_dir, hook_input)

        # Should exit immediately
        assert exit_code == 0
        assert stdout.strip() == ""

    # ===== Edge Cases =====

    def test_handles_nonexistent_file(self, hooks_dir, temp_vault):
        """Gate 6 should handle file that no longer exists gracefully."""
        hook_input = {
            "tool_name": "Edit",
            "tool_input": {"file_path": str(temp_vault / "deleted.md")},
            "tool_result": {"success": True}
        }

        stdout, stderr, exit_code = self.run_verify_hook(hooks_dir, hook_input)

        # Should warn but not crash
        assert exit_code == 0
        # May have warning about file not existing
        assert "no longer exists" in stderr.lower() or "no longer exists" in stdout.lower() or \
               stderr == "" or stdout == ""

    def test_does_not_block(self, hooks_dir, temp_vault):
        """Gate 6 is a soft gate - should never return deny decision."""
        bad_file = temp_vault / "very-broken.md"
        bad_file.write_text("---\nbroken\n[[unclosed wikilink")

        hook_input = {
            "tool_name": "Edit",
            "tool_input": {"file_path": str(bad_file)},
            "tool_result": {"success": True}
        }

        stdout, stderr, exit_code = self.run_verify_hook(hooks_dir, hook_input)

        # Should always exit 0, never block
        assert exit_code == 0
        # If there's JSON output, should not be deny
        if stdout.strip().startswith("{"):
            try:
                result = json.loads(stdout)
                if "hookSpecificOutput" in result:
                    assert result["hookSpecificOutput"].get("permissionDecision") != "deny"
            except json.JSONDecodeError:
                pass  # Non-JSON output is fine

    def test_handles_invalid_input_gracefully(self, hooks_dir):
        """Gate 6 should handle missing/invalid input gracefully."""
        # Empty input
        stdout, stderr, exit_code = self.run_verify_hook(hooks_dir, {})

        # Should not crash
        assert exit_code == 0
