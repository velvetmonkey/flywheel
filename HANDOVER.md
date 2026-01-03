# [[Flywheel Project Handover Prompt]]

> **[[Purpose]]**: [[Complete]] [[Context]] for an agent taking over development of the Flywheel [[Project]]

---

## 1. PRODUCT [[Vision]]

**Flywheel** is the **[[Agentic Markdown Operating System]]** - enabling non-[[Technical]] knowledge workers to build [[Automated]] workflows [[Using]] markdown [[Files]] and agentic [[Systems]].

**The Pitch**: *"Starting a new business or project? [[Install Flywheel]] in [[Claude Code]] - it gives [[You]] the intelligence and workflows to [[Run]] your business from day [[One]]."*

### [[Core Concept

An Agentic]] Markdown OS where:
- **Files [[Are]] [[Data]] structures** ([[Not]] just [[Documents]])
- **[[Links]] are [[Relationships]]** (not just hypertext)
- **Folders are schemas** (not just organization)
- **AI agents are operators** (not just assistants)

Plain text markdown becomes queryable, executable, automatable.

### The Dual Paradigm

Flywheel supports [[Both]] knowledge [[Management]] philosophies:

| Philosophy | Primitives | Users | [[Pain Point Solved]] |
|------------|------------|-------|-------------------|
| **Graph-Native** | `[[wikilinks]]`, backlinks, graph traversal | [[Obsidian]], Roam users | Add queryability to organic structure |
| **Schema-Native** | YAML frontmatter, typed fields, schemas | VSCode, Cursor devs | Add graph traversal to typed data |

**The Unique [[Value]]**: Same markdown file works for BOTH. Users fluidly move between paradigms.

---

## 2. [[Architecture]]

```
┌─────────────────────────────────────────────────────────┐
│                   Claude Code                           │
│  ┌───────────────────┬─────────────────────────────┐    │
│  │  Skills (33)      │  Agents (8)                 │    │
│  │  /vault-health    │  rollup-agent               │    │
│  │  /auto-log        │  achievement-agent          │    │
│  │  /rollup          │  schema-enforcer-agent      │    │
│  └────────┬──────────┴──────────┬──────────────────┘    │
└───────────┼─────────────────────┼──────────────────────┘
            │                     │
┌───────────▼─────────────────────▼──────────────────────┐
│               Flywheel MCP Server (40+ tools)          │
│  ┌────────────────────────────────────────────────┐    │
│  │  Graph Tools  │  Query Tools  │  Schema Tools  │    │
│  │  backlinks    │  search       │  validate      │    │
│  │  hubs         │  temporal     │  frontmatter   │    │
│  │  orphans      │  sections     │  field rename  │    │
│  └────────────────────────────────────────────────┘    │
└───────────────────────────┬────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│              Markdown Vault                            │
│  .md files + wikilinks + YAML frontmatter              │
└────────────────────────────────────────────────────────┘
```

### Repository Structure

```
flywheel/
├── packages/
│   ├── mcp-server/          # Graph + schema intelligence (npm: @bencassie/flywheel-mcp)
│   │   ├── src/tools/       # 40+ MCP tools
│   │   └── package.json     # v1.0.1 (needs sync with plugin!)
│   └── claude-plugin/       # Workflows and automation
│       ├── .claude-plugin/  # Plugin manifest (v1.6.3)
│       ├── skills/          # 33 user-facing skills
│       ├── hooks/           # Event-driven automation (Six Gates)
│       └── agents/          # 8 multi-step workflows
├── demos/                   # 4 demo vaults
│   ├── artemis-rocket/      # Aerospace startup (65 notes)
│   ├── carter-strategy/     # Solo consultant (30 notes)
│   ├── nexus-lab/           # Research lab (30 notes)
│   └── startup-ops/         # B2B SaaS (30 notes)
├── docs/                    # Documentation
├── CLAUDE.md                # Agent instructions
└── README.md                # Main README
```

---

## 3. CURRENT STATE (v1.6.3)

### What's Complete

| Version | Features |
|---------|----------|
| v1.6.3 | Missing frontmatter tools registered, /onboard skill, QUICKSTART.md |
| v1.6.2 | Six Gates REAL enforcement (Gates 1,2,4 BLOCK operations) |
| v1.6.1 | Six Gates framework, session/verify hooks |
| v1.6.0 | Bidirectional Bridge (prose ↔ frontmatter), `/normalize-[[Note]]`, `/wikilinkify-frontmatter` |
| v1.5.0 | Startup Ops demo, marketplace installation |
| v1.4.0 | Periodic note detection (zero-config) |
| v1.3.0 | Task management tools |
| v1.2.0 | Structure tools (headings, sections) |
| v1.1.0 | Temporal tools (stale, concurrent) |
| v1.0.0 | Initial release |

