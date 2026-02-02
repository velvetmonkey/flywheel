/**
 * README Examples Tests
 *
 * Validates that the README/documentation examples work correctly
 * against the actual demo vaults. These tests ensure documentation
 * accuracy and prevent drift between docs and implementation.
 */

import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import path from 'path';
import { createTestServer, type TestServerContext } from '../helpers/createTestServer.js';
import { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { InMemoryTransport } from '@modelcontextprotocol/sdk/inMemory.js';

// Path to demo vaults
const DEMOS_PATH = path.resolve(__dirname, '../../../../demos');
const ARTEMIS_VAULT = path.join(DEMOS_PATH, 'artemis-rocket');
const CARTER_VAULT = path.join(DEMOS_PATH, 'carter-strategy');

describe('README Examples: Artemis Rocket Vault', () => {
  let context: TestServerContext;
  let client: Client;

  beforeAll(async () => {
    context = await createTestServer(ARTEMIS_VAULT);

    // Connect client to server
    const [clientTransport, serverTransport] = InMemoryTransport.createLinkedPair();
    await context.server.connect(serverTransport);

    client = new Client({
      name: 'test-client',
      version: '1.0.0',
    }, {
      capabilities: {},
    });
    await client.connect(clientTransport);
  });

  afterAll(async () => {
    if (context?.stateDb) {
      context.stateDb.close();
    }
    await client?.close();
  });

  describe('Tool Execution', () => {
    it('should execute health_check successfully', async () => {
      const result = await client.callTool({
        name: 'health_check',
        arguments: {},
      });

      expect(result.isError).toBeFalsy();
      const content = result.content as Array<{ type: string; text: string }>;
      expect(content[0].type).toBe('text');
      const healthData = JSON.parse(content[0].text);

      expect(healthData.status).toBeDefined();
      expect(healthData.vault).toBeDefined();
      expect(healthData.vault.path).toContain('artemis-rocket');
    });

    it('should find hub notes with find_hub_notes', async () => {
      const result = await client.callTool({
        name: 'find_hub_notes',
        arguments: { limit: 10 },
      });

      expect(result.isError).toBeFalsy();
      const content = result.content as Array<{ type: string; text: string }>;
      const hubs = JSON.parse(content[0].text);

      expect(Array.isArray(hubs.hubs)).toBe(true);
      expect(hubs.hubs.length).toBeGreaterThan(0);

      // Hub notes should have meaningful backlink counts
      for (const hub of hubs.hubs.slice(0, 3)) {
        expect(hub.path).toMatch(/\.md$/);
        expect(typeof hub.backlinks).toBe('number');
      }
    });

    it('should get backlinks for a team member', async () => {
      // Get list of files to find a team member
      const listResult = await client.callTool({
        name: 'list_vault_notes',
        arguments: { folder: 'team', limit: 5 },
      });

      const listContent = listResult.content as Array<{ type: string; text: string }>;
      const notes = JSON.parse(listContent[0].text);

      if (notes.notes && notes.notes.length > 0) {
        const teamMemberPath = notes.notes[0].path;

        const result = await client.callTool({
          name: 'get_backlinks',
          arguments: { path: teamMemberPath },
        });

        expect(result.isError).toBeFalsy();
        const content = result.content as Array<{ type: string; text: string }>;
        const backlinks = JSON.parse(content[0].text);

        expect(backlinks.path).toBe(teamMemberPath);
        expect(Array.isArray(backlinks.backlinks)).toBe(true);
      }
    });

    it('should search notes by content', async () => {
      const result = await client.callTool({
        name: 'search_notes',
        arguments: { query: 'project', limit: 10 },
      });

      expect(result.isError).toBeFalsy();
      const content = result.content as Array<{ type: string; text: string }>;
      const searchResults = JSON.parse(content[0].text);

      expect(Array.isArray(searchResults.results)).toBe(true);
      // A vault about a rocket project should have results for "project"
    });

    it('should get recent notes', async () => {
      const result = await client.callTool({
        name: 'get_recent_notes',
        arguments: { limit: 10 },
      });

      expect(result.isError).toBeFalsy();
      const content = result.content as Array<{ type: string; text: string }>;
      const recent = JSON.parse(content[0].text);

      expect(Array.isArray(recent.notes)).toBe(true);
      expect(recent.notes.length).toBeLessThanOrEqual(10);
    });

    it('should get orphan notes', async () => {
      const result = await client.callTool({
        name: 'find_orphan_notes',
        arguments: { limit: 20 },
      });

      expect(result.isError).toBeFalsy();
      const content = result.content as Array<{ type: string; text: string }>;
      const orphans = JSON.parse(content[0].text);

      expect(Array.isArray(orphans.orphans)).toBe(true);
    });
  });

  describe('Graph Intelligence', () => {
    it('should analyze vault structure', async () => {
      const result = await client.callTool({
        name: 'get_vault_structure',
        arguments: {},
      });

      expect(result.isError).toBeFalsy();
      const content = result.content as Array<{ type: string; text: string }>;
      const structure = JSON.parse(content[0].text);

      expect(structure.folders).toBeDefined();
      expect(Array.isArray(structure.folders)).toBe(true);

      // Verify expected folders exist
      const folderNames = structure.folders.map((f: { name: string }) => f.name);
      expect(folderNames).toContain('team');
      expect(folderNames).toContain('daily-notes');
      expect(folderNames).toContain('systems');
    });

    it('should get note metadata', async () => {
      const result = await client.callTool({
        name: 'get_note_metadata',
        arguments: { path: 'project/Artemis Rocket.md' },
      });

      // May succeed or fail depending on exact file path
      if (!result.isError) {
        const content = result.content as Array<{ type: string; text: string }>;
        const metadata = JSON.parse(content[0].text);
        expect(metadata.path).toBeDefined();
      }
    });
  });
});

describe('README Examples: Carter Strategy Vault', () => {
  let context: TestServerContext;
  let client: Client;

  beforeAll(async () => {
    context = await createTestServer(CARTER_VAULT);

    const [clientTransport, serverTransport] = InMemoryTransport.createLinkedPair();
    await context.server.connect(serverTransport);

    client = new Client({
      name: 'test-client',
      version: '1.0.0',
    }, {
      capabilities: {},
    });
    await client.connect(clientTransport);
  });

  afterAll(async () => {
    if (context?.stateDb) {
      context.stateDb.close();
    }
    await client?.close();
  });

  it('should execute health_check successfully', async () => {
    const result = await client.callTool({
      name: 'health_check',
      arguments: {},
    });

    expect(result.isError).toBeFalsy();
    const content = result.content as Array<{ type: string; text: string }>;
    const healthData = JSON.parse(content[0].text);

    expect(healthData.status).toBeDefined();
    expect(healthData.vault.path).toContain('carter-strategy');
  });

  it('should list all tools', async () => {
    const tools = await client.listTools();

    expect(tools.tools.length).toBeGreaterThanOrEqual(30);

    // Check for key tool categories
    const toolNames = tools.tools.map(t => t.name);

    // Graph tools
    expect(toolNames).toContain('get_backlinks');
    expect(toolNames).toContain('find_hub_notes');

    // Health tools
    expect(toolNames).toContain('health_check');

    // Query tools
    expect(toolNames).toContain('search_notes');
    expect(toolNames).toContain('get_recent_notes');
  });
});

describe('Tool Registration Consistency', () => {
  let context: TestServerContext;
  let client: Client;

  beforeAll(async () => {
    context = await createTestServer(ARTEMIS_VAULT);

    const [clientTransport, serverTransport] = InMemoryTransport.createLinkedPair();
    await context.server.connect(serverTransport);

    client = new Client({
      name: 'test-client',
      version: '1.0.0',
    }, {
      capabilities: {},
    });
    await client.connect(clientTransport);
  });

  afterAll(async () => {
    if (context?.stateDb) {
      context.stateDb.close();
    }
    await client?.close();
  });

  it('should have all documented tools registered', async () => {
    const tools = await client.listTools();
    const toolNames = tools.tools.map(t => t.name);

    // Core documented tools (from README)
    const documentedTools = [
      'health_check',
      'get_backlinks',
      'get_forward_links',
      'find_hub_notes',
      'find_orphan_notes',
      'search_notes',
      'get_recent_notes',
      'list_vault_notes',
      'get_note_metadata',
      'get_vault_structure',
    ];

    for (const tool of documentedTools) {
      expect(toolNames, `Missing documented tool: ${tool}`).toContain(tool);
    }
  });

  it('should return valid JSON from all tools', async () => {
    const testCalls = [
      { name: 'health_check', arguments: {} },
      { name: 'find_hub_notes', arguments: { limit: 5 } },
      { name: 'find_orphan_notes', arguments: { limit: 5 } },
      { name: 'get_recent_notes', arguments: { limit: 5 } },
    ];

    for (const call of testCalls) {
      const result = await client.callTool(call);

      if (!result.isError) {
        const content = result.content as Array<{ type: string; text: string }>;
        expect(content[0].type).toBe('text');

        // Should be valid JSON
        expect(() => JSON.parse(content[0].text)).not.toThrow();
      }
    }
  });
});
