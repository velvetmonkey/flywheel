#!/usr/bin/env python3
"""
Gate 3 Agent Validator - Runs at build/CI time.
Validates all agents in the plugin for Gate 3 compliance.

Usage:
    python packages/claude-plugin/scripts/validate-agents.py

Exit codes:
    0: All agents pass validation
    1: One or more agents fail validation
"""

import re
import sys
from pathlib import Path

# Configure UTF-8 output for Windows console
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

# Try to import yaml, but make it optional
try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


def is_multi_step_agent(content: str) -> bool:
    """Check if agent calls Task() - making it multi-step."""
    return bool(re.search(r'Task\s*\(', content))


def validate_gate3(file_path: Path, content: str) -> list:
    """Validate Gate 3 requirements for multi-step agents."""
    errors = []

    if not is_multi_step_agent(content):
        return []  # Single-step agents don't need Gate 3

    # REQUIRED sections for multi-step agents
    checks = {
        "Critical Rules section": "## Critical Rules" in content,
        "Sequential execution pattern": any(x in content.lower() for x in
            ["sequential", "wait for completion", "before calling next", "before proceeding"]),
        "Error handling section": "error" in content.lower() and
            any(x in content.lower() for x in ["handling", "continue", "fail"]),
        "Verification output (✓/✗)": ("✓" in content and "✗" in content) or
            ("completed" in content.lower() and "failed" in content.lower()),
        "Success tracking": any(x in content.lower() for x in
            ["track success", "note which", "report", "summary"]),
    }

    for check_name, passed in checks.items():
        if not passed:
            errors.append(f"Missing: {check_name}")

    return errors


def validate_frontmatter(file_path: Path, content: str) -> list:
    """Validate required YAML frontmatter."""
    errors = []

    if not content.startswith('---'):
        errors.append("Missing YAML frontmatter")
        return errors

    # Find end of frontmatter
    try:
        end = content.index('---', 3)
        frontmatter_text = content[3:end]
    except ValueError:
        errors.append("Unclosed YAML frontmatter (missing closing ---)")
        return errors

    # Parse frontmatter
    if HAS_YAML:
        try:
            frontmatter = yaml.safe_load(frontmatter_text)
            if frontmatter is None:
                frontmatter = {}
        except yaml.YAMLError as e:
            errors.append(f"Invalid YAML frontmatter: {e}")
            return errors
    else:
        # Basic check without yaml library
        frontmatter = {}
        for line in frontmatter_text.split('\n'):
            if ':' in line:
                key = line.split(':')[0].strip()
                frontmatter[key] = True

    required = ['name', 'description', 'allowed-tools', 'model']
    for field in required:
        if field not in frontmatter:
            errors.append(f"Missing frontmatter field: {field}")

    return errors


def main():
    # Find agents directory
    script_dir = Path(__file__).parent
    agents_dir = script_dir.parent / "agents"

    if not agents_dir.exists():
        print(f"Error: Agents directory not found: {agents_dir}")
        sys.exit(1)

    all_errors = {}
    agent_count = 0
    multi_step_count = 0

    for agent_file in agents_dir.rglob("*.md"):
        # Skip templates
        if '_templates' in str(agent_file):
            continue

        agent_count += 1
        content = agent_file.read_text(encoding='utf-8')
        errors = []

        # Validate frontmatter
        errors.extend(validate_frontmatter(agent_file, content))

        # Validate Gate 3
        gate3_errors = validate_gate3(agent_file, content)
        if gate3_errors:
            multi_step_count += 1
        errors.extend(gate3_errors)

        if errors:
            rel_path = str(agent_file.relative_to(agents_dir))
            all_errors[rel_path] = errors

    # Report results
    print(f"\nAgent Validation Report")
    print("=" * 60)
    print(f"Total agents checked: {agent_count}")
    print(f"Multi-step agents: {multi_step_count}")
    print(f"Agents with errors: {len(all_errors)}")

    if all_errors:
        print("\n❌ GATE 3 VALIDATION FAILED")
        print("-" * 60)

        for file, errors in sorted(all_errors.items()):
            print(f"\n{file}:")
            for error in errors:
                print(f"  ✗ {error}")

        print("\n" + "-" * 60)
        print("Fix these issues before committing.")
        print("See: packages/claude-plugin/skills/_patterns/SIX_GATES.md")
        print("=" * 60)
        sys.exit(1)
    else:
        print("\n✓ All agents pass validation")
        print("=" * 60)
        sys.exit(0)


if __name__ == "__main__":
    main()
