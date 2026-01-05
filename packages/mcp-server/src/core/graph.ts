/**
 * Graph builder - builds VaultIndex from parsed notes
 *
 * Performance features:
 * - Parallel parsing with concurrency limit
 * - Progress reporting for large vaults
 * - Timeout protection
 */

import type { VaultNote, VaultIndex, Backlink } from './types.js';
import type { VaultFile } from './vault.js';
import { scanVault } from './vault.js';
import { parseNote } from './parser.js';

/** Default timeout for vault indexing (5 minutes) */
const DEFAULT_TIMEOUT_MS = 5 * 60 * 1000;

/** Concurrency limit for parallel file parsing */
const PARSE_CONCURRENCY = 50;

/** Progress reporting interval (every N files) */
const PROGRESS_INTERVAL = 100;

/**
 * Normalize a link target for matching
 * - Lowercase for case-insensitive matching
 * - Remove .md extension if present
 */
export function normalizeTarget(target: string): string {
  return target.toLowerCase().replace(/\.md$/, '');
}

/**
 * Normalize a note path to a matchable key
 * - Remove .md extension
 * - Lowercase
 */
function normalizeNotePath(path: string): string {
  return path.toLowerCase().replace(/\.md$/, '');
}

/**
 * Get the title from a path (filename without extension)
 */
function getTitleFromPath(path: string): string {
  return path.replace(/\.md$/, '').split('/').pop() || path;
}

/** Options for building the vault index */
export interface BuildOptions {
  /** Timeout in milliseconds (default: 5 minutes) */
  timeoutMs?: number;
  /** Callback for progress updates */
  onProgress?: (parsed: number, total: number) => void;
}

/**
 * Build the complete vault index with timeout protection
 */
export async function buildVaultIndex(
  vaultPath: string,
  options: BuildOptions = {}
): Promise<VaultIndex> {
  const { timeoutMs = DEFAULT_TIMEOUT_MS, onProgress } = options;

  console.error(`Scanning vault: ${vaultPath}`);
  const startTime = Date.now();

  // Create timeout promise
  const timeoutPromise = new Promise<never>((_, reject) => {
    setTimeout(() => {
      reject(new Error(`Vault indexing timed out after ${timeoutMs / 1000}s`));
    }, timeoutMs);
  });

  // Run indexing with timeout
  return Promise.race([
    buildVaultIndexInternal(vaultPath, startTime, onProgress),
    timeoutPromise,
  ]);
}

/**
 * Internal implementation of vault index building
 */
async function buildVaultIndexInternal(
  vaultPath: string,
  startTime: number,
  onProgress?: (parsed: number, total: number) => void
): Promise<VaultIndex> {
  // Scan for files
  const files = await scanVault(vaultPath);
  console.error(`Found ${files.length} markdown files`);

  // Parse all notes with concurrency control
  const notes = new Map<string, VaultNote>();
  const parseErrors: string[] = [];
  let parsedCount = 0;

  // Process files in batches for controlled concurrency
  for (let i = 0; i < files.length; i += PARSE_CONCURRENCY) {
    const batch = files.slice(i, i + PARSE_CONCURRENCY);

    const results = await Promise.allSettled(
      batch.map(async (file) => {
        const note = await parseNote(file);
        return { file, note };
      })
    );

    for (const result of results) {
      if (result.status === 'fulfilled') {
        notes.set(result.value.note.path, result.value.note);
      } else {
        // Extract file path from the batch (best effort)
        const batchIndex = results.indexOf(result);
        if (batchIndex >= 0 && batch[batchIndex]) {
          parseErrors.push(batch[batchIndex].path);
        }
      }
      parsedCount++;
    }

    // Progress reporting
    if (parsedCount % PROGRESS_INTERVAL === 0 || parsedCount === files.length) {
      const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);
      console.error(`Parsed ${parsedCount}/${files.length} files (${elapsed}s)`);
      onProgress?.(parsedCount, files.length);
    }
  }

  if (parseErrors.length > 0) {
    console.error(`Failed to parse ${parseErrors.length} files`);
  }

  // Build entities map (for resolving link targets)
  // Maps: normalized title/alias -> path
  const entities = new Map<string, string>();

  for (const note of notes.values()) {
    // Map by title
    const normalizedTitle = normalizeTarget(note.title);
    if (!entities.has(normalizedTitle)) {
      entities.set(normalizedTitle, note.path);
    }

    // Map by full path (without extension)
    const normalizedPath = normalizeNotePath(note.path);
    entities.set(normalizedPath, note.path);

    // Map by aliases
    for (const alias of note.aliases) {
      const normalizedAlias = normalizeTarget(alias);
      if (!entities.has(normalizedAlias)) {
        entities.set(normalizedAlias, note.path);
      }
    }
  }

  // Build backlinks index
  // Maps: normalized target -> backlinks from sources
  const backlinks = new Map<string, Backlink[]>();

  for (const note of notes.values()) {
    for (const link of note.outlinks) {
      const normalizedTarget = normalizeTarget(link.target);

      // Resolve the target to an actual note path if possible
      const targetPath = entities.get(normalizedTarget);
      const key = targetPath ? normalizeNotePath(targetPath) : normalizedTarget;

      if (!backlinks.has(key)) {
        backlinks.set(key, []);
      }

      backlinks.get(key)!.push({
        source: note.path,
        line: link.line,
        // Context will be loaded on-demand to save memory
      });
    }
  }

  // Build tags index
  const tags = new Map<string, Set<string>>();

  for (const note of notes.values()) {
    for (const tag of note.tags) {
      if (!tags.has(tag)) {
        tags.set(tag, new Set());
      }
      tags.get(tag)!.add(note.path);
    }
  }

  console.error(`Index built: ${notes.size} notes, ${entities.size} entities, ${backlinks.size} link targets, ${tags.size} tags`);

  return {
    notes,
    backlinks,
    entities,
    tags,
    builtAt: new Date(),
  };
}

