import * as fs from 'fs';
import * as path from 'path';

export interface FlywheelConfig {
  exclude_task_tags?: string[];
}

/**
 * Load .flywheel.json from the vault root.
 * Returns empty config if file doesn't exist or can't be parsed.
 */
export function loadConfig(vaultPath: string): FlywheelConfig {
  const configPath = path.join(vaultPath, '.flywheel.json');
  try {
    if (fs.existsSync(configPath)) {
      const content = fs.readFileSync(configPath, 'utf-8');
      const config = JSON.parse(content);
      return config;
    }
  } catch (err) {
    console.error('[Flywheel] Failed to load .flywheel.json:', err);
  }
  return {};
}
