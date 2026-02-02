# README Claims Audit

This document tracks all quantitative claims made in Flywheel and Flywheel-Crank README files, with evidence sources and verification status.

---

## Flywheel README Claims

### "See It In Action" Section

| Claim | Value | Evidence Source | Verification |
|-------|-------|-----------------|--------------|
| Query response time | "2 seconds" | `test/performance/graph.benchmark.test.ts` | **Tested** |
| Query token cost | "~200 tokens" | TOKEN_BENCHMARKS.md:197, carter-strategy README:79 | **Documented** |
| Traditional approach | "~6,000 tokens" | TOKEN_BENCHMARKS.md:32, carter-strategy README:79 | **Documented** |
| Efficiency multiplier | "30× more efficient" | carter-strategy README:198 ("22-44x savings") | **Documented** |
| Notes surfaced | "12 notes" | Illustrative example | **Narrative** |

### Verified Capabilities Section

| Claim | Value | Evidence Source | Verification |
|-------|-------|-----------------|--------------|
| Scale | "100k Note Scale" | `docs/SCALE_BENCHMARKS.md` | **Benchmarked** |
| Tool count | "51 Read-Only Tools" | Tool registration in `src/index.ts` | **Code** |
| Query latency | "Sub-Second Queries" | `test/performance/graph.benchmark.test.ts` | **Tested** |
| Platform support | "Cross-Platform" | CI workflows (Ubuntu, Windows, macOS) | **CI** |

---

## Flywheel-Crank README Claims

### "See It In Action" Section

| Claim | Value | Evidence Source | Verification |
|-------|-------|-----------------|--------------|
| Atomic commits | "4 files, 1 git commit" | Illustrative demo | **Narrative** |
| Auto-wikilinks | Feature demo | 108 tests in `wikilinks.test.ts` | **Tested** |
| Context cloud | Feature demo | `wikilinks.test.ts` | **Tested** |
| Single undo | Feature demo | `git-integration.test.ts` | **Tested** |

### Verified Capabilities Section

| Claim | Value | Evidence Source | Verification |
|-------|-------|-----------------|--------------|
| Scale | "100k Note Scale" | `docs/SCALE_BENCHMARKS.md` | **Benchmarked** |
| Mutation stability | "10k Mutation Stability" | `docs/SCALE_BENCHMARKS.md` | **Benchmarked** |
| Platform support | "Cross-Platform" | CI workflows | **CI** |
| Security | "Security Hardened" | Security test suite | **Tested** |
| Format preservation | "CRLF, indentation..." | Golden tests | **Tested** |

---

## Token Efficiency Claims (Shared)

From `flywheel-crank/docs/TOKEN_BENCHMARKS.md`:

| Operation | Traditional | With Flywheel | Savings | Type |
|-----------|-------------|---------------|---------|------|
| Add wikilinks | 1,000-1,500 tokens | 50-100 tokens | 10-20x | **Measured** |
| Daily note logging | 1,500-3,000 tokens | 150-300 tokens | 80-90% | **Measured** |
| Task management | 1,000-2,000 tokens | 100-200 tokens | 80-90% | **Measured** |
| Finding related notes | 5,000-20,000 tokens | 200-500 tokens | 95-99% | **Measured** |

---

## Verification Legend

| Status | Meaning |
|--------|---------|
| **Tested** | Automated test validates claim |
| **Benchmarked** | Performance benchmark with reproducible results |
| **Documented** | Detailed methodology in docs |
| **Code** | Verifiable by code inspection |
| **CI** | Continuous integration validates |
| **Narrative** | Illustrative example (not a performance claim) |

---

## Test Files

| Claim Category | Test File |
|----------------|-----------|
| Query latency | `packages/mcp-server/test/performance/graph.benchmark.test.ts` |
| Token efficiency | `flywheel-crank/docs/TOKEN_BENCHMARKS.md` |
| Wikilinks | `flywheel-crank/packages/mcp-server/test/core/wikilinks.test.ts` |
| Git integration | `flywheel-crank/packages/mcp-server/test/tools/git-integration.test.ts` |
| Scale benchmarks | `flywheel-crank/docs/SCALE_BENCHMARKS.md` |

---

## Running Verification

```bash
# Flywheel query benchmarks
cd flywheel
npm test -- --grep "Graph Query Performance"

# Flywheel-Crank token benchmarks
cd flywheel-crank
npm test -- --grep "performance benchmarks"

# Full test suites
npm test  # in each repo
```

---

*Last updated: 2026-02-02*
*Generated during front page redesign implementation*
