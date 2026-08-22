# Murphy 0047–0049 — Runtime Audit

Date: 2026-08-22
Status: 0047 VERIFIED; 0048/0049 BLOCKED ON OPERATOR CONTRACT

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

## 0048 / 0049 compatibility audit
Canonical TRIN evidence is now present and historically ingested, but the authoritative rule-specific operator needed to turn the available fields into a deterministic evaluator was not recovered from the current source/contract artifacts.

Therefore:
- 0048: **NOT_EVALUABLE / RUNTIME UNPROVEN**
- 0049: **NOT_EVALUABLE / RUNTIME UNPROVEN**

Do not introduce common-market TRIN thresholds or substitutes. The final historical labels are evidence for reconciliation, not a license to infer an operator that the project has not source-locked.

## Governance controls
- Existing evidence reused; no rebuild of breadth/TRIN ingestion.
- 2025 remains OOS and was not used for tuning or operator selection.
- No proxies, synthetic rows, new thresholds, or new timeframes were introduced.
