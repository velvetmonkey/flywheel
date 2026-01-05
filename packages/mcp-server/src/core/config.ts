import * as fs from 'fs';
import * as path from 'path';

export interface FlywheelConfig {
  exclude_task_tags?: string[];
}

/** Default config for new vaults */
const DEFAULT_CONFIG: FlywheelConfig = {
  exclude_task_tags: [],
};

/**
 * Load .flywheel.json from the vault root.
 * Creates the file with defaults if it doesn't exist.
 */
export function loadConfig(vaultPath: string): FlywheelConfig {
  const configPath = path.join(vaultPath, '.flywheel.json');
  try {
    if (fs.existsSync(configPath)) {
      const content = fs.readFileSync(configPath, 'utf-8');
      const config = JSON.parse(content);
      return config;
    } else {
      // Create default config file so users can discover and edit it
      const content = JSON.stringify(DEFAULT_CONFIG, null, 2);
      fs.writeFileSync(configPath, content, 'utf-8');
      console.error(`[Flywheel] Created .flywheel.json with defaults`);
      return DEFAULT_CONFIG;
    }
  } catch (err) {
    console.error('[Flywheel] Failed to load/create .flywheel.json:', err);
  }
  return {};
}
