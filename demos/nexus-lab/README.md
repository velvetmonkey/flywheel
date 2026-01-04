# Nexus Lab - Flywheel Demo Vault #3

**Domain**: Computational Biology Research Lab (PhD student)
**Scale**: 30 notes
**Focus**: Relationship intelligence, temporal analysis, rollup agents, source/dead-end analysis

## Overview

This demo vault simulates a computational biology PhD student's research notes. It showcases Flywheel capabilities not demonstrated in the Artemis (aerospace) or Carter (consulting) demos.

### Graph Pattern: Citation/Influence Network

```
Literature (sources)
    ↓
Methods (common neighbors)
    ↓
Experiments (temporal clusters)
    ↓
Projects (dead-ends)
```

### Vault Structure

```
nexus-lab/
├── literature/      # 7 foundational papers (sources)
├── methods/         # 6 methodology notes (common neighbors)
├── experiments/     # 10 experiments (temporal clusters, citations)
├── daily/           # 5 daily lab notes (rollup chain)
├── projects/        # 2 active projects (dead-ends)
└── README.md        # This file
```

## Key Patterns

### 1. Sources (Literature Notes)
**High outlinks, low backlinks** - foundational knowledge consumed by experiments
- `Jumper2021-AlphaFold.md` → 3 outlinks, 0 backlinks
- `Mortazavi2008-RNA-Seq.md` → 4 outlinks, 0 backlinks

### 2. Common Neighbors (Methods)
**Referenced by multiple experiments** - shared methodologies
- `Centrality Measures.md` → Used by Exp-2024-11-18, Exp-2024-11-12
- `RPKM Normalization.md` → Used by Exp-2024-11-15, Mortazavi2008
- `AMBER Force Field.md` → Used by Exp-2024-11-22, Exp-2024-11-08

### 3. Temporal Clusters (Experiments)
**Nov 18-22 cluster** - 6 experiments in one week (contemporaneous)
- Exp-2024-11-15 (scRNA-Seq)
- Exp-2024-11-16 (validation)
- Exp-2024-11-18 (PPI network)
- Exp-2024-11-19 (CRISPR)
- Exp-2024-11-20 (ML prediction)
- Exp-2024-11-22 (docking)

### 4. Citation Chains
**Experiments build on each other** - demonstrates get_link_path
- Jumper2021-AlphaFold → Transformer Architecture → Exp-2024-10-28 → Exp-2024-11-22
- Barabasi2004-Network-Biology → Centrality Measures → Exp-2024-11-18 → Exp-2024-11-19

### 5. Bidirectional Links
**Mutual citations** - experiments validate each other
- Exp-2024-11-15 ↔ Exp-2024-11-16 (scRNA + validation)
- Exp-2024-11-18 ↔ Exp-2024-11-19 (network + CRISPR)
- Exp-2024-11-20 ↔ Exp-2024-11-22 (ML + docking)

### 6. Dead-Ends (Projects)
**High backlinks, low outlinks** - consume knowledge but don't produce new links yet
- `Drug-Target Prediction.md` → 4 backlinks (experiments), 0 outlinks
- `Single-Cell RNA-Seq Analysis.md` → 2 backlinks, 0 outlinks

---

## Demo Scenarios

### Scenario 1: Relationship Intelligence

**Goal**: Understand how different experiments relate to each other

#### 1A: Find Connection Path
```
Query: How does the AlphaFold paper connect to the docking experiment?

Tools:
- get_link_path("literature/Jumper2021-AlphaFold.md", "experiments/Experiment-2024-11-22.md")

Expected Result:
Jumper2021-AlphaFold
  → Transformer Architecture
  → Experiment-2024-10-28
  → Experiment-2024-11-22

Insight: 4-step chain from foundational paper to application
```

#### 1B: Measure Connection Strength
```
Query: How strongly related are the PPI network and CRISPR experiments?

Tools:
- get_connection_strength("experiments/Experiment-2024-11-18.md", "experiments/Experiment-2024-11-19.md")

Expected Result:
- Direct links: 2 (bidirectional)
- Common references: Barabasi2004, Centrality Measures
- Temporal proximity: 1 day apart
- Strength score: HIGH

Insight: Strong relationship - validation experiment of network predictions
```

#### 1C: Find Common References
```
Query: What methodologies do multiple experiments share?

Tools:
- get_common_neighbors("experiments/Experiment-2024-11-18.md", "experiments/Experiment-2024-11-12.md")

Expected Result:
Common neighbors:
- Centrality Measures (both use network analysis)
- Barabasi2004-Network-Biology (shared foundation)

Insight: Network analysis methods are common thread
```

