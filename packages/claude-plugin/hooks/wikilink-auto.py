#!/usr/bin/env python3
"""
Wikilink Auto-Apply Hook (wikilink-auto.py)

Part of the wikilink-* hook family:
- wikilink-cache.py : SessionStart - Rebuilds entity cache from vault pages
- wikilink-auto.py  : PostToolUse  - Auto-applies wikilinks after edits

Runs after Edit/Write operations to AUTO-APPLY wikilinks to known entities.
This hook MODIFIES files - it doesn't just suggest, it applies.

Detects:
- People names (capitalized multi-word)
- Project names (MyProject, Project 2024, etc.)
- Technologies (Claude Code, Azure, etc.)
- Known entities from wikilink cache

Protected zones (never wikilinked):
- YAML frontmatter
- Code blocks (``` and `)
- Existing wikilinks
- Markdown links
- URLs
- Hashtags (#tag)
- HTML/XML tags (<tag>)
- Obsidian comments (%% ... %%)
- Math expressions ($ ... $)

Exit codes:
- 0: Always (informational only, never blocks)
"""

import json
import sys
import re
from pathlib import Path
from collections import defaultdict

# Configure UTF-8 output for Windows console
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass


# Common words to exclude from wikilink suggestions
EXCLUDE_WORDS = {
    'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday',
    'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august',
    'september', 'october', 'november', 'december',
    'today', 'tomorrow', 'yesterday', 'week', 'month', 'year',
    'the', 'and', 'for', 'with', 'from', 'this', 'that',
    'christmas', 'holiday', 'break',
}

# Common phrases to exclude (not proper nouns despite capitalization)
EXCLUDE_PHRASES = {
    'go for', 'next step', 'good morning', 'happy birthday',
    'thank you', 'please see', 'best regards', 'kind regards',
}


def load_wikilinks_from_cache(vault_path: Path) -> set:
    """Load existing wikilinks from cache file."""
    cache_file = vault_path / '.claude' / 'wikilink-entities.json'

    if not cache_file.exists():
        # Fallback: scan vault if cache doesn't exist
        return extract_existing_wikilinks_fallback(vault_path)

    try:
        cache_data = json.loads(cache_file.read_text(encoding='utf-8'))
        wikilinks = set()

        # Combine all categories (skip metadata)
        for category, entities in cache_data.items():
            if category != '_metadata':
                wikilinks.update(entities)

        return wikilinks
    except Exception:
        # Fallback on error
        return extract_existing_wikilinks_fallback(vault_path)


