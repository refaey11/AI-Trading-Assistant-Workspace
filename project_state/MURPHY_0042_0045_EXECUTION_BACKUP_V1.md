# Murphy 0042-0045 Execution Backup V2

Date: 2026-08-17

## Scope
Final execution backup for Murphy Chapter 16 Capital Allocation / Portfolio Risk rules 0042-0045.

## Source-derived constraints
- 0042 Capital reserve: total investment <= 50% of available capital.
- 0043 Single-market exposure: source states 10%-15% of total capital; operational adapter uses 15% as the maximum boundary while preserving the source range metadata.
- 0044 Maximum risk per market: <= 5% of total capital.
- 0045 Total margin: source states 20%-25% of total capital; operational adapter uses 25% as the maximum boundary while preserving the source range metadata.

## Architecture
These are portfolio-level NO_TRADE / risk constraints, not entry signals. They are isolated in `risk_engine/murphy_0042_0045_risk_adapter.py` and do not alter Murphy direction, confirmation, or entry logic.

## Implementation
- Risk adapter: `risk_engine/murphy_0042_0045_risk_adapter.py`
- Evaluator tests: `tests/risk_engine/test_murphy_0042_0045.py`
- Gate-adapter tests: `tests/risk_engine/test_murphy_0042_0045_gate_adapter.py`
- Canonical integration tests: `tests/risk_engine/test_murphy_0042_0045_integration.py`
- CI workflow: `.github/workflows/murphy-0042-0045-risk-tests.yml`

## Problems and solutions
1. The rules were incomplete in the generic trading-rules schema. Solution: dedicated portfolio-risk adapter.
2. Murphy gives ranges for 0043 and 0045 rather than one project execution number. Solution: preserve source ranges and use only the upper boundary as the conservative operational maximum.
3. These rules do not generate BUY/SELL signals. Solution: evaluator returns constraint pass/fail only.

## QA evidence
- Existing local evaluator QA: 5/5 PASS.
- Gate adapter tests cover PASS, FAIL, NOT_EVALUABLE, and UNKNOWN behavior.
- Canonical integration QA covers all four rules, boundary behavior, hard-fail behavior, and missing/unknown evidence.
- CI workflow is configured to execute evaluator, gate-adapter, and integration tests together.
- GitHub Actions execution evidence must not be called CI PASS unless an actual successful run is present.

## Freeze
STATUS: PRODUCTION FROZEN / CLOSED.

Freeze boundary:
- Rule semantics implemented.
- Risk adapter contract implemented.
- Evaluator and gate behavior tested.
- Canonical integration QA added.
- Registry synchronization completed.
- No unresolved rule-logic defect identified.
- No new numeric semantics or tuning introduced.

## Governance
- These rules remain portfolio-risk constraints, not trade-entry signals.
- 2025 is OOS and was not used for tuning, selection, calibration, optimization, or status decisions.
- Existing components were integrated rather than rebuilt.

## Recovery instruction
If this batch needs to be restored, use the files listed in the Implementation section together with the canonical Murphy 51 status registry. Do not reopen 0042-0045 as routine cleanup.
