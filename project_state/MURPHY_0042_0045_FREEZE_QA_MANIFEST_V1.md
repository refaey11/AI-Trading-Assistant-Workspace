# MURPHY 0042–0045 — FREEZE QA MANIFEST V1
Date: 2026-08-17

## Batch
Murphy Chapter 16 — Capital Allocation / Portfolio Risk Constraints

## Rules
- 0042: total investment <= 50%
- 0043: single-market exposure; source range 10–15%, operational upper bound 15%
- 0044: risk per market <= 5%
- 0045: total margin; source range 20–25%, operational upper bound 25%

## Implementation
Adapter: risk_engine/murphy_0042_0045_risk_adapter.py
Implementation commit: 26ebae1bf37209dce0012c465f7071bf05a8ca63

## Tests
Existing boundary suite covers all four rules and individual breach cases.
Canonical gate adapter tests cover:
- PASS -> pass
- FAIL -> fail / hard block
- missing evidence -> needs_review
- UNKNOWN -> needs_review, never PASS
Test commit: f37063b5c6073783ca30b841e7ebeb7ded080312

## QA Status
Local adapter/gate contract execution reported PASS.
Historical market backtest is NOT applicable to these portfolio-level constraints.

## CI Investigation
Multiple GitHub Actions workflows were triggered from the same test branch and failed immediately with jobs reporting `steps: null`, including the Murphy Evidence Adapter workflow and unrelated overnight/smoke workflows. This reproduces outside the 0042–0045 workflow and therefore is treated as a repository-level Actions execution blocker, not a rule/test failure.
The last known-good Murphy CI run (run 30) completed with all checkout/setup/pytest steps and 7 tests passing.

Representative failed runs:
- Murphy Evidence Adapter Tests run 33: failure, no job steps.
- Murphy Evidence Adapter Tests run 32: failure, no job steps.
- Murphy Evidence Adapter Tests run 31: failure, no job steps.
- Unrelated workflows on the same commit also failed with no job steps.

## Freeze Decision
STATUS: READY_EXCEPT_CI_ENVIRONMENT_BLOCKER
The 0042–0045 implementation and contract QA are complete. Production Freeze is intentionally not falsely claimed while the repository Actions runner cannot execute jobs.

## Cleanup
The temporary CI validation PR #21 was closed without merge, and the main Murphy workflow was restored to the previously known-good structure so the project is not left carrying experimental CI changes.

## Boundary
These rules are portfolio risk constraints, not trade-entry signals. Numeric semantics are source-derived; project operationalization is explicitly separated from Murphy source claims.