#### 1D: Find Bidirectional Links
```
Query: Which experiments cite each other mutually?

Tools:
- find_bidirectional_links()

Expected Result:
Bidirectional pairs:
- Experiment-2024-11-15 ↔ Experiment-2024-11-16
- Experiment-2024-11-18 ↔ Experiment-2024-11-19
- Experiment-2024-11-20 ↔ Experiment-2024-11-22

Insight: Validation experiments create bidirectional relationships
```

#### 1E: Identify Knowledge Clusters
```
Query: What are the tightly connected knowledge areas?

Tools:
- /vault-clusters (Flywheel skill)

Expected Result:
Cluster 1: RNA-Seq ecosystem
- Mortazavi2008, Tang2009, RPKM Normalization
- Experiment-2024-11-15, Experiment-2024-11-16

Cluster 2: Network biology
- Barabasi2004, Centrality Measures, Graph Theory
- Experiment-2024-11-18, Experiment-2024-11-19, Experiment-2024-11-12

Cluster 3: Protein structure & docking
- Jumper2021-AlphaFold, Karplus2002, AMBER Force Field
- Experiment-2024-10-28, Experiment-2024-11-08, Experiment-2024-11-22

Insight: Three distinct research threads in the vault
```

---

### Scenario 2: Temporal Analysis

**Goal**: Understand work patterns and contemporaneous notes

#### 2A: Find Contemporaneous Experiments
```
Query: What other work was happening during the PPI network experiment?

Tools:
- get_contemporaneous_notes("experiments/Experiment-2024-11-18.md", hours=72)

Expected Result:
Notes edited within 72 hours of 2024-11-18:
- Experiment-2024-11-15 (Nov 15, -3 days)
- Experiment-2024-11-16 (Nov 16, -2 days)
- Experiment-2024-11-19 (Nov 19, +1 day)
- Experiment-2024-11-20 (Nov 20, +2 days)
- daily/2024-11-18.md (same day)
- daily/2024-11-19.md (next day)

Insight: High-activity week with 6 experiments in 8 days
```

#### 2B: Analyze Vault Activity
```
Query: How active has the vault been in the last month?

Tools:
- get_activity_summary(days=30)

Expected Result:
Activity summary (Oct 28 - Nov 22):
- Notes created: 30
- Notes modified: 35
- Most active week: Nov 18-22 (10 notes)
- Most active day: Nov 20 (4 notes)
- Peak activity: experiments/ folder

Insight: Experimental phase in late November with high output
```

#### 2C: Get Recent Work
```
Query: What have I worked on in the last week?

Tools:
- get_recent_notes(days=7)

Expected Result (from Nov 22):
- 2024-11-22: Experiment-2024-11-22, daily/2024-11-22.md
- 2024-11-21: daily/2024-11-21.md
- 2024-11-20: Experiment-2024-11-20, daily/2024-11-20.md
- 2024-11-19: Experiment-2024-11-19, daily/2024-11-19.md
- 2024-11-18: Experiment-2024-11-18, daily/2024-11-18.md
- 2024-11-16: Experiment-2024-11-16
- 2024-11-15: Experiment-2024-11-15

Insight: Busy experimental week with daily documentation
```

---

### Scenario 3: Source & Dead-End Analysis

**Goal**: Identify information flow patterns in the vault

#### 3A: Find Sources (Foundational Knowledge)
```
Query: Which notes are sources of knowledge (high outlinks, low backlinks)?

Tools:
- find_sources()

Expected Result:
Source notes (outlinks >> backlinks):
- Jumper2021-AlphaFold.md (5 outlinks, 2 backlinks)
- Mortazavi2008-RNA-Seq.md (5 outlinks, 3 backlinks)
- Barabasi2004-Network-Biology.md (4 outlinks, 3 backlinks)
- Libbrecht2015-ML-Genomics.md (5 outlinks, 3 backlinks)
- Karplus2002-Molecular-Dynamics.md (4 outlinks, 2 backlinks)

Insight: Literature notes are knowledge sources - they inform but aren't referenced
```