### Version Discrepancy (ACTION NEEDED)

| Location | Version |
|----------|---------|
| GitHub plugin.json | 1.6.3 |
| npm package.json | 1.0.1 |

**The npm package is ~6 versions behind.** This needs to be resolved.

---

## 4. SIX GATES SAFETY FRAMEWORK (MANDATORY)

All Flywheel extensions MUST observe Six Gates. This is enforced, not optional.

| Gate | Purpose | Enforced By | Blocks? |
|------|---------|-------------|---------|
| **1. Read Before Write** | Read current state before mutation | `pre-mutation-gate.py` | ✓ YES |
| **2. File Exists for Edit** | Validate Edit targets exist | `pre-mutation-gate.py` | ✓ YES |
| **3. Agent Chain Validation** | Verify each step before next | `validate-agent-gate3.py` | ✓ YES |
| **4. Mutation Confirmation** | User confirms writes | `pre-mutation-gate.py` | ✓ YES |
| **5. MCP Health Check** | Verify MCP on session start | `[[Session]]-gate.py` | ⚠ WARN |
| **6. Post-Execution Validation** | Verify writes succeeded | `verify-mutation.py` | ⚠ WARN |

**Gate 3 is enforced by hooks. Non-compliant agents are BLOCKED.**

---

## 5. THE BIDIRECTIONAL BRIDGE (Critical Differentiator)

**Key Insight**: Wikilinks and frontmatter are two representations of the SAME information.

### Pattern 1: Prose → Frontmatter (help Graph-Native users add structure)

```markdown
# What they write (prose patterns)
Client: [[Acme Corp]]
Owner: [[Ben Carter]]
Status: Active

# What Flywheel suggests
---
type: project
client: [[Acme Corp]]
owner: [[Ben Carter]]
status: active
---
```

### Pattern 2: Frontmatter → Wikilinks (help Schema-Native users traverse)

```yaml
# What they write (strings)
---
attendees: ["Ben Carter", "John Smith"]
client: "Acme Corp"
---

# What Flywheel suggests
---
attendees:
  - [[Ben Carter]]
  - [[John Smith]]
client: [[Acme Corp]]
---
```

### Skills That Implement This

- `/normalize-note` - Harmonize frontmatter + wikilinks
- `/promote-to-frontmatter` - Extract prose patterns to YAML
- `/wikilinkify-frontmatter` - Convert strings to wikilinks

---

## 6. ROADMAP - WHAT'S REMAINING

### v1.7.0 - Advanced Schema Intelligence (NEXT)

**Goal**: Make frontmatter as powerful as a database.

**New MCP Tools Needed:**
- `compute_frontmatter(path, fields)` - Auto-compute derived fields (word_count, backlink_count, last_updated)
- `rename_field(old, new, scope)` - Bulk rename frontmatter fields across vault

**New Skills Needed:**
- `/schema-define` - Define reusable schemas
- `/schema-apply` - Apply schema to notes
- `/schema-migrate` - Migrate notes between schema versions

**Schema Features:**
- Schema inheritance (project inherits from base)
- Required vs optional fields
- Type coercion (string dates → Date objects)
- Computed fields

### v1.8.0 - Workflow Templates

**Goal**: Pre-built automation for common business processes.

**Templates:**
- Weekly review workflow
- Meeting notes → action items
- Daily standup rollup
- Quarterly OKR review
- Customer onboarding checklist

**Features:**
- Workflow editor (define steps, triggers, conditions)
- Trigger-based automation (on file create, on schedule)
- Workflow variables and templating

### v2.0 - Enterprise Features

**Multi-Vault:**
- Cross-vault linking
- Vault federation
- Shared schemas across vaults

