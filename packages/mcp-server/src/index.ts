#!/usr/bin/env node
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import chokidar from 'chokidar';
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
import {
  createVaultWatcher,
  parseWatcherConfig,
  processBatch as processBatchIncremental,
  type VaultWatcher,
} from './core/watch/index.js';
import { exportHubScores } from './core/hubExport.js';
import { initializeLogger, getLogger } from './core/logging.js';
import {
  openStateDb,
  type StateDb,
  migrateFromJsonToSqlite,
  getLegacyPaths,
} from '@velvetmonkey/vault-core';

// Auto-detect vault root, with PROJECT_PATH as override
const vaultPath: string = process.env.PROJECT_PATH || findVaultRoot();

// Initialize unified logging (disabled by default, configured via .flywheel.json)
initializeLogger(vaultPath).then(() => {
  const logger = getLogger();
  if (logger?.enabled) {
    console.error(`[Flywheel] Unified logging enabled`);
  }
}).catch(() => {
  // Logging initialization failed, continue without it
});

// Flywheel config (loaded on startup from .flywheel.json)
let flywheelConfig: FlywheelConfig = {};

// Vault index (built on startup)
let vaultIndex: VaultIndex;

// State database (SQLite with FTS5)
let stateDb: StateDb | null = null;

// ============================================================================
// Tool Category System
// ============================================================================
// FLYWHEEL_TOOLS env var controls which tool categories are loaded.
// This reduces context window usage by only exposing tools you need.
//
// Categories:
//   core      - health_check, get_vault_stats, refresh_index, get_note_metadata, get_folder_structure
//   graph     - backlinks, forward_links, orphans, hubs, wikilink suggestions, link validation
//   search    - search_notes
//   tasks     - get_all_tasks, get_tasks_from_note, get_tasks_with_due_dates, get_incomplete_tasks
//   schema    - frontmatter queries, field values, schema inference, validation
//   structure - note structure, headings, sections
//   temporal  - date-based queries, periodic notes, activity summaries
//   advanced  - bidirectional bridge tools, computed frontmatter, migrations
//
// Presets:
//   minimal   - core only (~5% of tools)
//   standard  - core,graph,search,tasks (~45% of tools) [DEFAULT]
//   full      - all tools (~100%)
//
// Examples:
//   FLYWHEEL_TOOLS=minimal           # Just vault stats and metadata
//   FLYWHEEL_TOOLS=core,graph        # Core + graph tools
//   FLYWHEEL_TOOLS=standard          # Default set (most common use cases)
//   FLYWHEEL_TOOLS=full              # Everything
//   FLYWHEEL_TOOLS=core,tasks,schema # Custom combination
// ============================================================================

type ToolCategory = 'core' | 'graph' | 'search' | 'tasks' | 'schema' | 'structure' | 'temporal' | 'advanced';

// Preset definitions
const PRESETS: Record<string, ToolCategory[]> = {
  minimal: ['core'],
  standard: ['core', 'graph', 'search', 'tasks'],
  full: ['core', 'graph', 'search', 'tasks', 'schema', 'structure', 'temporal', 'advanced'],
};

const ALL_CATEGORIES: ToolCategory[] = ['core', 'graph', 'search', 'tasks', 'schema', 'structure', 'temporal', 'advanced'];
const DEFAULT_PRESET = 'standard';

/**
 * Parse FLYWHEEL_TOOLS env var into enabled categories
 */
function parseEnabledCategories(): Set<ToolCategory> {
  const envValue = process.env.FLYWHEEL_TOOLS?.trim();

  // No env var = use default preset
  if (!envValue) {
    return new Set(PRESETS[DEFAULT_PRESET]);
  }

  // Check if it's a preset name
  const lowerValue = envValue.toLowerCase();
  if (PRESETS[lowerValue]) {
    return new Set(PRESETS[lowerValue]);
  }

  // Parse comma-separated categories
  const categories = new Set<ToolCategory>();
  for (const item of envValue.split(',')) {
    const category = item.trim().toLowerCase() as ToolCategory;
    if (ALL_CATEGORIES.includes(category)) {
      categories.add(category);
    } else if (PRESETS[category]) {
      // Allow preset names in comma list
      for (const c of PRESETS[category]) {
        categories.add(c);
      }
    } else {
      console.error(`[Flywheel] Warning: Unknown tool category "${item}" - ignoring`);
    }
  }

  // If nothing valid, fall back to default
  if (categories.size === 0) {
    console.error(`[Flywheel] No valid categories found, using default (${DEFAULT_PRESET})`);
    return new Set(PRESETS[DEFAULT_PRESET]);
  }

  return categories;
}

