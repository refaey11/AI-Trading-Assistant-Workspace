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
Local execution reported PASS for the adapter/gate contract checks.
GitHub Actions has no workflow run attached to the test commit, so CI execution is NOT CLAIMED.
Historical market backtest is NOT applicable to these portfolio-level constraints.

## Freeze Decision
STATUS: NOT_YET_FROZEN
Reason: official repository CI execution and final production freeze evidence are still absent.
No false PASS or false production-freeze claim is permitted.

## Boundary
These rules are portfolio risk constraints, not trade-entry signals. Numeric semantics are source-derived; project operationalization is explicitly separated from Murphy source claims.
