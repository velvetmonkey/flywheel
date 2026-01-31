# Flywheel Roadmap

This document outlines planned features and research initiatives for Flywheel development.

---

## 🌊 Market Opportunities (January 2026)

**Context:** Based on January 2026 AI/Tech market analysis, several converging trends create significant opportunities for Flywheel's positioning and feature development.

### Market Trends Shaping Strategy

**MCP Mainstream Adoption**
- Model Context Protocol becoming standard for AI tool integration
- Claude Code dominance driving MCP ecosystem growth
- Developers migrating from proprietary APIs to MCP-first architecture

**Autonomous Agent Explosion**
- 147k autonomous agents in Open Claw ecosystem (as of Jan 2026)
- Multi-agent coordination becoming critical requirement
- Agent swarms need shared knowledge infrastructure

**Claude Code Migration Wave**
- Developers abandoning IDE-specific AI plugins for Claude Code
- Opus + MCP enabling sophisticated agent workflows
- 20+ minute agent tasks becoming common (complex refactoring, research)

**Markdown-as-Infrastructure Paradigm**
- Markdown files emerging as primary agent memory format
- "Infrastructure > Models" - tooling quality matters more than model selection
- Git-backed markdown becoming standard for agent state management

**Token Economics Crisis**
- $100-200/dev/month AI costs driving efficiency focus
- Long-running workflows (20+ mins) need 100+ vault queries
- File-reading approach unsustainable at scale

### Strategic Implications

These trends validate Flywheel's architecture and create clear feature priorities:
1. **Multi-agent use cases** - Show coordination patterns (147k agents need this)
2. **Token efficiency benchmarks** - Quantify savings with hard numbers (MCP crowd demands proof)
3. **Agent memory patterns** - Document how autonomous agents should structure knowledge
4. **Federated queries** - Agent swarms operating across multiple vaults
5. **Real-time coordination** - Event streaming for agent collaboration

---

## Immediate (Pre-Launch Priority)

### 1. Multi-Agent Use Case Documentation

**Priority:** CRITICAL for positioning in autonomous agent ecosystem

**What:**
- Document patterns for multiple agents querying same vault
- Demo: Coordinator agent + specialist agents using shared knowledge graph
- Show how Flywheel enables agent swarm coordination

**Why it matters:**
- 147k autonomous agents (Open Claw ecosystem) need coordination infrastructure
- Current bottleneck: agents can't share knowledge efficiently
- Flywheel provides natural coordination layer via shared graph

**Deliverables:**
- [ ] `docs/MULTI_AGENT_PATTERNS.md` - Coordination patterns guide
- [ ] Demo: 3-agent workflow (coordinator + 2 specialists) on single vault
- [ ] Example: Research agent queries → Writing agent uses results → Review agent validates
- [ ] Security patterns: Which agents query what sections
- [ ] Performance: Multiple agents querying simultaneously

**Target:** Complete before major announcement (validates positioning)

---

### 2. Token Efficiency Benchmarks

**Priority:** CRITICAL for credibility with MCP/Claude Code crowd

**What:**
- Quantify actual token savings vs file-reading approach
- Real measurements from production usage (BenVM vault)
- "Agent runs 20min task, queries vault 100x - here's the cost comparison"

**Why it matters:**
- Current claims ("100x savings") lack hard evidence
- MCP developers demand quantified performance data
- Token costs are PRIMARY decision factor for agent builders

**Deliverables:**
- [ ] `docs/TOKEN_BENCHMARKS.md` - Measured savings with methodology
- [ ] Before/After comparison tables:
  - Graph-only queries (backlinks, orphans): True 100x savings
  - Graph + content queries (find then read): 10-20x savings
  - Long-session cumulative savings: 50-80x
- [ ] Real examples: "Finding all #urgent tasks: 50 tokens (Flywheel) vs 5000 tokens (read files)"
- [ ] Cost calculator: Input vault size + query frequency → annual savings
- [ ] Production data: Week-long measurement from active vault

**Acceptance criteria:** Every claim backed by real measurement, methodology documented

**Target:** Complete before any major announcement (credibility requirement)

---

### 3. Agent Memory Patterns Guide

**Priority:** HIGH - Positions Flywheel as "DNA for future agents"

**What:**
- How autonomous agents should structure vault knowledge
- Skills → Flywheel queries → Actions workflow patterns
- "Building Blocks for Agent Memory" design guide

