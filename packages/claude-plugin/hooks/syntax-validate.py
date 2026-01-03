#!/usr/bin/env python3
"""
Obsidian Syntax Validator and Auto-Fixer Hook

Runs after Edit/Write operations to detect and fix syntax issues that break Obsidian.
Fixes:
1. Angle brackets outside code blocks (breaks wikilinks) → converts to parentheses
2. Wrapped wikilinks like **[[Link]]** → unwraps to [[Link]]

Exit codes:
- 0: No issues found, or issues fixed successfully
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


def protect_code_blocks(content: str) -> tuple[str, list]:
    """Extract and protect code blocks, return (content_with_placeholders, code_blocks)."""
    code_blocks = []

    # Protect fenced code blocks
    def save_fenced(match):
        code_blocks.append(('fenced', match.group(0)))
        return f'___CODE_BLOCK_{len(code_blocks)-1}___'

    content = re.sub(r'```[\s\S]*?```', save_fenced, content)

    # Protect inline code
    def save_inline(match):
        code_blocks.append(('inline', match.group(0)))
        return f'___INLINE_CODE_{len(code_blocks)-1}___'

    content = re.sub(r'`[^`]+`', save_inline, content)

    return content, code_blocks


def restore_code_blocks(content: str, code_blocks: list) -> str:
    """Restore protected code blocks."""
    for i, (block_type, block_content) in enumerate(code_blocks):
        if block_type == 'fenced':
            content = content.replace(f'___CODE_BLOCK_{i}___', block_content)
        elif block_type == 'inline':
            content = content.replace(f'___INLINE_CODE_{i}___', block_content)
    return content


def fix_angle_brackets(content: str) -> tuple[str, list]:
    """Fix angle brackets by converting them to parentheses."""
    fixes = []

    # Find and fix angle brackets
    angle_pattern = r'<([^>]+)>'

    def replace_angle(match):
        original = match.group(0)
        inner = match.group(1)
        replacement = f'({inner})'
        fixes.append({
            'type': 'angle_bracket',
            'original': original,
            'fixed': replacement
        })
        return replacement

    fixed_content = re.sub(angle_pattern, replace_angle, content)
    return fixed_content, fixes


def fix_wrapped_wikilinks(content: str) -> tuple[str, list]:
    """Fix wrapped wikilinks by removing the wrapping."""
    fixes = []

    patterns = [
        (r'\*\*(\[\[[^\]]+\]\])\*\*', 'bold'),      # **[[Link]]** → [[Link]]
        (r'\*(\[\[[^\]]+\]\])\*', 'italic'),         # *[[Link]]* → [[Link]]
        (r'_(\[\[[^\]]+\]\])_', 'underscore'),       # _[[Link]]_ → [[Link]]
        (r'__(\[\[[^\]]+\]\])__', 'double_under'),   # __[[Link]]__ → [[Link]]
    ]

    for pattern, wrap_type in patterns:
        def replace_wrapped(match):
            original = match.group(0)
            wikilink = match.group(1)
            fixes.append({
                'type': 'wrapped_wikilink',
                'wrap_type': wrap_type,
                'original': original,
                'fixed': wikilink
            })
            return wikilink

        content = re.sub(pattern, replace_wrapped, content)

    return content, fixes


def main():
    try:
        # Read hook input from stdin
        hook_input = json.load(sys.stdin)

        # CRITICAL: Only run auto-fixes on Edit/Write, not Read
        tool_name = hook_input.get('tool_name', '')
        if tool_name not in ['Edit', 'Write']:
            sys.exit(0)

        # Get the file path from tool input
        tool_input = hook_input.get('tool_input', {})
        file_path = tool_input.get('file_path', '')

        # Only check markdown files
        if not file_path.endswith('.md'):
            sys.exit(0)

        # Check if file exists
        path = Path(file_path)
        if not path.exists():
            sys.exit(0)

        # Read file content
        content = path.read_text(encoding='utf-8')
        original_content = content

        # Protect code blocks from modification
        content, code_blocks = protect_code_blocks(content)

        # Fix issues
        all_fixes = []

        # Fix angle brackets
        content, angle_fixes = fix_angle_brackets(content)
        all_fixes.extend(angle_fixes)

        # Fix wrapped wikilinks
        content, wikilink_fixes = fix_wrapped_wikilinks(content)
        all_fixes.extend(wikilink_fixes)

        # Restore code blocks
        content = restore_code_blocks(content, code_blocks)

        # If fixes were made, write back to file and report
        if all_fixes and content != original_content:
            path.write_text(content, encoding='utf-8')

            print(f"\n✓ Auto-Fixed Obsidian Syntax Issues in {path.name}:")
            print("-" * 60)

            # Group fixes by type
            angle_bracket_fixes = [f for f in all_fixes if f['type'] == 'angle_bracket']
            wikilink_fixes = [f for f in all_fixes if f['type'] == 'wrapped_wikilink']

            if angle_bracket_fixes:
                print(f"Angle Brackets ({len(angle_bracket_fixes)} fixed):")
                for fix in angle_bracket_fixes[:5]:  # Show max 5
                    print(f"  {fix['original']} → {fix['fixed']}")
                if len(angle_bracket_fixes) > 5:
                    print(f"  ... and {len(angle_bracket_fixes) - 5} more")

            if wikilink_fixes:
                print(f"\nWrapped Wikilinks ({len(wikilink_fixes)} fixed):")
                for fix in wikilink_fixes[:5]:  # Show max 5
                    print(f"  {fix['original']} → {fix['fixed']}")
                if len(wikilink_fixes) > 5:
                    print(f"  ... and {len(wikilink_fixes) - 5} more")

            print("-" * 60)
            print("")

        sys.exit(0)

    except json.JSONDecodeError:
        # No input or invalid JSON - skip silently
        sys.exit(0)
    except FileNotFoundError as e:
        print(f"[flywheel] Syntax validator: File not found - {e.filename}", file=sys.stderr)
        sys.exit(0)
    except PermissionError as e:
        print(f"[flywheel] Syntax validator: Permission denied - {e.filename}", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        print(f"[flywheel] Syntax validator error: {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(0)


if __name__ == '__main__':
    main()
