"""
Shared Achievement Detection Library

This module provides reusable achievement detection logic used by:
- achievement-detect.py hook (PostToolUse event-driven)
- achievement-extraction-agent.md (Task agent for manual/rollup extraction)

LIBERAL DETECTION: Captures a wide range of achievements including:
- Simple actions (built, created, tested, configured)
- Learning (figured out, discovered, learned)
- Problem solving (debugged, solved, fixed)
- Communication (presented, documented, reviewed)
- Success signals (works, passed, green)
- Emojis (✅ 🎉 🚀 💪 🏆 🔥)
- Late night work (22:00-05:00 timestamps)
- Bold text (user convention for important items)

Strategy: Capture more, curate later. Better to catch too much than miss achievements.
"""

import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional


# Keywords that suggest significant achievements (LIBERAL - capture more, curate later)
ACHIEVEMENT_KEYWORDS = [
    # 1. Simple Action Verbs (liberal)
    r'wrote',
    r'coded',
    r'developed',
    r'programmed',
    r'built',
    r'made',
    r'created',
    r'added',
    r'set\s*up',
    r'configured',
    r'installed',
    r'tested',
    r'validated',
    r'verified',
    r'confirmed',
    r'fixed',
    r'repaired',
    r'patched',
    r'resolved',
    r'updated',
    r'upgraded',
    r'enhanced',
    r'improved',
    r'refactored',
    r'cleaned\s*up',
    r'reorganized',
    r'automated',
    r'scripted',

    # 2. Learning & Discovery
    r'learned',
    r'figured\s*out',
    r'understood',
    r'discovered',
    r'found\s*(?:out|that|the)',
    r'realized',
    r'noticed',
    r'researched',
    r'investigated',
    r'explored',
    r'analyzed',

    # 3. Problem Solving
    r'solved',
    r'debugged',
    r'troubleshot',
    r'diagnosed',
    r'identified\s*(?:the|root|cause)',
    r'worked\s*around',
    r'workaround',

    # 4. Communication & Collaboration
    r'presented',
    r'demoed',
    r'showed',
    r'taught',
    r'explained',
    r'documented',
    r'shared',
    r'published',
    r'posted',
    r'reviewed',
    r'approved',
    r'merged',
    r'paired',
    r'collaborated',
    r'helped',

    # 5. Progress Indicators
    r'finished',
    r'done',
    r'completed',
    r'wrapped\s*up',
    r'closed\s*out',
    r'shipped',
    r'released',
    r'deployed',
    r'started',
    r'began',
    r'kicked\s*off',

    # 6. Success Signals
    r'works',
    r'working',
    r'passed',
    r'passing',
    r'success',
    r'successful',
    r'succeeded',
    r'green',
    r'all\s*(?:tests|checks)\s*pass',
    r'confirmed\s*(?:working|functional)',

    # 7. First-Time / Milestone Events
    r'first\s*(?:time|ever|successful)',
    r'finally',
    r'at\s*last',
    r'breakthrough',
    r'milestone',
    r'v\d+\.\d+',  # version numbers

    # 8. Bold Text Detection (user convention: bold = important)
    r'\*\*[^*]{10,}\*\*',

    # 9. Ticket/Work Items
    r'(?:completed?|closed?|resolved?)\s*(?:ticket|issue|task|bug|story)',
    r'PR\s*(?:merged|approved|created)',
    r'(?:OC|JIRA|ticket)\s*\d+',

    # 10. Meta-Achievements
    r'achieved',
    r'accomplished',
    r'delivered',
    r'nailed',
    r'crushed',
    r'knocked\s*out',
    r'got\s*(?:it|this)\s*working',

    # 11. Emoji Detection
    r'✅',  # checkmark
    r'🎉',  # celebration
    r'🚀',  # rocket
    r'💪',  # strength
    r'🏆',  # trophy
    r'⭐',  # star
    r'🔥',  # fire
    r'✨',  # sparkles
    r'👍',  # thumbs up
    r'🎯',  # target

    # 12. Late Night/Early Morning Work (22:00-05:00)
    r'(?:22|23|00|01|02|03|04|05):\d{2}',

    # Legacy patterns (keep for backward compatibility)
    r'deployed?\s+(?:to\s+)?(?:prod|production|prd)',
    r'pushed?\s+(?:to\s+)?(?:prod|production)',
    r'went\s+live',
    r'production\s+release',
    r'hotfix',
    r'incident\s+resolved',
    r'\d+%\s+(?:improvement|reduction|increase)',
    r'zero\s+(?:downtime|rollbacks|issues)',
    r'successfully\s+(?:completed|implemented|deployed|built|created|established|integrated|configured|resolved|migrated)',
    r'established\s+(?:the\s+)?(?:system|framework|pipeline|integration|platform|infrastructure)',
]


