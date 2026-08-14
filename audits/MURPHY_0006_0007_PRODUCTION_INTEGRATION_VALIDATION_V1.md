# MURPHY 0006/0007 — PRODUCTION-PATH INTEGRATION VALIDATION V1

Date: 2026-08-15
Status: IMPLEMENTED / VALIDATION PENDING CI

## Scope

Connect the existing Murphy 0006/0007 confirmation operator to the generic Decision Brain evidence shape without changing Murphy rule semantics.

## Compatibility decision

The generic Decision Brain adapter contract requires normalized evidence with module, source_rule_id, statement, direction, strength, available, gate, conflict, plus decision_hint/confidence_delta at the broader contract level.

The Murphy bridge therefore maps only an already-evaluated `Confirmation` object. It does not calculate third touch, reaction, no-break, thresholds, or lookbacks.

## Mapping

- `MURPHY_0006` -> `module=murphy_context`, `direction=bullish`
- `MURPHY_0007` -> `module=murphy_context`, `direction=bearish`
- confirmed evidence -> `available=true`, `gate=pass`, `conflict=supports`
- `strength=0.45` is a bounded adapter value only; it is not a Murphy threshold and does not create a trade
- `confidence_delta=0.0`; final confidence remains a Decision Brain responsibility
- unavailable confirmation -> neutral / unavailable / needs_review / insufficient

## Anti-regression constraints

1. Pivot V2 is unchanged.
2. Geometry V1 is unchanged.
3. Murphy 0006/0007 evaluator semantics are unchanged.
4. No 3%, 2-close, ATR, pip, percentage, or hidden lookback threshold was added.
5. 2025 remains excluded from tuning/selection.
6. Adapter output is evidence, not an autonomous trade decision.
7. Similarity, Nison, process, and risk precedence remain outside this bridge.

## Changes committed

- `src/murphy_0006_0007/decision_brain_adapter.py`
- `tests/test_murphy_0006_0007_decision_brain_adapter.py`
- `.github/workflows/murphy-evidence-adapter-tests.yml` updated to execute both Murphy adapter test files.

## Validation state

The implementation and regression tests are committed. GitHub combined status for the latest commit currently reports no status entries, so CI execution is not yet independently evidenced by a completed workflow result.

Therefore this gate is **NOT YET CLOSED**. The next required action is to obtain a successful CI run and then perform the final production-path validation against the frozen 2016–2024 evidence.

## Freeze impact

This work closes the implementation gap only. It does not by itself close the numeric no-break governance gate or authorize Production Frozen status.
