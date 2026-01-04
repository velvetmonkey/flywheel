#!/usr/bin/env python3
"""
Flywheel Configuration Loader

Loads configuration from .flywheel.json in vault root.
Falls back to defaults if no config file exists.

Usage:
    from config.loader import load_config
    config = load_config()
    daily_path = config['paths']['daily_notes']
"""

import json
from pathlib import Path
from typing import Any

# Default configuration
DEFAULTS = {
    "paths": {
        "daily_notes": "daily-notes",
        "weekly_notes": "weekly-notes",
        "monthly_notes": "monthly-notes",
        "quarterly_notes": "quarterly-notes",
        "yearly_notes": "yearly-notes",
        "achievements": "Achievements.md",
        "templates": "templates"
    },
    "sections": {
        # Section headers use TEXT ONLY (no # prefix)
        # MCP section matching is case-insensitive and level-agnostic
        # "Log" matches # Log, ## Log, ### Log, ## LOG, etc.
        "log": "Log",
        "food": "Food",
        "tasks": "Tasks",
        "habits": "Habits"
    },
    "folders": {
        "protected": [".obsidian", ".git", ".claude"],
        "require_subfolders": [],
        "allow_direct_files": ["templates"]
    },
    "habits": ["Walk", "Stretch", "Vitamins"]
}


def deep_merge(base: dict, override: dict) -> dict:
    """Deep merge override into base, returning new dict."""
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def resolve_achievements_path(vault_path: Path, config: dict) -> str:
    """
    Achievements path resolution:
    1. If user explicitly configured via .flywheel.json, use that
    2. Otherwise default to Achievements.md at vault root
    3. If file doesn't exist, create it for user to customize
    """
    root_path = "Achievements.md"

    user_path = config.get('paths', {}).get('achievements')

    # User explicitly configured - use as-is
    if user_path and user_path != root_path:
        return user_path

    # Default to root - create if doesn't exist
    root_file = vault_path / root_path
    if not root_file.exists():
        try:
            root_file.write_text(
                "# Achievements\n\n"
                "Track your wins here. Flywheel will detect and display recent achievements.\n\n"
                "## Format\n\n"
                "Use date headers and bullet points:\n\n"
                "## 2026-01-04\n\n"
                "- First achievement!\n",
                encoding='utf-8'
            )
        except (IOError, PermissionError):
            pass  # Failed to create, will show "not found"

    return root_path


def find_vault_root(start_path: Path = None) -> Path:
    """Find vault root by looking for .obsidian or .claude folder."""
    if start_path is None:
        start_path = Path.cwd()

    current = start_path.resolve()
    while current != current.parent:
        if (current / '.obsidian').exists() or (current / '.claude').exists():
            return current
        current = current.parent

    # Fallback to cwd
    return Path.cwd()


def load_config(vault_path: Path = None) -> dict:
    """
    Load configuration from .flywheel.json.

    Args:
        vault_path: Path to vault root. If None, auto-detects.

    Returns:
        Merged configuration dict (user config over defaults)
    """
    if vault_path is None:
        vault_path = find_vault_root()

    config_file = vault_path / '.flywheel.json'

    if config_file.exists():
        try:
            user_config = json.loads(config_file.read_text(encoding='utf-8'))
            config = deep_merge(DEFAULTS, user_config)
        except (json.JSONDecodeError, IOError):
            # Invalid config, use defaults
            config = DEFAULTS.copy()
    else:
        config = DEFAULTS.copy()

    # Smart path resolution for achievements
    config['paths']['achievements'] = resolve_achievements_path(vault_path, config)

    return config


def get_path(config: dict, key: str, vault_path: Path = None) -> Path:
    """
    Get a path from config, resolved relative to vault root.

    Args:
        config: Configuration dict
        key: Key in config['paths']
        vault_path: Vault root path

    Returns:
        Resolved Path object
    """
    if vault_path is None:
        vault_path = find_vault_root()

    relative_path = config.get('paths', {}).get(key, DEFAULTS['paths'].get(key, ''))
    return vault_path / relative_path


def get_section(config: dict, key: str) -> str:
    """Get a section header from config."""
    return config.get('sections', {}).get(key, DEFAULTS['sections'].get(key, ''))


def get_periodic_folders(config: dict) -> list:
    """Get list of periodic note folder names."""
    paths = config.get('paths', DEFAULTS['paths'])
    return [
        paths.get('daily_notes', 'daily-notes'),
        paths.get('weekly_notes', 'weekly-notes'),
        paths.get('monthly_notes', 'monthly-notes'),
        paths.get('quarterly_notes', 'quarterly-notes'),
        paths.get('yearly_notes', 'yearly-notes'),
    ]


if __name__ == '__main__':
    # Test loading
    config = load_config()
    print(json.dumps(config, indent=2))
