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

const VAULT_PATH = process.env.PROJECT_PATH;

if (!VAULT_PATH) {
  console.error('Error: PROJECT_PATH environment variable is required');
  process.exit(1);
}

// Type assertion after validation
const vaultPath: string = VAULT_PATH;

// Vault index (built on startup)
let vaultIndex: VaultIndex;

const server = new McpServer({
  name: 'flywheel',
  version: '1.6.1',
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
  () => vaultPath
);

registerPrimitiveTools(
  server,
  () => vaultIndex,
  () => vaultPath
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

  // Start the MCP server
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error('Flywheel MCP server running on stdio');
}

main().catch((error) => {
  console.error('Fatal error:', error);
  process.exit(1);
});
