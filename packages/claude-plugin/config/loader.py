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
            return deep_merge(DEFAULTS, user_config)
        except (json.JSONDecodeError, IOError):
            # Invalid config, use defaults
            pass

    return DEFAULTS.copy()


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
