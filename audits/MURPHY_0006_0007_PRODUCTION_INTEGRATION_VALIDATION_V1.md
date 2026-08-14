# MURPHY 0006/0007 — PRODUCTION-PATH INTEGRATION VALIDATION V1

Date: 2026-08-15
Status: PASS / INTEGRATION GATE CLOSED FOR PROJECT EVALUATOR

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

## CI evidence
Audit #14 was manually dispatched on the current freeze-review HEAD:
- HEAD: `c8497ef4a761856c6138a9c34c28ccd00305e99c`
- Branch: `audit/murphy-0006-0007-freeze-review-v1`
- Workflow: `0006-0007-deterministic-audit.yml`
- Run: #14
- Result: SUCCESS
- Deterministic test result: `4 passed in 0.03s`
- Artifact: `0006-0007-deterministic-audit-14`
- Artifact SHA-256: recorded by GitHub Actions for the run
- Artifact contents include commit.txt, evidence.txt, pytest.txt, run_utc.txt, and run_cairo.txt.

The uploaded Audit #14 artifact independently confirms the tested commit as `c8497ef4a761856c6138a9c34c28ccd00305e99c` and records `4 passed in 0.03s`.

## Historical production-path evidence
`MURPHY_0006_0007_PRODUCTION_PATH_VALIDATION_V1.md` records a fresh 2016–2024 replay using canonical Pivot V2 + Geometry V1 and a freshly rebuilt D1 series, with:
- MURPHY_0006: 8
- MURPHY_0007: 7
- Total: 15
- 15/15 confirmation rows reproduced
- 2025 excluded
- availability/no-lookahead safeguards enforced
- no ATR/pip/percentage/2-day/3%/2025 tuning

## Gate decision
The Decision Brain adapter implementation/integration gate is CLOSED for the project evaluator layer. This closure means the evaluated Murphy confirmation can be represented as Decision Brain evidence without changing Murphy semantics.

This does NOT claim that an external live trading runtime has been proven. The adapter remains evidence-only and cannot autonomously create a trade.

## Freeze impact
The evaluator-layer integration gate is closed. Final rule freeze is governed by the dedicated freeze manifest, which must separately distinguish evaluator freeze from any future live/runtime deployment claim.
