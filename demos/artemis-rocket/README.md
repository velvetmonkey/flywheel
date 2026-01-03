# Artemis Rocket Project - Demo Vault

**Scenario**: A 15-person aerospace startup building a small launch vehicle for delivering 250kg payloads to low Earth orbit.

**Project Phase**: Between Preliminary Design Review (PDR) and Critical Design Review (CDR)
**Timeline**: 18-month program, currently at month 8
**Status**: Propulsion system testing, avionics integration, structures in fabrication

## Quick Start

1. **Open this folder in your markdown editor**:
   - Obsidian: Open as vault
   - VSCode: Open folder
   - Cursor: Open folder

2. **Install Flywheel** (if you haven't):
   ```
   /plugin marketplace add bencassie/flywheel
   /plugin install flywheel@flywheel
   ```

3. **Start exploring**:
   - Try: `/vault-health` - See project status
   - Try: `/auto-log "Reviewing propulsion test results"` - Add to daily standup
   - Ask: "What's the current status of the propulsion system?"

## What This Demonstrates

**Graph-first knowledge base**: This isn't a personal notes system - it's an organizational operating system.

### Graph Patterns

| Pattern | Example | Purpose |
|---------|---------|---------|
| **Hubs** | Project Roadmap (38 backlinks) | Central navigation points |
| **Clusters** | Propulsion system (10 notes, 40+ links) | Tightly connected subsystems |
| **Bridges** | ADRs connect systems to decisions | Cross-cutting concerns |
| **Orphans** | 4 intentional disconnected notes | Demo `/vault-orphans` |
| **Broken Links** | 3 intentional invalid links | Demo `/vault-fix-links` |

### File Structure

```
artemis-rocket/
├── daily-notes/        # Team standups (10 notes)
├── weekly-notes/       # Weekly reviews (2 notes)
├── project/            # PM docs (8 notes)
├── team/               # People (8 notes)
├── systems/
│   ├── propulsion/     # 10 notes - CLUSTER
│   ├── avionics/       # 8 notes - CLUSTER
│   ├── structures/     # 6 notes - CLUSTER
│   └── gnc/            # 5 notes - CLUSTER
├── decisions/          # ADRs (5 notes)
├── requirements/       # System reqs (4 notes)
├── tests/              # Test docs (4 notes)
├── meetings/           # Meeting notes (6 notes)
└── suppliers/          # Vendor info (3 notes)

Total: ~65 notes
```

## User Journey Example

```
New team member's first day:

1. Clone repo → Open in VSCode with Claude Code
2. "Hey Claude, what is this project about?"
   → Claude explains the rocket project

3. `/vault-health`
   → Notes: 65 | Links: 312 | Avg connectivity: 4.8
   → 4 orphan notes, 3 broken links, 2 stale notes

4. "What's the status of the propulsion system?"
   → Status: Testing Phase (hot fire campaign)
   → Lead: Marcus Johnson
   → Next milestone: Full duration burn (Jan 15)

5. `/auto-log "Onboarding - reviewed propulsion with Marcus"`
   → Added to today's daily note with wikilinks

Productive in 5 minutes.
```

## Why This Works

**vs Traditional Project Management**:
- No rigid schema - notes grow organically
- No vendor lock-in - plain markdown
- AI has full context - local filesystem access
- Git-friendly - version control everything

**vs Wiki Systems**:
- AI-powered workflows (auto-log, rollup, health checks)
- Graph intelligence (find orphans, broken links, clusters)
- Zero-config - just works

**vs Personal PKM**:
- Team-scale graph (65 notes, 300+ links)
- Multi-role perspectives (engineers, PMs, vendors)
- Realistic complexity (subsystems, interfaces, decisions)

## Intentional Issues (For Demo)

**Orphan Notes** (no backlinks):
1. `team/Onboarding Guide.md` - Useful but never linked
2. `tests/Upcoming Tests.md` - Draft not integrated
3. `suppliers/Precision Components Inc.md` - Vendor forgotten
4. `systems/gnc/Trajectory Optimization.md` - Unref'd technical note

**Broken Links** (for `/vault-fix-links` demo):
1. `Propulsion System.md` → `[[Combustion Chamber]]` (doesn't exist)
2. `Risk Register.md` → `[[DR-007]]` (typo, should be `[[ADR-007]]`)
3. Meeting notes → `[[Q1 Planning]]` (renamed)

**Varying Heading Styles** (tests section matching):
- Some notes use `## Log`, others `### Log`, one uses `# Log`
- Demonstrates Flywheel works regardless of heading level

## Technical Content

All aerospace content is technically accurate but not proprietary:
- Real terminology (ISP, delta-v, LOX, RP-1)
- Realistic performance numbers
- Actual engineering processes (FEA, CFD, FMEA)
- No export-controlled info (ITAR/EAR compliant)

## Next Steps

1. Explore the graph - click through wikilinks
2. Try Flywheel workflows - `/vault-health`, `/auto-log`
3. Ask questions - "How does X connect to Y?"
4. See the pattern - this scales to any business/project

## About Flywheel

This demo showcases **Flywheel** - The Agentic Markdown Operating System.

Starting a new business or project? Install Flywheel - get AI-powered business infrastructure from day one.

Learn more: https://github.com/bencassie/flywheel
