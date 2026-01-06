#!/usr/bin/env python3
"""
Gate 6 Skill Validator - Runs at build/CI time.
Validates all skills in the plugin for Gate 6 compliance.

Mutation skills (those using Edit or Write tools) MUST include:
1. A verification step that re-reads the file after mutation
2. Error handling for blocked/failed Edit/Write operations
3. Distinct output for success vs failure (only confirm if verified)

Usage:
    python packages/claude-plugin/scripts/validate-skills.py

Exit codes:
    0: All skills pass validation
    1: One or more skills fail validation
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


def is_mutation_skill(content: str) -> bool:
    """Check if skill uses Edit or Write tools.

    Checks allowed-tools frontmatter for Edit or Write tools.
    This is more precise than searching the whole content, which catches
    false positives like "Write architecture document" in example output.

    Note: TodoWrite is NOT a mutation tool (it's for task tracking),
    so we check for exact tool names, not substrings.
    """
    # Extract allowed-tools from frontmatter
    if not content.startswith('---'):
        return False

    try:
        end = content.index('---', 3)
        frontmatter = content[3:end]
    except ValueError:
        return False

    # Look for allowed-tools line
    for line in frontmatter.split('\n'):
        if line.strip().startswith('allowed-tools:'):
            tools_value = line.split(':', 1)[1].strip()
            # Split by comma and check for exact Edit or Write tool names
            tools = [t.strip() for t in tools_value.split(',')]
            for tool in tools:
                # Check for exact Edit or Write (not TodoWrite, NotebookEdit, etc.)
                if tool == 'Edit' or tool == 'Write':
                    return True
            return False

    return False


def validate_gate6(file_path: Path, content: str) -> list:
    """Validate Gate 6 requirements for mutation skills.

    Returns list of missing requirements. Empty list means compliant.
    """
    errors = []

    if not is_mutation_skill(content):
        return []  # Read-only skills don't need Gate 6

    content_lower = content.lower()

    # REQUIRED sections for mutation skills
    checks = {
        "Verification step (re-read after write)": any(x in content_lower for x in
            ["verify", "re-read", "reread", "confirm written", "check result",
             "verification", "read the file", "read back"]),
        "Error handling for blocked/failed mutation": any(x in content_lower for x in
            ["if failed", "if blocked", "edit fails", "write fails",
             "blocked or failed", "failed or blocked", "if edit", "if write"]),
        "Success/failure output distinction": any(x in content_lower for x in
            ["if found", "if not found", "if succeeded", "if failed",
             "only if step", "only if verification", "proceed to confirm"]),
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

    # Required fields for skills
    required = ['name', 'description']
    for field in required:
        if field not in frontmatter:
            errors.append(f"Missing frontmatter field: {field}")

    return errors


def main():
    # Find skills directory
    script_dir = Path(__file__).parent
    skills_dir = script_dir.parent / "skills"

    if not skills_dir.exists():
        print(f"Error: Skills directory not found: {skills_dir}")
        sys.exit(1)

    all_errors = {}
    skill_count = 0
    mutation_skill_count = 0

    for skill_file in skills_dir.rglob("SKILL.md"):
        # Skip patterns and templates
        if '_patterns' in str(skill_file) or '_templates' in str(skill_file):
            continue

        skill_count += 1
        content = skill_file.read_text(encoding='utf-8')
        errors = []

        # Validate frontmatter
        errors.extend(validate_frontmatter(skill_file, content))

        # Validate Gate 6 (only counts as mutation skill if it uses Edit/Write)
        if is_mutation_skill(content):
            mutation_skill_count += 1
            gate6_errors = validate_gate6(skill_file, content)
            errors.extend(gate6_errors)

        if errors:
            # Get relative path from skills directory
            rel_path = str(skill_file.relative_to(skills_dir))
            all_errors[rel_path] = errors

    # Report results
    print(f"\nSkill Validation Report")
    print("=" * 60)
    print(f"Total skills checked: {skill_count}")
    print(f"Mutation skills (Edit/Write): {mutation_skill_count}")
    print(f"Skills with errors: {len(all_errors)}")

    if all_errors:
        print(f"\n{'=' * 60}")
        print("GATE 6 VALIDATION FAILED")
        print("-" * 60)

        for file, errors in sorted(all_errors.items()):
            print(f"\n{file}:")
            for error in errors:
                print(f"  - {error}")

        print("\n" + "-" * 60)
        print("Fix these issues before committing.")
        print("See: packages/claude-plugin/skills/_patterns/SIX_GATES.md")
        print("=" * 60)
        sys.exit(1)
    else:
        print(f"\nAll skills pass validation")
        print("=" * 60)
        sys.exit(0)


if __name__ == "__main__":
    main()
