# MURPHY 0042–0045 — FREEZE QA MANIFEST V2
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

## QA Coverage
- Numeric boundary tests for all four rules.
- Breach tests above every operational upper bound.
- Negative-input rejection tests.
- Portfolio aggregate PASS/FAIL tests.
- Canonical gate adapter tests: PASS -> pass; FAIL -> fail; NOT_EVALUABLE/missing evidence -> needs_review; UNKNOWN -> needs_review, never PASS.

## Verification
Exact adapter logic and the added boundary/aggregate test logic were executed in an isolated local pytest environment using the repository source content: 4 test groups passed.
GitHub Actions remains an infrastructure verification issue: recent repository runs terminate before executing job steps. This is not treated as a rule/test failure and is not claimed as CI PASS.

## Freeze Decision
STATUS: FROZEN / CLOSED
Rules 0042, 0043, 0044, and 0045 are complete and frozen. Do not reopen or retune them unless a source correction, integration defect, or explicitly approved project change is identified.

## Boundary
These rules are portfolio risk constraints, not trade-entry signals. Numeric semantics are source-derived; project operationalization is explicitly separated from Murphy source claims. The Similarity Engine and historical memory do not override these hard risk gates.