**Why it matters:**
- Agent builders need proven patterns, not blank canvas
- "Infrastructure > Models" - show that tooling architecture matters
- Flywheel becomes reference implementation for agent memory

**Deliverables:**
- [ ] `docs/AGENT_MEMORY_PATTERNS.md` - Comprehensive guide
- [ ] Recommended vault structure for agents:
  - Skills/ - Agent capabilities documentation
  - Memory/ - Episodic memory (dated entries)
  - Knowledge/ - Semantic memory (timeless facts)
  - Context/ - Working memory (current tasks)
- [ ] Query workflows: How agents should use Flywheel tools
- [ ] Example: "Morning briefing" agent workflow using 8 Flywheel queries
- [ ] Integration with Skills system: Skill definitions → Flywheel lookups → Execution
- [ ] Template vault for new agent projects

**Target:** v0.9.0 - Positions Flywheel as agent infrastructure (not just PKM tool)

---

## Near-Term (Post-Launch)

### 4. Multi-Vault / Federated Queries

**Priority:** HIGH - Enables agent swarm coordination

**What:**
- Agents operating across multiple knowledge bases simultaneously
- Shared team vault + personal vault scenarios
- Cross-vault link resolution and entity matching

**Why it matters:**
- Real-world agents need: Personal context + Team knowledge + Project-specific data
- Agent swarms coordinating via federated knowledge access
- Enterprise use case: Department vaults + personal vaults

**Deliverables:**
- [ ] Multi-vault configuration in MCP settings
- [ ] Cross-vault query tools: `search_across_vaults`, `get_federated_backlinks`
- [ ] Entity deduplication across vaults (same concept, different vaults)
- [ ] Access control: Which agents can query which vaults
- [ ] Performance: Index multiple vaults without memory bloat

**Use cases:**
- Developer: Personal notes + team wiki + project docs
- Consultant: Client vaults + templates + personal knowledge
- Researcher: Literature vault + lab notes + personal insights

**Target:** v0.10.0 - After single-vault experience is solid

---

### 5. Event Streaming / Watch Mode

**Priority:** MEDIUM-HIGH - Real-time coordination for autonomous agents

**What:**
- Agents subscribe to graph changes
- "Notify me when new task tagged #urgent appears"
- Real-time coordination for multi-agent workflows

**Why it matters:**
- Autonomous agents need reactive triggers, not just polling
- Enable workflows: "Research agent finds insight → Writing agent notified → Drafts update"
- Reduces latency and query overhead

**Deliverables:**
- [ ] `watch_graph_changes` tool - Subscribe to vault mutations
- [ ] Event types: New notes, updated frontmatter, new links, task status changes
- [ ] Filter subscriptions: "Only #urgent tasks", "Notes in Projects/ folder"
- [ ] Webhook integration: Push events to external agents
- [ ] Performance: Efficient change detection without constant reindexing

**Use cases:**
- Task triage: Agent monitors for #urgent, prioritizes automatically
- Content pipeline: Draft → Review → Publish workflow coordination
- Team coordination: Agent A completes → Agent B notified → Next step triggered

**Target:** v0.11.0 - After multi-vault support proves demand for coordination

---

### 6. Agent Identity & Permissions

**Priority:** MEDIUM - Security layer for agent economies

**What:**
- Which agents can query what sections
- Audit trail: which agent queried what, when
- Role-based access control for multi-agent systems

**Why it matters:**
- Enterprise adoption requires access control
- Multi-agent systems need security boundaries
- Audit compliance (who accessed sensitive data?)

**Deliverables:**
- [ ] Agent identity in MCP requests (authenticate via token/key)
- [ ] Permission model: Agent roles → Allowed query patterns
- [ ] Audit logging: Track all queries with agent identity timestamp
- [ ] Query restrictions: "Agent A can only query Projects/", "Agent B read-only"
- [ ] Admin tools: Review agent access patterns, revoke permissions

**Use cases:**
- Enterprise: Sensitive HR data accessible only to specific agents
- Team workflows: Junior agents can read, senior agents can mutate
- Client work: Per-client agents can't access other clients' data

**Target:** v0.12.0 - After multi-agent patterns are established

---

### 7. MCP Protocol Extensions

**Priority:** MEDIUM - Agent-optimized response formats

**What:**
- Batch queries (reduce round-trips)
- Streaming responses for large result sets
- Agent-optimized JSON formats (compact, structured)