def extract_existing_wikilinks_fallback(vault_path: Path) -> set:
    """Fallback: Extract all existing wikilinks from the vault."""
    wikilinks = set()

    # Search all markdown files
    for md_file in vault_path.rglob('*.md'):
        # Skip .claude directory
        if '.claude' in str(md_file):
            continue

        try:
            content = md_file.read_text(encoding='utf-8')
            # Match [[wikilink]] and [[wikilink|alias]]
            matches = re.findall(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', content)
            wikilinks.update(matches)
        except Exception:
            continue

    return wikilinks


def find_frontmatter_end(content: str) -> int:
    """Find where YAML frontmatter ends. Returns 0 if no frontmatter."""
    if not content.startswith('---'):
        return 0

    # Find the closing --- (must be on its own line)
    lines = content.split('\n')
    if len(lines) < 2:
        return 0

    # Start after the opening ---
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == '---':
            # Calculate character position after closing ---
            return sum(len(l) + 1 for l in lines[:i+1])

    return 0  # No closing --- found


def apply_wikilinks(content: str, entities_to_link: list) -> tuple[str, int]:
    """Apply wikilinks to entities in content.

    Returns: (updated_content, count_of_links_added)
    """
    if not entities_to_link:
        return content, 0

    # Sort by length (longest first) to avoid partial replacements
    entities_sorted = sorted(set(entities_to_link), key=len, reverse=True)

    # Skip areas we shouldn't link
    # CRITICAL: Skip YAML frontmatter (first thing in file between --- markers)
    frontmatter_end = find_frontmatter_end(content)
    frontmatter = [(0, frontmatter_end)] if frontmatter_end > 0 else []

    # Remove code blocks
    code_block_pattern = r'```[\s\S]*?```'
    code_blocks = list(re.finditer(code_block_pattern, content))

    # Remove inline code
    inline_code_pattern = r'`[^`]+`'
    inline_codes = list(re.finditer(inline_code_pattern, content))

    # Remove existing wikilinks
    wikilink_pattern = r'\[\[[^\]]+\]\]'
    existing_links = list(re.finditer(wikilink_pattern, content))

    # Remove markdown links [text](url)
    markdown_link_pattern = r'\[([^\]]+)\]\(([^\)]+)\)'
    markdown_links = list(re.finditer(markdown_link_pattern, content))

    # Remove bare URLs (http:// or https://)
    url_pattern = r'https?://[^\s\)\]]+(?:\([^\)]+\))?[^\s\)\]]*'
    bare_urls = list(re.finditer(url_pattern, content))

    # Remove hashtags (don't wikilink inside tags like #habit, #work)
    hashtag_pattern = r'#[\w-]+'
    hashtags = list(re.finditer(hashtag_pattern, content))

    # Remove HTML/XML tags (angle brackets break Obsidian rendering)
    html_tag_pattern = r'<[^>]+>'
    html_tags = list(re.finditer(html_tag_pattern, content))

    # Remove Obsidian comments (%% ... %%)
    obsidian_comment_pattern = r'%%.*?%%'
    obsidian_comments = list(re.finditer(obsidian_comment_pattern, content, re.DOTALL))

    # Remove math expressions ($ ... $ and $$ ... $$)
    math_block_pattern = r'\$\$[\s\S]*?\$\$|\$[^\$]+\$'
    math_blocks = list(re.finditer(math_block_pattern, content))

    # Combine all skip zones (frontmatter MUST be first to protect it)
    skip_zones = frontmatter + [(m.start(), m.end()) for m in code_blocks + inline_codes + existing_links + markdown_links + bare_urls + hashtags + html_tags + obsidian_comments + math_blocks]
    skip_zones.sort()

    links_added = 0
    new_content = content

    for entity in entities_sorted:
        # Find all occurrences with word boundaries (case-insensitive)
        pattern = r'\b' + re.escape(entity) + r'\b'

        for match in re.finditer(pattern, new_content, re.IGNORECASE):
            start, end = match.start(), match.end()

            # Check if this match is in a skip zone
            in_skip_zone = any(s <= start < e or s < end <= e for s, e in skip_zones)

            if not in_skip_zone:
                # Apply wikilink
                matched_text = match.group()
                wikilinked = f'[[{entity}]]'
                new_content = new_content[:start] + wikilinked + new_content[end:]

                # Update skip zones (shift positions after this insertion)
                shift = len(wikilinked) - len(matched_text)
                skip_zones = [(s if s <= start else s + shift,
                              e if e <= start else e + shift) for s, e in skip_zones]
                # Add this new wikilink to skip zones
                skip_zones.append((start, start + len(wikilinked)))
                skip_zones.sort()

                links_added += 1
                break  # Only link first occurrence to avoid over-linking

    return new_content, links_added


def find_heuristic_candidates(content_no_code: str) -> dict:
    """Find high-probability wikilink candidates using heuristic patterns.

    These are multi-word proper nouns that should be wikilinked even without
    backing notes, based on patterns that indicate importance.
    """
    heuristic = defaultdict(list)

    # Category 1: Capitalized Multi-Word Phrases (2-4 words)
    # "Claude Code", "Private Endpoint", "Machine Learning"
    multi_word_pattern = r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})\b'
    for match in re.finditer(multi_word_pattern, content_no_code):
        phrase = match.group(1)
        phrase_lower = phrase.lower()

        # Skip common words and phrases
        if phrase_lower in EXCLUDE_WORDS or phrase_lower in EXCLUDE_PHRASES:
            continue

        # Skip if any word is in EXCLUDE_WORDS
        words = phrase.split()
        if any(w.lower() in EXCLUDE_WORDS for w in words):
            continue

        heuristic['Multi-Word Proper Nouns'].append(phrase)

    # Category 2: Technology Patterns
    # Pattern: "X.js", "X Server", "X API", "X Framework", "X Code"
    tech_suffixes = ['Server', 'API', 'Framework', 'Code', 'Database', 'Platform',
                     'Service', 'Engine', 'Client', 'Library', 'Tool', 'App']
    tech_pattern = r'\b([A-Z][a-z]+(?:\s+(?:' + '|'.join(tech_suffixes) + r')))\b'
    for match in re.finditer(tech_pattern, content_no_code):
        phrase = match.group(1)
        heuristic['Technology Terms'].append(phrase)

    # Pattern: "X.js", "X.py", "X.net"
    dotjs_pattern = r'\b([A-Z][a-z]+\.(?:js|py|net|go|rb|rs))\b'
    for match in re.finditer(dotjs_pattern, content_no_code, re.IGNORECASE):
        phrase = match.group(1)
        heuristic['Technology Terms'].append(phrase)

    # Category 3: Version/Year Patterns
    # "Quest 3", "Python 3", ".NET 8", "SIP 2024", "GPT-4"
    version_patterns = [
        r'\b([A-Z][a-z]+\s+\d{1,2})\b',  # "Quest 3", "Python 3"
        r'\b(\.NET\s+\d)\b',              # ".NET 8"
        r'\b([A-Z]{2,}\s+\d{4})\b',       # "SIP 2024"
        r'\b(GPT-\d+(?:\.\d+)?)\b',       # "GPT-4", "GPT-4.5"
        r'\b([A-Z][a-z]+\s+v?\d+(?:\.\d+)*)\b',  # "React v18.2"
    ]
    for pattern in version_patterns:
        for match in re.finditer(pattern, content_no_code):
            phrase = match.group(1)
            heuristic['Versioned Products'].append(phrase)

    # Category 4: CamelCase/PascalCase
    # ESGHub, GraphAPI, PowerBI, TruCost
    camelcase_pattern = r'\b([A-Z][a-z]+[A-Z][a-z][A-Za-z]*)\b'
    for match in re.finditer(camelcase_pattern, content_no_code):
        phrase = match.group(1)
        # Must have at least 5 chars to avoid false positives
        if len(phrase) >= 5:
            heuristic['CamelCase Terms'].append(phrase)

    # Category 6: Acronym + Word/Acronym
    # "API Management", "MCP Server", "REST API"
    acronym_word_patterns = [
        r'\b([A-Z]{2,6}\s+[A-Z][a-z]+)\b',  # API Management, MCP Server
        r'\b([A-Z]{2,6}\s+[A-Z]{2,6})\b',   # REST API, HTTP POST
    ]
    for pattern in acronym_word_patterns:
        for match in re.finditer(pattern, content_no_code):
            phrase = match.group(1)
            heuristic['Acronym Compounds'].append(phrase)

    # Deduplicate each category
    for category in heuristic:
        heuristic[category] = sorted(set(heuristic[category]))

    return heuristic


