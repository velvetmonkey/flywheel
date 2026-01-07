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
import { loadConfig, inferConfig, saveConfig, type FlywheelConfig } from './core/config.js';
import { findVaultRoot } from './core/vaultRoot.js';

// Auto-detect vault root, with PROJECT_PATH as override
const vaultPath: string = process.env.PROJECT_PATH || findVaultRoot();

// Flywheel config (loaded on startup from .flywheel.json)
let flywheelConfig: FlywheelConfig = {};

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
  (newConfig) => { flywheelConfig = newConfig; }
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
  const existing = loadConfig(vaultPath);
  const inferred = inferConfig(vaultIndex, vaultPath);
  saveConfig(vaultPath, inferred, existing);
  flywheelConfig = loadConfig(vaultPath); // Reload merged config

  if (flywheelConfig.vault_name) {
    console.error(`[Flywheel] Vault: ${flywheelConfig.vault_name}`);
  }
  if (flywheelConfig.paths) {
    const detectedPaths = Object.entries(flywheelConfig.paths)
      .filter(([, v]) => v)
      .map(([k, v]) => `${k}: ${v}`);
    if (detectedPaths.length) {
      console.error(`[Flywheel] Detected paths: ${detectedPaths.join(', ')}`);
    }
  }
  if (flywheelConfig.exclude_task_tags?.length) {
    console.error(`[Flywheel] Excluding task tags: ${flywheelConfig.exclude_task_tags.join(', ')}`);
  }

  // Start the MCP server
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error('Flywheel MCP server running on stdio');

  // Periodic refresh for automatic index updates
  const refreshInterval = parseInt(process.env.FLYWHEEL_REFRESH_INTERVAL || '60000', 10);
  if (refreshInterval > 0) {
    setInterval(async () => {
      try {
        const newIndex = await buildVaultIndex(vaultPath);
        if (newIndex.notes.size !== vaultIndex.notes.size) {
          console.error(`[Flywheel] Periodic refresh: ${vaultIndex.notes.size} → ${newIndex.notes.size} notes`);
        }
        vaultIndex = newIndex;
      } catch (err) {
        console.error('[Flywheel] Periodic refresh failed:', err);
      }
    }, refreshInterval);
    console.error(`[Flywheel] Periodic refresh enabled (${refreshInterval / 1000}s interval)`);
  }
}

main().catch((error) => {
  console.error('Fatal error:', error);
  process.exit(1);
});