**Why it matters:**
- Current: 100 queries = 100 round-trips (latency bottleneck)
- Batch queries: 100 queries in 1 request (10x faster)
- Large result sets: Stream instead of waiting for full response

**Deliverables:**
- [ ] `batch_query` tool - Submit multiple queries, get combined results
- [ ] Streaming support for: `search_notes`, `get_all_tasks`, large backlink sets
- [ ] Compact response mode: Minimal JSON (reduce token overhead for agent-to-agent)
- [ ] Query composition: Chain queries (backlinks → filter by tag → sort by date)
- [ ] Error handling: Partial success (some queries succeed, some fail)

**Use cases:**
- Morning briefing: 10 queries in 1 batch (faster startup)
- Research workflow: Stream search results as they match (immediate feedback)
- Agent-to-agent: Compact format saves tokens in multi-hop workflows

**Target:** v0.13.0 - Performance optimization after core features stable

---

## Future Vision (6-12 Months)

### 8. Agent Collaboration Patterns

**Priority:** MEDIUM - Multi-agent task coordination via graph

**What:**
- Cross-agent graph annotations
- Shared working memory spaces
- Multi-agent task coordination via vault

**Why it matters:**
- Enable sophisticated agent workflows: Planning → Research → Execution → Review
- Shared working memory: Agents collaborate on same knowledge substrate
- Graph becomes coordination layer (not just storage)

**Deliverables:**
- [ ] Agent annotations: "Agent A marked this as reviewed", "Agent B assigned this"
- [ ] Working memory sections: Temporary collaboration space in vault
- [ ] Task handoff patterns: Agent A completes → Leaves notes for Agent B
- [ ] Coordination primitives: Locks, claims, status updates via frontmatter
- [ ] Visualization: Show agent activity on graph (which agent touched what)

**Use cases:**
- Research pipeline: Finder → Analyzer → Summarizer → Publisher (4 agents)
- Code review: Scanner → Analyzer → Suggester → Implementer workflow
- Content creation: Researcher → Drafter → Editor → Publisher chain

**Target:** v1.0.0 - Flagship multi-agent capability

---

### 9. Integration with Agent Identity Systems

**Priority:** LOW-MEDIUM - Future-proofing for AI accountability trends

**What:**
- If "AI accountability through AI identity" becomes real (regulatory trend)
- Flywheel as authenticated knowledge layer
- Wallet/on-chain integration (if agent economies mature)

**Why it matters:**
- Regulatory pressure for AI traceability increasing
- If agent identities become standard, knowledge access needs integration
- Positions Flywheel for enterprise compliance requirements

**Deliverables:**
- [ ] Identity provider integration (OAuth, DID, wallet-based)
- [ ] Cryptographic proof of agent queries (immutable audit trail)
- [ ] Compliance reporting: "Which agents accessed PII in last 30 days?"
- [ ] On-chain attestation (optional): Proof of knowledge access for audits

**Speculative:** Monitor regulatory developments, implement if demand emerges

**Target:** v1.x (if ecosystem matures in this direction)

---

### 10. Encrypted / Private Graph Sections

**Priority:** LOW-MEDIUM - Response to "agent-only language" concerns

**What:**
- Secure sub-graphs for sensitive knowledge
- Agent-level encryption keys
- Private sections invisible to unauthorized agents

**Why it matters:**
- Concerns about agents developing "hidden communication" patterns
- Enterprise: Sensitive data (HR, finance) needs encryption at rest
- Multi-tenant: Client data isolation in shared infrastructure

**Deliverables:**
- [ ] Encrypted vault sections (libsodium or similar)
- [ ] Per-agent decryption keys
- [ ] Secure queries: Decrypt on read, re-encrypt on write
- [ ] Key management: Rotation, revocation, access control
- [ ] Performance: Minimize decryption overhead

**Use cases:**
- Enterprise: PII data encrypted, accessible only to authorized agents
- Multi-tenant: Customer A's data encrypted separately from Customer B
- Personal: Sensitive journal entries readable only by trusted agents

**Target:** v1.x+ - After core multi-agent patterns proven

---

## Research & Discovery Phase

**Goal:** Study real-world vault patterns, schemas, and workflows to inform Flywheel development.

### Strategic Approach

This is market research for vault intelligence. Study the market systematically before building:

