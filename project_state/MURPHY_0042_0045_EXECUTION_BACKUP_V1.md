# Murphy 0042-0045 Execution Backup V1

Date: 2026-08-17

## Scope
Batch implementation for Murphy Chapter 16 Capital Allocation rules 0042-0045.

## Source-derived constraints
- 0042 Capital reserve: total investment <= 50% of available capital.
- 0043 Single-market exposure: source states 10%-15% of total capital; operational adapter uses 15% as the maximum boundary while preserving the source range metadata.
- 0044 Maximum risk per market: <= 5% of total capital.
- 0045 Total margin: source states 20%-25% of total capital; operational adapter uses 25% as the maximum boundary while preserving the source range metadata.

## Architecture
These are portfolio-level NO_TRADE / risk constraints, not entry signals. They are isolated in `risk_engine/murphy_0042_0045_risk_adapter.py` and do not alter Murphy direction, confirmation, or entry logic.

## Problems and solutions
1. The rules were represented as incomplete in the generic trading-rules schema. Solution: implement them as a dedicated portfolio-risk adapter rather than forcing them into indicator/backtest semantics.
2. Murphy gives ranges for 0043 and 0045 rather than a single project execution number. Solution: preserve the source range and use only the upper boundary as the conservative operational maximum; do not claim that 15% or 25% is a universal Murphy law beyond the source wording.
3. These rules do not generate BUY/SELL signals. Solution: evaluator returns constraint pass/fail only.

## Tests
Existing local pytest evidence: 5/5 PASS for boundary/evaluator coverage.
Existing gate tests cover PASS, FAIL, NOT_EVALUABLE, and UNKNOWN behavior.

New canonical integration QA:
- `tests/risk_engine/test_murphy_0042_0045_integration.py`
- all four boundaries pass through the evaluator;
- authoritative PASS maps to `pass` for all four rules;
- a boundary breach maps to `fail`;
- missing/unknown evidence maps to `needs_review`.

The CI workflow now executes evaluator, gate-adapter, and integration tests together.

## Freeze boundary
The previously identified integration/portfolio-QA gate is closed at the repository's canonical risk-adapter boundary. No new risk implementation or numeric semantics were introduced.

STATUS: PRODUCTION FROZEN / CLOSED pending registry synchronization in the same workflow.

## 2025
No tuning or selection uses 2025.