def find_linkable_candidates(content: str, existing_wikilinks: set) -> dict:
    """Find potential wikilink candidates in content."""
    candidates = defaultdict(list)

    # Remove code blocks and already wikilinked content
    # CRITICAL: Remove YAML frontmatter first
    frontmatter_end = find_frontmatter_end(content)
    content_no_code = content[frontmatter_end:] if frontmatter_end > 0 else content
    # Remove fenced code blocks
    content_no_code = re.sub(r'```[\s\S]*?```', '', content_no_code)
    # Remove inline code
    content_no_code = re.sub(r'`[^`]+`', '', content_no_code)
    # Remove existing wikilinks
    content_no_code = re.sub(r'\[\[[^\]]+\]\]', '', content_no_code)
    # Remove markdown links [text](url)
    content_no_code = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', '', content_no_code)
    # Remove bare URLs (http:// or https://)
    content_no_code = re.sub(r'https?://[^\s\)\]]+(?:\([^\)]+\))?[^\s\)\]]*', '', content_no_code)
    # Remove hashtags
    content_no_code = re.sub(r'#[\w-]+', '', content_no_code)
    # Remove HTML/XML tags
    content_no_code = re.sub(r'<[^>]+>', '', content_no_code)
    # Remove Obsidian comments
    content_no_code = re.sub(r'%%.*?%%', '', content_no_code, flags=re.DOTALL)
    # Remove math expressions
    content_no_code = re.sub(r'\$\$[\s\S]*?\$\$|\$[^\$]+\$', '', content_no_code)

    # Pattern 1: Capitalized multi-word phrases (2-4 words)
    multi_word_pattern = r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})\b'
    for match in re.finditer(multi_word_pattern, content_no_code):
        phrase = match.group(1)
        if phrase.lower() not in EXCLUDE_WORDS:
            # Check if phrase exists in vault
            if phrase in existing_wikilinks:
                candidates['Multi-Word Entities'].append(phrase)

    # Pattern 2: Known acronyms (2-6 uppercase letters)
    acronym_pattern = r'\b([A-Z]{2,6})\b'
    for match in re.finditer(acronym_pattern, content_no_code):
        acronym = match.group(1)
        if acronym in existing_wikilinks:
            candidates['Acronyms/Projects'].append(acronym)

    # Pattern 3: Technology/tool names (known from existing wikilinks)
    for wikilink in existing_wikilinks:
        # Use word boundaries to avoid partial matches
        pattern = r'\b' + re.escape(wikilink) + r'\b'
        if re.search(pattern, content_no_code, re.IGNORECASE):
            if any(char.isupper() for char in wikilink) and any(char.islower() for char in wikilink):
                candidates['Existing Entities'].append(wikilink)

    # Deduplicate each category
    for category in candidates:
        candidates[category] = sorted(set(candidates[category]))

    return candidates


