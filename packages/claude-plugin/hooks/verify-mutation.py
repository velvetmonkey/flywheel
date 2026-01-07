#!/usr/bin/env python3
"""
Post-Mutation Verification Hook
Part of the Six Gates Safety Framework (Gate 6: Post-Execution Validation).

Runs after Edit/Write operations to verify:
1. YAML frontmatter is valid (parseable)
2. Wikilinks are syntactically correct
3. File is still readable

This hook WARNS but does not auto-fix. It surfaces issues for user attention.

Exit codes:
- 0: Always exits 0 to not block operations
"""

import json
import sys
import re
from pathlib import Path

# Configure UTF-8 output for Windows console
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass


def validate_yaml_frontmatter(content: str) -> list:
    """
    Validate YAML frontmatter is parseable.
    Returns list of issues found.
    """
    issues = []

    # Check for frontmatter
    if not content.startswith('---'):
        return []  # No frontmatter, nothing to validate

    # Find end of frontmatter
    lines = content.split('\n')
    end_index = -1
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == '---':
            end_index = i
            break

    if end_index == -1:
        issues.append({
            'type': 'frontmatter_unclosed',
            'message': 'Frontmatter opened with --- but never closed',
            'severity': 'error'
        })
        return issues

    # Extract frontmatter content
    frontmatter_lines = lines[1:end_index]
    frontmatter_text = '\n'.join(frontmatter_lines)

    # Try to parse with PyYAML if available
    try:
        import yaml
        try:
            yaml.safe_load(frontmatter_text)
        except yaml.YAMLError as e:
            issues.append({
                'type': 'yaml_parse_error',
                'message': f'Invalid YAML: {str(e).split(chr(10))[0]}',
                'severity': 'error'
            })
    except ImportError:
        # No PyYAML, do basic validation
        for i, line in enumerate(frontmatter_lines, start=2):
            # Check for common YAML issues
            if line.strip() and not line.startswith(' ') and ':' not in line and not line.startswith('-'):
                issues.append({
                    'type': 'yaml_syntax',
                    'message': f'Line {i}: May be invalid YAML (no colon found)',
                    'severity': 'warning'
                })

    return issues


def validate_wikilinks(content: str) -> list:
    """
    Validate wikilink syntax is correct.
    Returns list of issues found.
    """
    issues = []

    # Find unclosed wikilinks
    # Pattern: [[ without matching ]]
    open_brackets = 0
    in_code_block = False
    in_inline_code = False

    lines = content.split('\n')
    for line_num, line in enumerate(lines, start=1):
        # Track code blocks
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            continue

        if in_code_block:
            continue

        # Check for wikilink issues in this line
        i = 0
        while i < len(line):
            # Track inline code
            if line[i] == '`':
                in_inline_code = not in_inline_code
                i += 1
                continue

            if in_inline_code:
                i += 1
                continue

            # Check for [[ opening
            if i < len(line) - 1 and line[i:i+2] == '[[':
                # Find closing ]]
                close_pos = line.find(']]', i + 2)
                if close_pos == -1:
                    # Check if it continues on next line (shouldn't for wikilinks)
                    issues.append({
                        'type': 'wikilink_unclosed',
                        'message': f'Line {line_num}: Wikilink opened [[ but not closed on same line',
                        'severity': 'error',
                        'line': line_num
                    })
                i += 2
            else:
                i += 1

    # Check for nested wikilinks (invalid)
    nested_pattern = r'\[\[.*\[\[.*\]\].*\]\]'
    for match in re.finditer(nested_pattern, content):
        issues.append({
            'type': 'wikilink_nested',
            'message': f'Nested wikilinks detected: {match.group()[:50]}...',
            'severity': 'error'
        })

    return issues


def main():
    try:
        # Read hook input from stdin
        hook_input = json.load(sys.stdin)

        # Only run on Edit/Write
        tool_name = hook_input.get('tool_name', '')
        if tool_name not in ['Edit', 'Write']:
            sys.exit(0)

        # Get the file path from tool input
        tool_input = hook_input.get('tool_input', {})
        file_path = tool_input.get('file_path', '')

        # Only check markdown files
        if not file_path.endswith('.md'):
            sys.exit(0)

        # Skip .claude directory
        if '.claude' in file_path:
            sys.exit(0)

        # Check if file exists
        path = Path(file_path)
        if not path.exists():
            print(f"\n⚠️  Post-Mutation Warning: File no longer exists: {file_path}", file=sys.stderr)
            sys.exit(0)

        # Read and validate
        try:
            content = path.read_text(encoding='utf-8')
        except Exception as e:
            print(f"\n⚠️  Post-Mutation Warning: Cannot read file after write: {e}", file=sys.stderr)
            sys.exit(0)

        all_issues = []

        # Validate YAML frontmatter
        yaml_issues = validate_yaml_frontmatter(content)
        all_issues.extend(yaml_issues)

        # Validate wikilinks
        wikilink_issues = validate_wikilinks(content)
        all_issues.extend(wikilink_issues)

        # Report issues
        if all_issues:
            errors = [i for i in all_issues if i['severity'] == 'error']
            warnings = [i for i in all_issues if i['severity'] == 'warning']

            print(f"\n⚠️  Post-Mutation Verification: {path.name}")
            print("-" * 60)

            if errors:
                print(f"ERRORS ({len(errors)}):")
                for issue in errors:
                    print(f"  ❌ {issue['message']}")

            if warnings:
                print(f"WARNINGS ({len(warnings)}):")
                for issue in warnings:
                    print(f"  ⚠️  {issue['message']}")

            print("-" * 60)
            print("Action: Review and fix the issues above.")
            print("")

        sys.exit(0)

    except json.JSONDecodeError:
        # No input or invalid JSON - skip silently
        sys.exit(0)
    except FileNotFoundError as e:
        print(f"[flywheel] Verify mutation: File not found - {e.filename}", file=sys.stderr)
        sys.exit(0)
    except PermissionError as e:
        print(f"[flywheel] Verify mutation: Permission denied - {e.filename}", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        print(f"[flywheel] Verify mutation error: {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(0)


if __name__ == '__main__':
    main()