def check_for_achievements(content: str, config: dict) -> List[Dict[str, str]]:
    """
    Scan content for achievement-worthy entries.

    Args:
        content: Text content to scan (typically from daily note)
        config: Configuration dict with 'sections' key containing 'log' header

    Returns:
        List of achievement dicts with keys: keyword, line, context
    """
    achievements = []

    # Focus on Log section if it exists
    log_header = config['sections']['log']
    log_pattern = re.escape(log_header) + r'\s*\n([\s\S]*?)(?=\n## |\n# |\Z)'
    log_match = re.search(log_pattern, content)
    search_content = log_match.group(1) if log_match else content

    for pattern in ACHIEVEMENT_KEYWORDS:
        matches = re.finditer(pattern, search_content, re.IGNORECASE)
        for match in matches:
            # Get the full line containing the match
            line_start = search_content.rfind('\n', 0, match.start()) + 1
            line_end = search_content.find('\n', match.end())
            if line_end == -1:
                line_end = len(search_content)

            full_line = search_content[line_start:line_end].strip()

            # Clean up the line (remove leading - or *)
            full_line = re.sub(r'^[-*]\s*', '', full_line)

            if full_line and len(full_line) > 10:  # Minimum meaningful length
                achievements.append({
                    'keyword': match.group(),
                    'line': full_line,
                    'context': pattern
                })

    # Deduplicate by line
    seen_lines = set()
    unique_achievements = []
    for a in achievements:
        if a['line'] not in seen_lines:
            seen_lines.add(a['line'])
            unique_achievements.append(a)

    return unique_achievements


def normalize_for_comparison(text: str) -> str:
    """
    Normalize text for duplicate comparison.

    Args:
        text: Achievement text to normalize

    Returns:
        Normalized text (lowercase, no timestamps, first 60 chars)
    """
    # Remove timestamps like "- 20:11 " or "- 08:42 "
    text = re.sub(r'^[\d:]+\s*', '', text)
    # Remove leading dashes, bullets, asterisks
    text = re.sub(r'^[-*•]\s*', '', text)
    # Remove wikilink brackets for comparison
    text = re.sub(r'\[\[([^\]]+)\]\]', r'\1', text)
    # Remove bold/italic markers
    text = re.sub(r'\*+', '', text)
    # Normalize whitespace
    text = ' '.join(text.split())
    # Take first 60 chars for fuzzy matching (avoid minor edits creating dupes)
    return text[:60].lower().strip()


def filter_existing_achievements(achievements: List[Dict[str, str]], existing_content: str) -> List[Dict[str, str]]:
    """
    Filter out achievements that already exist in the Achievements file.

    Args:
        achievements: List of achievement dicts to filter
        existing_content: Current content of Achievements.md

    Returns:
        Filtered list of new achievements only
    """
    # Normalize existing content for comparison
    existing_normalized = set()
    for line in existing_content.split('\n'):
        line = line.strip()
        if line.startswith('-') or line.startswith('*'):
            normalized = normalize_for_comparison(line)
            if len(normalized) > 10:  # Only meaningful lines
                existing_normalized.add(normalized)

    # Filter achievements
    new_achievements = []
    for a in achievements:
        normalized = normalize_for_comparison(a['line'])
        if normalized not in existing_normalized:
            new_achievements.append(a)

    return new_achievements


def write_achievements_to_file(
    achievements: List[Dict[str, str]],
    achievements_file: Path,
    max_achievements: int = 1000,
    target_month: Optional[str] = None
) -> int:
    """
    Write achievements to the Achievements.md file.

    Args:
        achievements: List of achievement dicts to write
        achievements_file: Path to Achievements.md
        max_achievements: Maximum number of achievements to write (default 1000, effectively unlimited)
        target_month: Optional month string like "December 2025" (defaults to current month)

    Returns:
        Number of achievements actually written
    """
    if not achievements or not achievements_file.exists():
        return 0

    # Get target month
    if target_month is None:
        target_month = datetime.now().strftime('%B %Y')  # e.g., "December 2025"

    # Read achievements file
    achievements_content = achievements_file.read_text(encoding='utf-8')

    # Filter out achievements that already exist in the file
    new_achievements = filter_existing_achievements(achievements, achievements_content)

    if not new_achievements:
        return 0  # All achievements already exist

    # Find or create current month section
    month_header = f"### {target_month}"

    if month_header in achievements_content:
        # Month section exists, add to it
        month_start = achievements_content.find(month_header)
        next_section = achievements_content.find('\n###', month_start + len(month_header))
        if next_section == -1:
            next_section = len(achievements_content)

        # Insert achievements before next section (limit to max)
        insert_point = next_section
        new_lines = '\n'.join(f"- {a['line']}" for a in new_achievements[:max_achievements])
        achievements_content = (
            achievements_content[:insert_point] +
            f"\n{new_lines}\n" +
            achievements_content[insert_point:]
        )
    else:
        # Create new month section - find current year
        current_year = datetime.now().strftime('%Y')
        year_section = f"## {current_year}"
        if year_section in achievements_content:
            year_start = achievements_content.find(year_section)
            next_year = achievements_content.find('\n##', year_start + len(year_section))
            if next_year == -1:
                next_year = len(achievements_content)

            new_lines = '\n'.join(f"- {a['line']}" for a in new_achievements[:max_achievements])
            new_section = f"\n\n{month_header}\n{new_lines}\n"

            achievements_content = (
                achievements_content[:next_year] +
                new_section +
                achievements_content[next_year:]
            )

    # Write back
    achievements_file.write_text(achievements_content, encoding='utf-8')

    return min(len(new_achievements), max_achievements)
