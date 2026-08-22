# Murphy 0030–0033 Runtime Audit — 2026-08-22

## Scope
Compatibility and runtime audit for frozen Murphy rules 0030–0033. No source semantics were reopened.

## 0030–0032
- Canonical shared core: `src/murphy_0030_0032/pnf_3box_reference.py`
- Compatibility entrypoint already existed and is explicitly part of the frozen implementation.
- Frozen semantic outputs:
  - 0030 = `PNF_BULLISH_SUPPORT_REFERENCE`
  - 0031 = `BELOW_PREVIOUS_O_COLUMN`
  - 0032 = `ABOVE_PREVIOUS_X_COLUMN`
- Runtime adapter: `MURPHY_EVALUATORS_V1/murphy_0030_0032_runtime_v1.py`
- Unified runtime entry point: `MURPHY_EVALUATORS_V1/murphy_runtime_entrypoint_v1.py`
- Smoke coverage: PASS for support reference, long-stop reference, short-stop reference, and missing-evidence handling.
- Historical evidence remains the already-frozen 2016–2024 P&F QA/prefix replay; 2025 remains OOS.

## 0033
- Existing frozen evaluator semantics reused unchanged from `rules/murphy/0033/evaluator_candidate_v1.py`.
- Runtime adapter: `MURPHY_EVALUATORS_V1/murphy_0033_runtime_v1.py`
- Unified runtime entry point integrated.
- Smoke coverage: PASS for confirmed contextual evidence and missing-input NOT_EVALUABLE.
- Existing historical QA: 273,387 rows, 2016–2024; prefix/no-lookahead PASS; 2025 excluded.

## Decision
0030, 0031, 0032, and 0033 are now **Runtime Implemented** because executable adapters are wired into the unified runtime entry point and the mapped behaviors pass direct smoke verification. This does not convert any historical QA into a profitability claim and does not change frozen source semantics.

## Boundaries
- 0030–0032 remain structural/evidence operators; no autonomous BUY/SELL trigger is introduced.
- 0031/0032 receive no invented ATR/pip/percentage offset.
- 0033 remains NEUTRAL/contextual evidence only and does not generate direction.
- 2025 remains OOS and unused for tuning/selection.
