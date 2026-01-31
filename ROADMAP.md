# Flywheel Roadmap

This document outlines planned features and research initiatives for Flywheel development.

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
