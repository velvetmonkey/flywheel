# Flywheel - Claude Code Instructions

## Product Overview

Flywheel is the **Agentic Markdown Operating System** - a unified system combining:

1. **MCP Server** (`packages/mcp-server/`) - Graph + schema intelligence
2. **Claude Plugin** (`packages/claude-plugin/`) - Workflows and automation
3. **Demo Vaults** (`demos/`) - Ready-to-use templates for common workflows

## Core Concept

An Agentic Markdown OS where:
- **Files are data structures** (not just documents)
- **Links are relationships** (not just hypertext)
- **Folders are schemas** (not just organization)
- **AI agents are operators** (not just assistants)

Plain text markdown becomes queryable, executable, automatable.

## The Dual Paradigm

Flywheel supports BOTH philosophies:

### Graph-Native (Wikilink-First)
- Philosophy: Knowledge is a network of interconnected thoughts
- Primitives: `[[wikilinks]]`, backlinks, graph traversal
- Users: PKM enthusiasts, researchers, Obsidian/Roam users

### Schema-Native (Frontmatter-First)
- Philosophy: Knowledge is typed, queryable structured data
- Primitives: YAML frontmatter, schemas, typed fields
- Users: Developers, project managers, VSCode/Cursor users

### The Synthesis
Best systems support BOTH - files have frontmatter schemas AND wikilinks. Users choose their patterns without sacrificing interoperability.

## The Bidirectional Bridge (CRITICAL)

**Key insight**: Wikilinks and frontmatter are the OVERLAP - two representations of the SAME information.

Flywheel's unique value is **bidirectional translation**:

**Pattern 1: Prose → Frontmatter** (help Graph-Native users add structure)
**Pattern 2: Frontmatter → Wikilinks** (help Schema-Native users traverse)
**Pattern 3: Perfect Hybrid** (both layers reinforcing each other)

See full documentation in `packages/mcp-server/docs/BIDIRECTIONAL.md`

## Development Principles

1. **Zero lock-in**: Pure markdown, Git-friendly, works offline
2. **Editor agnostic**: Obsidian, VSCode, Cursor, vim, any text editor
3. **AI-first architecture**: MCP layer gives agents full vault intelligence
4. **Convention over configuration**: Smart defaults, zero-config start
5. **Progressive disclosure**: Simple to start, powerful when needed
6. **Preserve working tech**: WSL + Windows tested and working

## Six Gates Safety Framework (MANDATORY - ENFORCED)

**CRITICAL**: All Flywheel extensions MUST observe the Six Gates. This is not optional.

See full specification: `packages/claude-plugin/skills/_patterns/SIX_GATES.md`

| Gate | Purpose | Enforcement | Blocks? |
|------|---------|-------------|---------|
| **1. Read Before Write** | Read before write | `pre-mutation-gate.py` | YES |
| **2. File Exists for Edit** | Validate targets | `pre-mutation-gate.py` | YES |
| **3. Agent Chain Validation** | Verify each step | `.claude/hooks/` | YES |
| **4. Mutation Confirmation** | User confirmation | `pre-mutation-gate.py` | YES |
| **5. MCP Health Check** | Health check | `session-gate.py` | WARN |
| **6. Post-Execution Validation** | Verify writes | `verify-mutation.py` | WARN |

**When writing new skills/tools:**
- Include Six Gates compliance checklist in SKILL.md
- Use the template in `skills/_patterns/SIX_GATES.md`
- Test all six gates before merging

## Agent Development Rules (GATE 3 ENFORCED)

**CRITICAL**: Gate 3 is enforced by project-level hooks. Non-compliant agents will be BLOCKED.

**Before creating any new agent:**

1. Check if it's multi-step (calls `Task()`)
2. If multi-step, MUST include:
   - `## Critical Rules` section with sequential execution
   - Error handling strategy
   - Verification checkpoints between phases
   - Expected output showing ✓/✗ for each step
3. Use template: `packages/claude-plugin/agents/_templates/MULTI_STEP_AGENT.md`
4. Run `npm run validate:agents` before committing

**Hooks that enforce Gate 3:**
- `.claude/hooks/validate-agent-gate3.py` - BLOCKS Write of non-compliant agents
- `.claude/hooks/validate-agent-gate3-post.py` - WARNS after Edit operations
- `packages/claude-plugin/scripts/validate-agents.py` - CI/build validation

**Agents that fail validation will be REJECTED.**

## Cross-Platform Support

**CRITICAL**: This codebase works on both WSL and Windows. DO NOT break this.

- Same tooling (TypeScript, npm)
- Same build process
- Tested on both platforms
- If making changes, test on both

### MCP Configuration

Create `.mcp.json` in your project/vault root with the appropriate platform config:

| Platform | Command | Path style |
|----------|---------|------------|
| Windows (`win32`) | `cmd /c npx` | `C:/...` |
| WSL (`linux`) | `npx` | `/mnt/c/...` |
| macOS (`darwin`) | `npx` | `/Users/...` |

Since `.mcp.json` is gitignored, each environment gets its own config without conflicts.

### MCP Configuration Generation

When generating `.mcp.json` for users, **check the `Platform:` field in env info** (AUTHORITATIVE):

| `Platform:` value | Command | Path style | Example |
|-------------------|---------|------------|---------|
| `linux` | `npx` | `/mnt/c/...` (WSL) or `/home/...` | WSL accessing Windows files |
| `win32` | `cmd /c npx` | `C:/...` | Native Windows |
| `darwin` | `npx` | `/Users/...` | macOS |

**NEVER infer platform from filesystem path.** `/mnt/c/...` means WSL accessing Windows files—the runtime is still Linux, so use `npx` directly (not `cmd /c`).

## Repository Structure

```
flywheel/
├── packages/
│   ├── mcp-server/          # Graph + schema intelligence
│   │   ├── src/tools/       # MCP tools (graph, frontmatter, periodic)
│   │   └── README.md
│   └── claude-plugin/       # Workflows and automation
│       ├── .claude-plugin/  # Plugin manifest
│       ├── skills/          # User-facing skills
│       ├── hooks/           # Event-driven automation
│       └── agents/          # Multi-step workflows
├── demos/
│   └── artemis-rocket/      # Demo: aerospace startup knowledge base
├── docs/                    # Documentation and guides
├── README.md                # Main project README
├── CLAUDE.md                # This file
└── package.json             # Monorepo configuration
```

## Key Files

**MCP Server**:
- `packages/mcp-server/src/index.ts` - Server entry point
- `packages/mcp-server/src/tools/` - Tool implementations

**Claude Plugin**:
- `packages/claude-plugin/.claude-plugin/plugin.json` - Plugin manifest
- `packages/claude-plugin/skills/` - Skill definitions
- `packages/claude-plugin/hooks/` - Hook scripts

## Working with Demos

Demo vaults demonstrate "2026 Business Replacements" - how AI + markdown replace traditional business software:

| Demo | Replaces | Notes |
|------|----------|-------|
| Artemis Rocket | 200-person aerospace corp | 65 notes, graph-first design |
| Consulting Firm | Partner-heavy firm | Solo consultant + AI |
| Startup Ops | Founders doing everything | AI handles ops |
| Research Lab | Manual lit review | 100 papers/week processed |

Each demo should:
- Show real-world usage patterns
- Demonstrate graph + schema balance
- Include intentional issues for troubleshooting demos
- Work zero-config with Flywheel

## Development Workflow

```bash
# Install dependencies
npm install

# Build all packages
npm run build

# Develop MCP server
npm run dev:mcp

# Develop plugin
npm run dev:plugin

# Run tests
npm run test
```

## Related Documentation

- Agentic Markdown OS concept: `docs/CONCEPT.md`
- Bidirectional bridge design: `docs/BIDIRECTIONAL.md`
- Roadmap: `docs/ROADMAP.md`
- MCP Server docs: `packages/mcp-server/README.md`
- Plugin docs: `packages/claude-plugin/README.md`

**Skill naming**: Use verb-noun format (e.g., `add-log`, `find-stale-notes`, `check-health`).

**Trigger support**: Both slash commands (`/vault-health`) AND keywords ("check vault health") for accessibility.

## Release Workflow (MANDATORY)

**CRITICAL**: When bumping version numbers, you MUST create a GitHub release.

### Version Files (keep in sync)

ALL version bumps require updating FIVE files:
- `.claude-plugin/marketplace.json` (repo root)
- `packages/claude-plugin/.claude-plugin/marketplace.json`
- `packages/claude-plugin/.claude-plugin/plugin.json`
- `packages/mcp-server/package.json`
- `package.json` (root)

Then run `npm install --package-lock-only` to update `package-lock.json`.

### GitHub Release Process

When version changes:
1. **Commit** version bump with message: `chore: Bump version to vX.Y.Z`
2. **Push** to main
3. **Create GitHub Release**:
   ```bash
   gh release create vX.Y.Z --title "vX.Y.Z" --notes "## Changes\n\n- [list changes]"
   ```
4. Tag should match version (e.g., `v1.6.3`)

### Release Notes Format

```markdown
## Changes

- Feature: [description]
- Fix: [description]
- Docs: [description]

## Migration Notes

[Any breaking changes or migration steps]
```

### Don't Auto-Push

- Only push when user explicitly asks
- Users run `/plugin update flywheel@bencassie-flywheel` to get latest version

## Vision

"Starting a new business or project? Install Flywheel in Claude Code - it gives you the intelligence and workflows to run your business from day one."

The product aligns with 2026 predictions: long-running agents, proactive AI, non-technical users running businesses with markdown + AI.
