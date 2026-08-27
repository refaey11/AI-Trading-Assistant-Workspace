# Final 78 Wiring Fix — 2026-08-26

## Problem reproduced
The governed final run preserved 34 Murphy + 44 Nison rows per timestamp, but the historical decision producer passed a legacy single-row Murphy candidate into the Three-Book evaluator while keeping the complete 34-rule envelope only for provenance.

The 2025 artifact therefore showed 6,225 NO_TRADE events: 3,534 `MURPHY_CONTEXT_NOT_PASS` and 2,691 `MURPHY_BRAIN_DIRECTION_CONFLICT`.

## Root cause
The legacy compatibility row can be a FAIL/NOT_EVALUABLE even when another Murphy rule in the complete 34-rule envelope has a directional PASS. This is a lossy reduction at the Decision Boundary.

## Fix implemented
`OOS_2025/full_decision_brain_assembler_v1.py` now creates a compatibility view from the complete governed Murphy `evidence_set` when the full 78-rule path is active:
- one directional PASS side -> compatibility PASS with that direction;
- both directional PASS sides -> explicit CONFLICT;
- no PASS but at least one FAIL -> FAIL;
- otherwise -> NOT_EVALUABLE.

The full evidence remains lossless and unchanged. No rule threshold, book semantics, P&L formula, risk protocol, or 2025 tuning was changed.

## Regression protection
Added `tests/evaluation/test_full_murphy_compatibility_view_v1.py` covering:
1. full-rule PASS must not be masked by a legacy FAIL;
2. conflicting PASS directions must not choose a side;
3. all-fail remains FAIL.

## Next gate
Wait for CircleCI on the new head. Compare the new 2025 event reason counts and executable events against the prior baseline. Do not accept profitability until the wiring behavior is verified.