**Collaboration:**
- Real-time presence (who's editing what)
- Comment threads on notes
- Review workflows

**Compliance:**
- Audit logging
- Access control
- Data retention policies

---

## 7. ADDITIONAL IDEAS FROM OWNER'S NOTES (Not Yet in GitHub Roadmap)

These are from the owner's vault notes but haven't been added to the official roadmap:

### Bidirectional Bridge Tools (v1.1 in owner's notes)

```
MCP Tools:
- detect_prose_patterns() - Find structure in prose
- suggest_frontmatter_from_prose() - Prose → YAML suggestions
- suggest_wikilinks_in_frontmatter() - String → wikilink suggestions
- validate_cross_layer() - Check consistency
- search_notes_advanced() - Rich queries (gte, in, contains operators)
```

### Advanced Schema Intelligence (v1.2 in owner's notes)

```
- infer_conventions() - Auto-detect vault conventions
- find_incomplete_notes() - Missing required fields
- migrate_field_values() - Transform values (e.g., "todo" → "pending")
- get_type_defaults() - Default frontmatter by type
```

---

## 8. DEMO VAULTS

Each demo answers: *"How does this new business replace a 20th century equivalent?"*

| Demo | 20th Century Replaces | Notes | Key Focus |
|------|----------------------|-------|-----------|
| **Artemis Rocket** | 200-person aerospace corp | 65 | Graph patterns, vault health, intentional issues |
| **Carter Strategy** | Partner-heavy consulting firm | 30 | Tasks, schema, rollups, stale detection |
| **Nexus Lab** | PhD students doing lit review | 30 | Citation networks, knowledge paths |
| **Startup Ops** | Founders doing everything | 30 | Bidirectional bridge, automation zones |

All 4 demos are COMPLETE and ready.

---

## 9. DEVELOPMENT PRINCIPLES

1. **Zero lock-in**: Pure markdown, Git-friendly, works offline
2. **Editor agnostic**: Obsidian, VSCode, Cursor, vim, any text editor
3. **AI-first architecture**: MCP layer gives agents full vault intelligence
4. **Convention over configuration**: Smart defaults, zero-config start
5. **Progressive disclosure**: Simple to start, powerful when needed
6. **Cross-platform**: WSL + Windows tested and working (DO NOT BREAK)

---

## 10. AGENT DEVELOPMENT RULES

**Multi-step agents MUST include:**
1. `## Critical Rules` section with sequential execution
2. Error handling strategy
3. Verification checkpoints between phases
4. Expected output showing ✓/✗ for each step

**Template**: `packages/claude-plugin/agents/_templates/MULTI_STEP_AGENT.md`

**Validation**: `npm run validate:agents` before committing

---

## 11. RELEASE WORKFLOW

### Version Files (keep in sync!)

ALL version bumps require updating THREE files:
- `.claude-plugin/marketplace.json` (repo root)
- `packages/claude-plugin/.claude-plugin/marketplace.json`
- `packages/claude-plugin/.claude-plugin/plugin.json`

### GitHub Release Process

```bash
# After version bump commit
gh release create vX.Y.Z --title "vX.Y.Z" --notes "## Changes\n\n- [list changes]"
```

---

## 12. COMPETITIVE POSITIONING

| System | Graph | Schema | AI-Native | Open |
|--------|-------|--------|-----------|------|
| **Flywheel** | ✅ | ✅ | ✅ | ✅ |
| Notion | ❌ | ✅ | 🟡 | ❌ |
| Roam Research | ✅ | ❌ | ❌ | ❌ |
| Linear / Asana | ❌ | ✅ | ❌ | ❌ |
| Salesforce | ❌ | ✅ | ❌ | ❌ |

**Flywheel's unique position**: Full graph + schema support, AI-native from day one, completely open (plain markdown).

---

## 13. KEY FILES TO KNOW

**MCP Server:**
- `packages/[[MCP]]-server/src/index.ts` - Server entry point
- `packages/mcp-server/src/[[Tools]]/` - Tool implementations

**Claude Plugin:**
- `packages/claude-plugin/.claude-plugin/plugin.json` - Plugin manifest
- `packages/claude-plugin/skills/` - Skill definitions
- `packages/claude-plugin/hooks/` - Hook scripts (Six Gates)
- `packages/claude-plugin/agents/` - Multi-step workflows

**Documentation:**
- `docs/ROADMAP.md` - Version history & future plans
- `docs/AGENTIC_PATTERNS.md` - Design patterns for AI workflows
- `docs/GETTING_STARTED.md` - Installation guide

---

## 14. IMMEDIATE PRIORITIES

1. **Sync npm version** - Package is at 1.0.1, should be 1.6.3
2. **v1.7.0 Planning** - Advanced Schema Intelligence is next milestone
3. **Publish to npm** - Run `npm publish` in `packages/mcp-server/` after version sync

---

## 15. CONTEXT: 2026 AI PREDICTIONS

Flywheel aligns with these predictions:
1. **Long-running agents** - Operating days/weeks
2. **Memory breakthrough** - AI retaining context via external memory (graphs!)
3. **AI reviewing AI** - Automated quality checks
4. **Non-technical → engineering** - Knowledge workers writing precise requirements
5. **Proactive AI** - Suggests issues before asked
6. **Continual learning** - Improves from vault context

**Flywheel is the onramp** for knowledge workers entering the Claude Code paradigm.

---

## END OF HANDOVER

**Repository**: https://github.com/bencassie/flywheel
**Local Path**: `C:\Users\benca\src\flywheel`
**npm Package**: `@bencassie/flywheel-mcp`
**[[Current Version]]**: v1.6.3 (plugin) / v1.0.1 (npm - needs sync)
