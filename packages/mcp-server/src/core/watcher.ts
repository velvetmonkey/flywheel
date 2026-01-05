import chokidar from 'chokidar';
import { buildVaultIndex } from './graph.js';
import type { VaultIndex } from './types.js';

const DEBOUNCE_MS = 2000; // Wait 2s after last change before rebuilding

/**
 * Watch vault for file changes and automatically rebuild index.
 * Uses debouncing to batch rapid changes into a single rebuild.
 */
export function watchVault(
  vaultPath: string,
  onIndexRebuilt: (index: VaultIndex) => void
): chokidar.FSWatcher {
  let debounceTimer: NodeJS.Timeout | null = null;
  let isRebuilding = false;

  const watcher = chokidar.watch('**/*.md', {
    cwd: vaultPath,
    ignored: [
      '**/node_modules/**',
      '**/.git/**',
      '**/.obsidian/**',
      '**/.trash/**',
    ],
    ignoreInitial: true, // Don't trigger on startup scan
    persistent: true,
  });

  const scheduleRebuild = (eventPath: string) => {
    // Clear any pending rebuild
    if (debounceTimer) {
      clearTimeout(debounceTimer);
    }

    debounceTimer = setTimeout(async () => {
      // Skip if already rebuilding
      if (isRebuilding) {
        return;
      }

      isRebuilding = true;
      console.error('[Flywheel] File changes detected, rebuilding index...');

      try {
        const startTime = Date.now();
        const newIndex = await buildVaultIndex(vaultPath);
        const duration = Date.now() - startTime;
        onIndexRebuilt(newIndex);
        console.error(
          `[Flywheel] Index rebuilt: ${newIndex.notes.size} notes (${duration}ms)`
        );
      } catch (err) {
        console.error('[Flywheel] Index rebuild failed:', err);
      } finally {
        isRebuilding = false;
      }
    }, DEBOUNCE_MS);
  };

  watcher
    .on('add', (path) => scheduleRebuild(path))
    .on('change', (path) => scheduleRebuild(path))
    .on('unlink', (path) => scheduleRebuild(path))
    .on('error', (error) => {
      console.error('[Flywheel] Watcher error:', error);
    });

  console.error('[Flywheel] File watcher started');
  return watcher;
}