- **Find the 80/20 patterns** that solve most problems
- **Build on conventions, identify gaps** in existing solutions
- **Community-driven research** - understand how people actually use vaults in the wild
- **Build a queryable corpus** of public vaults for ongoing analysis
- **Spot anti-patterns** - what breaks, what's brittle, what fails at scale
- **Publish findings** - position Flywheel as the thoughtful, research-driven choice

The goal isn't just to catalog, but to understand the *why* behind vault patterns and derive intelligence that shapes product direction.

### Active Research - In Progress

**4 Research Agents Deployed (2026-01-31 05:41 GMT):**

1. **Public PKM Vault Discovery**
   - Target: 30-50 public vaults (Obsidian, Foam, Logseq)
   - Sources: GitHub, forums, digital gardens, developer portfolios
   - Output: `/home/ben/clawd/memory/flywheel-research-vaults-catalog.md`
   - Duration: 1+ hour deep research

2. **Frontmatter Schema Analysis**
   - Target: 20-30 vaults
   - Focus: Common properties, domain-specific patterns, 80/20 schemas, naming conventions
   - Output: `/home/ben/clawd/memory/flywheel-research-frontmatter-patterns.md`
   - Duration: 1+ hour analysis

3. **Link Pattern & Graph Analysis**
   - Target: 15-20 vaults
   - Focus: Wikilink styles, link density, hub notes, orphans, graph topology, intelligent matching
   - Output: `/home/ben/clawd/memory/flywheel-research-link-patterns.md`
   - Duration: 1+ hour deep dive

4. **Agentic Markdown Vault Discovery**
   - Target: 15-25 AI agent workspaces
   - Focus: Clawdbot, Claude Code, Cursor, MCP servers, agent memory patterns
   - Output: `/home/ben/clawd/memory/flywheel-research-agentic-vaults.md`
   - Duration: 1+ hour research

All outputs will feed into the Research & Discovery phase deliverables.

### Research Insights & Strategic Implications

**Meta-Learning from Parallel Research (2026-01-31)**

The 4-agent research deployment itself validated a critical insight: **parallel research scales beautifully**. Four agents, each working 90+ minutes, delivered over 6 hours of deep research in ~7 minutes of wall-clock time. This methodology—orchestrated parallel investigation with synthesized convergence—is itself a pattern worth embedding in Flywheel's design philosophy.

#### Convergent Patterns Across Domains

Analyzing 129 vaults across PKM systems, agentic workspaces, frontmatter schemas, and link graphs revealed a remarkable DNA convergence:

**The 80/20 Rule Holds Everywhere:**
- Frontmatter: 8-12 core properties solve 80% of use cases
- Folder structure: 20-40 folders regardless of vault size (stable area grouping)
- Broken links: 15-25% is NORMAL and EXPECTED in healthy vaults

**Convention Over Configuration Wins:**
- Kebab-case naming: 70% adoption (standardizing on this reduces friction)
- PARA structure: Emerges organically in mature vaults
- Git version control: Universal infrastructure (100% of studied vaults)

**Structure ⇄ Flexibility Balance:**
- Folders define areas (stable, low-change organizational boundaries)
- Links express semantics (fluid, high-value cross-cutting connections)
- This tension should drive Flywheel's core architecture

#### Universal Design Tensions

**"Always-On Context vs Progressive Disclosure"** isn't just an agentic vault problem—it's fundamental to knowledge work:

- **PKM:** Hub notes (MOCs) provide overview; detailed notes provide depth
- **Frontmatter:** Core 8-12 properties are always visible; domain-specific extensions add richness
- **Links:** High-density reference notes vs low-density project notes serve different discovery needs

Flywheel must embrace this tension, not try to resolve it. The architecture should enable both modes seamlessly.

#### Workflow Realities

**"Link First, Create Later" is Fundamental:**
15-25% broken link rate is not a bug—it's how knowledge workers think. We sketch connections before filling in details. Tools that treat broken links as errors fundamentally misunderstand PKM workflow.

**Implication:** Flywheel should embrace broken links with intelligent management: age-based prioritization, one-click creation, connection-context preservation. Make the workflow feel natural, not shameful.

**Respect Existing Workflows:**
Dataview, Templater, and Tasks are deeply embedded in the Obsidian ecosystem. Users have invested thousands of hours in mastering these tools.

**Implication:** Flywheel should augment, not replace. Provide better substrate (smarter graph intelligence, richer context, automated maintenance), but maintain plugin interoperability. Compete on intelligence, not on lock-in.

#### Strategic Assets

