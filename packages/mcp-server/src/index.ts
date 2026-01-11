#!/usr/bin/env node
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import type { VaultIndex } from './core/types.js';
import { buildVaultIndex, setIndexState, setIndexError } from './core/graph.js';
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
  // Start the MCP server FIRST (immediate - no waiting for index)
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error('Flywheel MCP server running on stdio');

  // Build the vault index in background (non-blocking)
  console.error('Building vault index in background...');
  const startTime = Date.now();

  buildVaultIndex(vaultPath)
    .then((index) => {
      vaultIndex = index;
      setIndexState('ready');
      const duration = Date.now() - startTime;
      console.error(`Vault index ready in ${duration}ms`);

      // Now that index is ready, load/infer config
      const existing = loadConfig(vaultPath);
      const inferred = inferConfig(vaultIndex, vaultPath);
      saveConfig(vaultPath, inferred, existing);
      flywheelConfig = loadConfig(vaultPath);

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
    })
    .catch((err) => {
      setIndexState('error');
      setIndexError(err instanceof Error ? err : new Error(String(err)));
      console.error('Failed to build vault index:', err);
      // Don't exit - server is still running, tools will report the error
    });
}

main().catch((error) => {
  console.error('Fatal error:', error);
  process.exit(1);
});
