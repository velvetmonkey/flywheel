#!/usr/bin/env python3
"""
Frontmatter Auto-Complete Hook (frontmatter-auto.py)

Runs after Edit/Write operations to AUTO-ADD missing frontmatter fields
based on folder conventions. This hook MODIFIES files.

Logic:
1. Scan all notes in the same folder as the edited file
2. Find fields present in >90% of notes with enumerable values
3. If the edited file is missing those fields, auto-add them

Safety:
- Only auto-add fields with >90% frequency AND enumerable values
- Never guess free-text fields
- Skip periodic note folders (daily-notes, weekly-notes, etc.)
- Skip protected folders (.obsidian, .git, .claude)

Exit codes:
- 0: Always (informational only, never blocks)
"""

import json
import sys
import re
from pathlib import Path
from collections import defaultdict
from typing import Any

# Configure UTF-8 output for Windows console
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

# Add parent directory to path for config import
sys.path.insert(0, str(Path(__file__).parent.parent))
from config.loader import load_config, find_vault_root, get_periodic_folders

# Minimum frequency to consider a field "expected" (90%)
MIN_FREQUENCY = 0.9

# Maximum unique values to consider enumerable
MAX_ENUM_VALUES = 20

# Fields to never auto-add (computed or special)
SKIP_FIELDS = {
    'created', 'modified', 'word_count', 'reading_time',
    'aliases', 'tags', 'cssclass', 'cssclasses', 'publish'
}


def parse_frontmatter(content: str) -> tuple[dict, str, int]:
    """
    Parse YAML frontmatter from markdown content.

    Returns:
        (frontmatter_dict, body, frontmatter_end_pos)
    """
    if not content.startswith('---'):
        return {}, content, 0

    # Find closing ---
    lines = content.split('\n')
    end_idx = -1
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == '---':
            end_idx = i
            break

    if end_idx == -1:
        return {}, content, 0

    # Parse YAML manually (simple key: value pairs)
    frontmatter = {}
    for line in lines[1:end_idx]:
        if ':' in line:
            key, _, value = line.partition(':')
            key = key.strip()
            value = value.strip()

            # Handle quoted strings
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            elif value.startswith("'") and value.endswith("'"):
                value = value[1:-1]
            # Handle arrays (basic)
            elif value.startswith('['):
                try:
                    value = json.loads(value)
                except json.JSONDecodeError:
                    pass
            # Handle booleans
            elif value.lower() in ('true', 'false'):
                value = value.lower() == 'true'
            # Handle numbers
            elif value.isdigit():
                value = int(value)
            elif value.replace('.', '').isdigit():
                value = float(value)

            if key:
                frontmatter[key] = value

    # Calculate end position
    end_pos = sum(len(l) + 1 for l in lines[:end_idx + 1])
    body = '\n'.join(lines[end_idx + 1:])

    return frontmatter, body, end_pos


def add_frontmatter_fields(content: str, new_fields: dict) -> str:
    """
    Add new fields to existing frontmatter or create frontmatter.

    Returns updated content.
    """
    if not new_fields:
        return content

    existing, body, _ = parse_frontmatter(content)

    # Merge new fields (don't override existing)
    merged = {**new_fields, **existing}

    # Build new frontmatter
    lines = ['---']
    for key, value in merged.items():
        if isinstance(value, bool):
            lines.append(f'{key}: {str(value).lower()}')
        elif isinstance(value, (int, float)):
            lines.append(f'{key}: {value}')
        elif isinstance(value, list):
            lines.append(f'{key}: {json.dumps(value)}')
        elif isinstance(value, str) and (':' in value or '\n' in value):
            lines.append(f'{key}: "{value}"')
        else:
            lines.append(f'{key}: {value}')
    lines.append('---')

    return '\n'.join(lines) + '\n' + body.lstrip('\n')