**The Research Corpus (129 Vaults):**
This isn't just data—it's a strategic testing corpus for validation, benchmarking, and real-world pattern testing. It should be maintained, expanded, and version-controlled as Flywheel evolves.

**Domain-Specific Patterns:**
Academic ≠ Developer ≠ Creative vaults. One-size-fits-all frontmatter fails in practice. Successful vaults adapt schemas to domain needs.

**Implication:** Flywheel needs domain-aware templates and presets. Start with evidence-based defaults for common domains, allow elegant customization.

#### Architectural Guidance

**Folders are for Areas, Links are for Semantics:**
Most vaults stabilize at 20-40 folders regardless of size—these represent stable conceptual areas. Real value emerges in cross-cutting links that connect across folder boundaries.

**Implication:** Flywheel should prioritize cross-folder link suggestions, detect emergent themes that span organizational boundaries, and surface connections that folders can't express.

**Git is Universal Infrastructure:**
100% of studied vaults use git. Git-based knowledge evolution tracking (from agentic vault research) could be transformative for PKM too—imagine surfacing insights about how concepts evolved, what connections formed over time, when ideas matured.

**Implication:** Deep git integration isn't optional—it's foundational. Flywheel should treat git history as first-class intelligence, not just backup infrastructure.

#### Design Philosophy

These insights crystallize Flywheel's strategic positioning:

1. **Evidence-driven defaults** - Use the 80/20 patterns from real vaults, not theoretical ideals
2. **Embrace organic workflows** - Link-first thinking, broken links, iterative refinement
3. **Augment, don't replace** - Respect existing tools, compete on intelligence
4. **Domain-aware flexibility** - Templates for common patterns, elegant customization for edge cases
5. **Intelligence in the substrate** - Smart suggestions, automated maintenance, evolution tracking
6. **Scale-conscious architecture** - Patterns that work at 100 notes and 10,000 notes

The research phase isn't just about cataloging—it's about understanding the *why* behind vault patterns and letting real-world usage shape Flywheel's intelligence.

### Objectives

- **Discover ~100 open PKM vaults** across different platforms:
  - Public Obsidian vaults
  - Foam repositories
  - Logseq projects
  - Other markdown-based PKM systems

- **Find open agentic markdown vaults:**
  - AI agent workspaces using markdown
  - Automation workflows and patterns
  - Agent-driven knowledge management systems

### Research Questions

#### Core Patterns

- What frontmatter schemas are commonly used?
- How do users structure their daily notes, projects, and tasks?
- What linking patterns emerge in mature vaults?
- What automation workflows are most valuable?
- How do agentic systems organize their context and memory?

#### Temporal Patterns - Vault Evolution

How do vaults change over time?

- **Link graph growth** - how connection density evolves
- **Refactoring patterns** - reorganization, renames, restructuring
- **Abandoned structures** - failed experiments, deprecated patterns
- What triggers major vault reorganizations?

#### Query Patterns

If vaults contain Dataview queries, analyze what people actually search for:

- Most common query types
- Complexity patterns (simple filters vs complex joins)
- Performance bottlenecks at scale
- Gaps where queries can't express intent

#### Scale Breakpoints

100-note vault vs 10,000-note vault - what changes?

- When do naive wikilinks break?
- When do people introduce namespaces/prefixes?
- What organizational strategies emerge at scale?
- Performance characteristics and optimization patterns

#### Plugin Dependencies

Dataview, Templater, and other plugin usage patterns:

- What gaps do these plugins fill?
- Where should Flywheel provide native solutions?
- What capabilities are essential vs nice-to-have?
- Plugin interaction patterns and conflicts

#### Domain-Specific Patterns

Academic vs developer vs creative vaults - how do they differ?

- **Frontmatter schemas** - research papers vs code projects vs creative work
- **Link densities** - citation-heavy vs sparse connections
- **Task workflows** - academic deadlines vs sprint planning vs creative processes
- Vocabulary and terminology patterns

#### Collaboration & Sync Artifacts

Git-backed vaults and multi-device usage:

- Merge conflict patterns
- Concurrent editing strategies
- What breaks when synced across devices?
- Collaboration workflows (shared vaults, team patterns)

#### Migration Scars

Roam/Notion/other platform migrations:

- What anti-patterns carry over from other tools?
- Import conversion issues
- Mental model mismatches
- What users struggle to adapt

#### Negative Space

What people *wish* they could do but can't:

