# Nexus Lab

> See how your research connects - from foundational papers to your latest experiments.

---

**You are**: A PhD student in computational biology

**Your situation**: You're studying protein folding and drug-target prediction. Your notes include 7 foundational papers, 6 methods, 10 experiments, and 2 active projects. You need to trace how ideas flow from literature through your work.

## Vault Map

```
┌─────────────────────────────────────────────────────────┐
│                      NEXUS LAB                          │
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │ PAPERS        AlphaFold 2 ─── ESMFold ─── GROMACS│   │
│  └────────────────────┬────────────────────────────┘   │
│                       │ informs                        │
│                       ▼                                │
│  ┌─────────────────────────────────────────────────┐   │
│  │ METHODS           Protein Folding Method        │   │
│  └────────────────────┬────────────────────────────┘   │
│                       │ used-by                        │
│                       ▼                                │
│  ┌─────────────────────────────────────────────────┐   │
│  │ EXPERIMENTS   Run 1 ─► Run 2 ─► Run 3 ─► Run 7  │   │
│  └────────────────────┬────────────────────────────┘   │
│                       │ feeds                          │
│                       ▼                                │
│  ┌─────────────────────────────────────────────────┐   │
│  │ PROJECTS          Drug Target Prediction        │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

## Try it now

Ask Claude:

- "How does AlphaFold connect to my docking experiment?"
- "What did I work on last week?"
- "Which experiments share the same methods?"
- "Summarize my November research"
- "What papers haven't I built on yet?"

## What you'll discover

- Trace citation chains from papers through methods to your experiments
- Find which experiments build on each other
- See patterns in your research you didn't notice

---

## How mutations work

When you ask Claude to make changes:

### Log experiment results

```
You: "/log docking run 7 complete - 0.3Å RMSD"

┌─ MUTATION ───────────────────────────────────────┐
│ Reads:   ## Log section (35 tokens)              │
│ Appends: daily-notes/2026-01-04.md               │
└──────────────────────────────────────────────────┘

## Log
- 09:00 Literature review
- 15:22 docking run 7 complete - 0.3Å RMSD         ← NEW
```

### Trace a connection

```
You: "How does AlphaFold connect to my docking experiment?"

┌─ QUERY ──────────────────────────────────────────┐
│ Source: Graph index (no file reads)              │
│ Tokens: ~60 vs ~4,000 without Flywheel           │
└──────────────────────────────────────────────────┘

Claude traces the graph:
  [[AlphaFold 2]] (paper)
    → informs → [[Protein Folding Method]]
    → used by → [[Structure Prediction Exp]]
    → provides input to → [[Docking Experiment 7]]

Connection path (3 hops):
1. AlphaFold 2 paper introduced attention-based folding
2. You adapted this in your Protein Folding Method
3. That method generates structures for your docking runs
```

### Link a paper to your method

```
You: "connect AlphaFold paper to my folding method"

┌─ MUTATION ───────────────────────────────────────┐
│ Reads:   methods/protein-folding.md              │
│ Modifies: methods/protein-folding.md             │
└──────────────────────────────────────────────────┘

## References
- [[AlphaFold 2]]                                  ← NEW
```

### Find unused papers

```
You: "What papers haven't I built on yet?"

┌─ QUERY ──────────────────────────────────────────┐
│ Source: Graph index (backlink analysis)          │
│ Tokens: ~40 vs ~2,500 without Flywheel           │
└──────────────────────────────────────────────────┘

Orphan Papers (no outgoing links to your work):
- [[Rosetta Commons]] - docking algorithms
- [[GROMACS Tutorial]] - MD simulation setup

These papers are in your library but not connected
to any methods or experiments yet.
```

### Map my research

```
You: "How does my work connect to the literature?"

┌─ CHAIN ──────────────────────────────────────────┐
│ Queries: Papers with forward links to methods    │
│          Methods with backlinks from experiments │
│          Build citation flow map                 │
│          (~180 tokens vs ~4,000 full reads)      │
└──────────────────────────────────────────────────┘

Research Connection Map
=======================
[[AlphaFold 2]] → [[Protein Folding Method]] → 7 experiments
[[ESMFold]] → [[Structure Prediction]] → 3 experiments
[[GROMACS]] → (no connections yet)

Suggestion: Link GROMACS to your MD simulation work
```

---

*30 notes. Just start asking questions.*

---

**Token savings:** Each note in this vault averages ~160 lines (~2,400 tokens).
With Flywheel, graph queries cost ~50-100 tokens instead of reading full files.
That's **24-48x savings** per query—enabling hundreds of queries in agentic workflows.
