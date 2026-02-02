/**
 * Hub score export - enriches entity cache with backlink counts
 *
 * After graph build, this module computes hub scores from backlinks
 * and writes them to the entity cache so Flywheel-Crank can use them
 * for wikilink prioritization.
 *
 * Architecture:
 * - Flywheel builds VaultIndex with backlinks (in-memory)
 * - This module exports hub scores to .claude/wikilink-entities.json
 * - Flywheel-Crank reads enriched cache for wikilink suggestions
 */

import fs from 'fs/promises';
import path from 'path';
import type { VaultIndex } from './types.js';
import { getBacklinksForNote, normalizeTarget } from './graph.js';
import type { StateDb } from '@velvetmonkey/vault-core';

/**
 * Entity cache structure (matches vault-core's EntityIndex)
 */
interface EntityWithAliases {
  name: string;
  path: string;
  aliases: string[];
  hubScore?: number;
}

type Entity = string | EntityWithAliases;

interface EntityIndex {
  technologies: Entity[];
  acronyms: Entity[];
  people: Entity[];
  projects: Entity[];
  organizations: Entity[];
  locations: Entity[];
  concepts: Entity[];
  other: Entity[];
  _metadata: {
    total_entities: number;
    generated_at: string;
    vault_path: string;
    source: string;
    version?: number;
  };
}

/**
 * Compute hub scores from the vault index
 *
 * Returns a map of normalized note path -> backlink count
 */
export function computeHubScores(index: VaultIndex): Map<string, number> {
  const hubScores = new Map<string, number>();

  for (const note of index.notes.values()) {
    const backlinks = getBacklinksForNote(index, note.path);
    const backlinkCount = backlinks.length;

    // Store by normalized path (lowercase, no .md)
    const normalizedPath = normalizeTarget(note.path);
    hubScores.set(normalizedPath, backlinkCount);

    // Also store by title for matching by name
    const title = note.title.toLowerCase();
    if (!hubScores.has(title) || backlinkCount > hubScores.get(title)!) {
      hubScores.set(title, backlinkCount);
    }
  }

  return hubScores;
}

/**
 * Enrich an entity with hub score
 */
function enrichEntity(entity: Entity, hubScores: Map<string, number>): EntityWithAliases {
  // Convert string entity to object
  const entityObj: EntityWithAliases = typeof entity === 'string'
    ? { name: entity, path: '', aliases: [] }
    : { ...entity };

  // Try to find hub score by path first, then by name
  let hubScore = 0;

  if (entityObj.path) {
    const normalizedPath = normalizeTarget(entityObj.path);
    hubScore = hubScores.get(normalizedPath) ?? 0;
  }

  if (hubScore === 0) {
    const normalizedName = entityObj.name.toLowerCase();
    hubScore = hubScores.get(normalizedName) ?? 0;
  }

  entityObj.hubScore = hubScore;
  return entityObj;
}

/**
 * Enrich all entities in an index with hub scores
 */
function enrichEntityIndex(index: EntityIndex, hubScores: Map<string, number>): EntityIndex {
  const categories: (keyof Omit<EntityIndex, '_metadata'>)[] = [
    'technologies',
    'acronyms',
    'people',
    'projects',
    'organizations',
    'locations',
    'concepts',
    'other',
  ];

  const enriched: EntityIndex = {
    ...index,
    _metadata: {
      ...index._metadata,
      generated_at: new Date().toISOString(),
    },
  };

  for (const category of categories) {
    if (enriched[category]) {
      enriched[category] = enriched[category].map(e => enrichEntity(e, hubScores));
    }
  }

  return enriched;
}

/**
 * Update hub scores directly in SQLite database
 *
 * @param stateDb - State database instance
 * @param hubScores - Map of entity name -> backlink count
 * @returns Number of entities updated
 */
function updateHubScoresInDb(stateDb: StateDb, hubScores: Map<string, number>): number {
  // Prepare an update statement for hub scores
  const updateStmt = stateDb.db.prepare(`
    UPDATE entities SET hub_score = ? WHERE name_lower = ?
  `);

  let updated = 0;
  const transaction = stateDb.db.transaction(() => {
    for (const [nameLower, score] of hubScores) {
      const result = updateStmt.run(score, nameLower);
      if (result.changes > 0) {
        updated++;
      }
    }
  });

  transaction();
  return updated;
}

/**
 * Export hub scores to the entity cache
 *
 * This reads the existing entity cache, enriches it with hub scores
 * computed from the vault index, and writes it back.
 *
 * When stateDb is provided, hub scores are also written to SQLite.
 *
 * @param vaultPath - Path to the vault
 * @param vaultIndex - Built vault index with backlinks
 * @param stateDb - Optional StateDb for SQLite storage
 * @returns Number of entities enriched, or -1 if cache doesn't exist
 */
export async function exportHubScores(
  vaultPath: string,
  vaultIndex: VaultIndex,
  stateDb?: StateDb | null
): Promise<number> {
  const cachePath = path.join(vaultPath, '.claude', 'wikilink-entities.json');

  // Check if cache exists
  try {
    await fs.access(cachePath);
  } catch {
    console.error('[Flywheel] Entity cache not found, skipping hub score export');
    return -1;
  }

  // Load existing cache
  let entityIndex: EntityIndex;
  try {
    const content = await fs.readFile(cachePath, 'utf-8');
    entityIndex = JSON.parse(content) as EntityIndex;
  } catch (e) {
    console.error('[Flywheel] Failed to load entity cache:', e);
    return -1;
  }

  // Compute hub scores from vault index
  const hubScores = computeHubScores(vaultIndex);
  console.error(`[Flywheel] Computed hub scores for ${hubScores.size} notes`);

  // Update hub scores in SQLite if available
  if (stateDb) {
    try {
      const dbUpdated = updateHubScoresInDb(stateDb, hubScores);
      console.error(`[Flywheel] Updated ${dbUpdated} hub scores in StateDb`);
    } catch (e) {
      console.error('[Flywheel] Failed to update hub scores in StateDb:', e);
      // Non-fatal - continue with JSON export
    }
  }

  // Enrich entities with hub scores
  const enriched = enrichEntityIndex(entityIndex, hubScores);

  // Count entities with hub scores > 0
  let hubCount = 0;
  const categories: (keyof Omit<EntityIndex, '_metadata'>)[] = [
    'technologies', 'acronyms', 'people', 'projects',
    'organizations', 'locations', 'concepts', 'other',
  ];
  for (const category of categories) {
    for (const entity of enriched[category] ?? []) {
      if (typeof entity !== 'string' && entity.hubScore && entity.hubScore > 0) {
        hubCount++;
      }
    }
  }

  // Save enriched cache
  try {
    await fs.writeFile(cachePath, JSON.stringify(enriched, null, 2), 'utf-8');
    console.error(`[Flywheel] Exported hub scores: ${hubCount} entities with backlinks`);
    return hubCount;
  } catch (e) {
    console.error('[Flywheel] Failed to save enriched entity cache:', e);
    return -1;
  }
}