- Links they want to create but don't (manual processes)
- Automation they'd like but can't express
- Queries they can't write
- Patterns too brittle to maintain
- What's manual that should be automatic?

### Deliverables

- **Queryable vault corpus** - indexed, searchable database of public vaults
- **Pattern catalog** - common structures, schemas, and workflows with frequency analysis
- **Anti-pattern documentation** - what breaks, what's brittle, what doesn't scale
- **Scale research report** - breakpoints, optimization strategies, architecture guidance
- **Plugin gap analysis** - where Flywheel should provide native solutions
- **Domain-specific guides** - recommended patterns for academic/developer/creative use cases
- **Published research findings** - blog posts, documentation positioning Flywheel as research-driven
- **Schema recommendations** - evidence-based frontmatter and structure guidance
- **Workflow pattern library** - proven automation and process templates

---

## Documentation & Integration

### Clawdbot Integration & Architecture Documentation

**Goal:** Document the Clawdbot → Claude Code workflow and clarify Flywheel's positioning in the AI tooling ecosystem.

**Deliverables:**

- **Visual Demo:** Telegram → Clawdbot → Claude Code agents/sub-agents workflow diagram
- **Plugin Architecture Overview:** Skills system, MCP server integrations, tool orchestration
- **Navigation Layer vs Raw Memory:** How Flywheel provides structured navigation compared to raw memory systems

**Token Usage Comparison:**

| System | Approach | Token Range | Use Case |
|--------|----------|-------------|----------|
| Flywheel | Graph-aware, structured queries | 200-800 tokens | Navigate my thinking (PKM with graph intelligence) |
| ClawdMem | Semantic search, raw memory | 500-2k tokens | Remember everything I did (dev work logs) |

**Positioning:**

- **ClawdMem:** "Remember everything I did" — development work logs, raw memory storage, semantic retrieval
- **Flywheel:** "Navigate my thinking" — PKM with graph intelligence, structured knowledge, relationship awareness
- **Complementary Systems:** Not competing tools. Flywheel adds structure, relationships, and contextual meaning on top of raw memory

**Flywheel Advantages:**

- **Relationship awareness** — understands how notes connect, not just what they contain
- **Schema-driven intelligence** — typed frontmatter enables precise queries
- **Token efficiency** — graph-aware queries return targeted context, not bulk retrieval
- **Cross-cutting discovery** — surfaces connections that folder organization can't express

---

## Known Issues

### Bug Report: vault_add_to_section Breaking Bullet List Indentation

**Reported:** 2026-01-31 06:10 GMT  
**Reporter:** Velvet Monkey  
**Component:** Flywheel-Crank MCP (`vault_add_to_section`)

**Description:**
The `vault_add_to_section` tool is breaking bullet list indentation when adding multi-level nested content to daily notes. During tonight's research logging operations (05:28, 05:52, 05:58 GMT), multiple calls to `vault_add_to_section` with nested bullet structures resulted in malformed indentation in `daily-notes/2026-01-31.md`.

**Expected Behavior:**
Nested bullet lists should maintain proper indentation:
```markdown
- Top level
  - Second level
    - Third level
```

**Actual Behavior:**
Indentation is flattened or corrupted, breaking the hierarchical structure of the logged content.

**Reproduction:**
1. Use `vault_add_to_section` with multi-level nested bullet content
2. Content includes sub-bullets (2-3 levels deep)
3. Check daily note after operation
4. Observe broken indentation

**Impact:**
- Daily notes become hard to read
- Hierarchical structure is lost
- Manual cleanup required
- Multiple instances tonight (3+ logging operations affected)

**Context:**
- Occurred during parallel research agent logging
- All 3 major logging operations tonight showed this issue
- Tool was invoked with `commit:true` parameter
- Operations otherwise successful (content added, wikilinks applied)

**Affected Operations Tonight:**
- 05:28 GMT: MarkdownDB comparison + Twitter planning log
- 05:52 GMT: Full research summary (4 agents, verbose)
- 05:58 GMT: Executive summary (brief)

**Workaround:**
Manual editing of daily notes to fix indentation post-logging.

**Priority:** Medium-High (affects daily workflow, requires manual cleanup)

**Next Steps:**
- Investigate vault_add_to_section indentation handling
- Test with various nested bullet structures
- Fix indentation preservation logic
- Add regression tests for multi-level bullets

---

## Future Phases

*To be added as the project evolves*