def get_vault_path_from_env() -> Path | None:
    """Get the vault path from PROJECT_PATH environment variable."""
    import os
    project_path = os.environ.get('PROJECT_PATH', '')
    if project_path:
        return Path(project_path).resolve()
    return None


def is_within_vault(file_path: Path, vault_path: Path) -> bool:
    """Check if a file is within the vault directory.

    This prevents the hook from modifying files outside the vault,
    avoiding pollution of other repositories.
    """
    try:
        file_resolved = file_path.resolve()
        vault_resolved = vault_path.resolve()
        # Use is_relative_to for Python 3.9+ or fallback for older versions
        try:
            return file_resolved.is_relative_to(vault_resolved)
        except AttributeError:
            # Python < 3.9 fallback
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

        # CRITICAL: Only run auto-fixes on Edit/Write, not Read
        tool_name = hook_input.get('tool_name', '')
        if tool_name not in ['Edit', 'Write']:
            sys.exit(0)

        # Get the file path from tool input
        tool_input = hook_input.get('tool_input', {})
        file_path = tool_input.get('file_path', '')

        # CRITICAL: Check vault boundary - only operate on files within PROJECT_PATH
        # This prevents pollution of files outside the vault (e.g., other repos)
        env_vault_path = get_vault_path_from_env()
        if env_vault_path:
            file_p = Path(file_path)
            if not is_within_vault(file_p, env_vault_path):
                # File is outside vault - skip silently
                sys.exit(0)

        # Only check markdown files
        if not file_path.endswith('.md'):
            sys.exit(0)

        # Skip any dot-folder (.claude, .git, .obsidian, etc.)
        # Check if any path component starts with a dot
        path_parts = Path(file_path).parts
        if any(part.startswith('.') and len(part) > 1 for part in path_parts):
            sys.exit(0)

        # Skip CLAUDE.md files (case-insensitive)
        if file_path.lower().endswith('claude.md'):
            sys.exit(0)

        # Skip documentation/ directory
        if '/documentation/' in file_path or '\\documentation\\' in file_path:
            sys.exit(0)

        # Skip docs/ directory (repo documentation)
        if '/docs/' in file_path or '\\docs\\' in file_path:
            sys.exit(0)

        # Skip root-level documentation files
        root_skip = ['README.md', 'CONTRIBUTING.md', 'LICENSE.md', 'CHANGELOG.md']
        file_name = Path(file_path).name
        if file_name in root_skip:
            sys.exit(0)

        # Check if file exists
        path = Path(file_path)
        if not path.exists():
            sys.exit(0)

        # Get vault root (assuming file is in vault)
        vault_path = path
        while vault_path.parent != vault_path:
            if (vault_path / '.obsidian').exists() or (vault_path / '.claude').exists():
                break
            vault_path = vault_path.parent

        # Load existing wikilinks from cache
        existing_wikilinks = load_wikilinks_from_cache(vault_path)

        # Read file content
        content = path.read_text(encoding='utf-8')

        # Prepare cleaned content for analysis (reuse the cleaning logic)
        frontmatter_end = find_frontmatter_end(content)
        content_no_code = content[frontmatter_end:] if frontmatter_end > 0 else content
        content_no_code = re.sub(r'```[\s\S]*?```', '', content_no_code)
        content_no_code = re.sub(r'`[^`]+`', '', content_no_code)
        content_no_code = re.sub(r'\[\[[^\]]+\]\]', '', content_no_code)
        content_no_code = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', '', content_no_code)
        content_no_code = re.sub(r'https?://[^\s\)\]]+(?:\([^\)]+\))?[^\s\)\]]*', '', content_no_code)
        content_no_code = re.sub(r'#[\w-]+', '', content_no_code)
        content_no_code = re.sub(r'<[^>]+>', '', content_no_code)
        content_no_code = re.sub(r'%%.*?%%', '', content_no_code, flags=re.DOTALL)
        content_no_code = re.sub(r'\$\$[\s\S]*?\$\$|\$[^\$]+\$', '', content_no_code)

        # TIER 1: Find cache-based candidates (entities with backing notes)
        cache_candidates = find_linkable_candidates(content, existing_wikilinks)

        # TIER 2: Find heuristic candidates (high-probability patterns)
        heuristic_candidates = find_heuristic_candidates(content_no_code)

        # Merge candidates (cache takes precedence, heuristic fills gaps)
        all_candidates = defaultdict(list)

        # Add cache-based first (HIGH confidence - they have backing notes)
        for category, items in cache_candidates.items():
            all_candidates[f"✓ {category} (Has Notes)"].extend(items)

        # Add heuristic-based (MEDIUM-HIGH confidence - pattern match only)
        for category, items in heuristic_candidates.items():
            # Don't add if already in cache
            new_items = [item for item in items if not any(
                item in cache_items for cache_items in cache_candidates.values()
            )]
            if new_items:
                all_candidates[f"⚡ {category} (Heuristic)"].extend(new_items)

        # Remove empty categories
        all_candidates = {k: v for k, v in all_candidates.items() if v}

        if all_candidates:
            # Collect all entities to link
            all_entities = []
            for items in all_candidates.values():
                all_entities.extend(items)

            # Apply wikilinks automatically
            updated_content, links_added = apply_wikilinks(content, all_entities)

            if links_added > 0:
                # Write updated content back to file
                path.write_text(updated_content, encoding='utf-8')

                print(f"\n✓ Auto-Applied {links_added} Wikilinks to {path.name}")
                print("-" * 60)

                for category, items in all_candidates.items():
                    # Show what was linked (limit to top 5 per category)
                    display_items = items[:min(5, len(items))]
                    print(f"{category}: {', '.join(display_items)}")
                    if len(items) > 5:
                        print(f"  ... and {len(items) - 5} more")

                print("-" * 60)
                print("")

        sys.exit(0)

    except json.JSONDecodeError:
        sys.exit(0)
    except FileNotFoundError as e:
        print(f"[flywheel] Wikilink suggest: File not found - {e.filename}", file=sys.stderr)
        sys.exit(0)
    except PermissionError as e:
        print(f"[flywheel] Wikilink suggest: Permission denied - {e.filename}", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        print(f"[flywheel] Wikilink suggest error: {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(0)


if __name__ == '__main__':
    main()
