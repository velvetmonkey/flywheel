#!/usr/bin/env node
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import type { VaultIndex } from './core/types.js';
import { buildVaultIndex } from './core/graph.js';
import { registerGraphTools } from './tools/graph.js';
import { registerWikilinkTools } from './tools/wikilinks.js';
import { registerHealthTools } from './tools/health.js';
import { registerQueryTools } from './tools/query.js';
import { registerSystemTools } from './tools/system.js';
import { registerPrimitiveTools } from './tools/primitives.js';
import { registerPeriodicTools } from './tools/periodic.js';
import { registerBidirectionalTools } from './tools/bidirectional.js';
import { registerSchemaTools } from './tools/schema.js';
import { registerComputedTools } from './tools/computed.js';
import { registerMigrationTools } from './tools/migrations.js';
import { watchVault } from './core/watcher.js';
import { loadConfig, inferConfig, saveConfig, type FlywheelConfig } from './core/config.js';

// Default to current working directory if PROJECT_PATH not specified
const vaultPath: string = process.env.PROJECT_PATH || process.cwd();

// Config root is always the project root (where Claude Code runs)
const configRoot: string = process.cwd();

// Flywheel config (loaded on startup from .flywheel.json)
let flywheelConfig: FlywheelConfig = {};

// File watcher enabled by default, set FLYWHEEL_WATCH=false to disable
const watchEnabled = process.env.FLYWHEEL_WATCH !== 'false';

// Vault index (built on startup)
let vaultIndex: VaultIndex;

const server = new McpServer({
  name: 'flywheel',
  version: '1.7.0',
});

// Register all tools
registerGraphTools(
  server,
  () => vaultIndex,
  () => vaultPath
);

registerWikilinkTools(
  server,
  () => vaultIndex,
  () => vaultPath
);

registerHealthTools(
  server,
  () => vaultIndex,
  () => vaultPath
);

registerQueryTools(
  server,
  () => vaultIndex,
  () => vaultPath
);

registerSystemTools(
  server,
  () => vaultIndex,
  (newIndex) => { vaultIndex = newIndex; },
  () => vaultPath,
  (newConfig) => { flywheelConfig = newConfig; },
  () => configRoot
);

registerPrimitiveTools(
  server,
  () => vaultIndex,
  () => vaultPath,
  () => flywheelConfig
);

registerPeriodicTools(
  server,
  () => vaultIndex
);

registerBidirectionalTools(
  server,
  () => vaultIndex,
  () => vaultPath
);

registerSchemaTools(
  server,
  () => vaultIndex,
  () => vaultPath
);

registerComputedTools(
  server,
  () => vaultIndex,
  () => vaultPath
);

registerMigrationTools(
  server,
  () => vaultIndex,
  () => vaultPath
);

async function main() {
  // Build the vault index
  console.error('Building vault index...');
  const startTime = Date.now();

  try {
    vaultIndex = await buildVaultIndex(vaultPath);
    const duration = Date.now() - startTime;
    console.error(`Vault index built in ${duration}ms`);
  } catch (err) {
    console.error('Failed to build vault index:', err);
    process.exit(1);
  }

  // Load existing config, infer from vault, merge and save
  const existing = loadConfig(configRoot);
  const inferred = inferConfig(vaultIndex);
  saveConfig(configRoot, inferred, existing);
  flywheelConfig = loadConfig(configRoot); // Reload merged config

  if (flywheelConfig.exclude_task_tags?.length) {
    console.error(`[Flywheel] Excluding task tags: ${flywheelConfig.exclude_task_tags.join(', ')}`);
  }

  // Start the MCP server
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error('Flywheel MCP server running on stdio');

  // Start file watcher for automatic index refresh
  if (watchEnabled) {
    watchVault(vaultPath, (newIndex) => {
      vaultIndex = newIndex;
    });
  }
}

main().catch((error) => {
  console.error('Fatal error:', error);
  process.exit(1);
});
