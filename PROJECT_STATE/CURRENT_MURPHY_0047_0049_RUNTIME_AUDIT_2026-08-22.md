# Murphy 0047–0049 — Runtime Audit

Date: 2026-08-22
Status: 0047 VERIFIED; 0048/0049 VERIFIED

## Historical closure reconciliation
- 0047: 25 final occurrences
- 0048: 186 final occurrences
- 0049: 122 final occurrences
- Coverage: 2016-01-04 through 2020-02-10
- Final replay trading-day rows: 1,033
- 2025 used: false
- Synthetic rows: false
- Proxy substitution: false

## 0047 compatibility audit
Canonical final replay exposes the normalized evidence fields:
- `index_new_high`
- `ad_fails_high`
- `rule_0047`

The executable rule contract is source-bounded to the replay evidence:
`index_new_high AND ad_fails_high -> 0047 PASS`.
No new threshold, timeframe, proxy, or future-looking condition was introduced.

Replay reconciliation already established:
- Expected 0047 condition count: 25
- Existing `rule_0047` label count: 25
- Label mismatches: 0

## 0047 runtime
- Evaluator: `MURPHY_EVALUATORS_V1/murphy_0047_runtime_v1.py`
- Tests: `MURPHY_EVALUATORS_V1/test_murphy_0047_runtime_v1.py`
- Unified entry point: `MURPHY_EVALUATORS_V1/murphy_runtime_entrypoint_v1.py`
- Local deterministic smoke: 4/4 PASS
- Status: **RUNTIME VERIFIED**

## 0048 compatibility audit
The Murphy Chapter 18 TRIN source defines extremely high TRIN readings as above **1.20 on a 10-day moving average**, indicating oversold/panic-selling conditions.

Source-bounded operator:
`trin_ma10 > 1.20 -> 0048 PASS`

Final replay reconciliation on all 1,033 trading-day rows:
- Expected 0048 labels: 186
- Operator hits: 186
- Overlap: 186
- Label-only: 0
- Operator-only: 0
- Mismatches: 0

## 0049 compatibility audit
The Murphy Chapter 18 TRIN source defines extremely low TRIN readings as below **0.70**, indicating excessive buying/overbought conditions.

Source-bounded operator:
`trin < 0.70 -> 0049 PASS`

Final replay reconciliation on all 1,033 trading-day rows:
- Expected 0049 labels: 122
- Operator hits: 122
- Overlap: 122
- Label-only: 0
- Operator-only: 0
- Mismatches: 0

## 0048 / 0049 runtime
- Evaluator: `MURPHY_EVALUATORS_V1/murphy_0048_0049_runtime_v1.py`
- Tests: `MURPHY_EVALUATORS_V1/test_murphy_0048_0049_runtime_v1.py`
- Unified entry point: `MURPHY_EVALUATORS_V1/murphy_runtime_entrypoint_v1.py`
- Unit assertions: 6/6 PASS
- Full historical operator-to-label reconciliation: 0048 = 186/186; 0049 = 122/122
- Status: **RUNTIME VERIFIED**

## Governance controls
- Existing TRIN/breadth evidence reused; no rebuild of ingestion.
- Murphy source thresholds only; no inferred/common-market substitutes.
- 2025 remains OOS and was not used for tuning or operator selection.
- No proxies, synthetic rows, new thresholds, or new timeframes were introduced.
