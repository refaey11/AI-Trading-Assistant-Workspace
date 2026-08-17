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

## Contract QA
Canonical gate adapter tests cover:
- PASS -> pass
- FAIL -> fail / hard block
- missing evidence -> needs_review
- UNKNOWN -> needs_review, never PASS
Test file: tests/risk_engine/test_murphy_0042_0045_gate_adapter.py

Boundary/evaluator coverage exists for all four rules and individual breach cases.
Local adapter/gate QA: PASS.

## CI Evidence
Official GitHub Actions was attempted and the repository repeatedly returned failed jobs with zero executed steps (`steps: []`), including run 31988569672 / job 95268788625. This is a repository Actions execution/environment blocker and not a failing 0042–0045 test result. The last known-good Murphy CI run completed successfully with 7 tests passing.

## Formal Freeze Decision
STATUS: FROZEN / CLOSED

Freeze basis:
1. Rule semantics are implemented.
2. Risk Engine adapter contract is implemented.
3. PASS/FAIL/NOT_EVALUABLE/UNKNOWN gate behavior is explicitly tested.
4. Local QA is PASS.
5. No unresolved rule-logic defect is present.
6. CI environment failure is independently documented and does not provide evidence of a rule/test failure.

CI note: this batch is frozen on the implementation/QA evidence above; the blocked GitHub Actions environment remains an infrastructure note and must not be represented as a CI PASS.

## Boundary
These rules are portfolio risk constraints, not trade-entry signals. Numeric semantics are source-derived; project operationalization is explicitly separated from Murphy source claims.
