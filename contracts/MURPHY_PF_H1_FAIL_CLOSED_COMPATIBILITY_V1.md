# Murphy PF-H1 Fail-Closed Compatibility Contract V1

Status: COMPATIBILITY CONTRACT — NOT PRODUCTION FROZEN

## Scope
PF-H1 is the horizontal-boundary primitive used by Murphy 0014 and 0020 and any later rule that explicitly requires a horizontal boundary.

## Accepted evidence
A boundary is horizontally compatible only when the canonical geometry artifact explicitly reports exact horizontal geometry (`slope == 0`).

## Rejected / non-evaluable evidence
- near-horizontal geometry
- approximate slope values
- inferred horizontal status from visual similarity
- any newly introduced percentage, pip, ATR, or angle tolerance
- any threshold selected from backtest performance

Such cases MUST return `NOT_EVALUABLE`.

## Provenance
The boundary must come from the canonical geometry pipeline and carry upstream pivot availability/provenance. Missing or future-dependent provenance is `NOT_EVALUABLE`.

## Rule use
- 0014: H1 may satisfy the upper horizontal-boundary prerequisite; remaining rule gates remain independent.
- 0020: H1 must satisfy both upper and lower horizontal-boundary prerequisites; parallelism remains a separate geometry gate.

## Freeze restriction
This contract is not a claim that PF-H1 is production-frozen. Production freeze requires the project's full compatibility, no-lookahead, test, historical QA, and evidence gates.

2025 remains OOS and must not be used for tuning.
