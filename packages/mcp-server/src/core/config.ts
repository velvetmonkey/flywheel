import * as fs from 'fs';
import * as path from 'path';
import type { VaultIndex } from './types.js';

export interface FlywheelConfig {
  exclude_task_tags?: string[];
}

/** Default config for new vaults */
const DEFAULT_CONFIG: FlywheelConfig = {
  exclude_task_tags: [],
};

/**
 * Load .flywheel.json from the .claude/ folder.
 * Returns defaults if file doesn't exist (no auto-create).
 */
export function loadConfig(vaultPath: string): FlywheelConfig {
  const claudeDir = path.join(vaultPath, '.claude');
  const configPath = path.join(claudeDir, '.flywheel.json');
  try {
    if (fs.existsSync(configPath)) {
      const content = fs.readFileSync(configPath, 'utf-8');
      const config = JSON.parse(content);
      // Merge with defaults so new config options get their defaults
      return { ...DEFAULT_CONFIG, ...config };
    }
  } catch (err) {
    console.error('[Flywheel] Failed to load .flywheel.json:', err);
  }
  return DEFAULT_CONFIG;
}

/** Common tags that indicate recurring/habit tasks users may want to exclude */
const RECURRING_TAG_PATTERNS = [
  'habit',
  'habits',
  'daily',
  'weekly',
  'monthly',
  'recurring',
  'routine',
  'template',
];

/**
 * Infer config values by analyzing the vault.
 * Returns smart defaults based on vault contents.
 */
export function inferConfig(index: VaultIndex): FlywheelConfig {
  const inferred: FlywheelConfig = {
    exclude_task_tags: [],
  };

  // Find tags that match recurring patterns
  for (const tag of index.tags.keys()) {
    const lowerTag = tag.toLowerCase();
    if (RECURRING_TAG_PATTERNS.some((pattern) => lowerTag.includes(pattern))) {
      inferred.exclude_task_tags!.push(tag);
    }
  }

  return inferred;
}

/**
 * Save config to .claude/.flywheel.json.
 * Merges inferred values with existing config (existing wins).
 */
export function saveConfig(
  vaultPath: string,
  inferred: FlywheelConfig,
  existing?: FlywheelConfig
): void {
  const claudeDir = path.join(vaultPath, '.claude');
  const configPath = path.join(claudeDir, '.flywheel.json');
  try {
    // Ensure .claude directory exists
    if (!fs.existsSync(claudeDir)) {
      fs.mkdirSync(claudeDir, { recursive: true });
    }
    // Existing config values take precedence over inferred
    const merged: FlywheelConfig = {
      ...DEFAULT_CONFIG,
      ...inferred,
      ...existing,
    };
    const content = JSON.stringify(merged, null, 2);
    fs.writeFileSync(configPath, content, 'utf-8');
    console.error(`[Flywheel] Saved .claude/.flywheel.json`);
  } catch (err) {
    console.error('[Flywheel] Failed to save .claude/.flywheel.json:', err);
  }
}
