/**
 * Vault health tools - diagnostics and statistics
 */

import * as fs from 'fs';
import { z } from 'zod';
import type { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import type { VaultIndex } from '../core/types.js';
import { resolveTarget, getBacklinksForNote } from '../core/graph.js';

/** Staleness threshold in seconds (5 minutes) */
const STALE_THRESHOLD_SECONDS = 300;

/**
 * Register vault health tools
 */
export function registerHealthTools(
  server: McpServer,
  getIndex: () => VaultIndex,
  getVaultPath: () => string
): void {
  // health_check - MCP server health status (Gate 5: MCP Connection Verification)
  const HealthCheckOutputSchema = {
    status: z.enum(['healthy', 'degraded', 'unhealthy']).describe('Overall health status'),
    vault_accessible: z.boolean().describe('Whether the vault path is accessible'),
    vault_path: z.string().describe('The vault path being used'),
    index_built: z.boolean().describe('Whether the index has been built'),
    index_age_seconds: z.number().describe('Seconds since the index was built'),
    index_stale: z.boolean().describe('Whether the index is stale (>5 minutes old)'),
    note_count: z.number().describe('Number of notes in the index'),
    entity_count: z.number().describe('Number of linkable entities (titles + aliases)'),
    tag_count: z.number().describe('Number of unique tags'),
    recommendations: z.array(z.string()).describe('Suggested actions if any issues detected'),
  };

  type HealthCheckOutput = {
    status: 'healthy' | 'degraded' | 'unhealthy';
    vault_accessible: boolean;
    vault_path: string;
    index_built: boolean;
    index_age_seconds: number;
    index_stale: boolean;
    note_count: number;
    entity_count: number;
    tag_count: number;
    recommendations: string[];
  };

  server.registerTool(
    'health_check',
    {
      title: 'Health Check',
      description:
        'Check MCP server health status. Returns vault accessibility, index freshness, and recommendations. Use at session start to verify MCP is working correctly.',
      inputSchema: {},
      outputSchema: HealthCheckOutputSchema,
    },
    async (): Promise<{
      content: Array<{ type: 'text'; text: string }>;
      structuredContent: HealthCheckOutput;
    }> => {
      const index = getIndex();
      const vaultPath = getVaultPath();
      const recommendations: string[] = [];

      // Check vault accessibility
      let vaultAccessible = false;
      try {
        fs.accessSync(vaultPath, fs.constants.R_OK);
        vaultAccessible = true;
      } catch {
        vaultAccessible = false;
        recommendations.push('Vault path is not accessible. Check PROJECT_PATH environment variable.');
      }

      // Check index status
      const indexBuilt = index !== undefined && index.notes !== undefined;
      const indexAge = indexBuilt && index.builtAt
        ? Math.floor((Date.now() - index.builtAt.getTime()) / 1000)
        : -1;
      const indexStale = indexAge > STALE_THRESHOLD_SECONDS;

      if (indexStale) {
        recommendations.push(`Index is ${Math.floor(indexAge / 60)} minutes old. Consider running refresh_index.`);
      }

      // Count metrics
      const noteCount = indexBuilt ? index.notes.size : 0;
      const entityCount = indexBuilt ? index.entities.size : 0;
      const tagCount = indexBuilt ? index.tags.size : 0;

      if (noteCount === 0 && vaultAccessible) {
        recommendations.push('No notes found in vault. Is PROJECT_PATH pointing to a markdown vault?');
      }

      // Determine overall status
      let status: 'healthy' | 'degraded' | 'unhealthy';
      if (!vaultAccessible || !indexBuilt) {
        status = 'unhealthy';
      } else if (indexStale || recommendations.length > 0) {
        status = 'degraded';
      } else {
        status = 'healthy';
      }

      const output: HealthCheckOutput = {
        status,
        vault_accessible: vaultAccessible,
        vault_path: vaultPath,
        index_built: indexBuilt,
        index_age_seconds: indexAge,
        index_stale: indexStale,
        note_count: noteCount,
        entity_count: entityCount,
        tag_count: tagCount,
        recommendations,
      };

      return {
        content: [
          {
            type: 'text',
            text: JSON.stringify(output, null, 2),
          },
        ],
        structuredContent: output,
      };
    }
  );

  // find_broken_links - Find all broken links in the vault
  const BrokenLinkSchema = z.object({
    source: z.string().describe('Path to the note containing the broken link'),
    target: z.string().describe('The broken link target'),
    line: z.number().describe('Line number where the link appears'),
  });

  const FindBrokenLinksOutputSchema = {
    scope: z.string().describe('Folder searched, or "all" for entire vault'),
    broken_count: z.number().describe('Total number of broken links found'),
    returned_count: z.number().describe('Number of broken links returned (may be limited)'),
    affected_notes: z.number().describe('Number of notes with broken links'),
    broken_links: z.array(BrokenLinkSchema).describe('List of broken links'),
  };

  type BrokenLink = {
    source: string;
    target: string;
    line: number;
  };

  type FindBrokenLinksOutput = {
    scope: string;
    broken_count: number;
    returned_count: number;
    affected_notes: number;
    broken_links: BrokenLink[];
  };

  server.registerTool(
    'find_broken_links',
    {
      title: 'Find Broken Links',
      description:
        'Find all wikilinks that point to non-existent notes. Useful for vault maintenance.',
      inputSchema: {
        folder: z.string().optional().describe('Limit search to a specific folder (e.g., "daily-notes/")'),
        limit: z.number().default(50).describe('Maximum number of results to return'),
        offset: z.number().default(0).describe('Number of results to skip (for pagination)'),
      },
      outputSchema: FindBrokenLinksOutputSchema,
    },
    async ({ folder, limit, offset }): Promise<{
      content: Array<{ type: 'text'; text: string }>;
      structuredContent: FindBrokenLinksOutput;
    }> => {
      const index = getIndex();
      const allBrokenLinks: BrokenLink[] = [];
      const affectedNotes = new Set<string>();

      for (const note of index.notes.values()) {
        // Filter by folder if specified
        if (folder && !note.path.startsWith(folder)) {
          continue;
        }

        for (const link of note.outlinks) {
          const resolved = resolveTarget(index, link.target);
          if (!resolved) {
            allBrokenLinks.push({
              source: note.path,
              target: link.target,
              line: link.line,
            });
            affectedNotes.add(note.path);
          }
        }
      }

      // Sort by source path, then line number
      allBrokenLinks.sort((a, b) => {
        const pathCompare = a.source.localeCompare(b.source);
        if (pathCompare !== 0) return pathCompare;
        return a.line - b.line;
      });

      const brokenLinks = allBrokenLinks.slice(offset, offset + limit);

      const output: FindBrokenLinksOutput = {
        scope: folder || 'all',
        broken_count: allBrokenLinks.length,
        returned_count: brokenLinks.length,
        affected_notes: affectedNotes.size,
        broken_links: brokenLinks,
      };

      return {
        content: [
          {
            type: 'text',
            text: JSON.stringify(output, null, 2),
          },
        ],
        structuredContent: output,
      };
    }
  );

  // get_vault_stats - Comprehensive vault statistics
  const TagStatSchema = z.object({
    tag: z.string().describe('The tag name'),
    count: z.number().describe('Number of notes with this tag'),
  });

  const FolderStatSchema = z.object({
    folder: z.string().describe('Folder path'),
    note_count: z.number().describe('Number of notes in this folder'),
  });

  const OrphanStatsSchema = z.object({
    total: z.number().describe('Total orphan notes (no backlinks)'),
    periodic: z.number().describe('Orphan periodic notes (daily/weekly/monthly - expected)'),
    content: z.number().describe('Orphan content notes (non-periodic - may need linking)'),
  });

  const GetVaultStatsOutputSchema = {
    total_notes: z.number().describe('Total number of notes in the vault'),
    total_links: z.number().describe('Total number of wikilinks'),
    total_tags: z.number().describe('Total number of unique tags'),
    orphan_notes: OrphanStatsSchema.describe('Orphan notes breakdown'),
    broken_links: z.number().describe('Links pointing to non-existent notes'),
    average_links_per_note: z.number().describe('Average outgoing links per note'),
    most_linked_notes: z
      .array(
        z.object({
          path: z.string(),
          backlinks: z.number(),
        })
      )
      .describe('Top 10 most linked-to notes'),
    top_tags: z.array(TagStatSchema).describe('Top 20 most used tags'),
    folders: z.array(FolderStatSchema).describe('Note counts by top-level folder'),
  };

  type VaultStatsOutput = {
    total_notes: number;
    total_links: number;
    total_tags: number;
    orphan_notes: {
      total: number;
      periodic: number;
      content: number;
    };
    broken_links: number;
    average_links_per_note: number;
    most_linked_notes: Array<{ path: string; backlinks: number }>;
    top_tags: Array<{ tag: string; count: number }>;
    folders: Array<{ folder: string; note_count: number }>;
  };

  /**
   * Check if a note is a periodic note (daily, weekly, monthly, quarterly, yearly).
   * Periodic notes naturally have fewer backlinks - they're time-based, not topic-based.
   */
  function isPeriodicNote(path: string): boolean {
    const filename = path.split('/').pop() || '';
    const nameWithoutExt = filename.replace(/\.md$/, '');

    // Date patterns for periodic notes
    const patterns = [
      /^\d{4}-\d{2}-\d{2}$/,           // YYYY-MM-DD (daily)
      /^\d{4}-W\d{2}$/,                // YYYY-Wnn (weekly)
      /^\d{4}-\d{2}$/,                 // YYYY-MM (monthly)
      /^\d{4}-Q[1-4]$/,                // YYYY-Qn (quarterly)
      /^\d{4}$/,                       // YYYY (yearly)
    ];

    // Also check common folder names
    const periodicFolders = ['daily', 'weekly', 'monthly', 'quarterly', 'yearly', 'journal', 'journals'];
    const folder = path.split('/')[0]?.toLowerCase() || '';

    return patterns.some(p => p.test(nameWithoutExt)) || periodicFolders.includes(folder);
  }

  server.registerTool(
    'get_vault_stats',
    {
      title: 'Get Vault Statistics',
      description:
        'Get comprehensive statistics about the vault: note counts, link metrics, tag usage, and folder distribution.',
      inputSchema: {},
      outputSchema: GetVaultStatsOutputSchema,
    },
    async (): Promise<{
      content: Array<{ type: 'text'; text: string }>;
      structuredContent: VaultStatsOutput;
    }> => {
      const index = getIndex();

      // Count totals
      const totalNotes = index.notes.size;
      let totalLinks = 0;
      let brokenLinks = 0;
      let orphanTotal = 0;
      let orphanPeriodic = 0;
      let orphanContent = 0;

      // Count links and broken links
      for (const note of index.notes.values()) {
        totalLinks += note.outlinks.length;

        for (const link of note.outlinks) {
          if (!resolveTarget(index, link.target)) {
            brokenLinks++;
          }
        }
      }

      // Count orphans, separating periodic notes from content notes
      for (const note of index.notes.values()) {
        const backlinks = getBacklinksForNote(index, note.path);
        if (backlinks.length === 0) {
          orphanTotal++;
          if (isPeriodicNote(note.path)) {
            orphanPeriodic++;
          } else {
            orphanContent++;
          }
        }
      }

      // Calculate most linked notes
      const linkCounts: Array<{ path: string; backlinks: number }> = [];
      for (const note of index.notes.values()) {
        const backlinks = getBacklinksForNote(index, note.path);
        if (backlinks.length > 0) {
          linkCounts.push({ path: note.path, backlinks: backlinks.length });
        }
      }
      linkCounts.sort((a, b) => b.backlinks - a.backlinks);
      const mostLinkedNotes = linkCounts.slice(0, 10);

      // Calculate top tags
      const tagStats: Array<{ tag: string; count: number }> = [];
      for (const [tag, notes] of index.tags) {
        tagStats.push({ tag, count: notes.size });
      }
      tagStats.sort((a, b) => b.count - a.count);
      const topTags = tagStats.slice(0, 20);

      // Calculate folder distribution
      const folderCounts = new Map<string, number>();
      for (const note of index.notes.values()) {
        const parts = note.path.split('/');
        const folder = parts.length > 1 ? parts[0] : '(root)';

        folderCounts.set(folder, (folderCounts.get(folder) || 0) + 1);
      }

      const folders = Array.from(folderCounts.entries())
        .map(([folder, count]) => ({ folder, note_count: count }))
        .sort((a, b) => b.note_count - a.note_count);

      const output: VaultStatsOutput = {
        total_notes: totalNotes,
        total_links: totalLinks,
        total_tags: index.tags.size,
        orphan_notes: {
          total: orphanTotal,
          periodic: orphanPeriodic,
          content: orphanContent,
        },
        broken_links: brokenLinks,
        average_links_per_note: totalNotes > 0 ? Math.round((totalLinks / totalNotes) * 100) / 100 : 0,
        most_linked_notes: mostLinkedNotes,
        top_tags: topTags,
        folders,
      };

      return {
        content: [
          {
            type: 'text',
            text: JSON.stringify(output, null, 2),
          },
        ],
        structuredContent: output,
      };
    }
  );
}