/**
 * Resolve a link target to a note path
 * Returns undefined if the target doesn't match any note
 */
export function resolveTarget(index: VaultIndex, target: string): string | undefined {
  const normalized = normalizeTarget(target);
  return index.entities.get(normalized);
}

/**
 * Get backlinks for a note
 */
export function getBacklinksForNote(index: VaultIndex, notePath: string): Backlink[] {
  const normalized = normalizeNotePath(notePath);
  return index.backlinks.get(normalized) || [];
}

/**
 * Get forward links (outlinks) for a note with resolution info
 */
export function getForwardLinksForNote(
  index: VaultIndex,
  notePath: string
): Array<{ target: string; alias?: string; line: number; resolvedPath?: string; exists: boolean }> {
  const note = index.notes.get(notePath);
  if (!note) return [];

  return note.outlinks.map((link) => {
    const resolvedPath = resolveTarget(index, link.target);
    return {
      target: link.target,
      alias: link.alias,
      line: link.line,
      resolvedPath,
      exists: resolvedPath !== undefined,
    };
  });
}

/**
 * Find orphan notes (notes with no backlinks)
 */
export function findOrphanNotes(
  index: VaultIndex,
  folder?: string
): Array<{ path: string; title: string; modified: Date }> {
  const orphans: Array<{ path: string; title: string; modified: Date }> = [];

  for (const note of index.notes.values()) {
    // Filter by folder if specified
    if (folder && !note.path.startsWith(folder)) {
      continue;
    }

    // Check if this note has any backlinks
    const backlinks = getBacklinksForNote(index, note.path);
    if (backlinks.length === 0) {
      orphans.push({
        path: note.path,
        title: note.title,
        modified: note.modified,
      });
    }
  }

  // Sort by modified date (most recent first)
  return orphans.sort((a, b) => b.modified.getTime() - a.modified.getTime());
}

/**
 * Find hub notes (highly connected notes)
 */
export function findHubNotes(
  index: VaultIndex,
  minLinks: number = 5
): Array<{
  path: string;
  title: string;
  backlink_count: number;
  forward_link_count: number;
  total_connections: number;
}> {
  const hubs: Array<{
    path: string;
    title: string;
    backlink_count: number;
    forward_link_count: number;
    total_connections: number;
  }> = [];

  for (const note of index.notes.values()) {
    const backlinkCount = getBacklinksForNote(index, note.path).length;
    const forwardLinkCount = note.outlinks.length;
    const totalConnections = backlinkCount + forwardLinkCount;

    if (totalConnections >= minLinks) {
      hubs.push({
        path: note.path,
        title: note.title,
        backlink_count: backlinkCount,
        forward_link_count: forwardLinkCount,
        total_connections: totalConnections,
      });
    }
  }

  // Sort by total connections (highest first)
  return hubs.sort((a, b) => b.total_connections - a.total_connections);
}

/**
 * Calculate Levenshtein distance between two strings
 * Returns the minimum number of single-character edits needed
 */
export function levenshteinDistance(a: string, b: string): number {
  if (a.length === 0) return b.length;
  if (b.length === 0) return a.length;

  const matrix: number[][] = [];

  // Initialize first column
  for (let i = 0; i <= b.length; i++) {
    matrix[i] = [i];
  }

  // Initialize first row
  for (let j = 0; j <= a.length; j++) {
    matrix[0][j] = j;
  }

  // Fill in the rest of the matrix
  for (let i = 1; i <= b.length; i++) {
    for (let j = 1; j <= a.length; j++) {
      if (b.charAt(i - 1) === a.charAt(j - 1)) {
        matrix[i][j] = matrix[i - 1][j - 1];
      } else {
        matrix[i][j] = Math.min(
          matrix[i - 1][j - 1] + 1, // substitution
          matrix[i][j - 1] + 1,     // insertion
          matrix[i - 1][j] + 1      // deletion
        );
      }
    }
  }

  return matrix[b.length][a.length];
}

/**
 * Find a similar entity in the index (for detecting typos/broken links)
 * Returns the path of the best matching note, or undefined if no close match
 *
 * Threshold based on string length:
 * - Length ≤ 5: max distance 1
 * - Length ≤ 10: max distance 2
 * - Length > 10: max distance 3
 *
 * Optimizations:
 * - Skip entities where length difference > maxDist (impossible to match)
 * - Early termination on distance=1 match (can't do better for typos)
 */
export function findSimilarEntity(
  index: VaultIndex,
  target: string
): { path: string; entity: string; distance: number } | undefined {
  const normalized = normalizeTarget(target);
  const normalizedLen = normalized.length;
  const maxDist = normalizedLen <= 5 ? 1 : normalizedLen <= 10 ? 2 : 3;

  let bestMatch: { path: string; entity: string; distance: number } | undefined;

  for (const [entity, path] of index.entities) {
    // Optimization 1: Skip if length difference exceeds maxDist
    // (Levenshtein distance >= |len(a) - len(b)|)
    const lenDiff = Math.abs(entity.length - normalizedLen);
    if (lenDiff > maxDist) {
      continue;
    }

    const dist = levenshteinDistance(normalized, entity);
    if (dist > 0 && dist <= maxDist) {
      if (!bestMatch || dist < bestMatch.distance) {
        bestMatch = { path, entity, distance: dist };

        // Optimization 2: Early termination on distance=1
        // (distance=0 means exact match, which resolveTarget would have found)
        if (dist === 1) {
          return bestMatch;
        }
      }
    }
  }

  return bestMatch;
}