def scan_folder_conventions(folder_path: Path, exclude_file: Path = None) -> dict:
    """
    Scan all markdown files in folder to infer conventions.

    Returns dict of field_name -> {frequency, common_values}
    """
    field_stats = defaultdict(lambda: {'count': 0, 'values': defaultdict(int)})
    total_notes = 0

    for md_file in folder_path.glob('*.md'):
        if md_file == exclude_file:
            continue

        try:
            content = md_file.read_text(encoding='utf-8')
            frontmatter, _, _ = parse_frontmatter(content)

            if frontmatter:
                total_notes += 1
                for key, value in frontmatter.items():
                    if key.lower() not in SKIP_FIELDS:
                        field_stats[key]['count'] += 1
                        # Track values (convert to string for counting)
                        value_str = json.dumps(value) if not isinstance(value, str) else value
                        field_stats[key]['values'][value_str] += 1
        except Exception:
            continue

    if total_notes < 3:
        # Not enough notes to infer conventions
        return {}

    # Calculate frequency and filter
    conventions = {}
    for field, stats in field_stats.items():
        frequency = stats['count'] / total_notes
        unique_values = len(stats['values'])

        # Only include high-frequency enumerable fields
        if frequency >= MIN_FREQUENCY and unique_values <= MAX_ENUM_VALUES:
            # Get most common value
            most_common = max(stats['values'].items(), key=lambda x: x[1])

            conventions[field] = {
                'frequency': frequency,
                'common_value': most_common[0],  # Still a string
                'unique_count': unique_values
            }

    return conventions


def get_vault_path_from_env() -> Path | None:
    """Get the vault path from PROJECT_PATH environment variable."""
    import os
    project_path = os.environ.get('PROJECT_PATH', '')
    if project_path:
        return Path(project_path).resolve()
    return None


def is_within_vault(file_path: Path, vault_path: Path) -> bool:
    """Check if a file is within the vault directory."""
    try:
        file_resolved = file_path.resolve()
        vault_resolved = vault_path.resolve()
        try:
            return file_resolved.is_relative_to(vault_resolved)
        except AttributeError:
            try:
                file_resolved.relative_to(vault_resolved)
                return True
            except ValueError:
                return False
    except Exception:
        return False


def main():
    try:
        # Read hook input from stdin
        hook_input = json.load(sys.stdin)

        # Only run on Edit/Write operations
        tool_name = hook_input.get('tool_name', '')
        if tool_name not in ['Edit', 'Write']:
            sys.exit(0)

        # Get the file path from tool input
        tool_input = hook_input.get('tool_input', {})
        file_path = tool_input.get('file_path', '')

        # Only check markdown files
        if not file_path.endswith('.md'):
            sys.exit(0)

        path = Path(file_path)
        if not path.exists():
            sys.exit(0)

        # Check vault boundary
        env_vault_path = get_vault_path_from_env()
        if env_vault_path and not is_within_vault(path, env_vault_path):
            sys.exit(0)

        # Skip dot folders
        path_parts = path.parts
        if any(part.startswith('.') and len(part) > 1 for part in path_parts):
            sys.exit(0)

        # Get vault root
        vault_path = find_vault_root(path)
        config = load_config(vault_path)

        # Skip periodic note folders (they have their own conventions)
        periodic_folders = get_periodic_folders(config)
        folder_name = path.parent.name
        if folder_name in periodic_folders:
            sys.exit(0)

        # Skip root-level files (no folder convention to infer)
        if path.parent == vault_path:
            sys.exit(0)

        # Scan folder for conventions
        conventions = scan_folder_conventions(path.parent, exclude_file=path)

        if not conventions:
            sys.exit(0)

        # Read current file content
        content = path.read_text(encoding='utf-8')
        existing_fm, _, _ = parse_frontmatter(content)

        # Find missing fields
        missing_fields = {}
        for field, stats in conventions.items():
            if field not in existing_fm:
                # Parse the common value back from JSON string
                try:
                    value = json.loads(stats['common_value'])
                except json.JSONDecodeError:
                    value = stats['common_value']

                missing_fields[field] = value

        if not missing_fields:
            sys.exit(0)

        # Add missing fields
        updated_content = add_frontmatter_fields(content, missing_fields)

        # Write back
        path.write_text(updated_content, encoding='utf-8')

        # Report what was added
        print(f"\n✓ Auto-Added Frontmatter to {path.name}")
        print("-" * 60)
        for field, value in missing_fields.items():
            display_value = value if len(str(value)) < 40 else str(value)[:37] + '...'
            print(f"  {field}: {display_value}")
        print("-" * 60)
        print("")

        sys.exit(0)

    except json.JSONDecodeError:
        sys.exit(0)
    except FileNotFoundError as e:
        print(f"[flywheel] Frontmatter complete: File not found - {e.filename}", file=sys.stderr)
        sys.exit(0)
    except PermissionError as e:
        print(f"[flywheel] Frontmatter complete: Permission denied - {e.filename}", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        print(f"[flywheel] Frontmatter complete error: {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(0)


if __name__ == '__main__':
    main()