const enabledCategories = parseEnabledCategories();

// Track which registration functions have been called (some are shared across categories)
const registeredModules = new Set<string>();

function shouldRegister(module: string, categories: ToolCategory[]): boolean {
  if (registeredModules.has(module)) return false;
  const shouldReg = categories.some(cat => enabledCategories.has(cat));
  if (shouldReg) registeredModules.add(module);
  return shouldReg;
}

const server = new McpServer({
  name: 'flywheel',
  version: '1.7.0',
});

// Log enabled categories
const categoryList = Array.from(enabledCategories).sort().join(', ');
console.error(`[Flywheel] Tool categories: ${categoryList}`);

// ============================================================================
// Register tools based on enabled categories
// ============================================================================

// CORE: Essential vault health and metadata tools
if (shouldRegister('health', ['core'])) {
  registerHealthTools(server, () => vaultIndex, () => vaultPath);
}

if (shouldRegister('system', ['core'])) {
  registerSystemTools(
    server,
    () => vaultIndex,
    (newIndex) => { vaultIndex = newIndex; },
    () => vaultPath,
    (newConfig) => { flywheelConfig = newConfig; }
  );
}

// GRAPH: Link analysis and wikilink tools
if (shouldRegister('graph', ['graph'])) {
  registerGraphTools(server, () => vaultIndex, () => vaultPath);
}

if (shouldRegister('wikilinks', ['graph'])) {
  registerWikilinkTools(server, () => vaultIndex, () => vaultPath);
}

// SEARCH: Note search tools
if (shouldRegister('query', ['search'])) {
  registerQueryTools(server, () => vaultIndex, () => vaultPath, () => stateDb);
}

// PRIMITIVES: Contains tools for tasks, structure, temporal, schema, and graph-advanced
// Register if ANY of these categories are enabled
if (shouldRegister('primitives', ['tasks', 'structure', 'temporal', 'schema', 'advanced'])) {
  registerPrimitiveTools(server, () => vaultIndex, () => vaultPath, () => flywheelConfig);
}

// TEMPORAL: Periodic note detection
if (shouldRegister('periodic', ['temporal'])) {
  registerPeriodicTools(server, () => vaultIndex);
}

// SCHEMA: Folder conventions and schema inference
if (shouldRegister('schema', ['schema'])) {
  registerSchemaTools(server, () => vaultIndex, () => vaultPath);
}

// ADVANCED: Bidirectional bridge, computed frontmatter, migrations
if (shouldRegister('bidirectional', ['advanced'])) {
  registerBidirectionalTools(server, () => vaultIndex, () => vaultPath);
}

if (shouldRegister('computed', ['advanced'])) {
  registerComputedTools(server, () => vaultIndex, () => vaultPath);
}

if (shouldRegister('migrations', ['advanced'])) {
  registerMigrationTools(server, () => vaultIndex, () => vaultPath);
}

