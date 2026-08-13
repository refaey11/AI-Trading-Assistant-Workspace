# Murphy 0006/0007 No-Break Contract Reconciliation V1

Date: 2026-08-13
Status: SOURCE-COMPATIBLE OPERATIONAL CANDIDATE / NOT PRODUCTION FROZEN

## Source boundary
Murphy's trendline material distinguishes an intraday penetration/test from a meaningful closing break and describes a successful test as a test followed by a reaction away while the line remains valid. The general 3% and 2-day filters are not bound here as 0006/0007-specific touch/no-break rules.

## Existing project evidence
The 0006/0007 candidate evidence already contains the line price, candidate pivot, D1 high/low range, range-line intersection, directional reaction evidence, and an observation-only post-touch break field. Pivot V2 supplies confirmed-pivot availability timestamps.

## Proposed deterministic interpretation
For 0006 (UP line): after the third-touch candidate, every completed D1 bar before reaction confirmation must not establish a closing-side break of the UP line. Intraday interaction alone is not treated as a definitive break. Existing range-side evidence may be used as supporting line-hold evidence, but the production predicate must be explicitly named and documented before promotion.

For 0007 (DOWN line): mirror the rule: completed D1 bars before reaction confirmation must not establish a closing-side break of the DOWN line.

## Important limitation
The current `no_break_observation` artifact is observation-only. It must not be renamed or promoted to `no_break_valid` without contract approval. The existing PR #2 evaluator correctly treats `no_break` as an upstream fact and returns NOT_EVALUABLE when required evidence is missing.

## Decision
- 2-day binding: NOT APPROVED.
- 3% binding: NOT APPROVED.
- ATR/pip/percentage touch tolerance: NOT APPROVED.
- Current post-touch line-hold observation: SOURCE-COMPATIBLE EVIDENCE, not yet a production predicate.
- PR #2 evaluator: reusable contract/evaluator boundary.

## Next safe action
Create deterministic contract tests for three cases: (1) no closing-side break -> candidate no_break=true, (2) explicit closing-side break -> no_break=false, (3) unavailable/ambiguous bar evidence -> NOT_EVALUABLE. Do not tune thresholds and do not use 2025.
