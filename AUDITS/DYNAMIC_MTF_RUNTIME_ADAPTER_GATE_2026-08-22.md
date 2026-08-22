# Dynamic MTF Runtime Adapter Gate — 2026-08-22

## Scope
Implement a deterministic adapter from the authoritative `DYNAMIC_MTF_BINDING_V1` contract using the existing six-timeframe evidence. No new scoring, thresholds, directional rules, or 2025-derived selection logic are introduced.

## Implemented
- `compatibility/dynamic_mtf_binding_adapter_v1.py`
- `tests/compatibility/test_dynamic_mtf_binding_adapter_v1.py`

## Contract guarantees
- Allowed runtime timeframes are limited to the governed six-timeframe set: M5/M15/M30/H1/H4/D1.
- Role assignment must be explicitly supplied by source-backed evidence; the adapter does not invent a selector heuristic.
- Missing required role evidence returns `NOT_EVALUABLE`.
- Forbidden/unavailable timeframe values return `NOT_EVALUABLE`.
- Higher-context roles cannot be overridden by a lower timeframe; inconsistent role ordering returns `CONFLICTED` / fail-closed.
- The adapter never produces BUY/SELL and leaves `final_trade_decision` unset.

## Evidence boundary
The six-timeframe as-of/no-lookahead evidence for 2020–2024 is already closed in `AUDITS/TIMEFRAME_FULL_SIX_TF_ASOF_ALIGNMENT_2020_2024_2026-08-22.md`.

## Status
**IMPLEMENTED — TEST EXECUTION/CI VERIFICATION PENDING**

This gate does not claim Dynamic MTF production readiness until the test suite is executed through the project CI path. Time/Session remains `NOT_EVALUABLE/BLOCKED` because exhaustive source search found no authoritative contract/runtime.

2025 remains protected OOS and is not used for tuning or selection.
