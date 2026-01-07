/**
 * Query tools - search notes by frontmatter, tags, and folders
 */

import { z } from 'zod';
import type { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import type { VaultIndex, VaultNote } from '../core/types.js';
import { MAX_LIMIT } from '../core/constants.js';

/**
 * Check if a note matches frontmatter filters
 */
function matchesFrontmatter(
  note: VaultNote,
  where: Record<string, unknown>
): boolean {
  for (const [key, value] of Object.entries(where)) {
    const noteValue = note.frontmatter[key];

    // Handle null/undefined
    if (value === null || value === undefined) {
      if (noteValue !== null && noteValue !== undefined) {
        return false;
      }
      continue;
    }

    // Handle arrays - check if any value matches
    if (Array.isArray(noteValue)) {
      if (!noteValue.some((v) => String(v).toLowerCase() === String(value).toLowerCase())) {
        return false;
      }
      continue;
    }

    // Handle string comparison (case-insensitive)
    if (typeof value === 'string' && typeof noteValue === 'string') {
      if (noteValue.toLowerCase() !== value.toLowerCase()) {
        return false;
      }
      continue;
    }

    // Handle other types (exact match)
    if (noteValue !== value) {
      return false;
    }
  }

  return true;
}

/**
 * Check if a note has a specific tag
 */
function hasTag(note: VaultNote, tag: string): boolean {
  const normalizedTag = tag.replace(/^#/, '').toLowerCase();
  return note.tags.some((t) => t.toLowerCase() === normalizedTag);
}

/**
 * Check if a note has any of the specified tags
 */
function hasAnyTag(note: VaultNote, tags: string[]): boolean {
  return tags.some((tag) => hasTag(note, tag));
}

/**
 * Check if a note has all of the specified tags
 */
function hasAllTags(note: VaultNote, tags: string[]): boolean {
  return tags.every((tag) => hasTag(note, tag));
}

/**
 * Check if a note is in a folder
 */
function inFolder(note: VaultNote, folder: string): boolean {
  const normalizedFolder = folder.endsWith('/') ? folder : folder + '/';
  return note.path.startsWith(normalizedFolder) || note.path.split('/')[0] === folder.replace('/', '');
}

/**
 * Sort notes by a field
 */
function sortNotes(
  notes: VaultNote[],
  sortBy: 'modified' | 'created' | 'title',
  order: 'asc' | 'desc'
): VaultNote[] {
  const sorted = [...notes];

  sorted.sort((a, b) => {
    let comparison = 0;

    switch (sortBy) {
      case 'modified':
        comparison = a.modified.getTime() - b.modified.getTime();
        break;
      case 'created':
        const aCreated = a.created || a.modified;
        const bCreated = b.created || b.modified;
        comparison = aCreated.getTime() - bCreated.getTime();
        break;
      case 'title':
        comparison = a.title.localeCompare(b.title);
        break;
    }

    return order === 'desc' ? -comparison : comparison;
  });

  return sorted;
}

/**
 * Register query tools
 */
export function registerQueryTools(
  server: McpServer,
  getIndex: () => VaultIndex,
  getVaultPath: () => string
): void {
  // search_notes - Search notes by frontmatter, tags, and folders
  const NoteResultSchema = z.object({
    path: z.string().describe('Path to the note'),
    title: z.string().describe('Note title'),
    modified: z.string().describe('Last modified date (ISO format)'),
    created: z.string().optional().describe('Creation date if available (ISO format)'),
    tags: z.array(z.string()).describe('Tags on this note'),
    frontmatter: z.record(z.unknown()).describe('Frontmatter fields'),
  });

  const SearchNotesOutputSchema = {
    query: z.object({
      where: z.record(z.unknown()).optional(),
      has_tag: z.string().optional(),
      has_any_tag: z.array(z.string()).optional(),
      has_all_tags: z.array(z.string()).optional(),
      folder: z.string().optional(),
      title_contains: z.string().optional(),
      sort_by: z.string().optional(),
      order: z.string().optional(),
      limit: z.number().optional(),
    }).describe('The search query that was executed'),
    total_matches: z.number().describe('Total number of matching notes'),
    returned: z.number().describe('Number of notes returned (may be limited)'),
    notes: z.array(NoteResultSchema).describe('Matching notes'),
  };

  type NoteResult = {
    path: string;
    title: string;
    modified: string;
    created?: string;
    tags: string[];
    frontmatter: Record<string, unknown>;
  };

  type SearchNotesOutput = {
    query: {
      where?: Record<string, unknown>;
      has_tag?: string;
      has_any_tag?: string[];
      has_all_tags?: string[];
      folder?: string;
      title_contains?: string;
      sort_by?: string;
      order?: string;
      limit?: number;
    };
    total_matches: number;
    returned: number;
    notes: NoteResult[];
  };

  server.registerTool(
    'search_notes',
    {
      title: 'Search Notes',
      description:
        'Search notes by frontmatter fields, tags, folders, or title. Covers ~80% of Dataview use cases.',
      inputSchema: {
        where: z
          .record(z.unknown())
          .optional()
          .describe('Frontmatter filters as key-value pairs. Example: { "type": "project", "status": "active" }'),
        has_tag: z
          .string()
          .optional()
          .describe('Filter to notes with this tag. Example: "work"'),
        has_any_tag: z
          .array(z.string())
          .optional()
          .describe('Filter to notes with any of these tags. Example: ["work", "personal"]'),
        has_all_tags: z
          .array(z.string())
          .optional()
          .describe('Filter to notes with all of these tags. Example: ["project", "active"]'),
        folder: z
          .string()
          .optional()
          .describe('Limit to notes in this folder. Example: "daily-notes"'),
        title_contains: z
          .string()
          .optional()
          .describe('Filter to notes whose title contains this text (case-insensitive)'),
        sort_by: z
          .enum(['modified', 'created', 'title'])
          .default('modified')
          .describe('Field to sort by'),
        order: z
          .enum(['asc', 'desc'])
          .default('desc')
          .describe('Sort order'),
        limit: z
          .number()
          .default(50)
          .describe('Maximum number of results to return'),
      },
      outputSchema: SearchNotesOutputSchema,
    },
    async ({
      where,
      has_tag,
      has_any_tag,
      has_all_tags,
      folder,
      title_contains,
      sort_by = 'modified',
      order = 'desc',
      limit: requestedLimit = 50,
    }): Promise<{
      content: Array<{ type: 'text'; text: string }>;
      structuredContent: SearchNotesOutput;
    }> => {
      const index = getIndex();

      // Cap limit to prevent massive payloads
      const limit = Math.min(requestedLimit, MAX_LIMIT);

      // Start with all notes
      let matchingNotes: VaultNote[] = Array.from(index.notes.values());

      // Apply filters
      if (where && Object.keys(where).length > 0) {
        matchingNotes = matchingNotes.filter((note) => matchesFrontmatter(note, where));
      }

      if (has_tag) {
        matchingNotes = matchingNotes.filter((note) => hasTag(note, has_tag));
      }

      if (has_any_tag && has_any_tag.length > 0) {
        matchingNotes = matchingNotes.filter((note) => hasAnyTag(note, has_any_tag));
      }

      if (has_all_tags && has_all_tags.length > 0) {
        matchingNotes = matchingNotes.filter((note) => hasAllTags(note, has_all_tags));
      }

      if (folder) {
        matchingNotes = matchingNotes.filter((note) => inFolder(note, folder));
      }

      if (title_contains) {
        const searchTerm = title_contains.toLowerCase();
        matchingNotes = matchingNotes.filter((note) =>
          note.title.toLowerCase().includes(searchTerm)
        );
      }

      // Sort
      matchingNotes = sortNotes(matchingNotes, sort_by, order);

      // Apply limit
      const totalMatches = matchingNotes.length;
      const limitedNotes = matchingNotes.slice(0, limit);

      // Format output
      const notes: NoteResult[] = limitedNotes.map((note) => ({
        path: note.path,
        title: note.title,
        modified: note.modified.toISOString(),
        created: note.created?.toISOString(),
        tags: note.tags,
        frontmatter: note.frontmatter,
      }));

      const output: SearchNotesOutput = {
        query: {
          where,
          has_tag,
          has_any_tag,
          has_all_tags,
          folder,
          title_contains,
          sort_by,
          order,
          limit,
        },
        total_matches: totalMatches,
        returned: notes.length,
        notes,
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
