# Three-Book Decision Evaluator V1 — Milestone Audit

Date: 2026-08-22
Status: IMPLEMENTED / CI PENDING

## Scope
A narrow evaluation boundary was added around the existing Decision Brain V1 and existing three-book decision contract. It does not modify the recovered Decision Brain source, does not alter frozen rule semantics, and does not use 2025 for tuning/calibration.

## Governance enforced
- Current runtime allowlist is the corrected 78-rule boundary: 34 Murphy + 44 Nison.
- MURPHY_0008 remains blocked / NOT_EVALUABLE.
- Unknown or non-allowlisted rule IDs are rejected.
- Murphy provides technical context/direction; Nison confirms or contradicts and cannot create direction alone.
- Trading in the Zone is process-only and can block execution; it cannot create or reverse direction.
- Risk is a hard gate and must explicitly pass.
- Stop loss must be defined before an EXECUTABLE result.
- Brain neutral/conflicted state is NO_TRADE.
- 2025 remains OOS-only; no tuning, calibration, threshold selection, or future data is introduced by this evaluator.

## Source basis
- DECISION_BRAIN_V1_SPEC.json
- recovered Decision Brain V1 source
- Three-Book Decision Contract V1 / Decision Schema V1
- frozen 78-rule allowlist
- existing Decision-to-Execution bridge and OOS contract

## Implemented files
- evaluation/three_book_decision_evaluator_v1.py
- tests/evaluation/test_three_book_decision_evaluator_v1.py
- .circleci/config.yml job: three_book_decision_evaluator_v1

## Verification
Local isolated evaluator tests: 6 passed.
GitHub implementation commit: 3be1d10ad6406b65f3715e5ec20b81f70468e890
GitHub test commit: 4207ea39ac0b00ddedd8c2dba04ea141a7abd03e
GitHub CI commit: cd95a1d08dbce36cd5c13dff0ca6201ab3d2452d
CircleCI hosted status: pending user refresh/verification.

## Important OOS boundary
This milestone does NOT claim 2025 profitability. The authoritative frozen 2025 trade-event stream still has to be produced from existing market/rule/evidence sources without changing the frozen Decision Brain. TRUE_BACKTEST_V2 is not accepted as proof for this path.

## Next gate
Verify CircleCI green for the new evaluator, then wire the real 2025 source data/evidence stream into this evaluator and emit immutable raw decision/trade events before calculating performance metrics.