async function main() {
  // Start the MCP server FIRST (immediate - no waiting for index)
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error('Flywheel MCP server running on stdio');

  // Build the vault index in background (non-blocking)
  console.error('Building vault index in background...');
  const startTime = Date.now();

  buildVaultIndex(vaultPath)
    .then(async (index) => {
      vaultIndex = index;
      setIndexState('ready');
      const duration = Date.now() - startTime;
      console.error(`Vault index ready in ${duration}ms`);

      // Initialize StateDb (auto-creates if missing)
      try {
        stateDb = openStateDb(vaultPath);
        console.error('[Flywheel] StateDb initialized');

        // Auto-migrate from JSON on first run
        const legacyPaths = getLegacyPaths(vaultPath);
        const migration = await migrateFromJsonToSqlite(stateDb, legacyPaths);
        if (migration.entitiesMigrated > 0) {
          console.error(`[Flywheel] Migrated ${migration.entitiesMigrated} entities from JSON`);
        }
        if (migration.recencyMigrated > 0) {
          console.error(`[Flywheel] Migrated ${migration.recencyMigrated} recency records`);
        }
        if (migration.crankStateMigrated > 0) {
          console.error(`[Flywheel] Migrated ${migration.crankStateMigrated} crank state entries`);
        }
      } catch (err) {
        console.error('[Flywheel] StateDb init failed:', err);
        // Non-fatal - search_entities tool will return error but other tools work
      }

      // Export hub scores to entity cache (for Flywheel-Crank wikilink prioritization)
      // Also updates StateDb if available
      await exportHubScores(vaultPath, index, stateDb);

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

      // Setup file watcher (enabled by default, disable with FLYWHEEL_WATCH=false)
      if (process.env.FLYWHEEL_WATCH !== 'false') {
        // Use v2 watcher if: explicitly enabled OR polling is requested (polling requires v2)
        const useV2Watcher = process.env.FLYWHEEL_WATCH_V2 === 'true' ||
                             process.env.FLYWHEEL_WATCH_POLL === 'true';
        if (useV2Watcher) {
          const config = parseWatcherConfig();
          console.error(`[flywheel] File watcher v2 enabled (debounce: ${config.debounceMs}ms, flush: ${config.flushMs}ms)`);

          const watcher = createVaultWatcher({
            vaultPath,
            config,
            onBatch: async (batch) => {
              console.error(`[flywheel] Processing ${batch.events.length} file changes`);
              // For now, do full rebuild on batches (incremental is additive)
              // In future: use processBatchIncremental for true incremental updates
              const startTime = Date.now();
              try {
                vaultIndex = await buildVaultIndex(vaultPath);
                setIndexState('ready');
                console.error(`[flywheel] Index rebuilt in ${Date.now() - startTime}ms`);
                // Re-export hub scores after rebuild (includes StateDb update)
                await exportHubScores(vaultPath, vaultIndex, stateDb);
              } catch (err) {
                setIndexState('error');
                setIndexError(err instanceof Error ? err : new Error(String(err)));
                console.error('[flywheel] Failed to rebuild index:', err);
              }
            },
            onStateChange: (status) => {
              if (status.state === 'dirty') {
                console.error('[flywheel] Warning: Index may be stale');
              }
            },
            onError: (err) => {
              console.error('[flywheel] Watcher error:', err.message);
            },
          });

          watcher.start();
        } else {
          // Legacy watcher (global debounce)
          const debounceMs = parseInt(process.env.FLYWHEEL_DEBOUNCE_MS || '60000');
          console.error(`[flywheel] File watcher v1 enabled (debounce: ${debounceMs}ms)`);

          const legacyWatcher = chokidar.watch(vaultPath, {
            ignored: /(^|[\/\\])\../, // ignore dotfiles
            persistent: true,
            ignoreInitial: true,
            awaitWriteFinish: {
              stabilityThreshold: 300,
              pollInterval: 100
            }
          });

          let rebuildTimer: NodeJS.Timeout;
          legacyWatcher.on('all', (event, path) => {
            if (!path.endsWith('.md')) return;
            clearTimeout(rebuildTimer);
            rebuildTimer = setTimeout(() => {
              console.error('[flywheel] Rebuilding index (file changed)');
              buildVaultIndex(vaultPath)
                .then(async (index) => {
                  vaultIndex = index;
                  setIndexState('ready');
                  console.error('[flywheel] Index rebuilt successfully');
                  // Re-export hub scores after rebuild (includes StateDb update)
                  await exportHubScores(vaultPath, index, stateDb);
                })
                .catch((err) => {
                  setIndexState('error');
                  setIndexError(err instanceof Error ? err : new Error(String(err)));
                  console.error('[flywheel] Failed to rebuild index:', err);
                });
            }, debounceMs);
          });
        }
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