#### 3B: Find Dead-Ends (Knowledge Sinks)
```
Query: Which notes consume knowledge but don't produce new connections?

Tools:
- find_dead_ends(min_backlinks=2)

Expected Result:
Dead-end notes (backlinks >> outlinks):
- Drug-Target Prediction.md (4 backlinks, 0 outlinks)
- Single-Cell RNA-Seq Analysis.md (2 backlinks, 0 outlinks)

Insight: Project notes are work-in-progress - they integrate findings but haven't yet produced new knowledge nodes
```

#### 3C: Compare Source vs Dead-End Patterns
```
Analysis: Information flow in the vault

Sources (literature):
- Publish knowledge outward
- Few notes cite them (used, not discussed)
- Foundational layer

Dead-ends (projects):
- Consume knowledge from experiments
- Don't yet produce new notes
- Integration layer (work-in-progress)

Experiments (middle layer):
- Moderate backlinks (from projects)
- Moderate outlinks (to methods, literature)
- Knowledge transformation layer

Insight: Three-tier knowledge flow: Sources → Experiments → Projects
```

---

### Scenario 4: Rollup Chain

**Goal**: Demonstrate daily → weekly → monthly → quarterly → yearly rollup

#### 4A: Weekly Rollup
```
Query: Summarize the week of Nov 18-22

Tools:
- /rollup (triggers rollup-agent)
- rollup-weekly-agent for 2024-W47

Process:
1. rollup-agent detects date range for 2024-W47: Nov 18-24
2. Spawns rollup-weekly-agent
3. Agent uses get_notes_in_range("2024-11-18", "2024-11-24")
4. Finds daily notes: 2024-11-18.md through 2024-11-22.md (5 notes)
5. Extracts:
   - Experiments completed: 5 (PPI, CRISPR, ML, docking, +1)
   - Key insights: Network features predictive, ML model 89% AUC
   - Papers read: 3 (Barabasi, Libbrecht, Karplus)
   - Next steps: IC50 validation, MD analysis
6. Writes weekly-notes/2024-W47.md

Expected Output:
# 2024-W47 Summary

## Experiments Completed
- PPI network analysis (EGFR pathway)
- CRISPR validation (hub proteins)
- ML drug-target prediction (89% AUC)
- Molecular docking (top 10 compounds)
- MD simulations launched

## Key Achievements
- Network centrality predicts essentiality (r=0.73)
- ML integrates network features successfully
- Compound_472: -11.2 kcal/mol (best hit)

## Papers Read
- [[Barabasi2004-Network-Biology]]
- [[Libbrecht2015-ML-Genomics]]
- [[Karplus2002-Molecular-Dynamics]]

## Next Week
- Analyze MD trajectories
- Plan IC50 experimental validation
```

#### 4B: Extract Achievements
```
Query: What significant accomplishments are in my notes?

Tools:
- extract-achievements-agent (Flywheel agent)

Process:
1. Agent scans all notes for achievement markers:
   - "completed", "achieved", "published"
   - Novel findings, validations
   - Graph-aware: detects hub note creation, orphan reduction
2. Identifies:
   - ML model development (89% AUC)
   - Experimental validation (CRISPR confirms network predictions)
   - Lead compound identification (Compound_472)
3. Formats for Achievements.md

Expected Output:
## November 2024
- **ML drug-target model**: 89% AUC-ROC, network features in top-3
- **CRISPR validation**: Confirmed hub protein essentiality (r=0.73 correlation)
- **Lead identification**: Compound_472 (-11.2 kcal/mol binding energy)
```

---

### Scenario 5: Combined Queries

**Goal**: Use multiple tools in sequence for complex questions

#### 5A: Research Impact Analysis
```
Question: "How has the AlphaFold paper influenced my work?"

Workflow:
1. get_backlinks("literature/Jumper2021-AlphaFold.md")
   → Direct citations: Transformer Architecture, Exp-2024-10-28, Exp-2024-11-22

2. For each backlink, get_backlinks() again (2nd-order impact)
   → Exp-2024-10-28 cited by: Exp-2024-11-22, Drug-Target Prediction project

3. get_link_path() for longest chain
   → Jumper2021 → Transformer → Exp-10-28 → Exp-11-22 → Drug-Target Prediction

Result: AlphaFold influenced 3 experiments + 1 project, with 4-step citation chain to current work
```

#### 5B: Method Usage Analysis
```
Question: "Which experiments use Random Forests, and how do they relate?"

Workflow:
1. get_backlinks("methods/Random Forests.md")
   → Experiment-2024-11-20, Libbrecht2015-ML-Genomics

2. get_common_neighbors("experiments/Experiment-2024-11-20.md", "literature/Libbrecht2015-ML-Genomics.md")
   → Random Forests, Feature Engineering, Drug-Target Prediction project

3. get_connection_strength()
   → High strength: Exp-2024-11-20 directly implements Libbrecht methods

Result: ML experiment directly applies literature methods, connected through shared methodology notes
```

