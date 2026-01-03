#!/usr/bin/env python3
"""
Wikilink Cache Hook (wikilink-cache.py)

Part of the wikilink-* hook family:
- wikilink-cache.py   : SessionStart - Rebuilds entity cache from vault pages
- wikilink-suggest.py : PostToolUse  - Auto-applies wikilinks after edits

Scans the vault for actual .md files and builds a cache of valid entities
that can be wikilinked. Only includes pages that actually exist.

Exit codes:
- 0: Success (cache rebuilt)
"""

import json
import sys
import re
from datetime import datetime
from pathlib import Path
from collections import defaultdict

# Add parent directory to path for config import
sys.path.insert(0, str(Path(__file__).parent.parent))
from config.loader import load_config, get_periodic_folders


def get_vault_path():
    """Get the vault path from current working directory."""
    return Path.cwd()


def rebuild_wikilink_cache():
    """Rebuild wikilink cache by scanning vault for actual page files."""
    config = load_config()
    vault_path = get_vault_path()
    cache_file = vault_path / '.claude' / 'wikilink-entities.json'

    # Tech keywords for categorization
    TECH_KEYWORDS = [
        'databricks', 'api', 'code', 'azure', 'sql', 'git',
        'node', 'react', 'powerbi', 'excel', 'copilot',
        'fabric', 'apim', 'endpoint', 'synology', 'tailscale',
        'obsidian', 'claude', 'powershell',
        'adf', 'adb', 'net', 'python', 'javascript'
    ]

    # Get periodic note folders from config
    periodic_folders = get_periodic_folders(config)

    # Build a set of all actual pages in the vault (file stems without .md)
    # Only include wikilinks that have backing pages
    existing_pages = set()
    page_paths = {}  # Map page name to relative path for context

    for md_file in vault_path.rglob('*.md'):
        # Skip .claude and .obsidian directories
        rel_path = md_file.relative_to(vault_path)
        if any(part.startswith('.') for part in rel_path.parts):
            continue

        # Get the page name (file stem)
        page_name = md_file.stem
        existing_pages.add(page_name)

        # Also add the relative path without extension as a valid link target
        rel_path_no_ext = str(rel_path.with_suffix('')).replace('\\', '/')
        existing_pages.add(rel_path_no_ext)
        page_paths[page_name] = str(rel_path)

    # Build exclusion patterns dynamically from config
    EXCLUDE_PATTERNS = [
        r'^\d{4}-\d{2}-\d{2}$',           # ISO dates like 2025-01-01
        r'^\d{1,2}/\d{1,2}/\d{4}$',       # UK dates like 1/10/2024
        r'^\d{4}-W\d{2}$',                 # Week dates like 2025-W17
        r'^\d{4}-\d{2}$',                  # Month format like 2025-01
        r'^\d{4}-Q\d$',                    # Quarter dates like 2025-Q4
        r'^\d+$',                          # Pure numbers
        r'^@',                             # Twitter handles
        r'^<',                             # XML/HTML tags
        r'^\{\{',                          # Template placeholders
        r'\\$',                            # Paths ending in backslash
        r'\.(?:md|js|py|json|jpg|png|pdf|csv)$',  # File extensions
        r'^[a-z0-9_-]+\.[a-z]+$',          # File names with extensions
    ]

    # Add periodic note folder exclusions from config
    for folder in periodic_folders:
        EXCLUDE_PATTERNS.append(f'^{re.escape(folder)}/')

    # Collect pages that pass all filters
    valid_entities = set()

    for page in existing_pages:
        # Skip if matches any exclude pattern
        if any(re.match(pattern, page, re.IGNORECASE) for pattern in EXCLUDE_PATTERNS):
            continue

        # Skip very short names (likely abbreviations or common words)
        if len(page) < 2:
            continue

        valid_entities.add(page)

    # Categorize
    categorized = defaultdict(list)

    for link in valid_entities:
        # Categorize
        if any(tech in link.lower() for tech in TECH_KEYWORDS):
            categorized['technologies'].append(link)
        elif link.isupper() and 2 <= len(link) <= 6:
            categorized['acronyms'].append(link)
        elif ' ' in link and len(link.split()) == 2:
            categorized['people'].append(link)
        elif ' ' in link:
            categorized['projects'].append(link)
        else:
            categorized['other'].append(link)

    # Sort each category
    cache = {k: sorted(set(v)) for k, v in categorized.items()}

    # Add metadata
    cache['_metadata'] = {
        'total_entities': sum(len(v) for v in categorized.values()),
        'generated_at': datetime.now().isoformat(),
        'vault_path': str(vault_path),
        'source': 'flywheel wikilink-cache hook',
        'generator': 'flywheel v1.0.0'
    }

    # Save cache
    try:
        cache_file.parent.mkdir(parents=True, exist_ok=True)
        cache_file.write_text(json.dumps(cache, indent=2), encoding='utf-8')
        return cache['_metadata']['total_entities']
    except Exception as e:
        raise RuntimeError(f"Failed to write cache: {e}")


def main():
    """Main entry point for SessionStart hook."""
    try:
        entity_count = rebuild_wikilink_cache()

        # Output status message (will be picked up by session-start.py)
        print(f"Wikilink cache: {entity_count} entities")
        sys.exit(0)

    except Exception as e:
        print(f"Wikilink cache error: {e}", file=sys.stderr)
        sys.exit(0)  # Don't block session start


if __name__ == "__main__":
    main()
