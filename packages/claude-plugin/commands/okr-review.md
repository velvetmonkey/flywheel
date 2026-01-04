# /okr-review - Quarterly OKR Review

Generate a quarterly OKR progress review.

## Usage

```
/okr-review                    # Current quarter
/okr-review Q4-2025            # Specific quarter
```

## What It Does

```
OKR Review
────────────────────────────────────────────────────────────────
Reviewing: Q4-2025 OKRs (3 objectives, 9 key results)
────────────────────────────────────────────────────────────────
```

## Where Output Goes

| Action | Target | Notes |
|--------|--------|-------|
| Review | Console output | Progress report |
| Summary | Quarterly note | OKR status |

## Example Output

```
OKR Review: Q4-2025
===============================================

OBJECTIVE 1: Launch Product X
Progress: 75%

  KR1: Complete development (90%)
    Evidence: [[Project Alpha]] shipped
    Status: On track

  KR2: Acquire 100 users (60%)
    Current: 60 users
    Status: At risk

  KR3: NPS > 40 (80%)
    Current: 42 NPS
    Status: Achieved

OBJECTIVE 2: Improve Infrastructure
Progress: 85%

  KR1: 99.9% uptime (100%)
    Current: 99.95%
    Status: Exceeded

  ...

OVERALL PROGRESS:
  Achieved: 4/9 key results
  On track: 3/9 key results
  At risk: 2/9 key results

RECOMMENDATIONS:
  Focus on KR2 (user acquisition)
  Continue momentum on infrastructure

===============================================
```
