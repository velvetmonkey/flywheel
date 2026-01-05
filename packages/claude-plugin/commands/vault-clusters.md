---
skill: vault-clusters
---

# /vault-clusters - Find Knowledge Clusters

Find groups of notes that are densely connected (knowledge clusters).

## Usage

```
/vault-clusters                      # Find all clusters
```

## What It Does

```
Cluster Analysis
────────────────────────────────────────────────────────────────
Found: 12 knowledge clusters
Avg size: 14 notes    Avg cohesion: 78%
────────────────────────────────────────────────────────────────
```

## What is a Cluster?

A cluster is 3+ notes where:
- Each links to at least 2 others in the group
- More connected internally than externally
- Forms a cohesive topic/project

## Where Output Goes

| Action | Target | Notes |
|--------|--------|-------|
| Report | Console output | Cluster list |
| MOC suggestions | Console output | Organization ideas |

## Example Output

```
Knowledge Clusters
===============================================

Found 12 knowledge clusters

TOP CLUSTERS BY SIZE:

**Cluster 1: Data Platform** (23 notes, 89% cohesion)
Hub: [[Main Project]]
Notes: [[Database]], [[API]], [[Pipeline]], [[Data Quality]]...

**Cluster 2: Development Tools** (18 notes, 76% cohesion)
Hub: [[Dev Environment]]
Notes: [[Git]], [[VS Code]], [[GitHub]], [[Python]]...

**Cluster 3: Work Process** (15 notes, 82% cohesion)
Hub: [[Workflow]]
Notes: [[Deployments]], [[Releases]], [[Testing]]...

STATISTICS:
  Total clusters: 12
  Average size: 14.3 notes
  Average cohesion: 78%
  Unclustered: 200 notes (20% of vault)

INSIGHTS:
  3 major topic areas dominate vault
  Data platform cluster is most cohesive
  Consider MOC for each cluster
  Unclustered notes may need topic assignment

===============================================
```
