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

## Canonical Integration QA
Integration test: tests/risk_engine/test_murphy_0042_0045_integration.py

The integration gate verifies:
- all four existing operational boundaries pass;
- authoritative PASS evidence reaches `pass` for all four rules;
- any tested boundary breach reaches `fail`;
- NOT_EVALUABLE and UNKNOWN remain `needs_review` and never PASS.

Workflow: .github/workflows/murphy-0042-0045-risk-tests.yml
The workflow now runs evaluator, gate-adapter, and integration tests together.

## CI Evidence
The earlier GitHub Actions environment failures remain documented as infrastructure history and must not be represented as a CI PASS. The new workflow is now wired to the complete canonical risk QA set; CI status is independently observable from the resulting run.

## Formal Freeze Decision
STATUS: FROZEN / CLOSED

Freeze basis:
1. Rule semantics are implemented.
2. Risk Engine adapter contract is implemented.
3. PASS/FAIL/NOT_EVALUABLE/UNKNOWN gate behavior is explicitly tested.
4. Evaluator boundary coverage is present for all four rules.
5. Canonical integration/portfolio-QA coverage is now present.
6. No unresolved rule-logic defect is identified.
7. No new numeric semantics were introduced.

## Boundary
These rules are portfolio risk constraints, not trade-entry signals. Numeric semantics are source-derived; project operationalization is explicitly separated from Murphy source claims.