#### 5C: Weekly Progress Deep-Dive
```
Question: "What happened during my most productive week?"

Workflow:
1. get_activity_summary(days=30)
   → Most active week: Nov 18-22

2. get_notes_in_range("2024-11-18", "2024-11-22")
   → 11 notes (5 daily, 6 experiments)

3. For each experiment, get_backlinks() to find impact
   → Exp-2024-11-18 → Exp-2024-11-19, Exp-2024-11-20, Drug-Target project
   → Exp-2024-11-20 → Exp-2024-11-22, Drug-Target project

4. find_bidirectional_links() within date range
   → 3 bidirectional pairs (validation experiments)

5. get_contemporaneous_notes() for each day
   → Shows experimental workflow: Network → Validate → ML → Dock

Result: Productive week with 6 experiments forming coherent research narrative: network analysis validated by CRISPR, predictions validated by docking
```

---

## Quick Start

### 1. Connect Flywheel MCP

Ensure `.mcp.json` in vault root:
```json
{
  "mcpServers": {
    "flywheel": {
      "command": "npx",
      "args": ["-y", "@bencassie/flywheel-mcp"],
      "env": {
        "PROJECT_PATH": "/absolute/path/to/nexus-lab"
      }
    }
  }
}
```

### 2. Install Flywheel Plugin

```bash
claude plugin install github:bencassie/flywheel@bencassie-flywheel
```

### 3. Test MCP Connection

```
User: Get vault stats
Claude: [Uses mcp__flywheel__get_vault_stats()]
```

Should show ~30 notes, ~150 links.

---

## Tool Showcase Checklist

| Tool | Scenario | Demonstrated |
|------|----------|--------------|
| `get_link_path` | 1A | ✓ Citation chains |
| `get_connection_strength` | 1B | ✓ Experiment relationships |
| `get_common_neighbors` | 1C, 5B | ✓ Shared methods |
| `find_bidirectional_links` | 1D | ✓ Mutual validation |
| `/vault-clusters` | 1E | ✓ Knowledge areas |
| `get_contemporaneous_notes` | 2A | ✓ Temporal clustering |
| `get_activity_summary` | 2B | ✓ Vault activity |
| `find_sources` | 3A | ✓ Literature as sources |
| `find_dead_ends` | 3B | ✓ Projects as sinks |
| `rollup-agent` | 4A | ✓ Weekly rollup |
| `extract-achievements-agent` | 4B | ✓ Achievement detection |

---

## Comparison with Other Demos

| Feature | Artemis | Carter | Nexus Lab |
|---------|---------|--------|-----------|
| **Domain** | Aerospace startup | Solo consultant | Research lab |
| **Scale** | 65 notes | 29 notes | 30 notes |
| **Graph** | Clusters | Star pattern | Citation chains |
| **Focus** | Wikilinks, health | Frontmatter, tasks | Relationships, temporal |
| **Showcases** | auto-log, orphans, fix-links | vault-health, stale notes, schema | link_path, clusters, rollup, sources/dead-ends |

---

## Data Attribution

This is a **synthetic demo vault** created for Flywheel demonstration. All experimental data, results, and research described are fictional. Cited papers are real publications but experiments are not.

---

## Questions & Scenarios

Try these queries to explore Flywheel capabilities:

**Relationship queries:**
- "How are the two scRNA-Seq experiments related?"
- "What's the connection between AlphaFold and my docking work?"
- "Which methods are used by multiple experiments?"

**Temporal queries:**
- "What was I working on during the week of Nov 18?"
- "How active have I been in the last 2 weeks?"
- "Show me all experiments from October"

**Knowledge flow:**
- "Which papers haven't been cited by any experiments?"
- "What notes are knowledge sinks (consume but don't produce)?"
- "Find all notes that cite each other bidirectionally"

**Rollup queries:**
- "Summarize this week's lab work"
- "Extract achievements from November"
- "Create weekly summary for W47"

**Complex queries:**
- "Map the influence of network biology papers on my experiments"
- "How do my three research threads (RNA-Seq, network, structure) relate?"
- "What's the path from Mortazavi's 2008 paper to my current scRNA-Seq project?"
