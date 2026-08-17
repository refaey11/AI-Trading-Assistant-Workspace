# Murphy 0033 — QA Manifest V1

Status: QA-CANDIDATE / NOT FROZEN

## Scope
- Historical period: 2016-2024 only
- 2025: OOS and excluded from tuning
- Evidence source: MARKET_STATE reader dataset

## Results
- Historical rows checked: 273,387
- Reversal-candle rows: 80,053
- Confirmed contextual evidence: 7,255
- Conflict: 69,733
- Not evaluable: 23

## Prefix replay
- EURUSD: PASS (25 sampled points, 0 mismatches)
- GBPUSD: PASS (25 sampled points, 0 mismatches)
- USDCAD: PASS (25 sampled points, 0 mismatches)
- USDJPY: PASS (25 sampled points, 0 mismatches)
- XAUUSD: PASS (25 sampled points, 0 mismatches)

## Gate status
- Source reconciliation: PASS
- Contract candidate: PASS
- Evaluator candidate: PASS
- Deterministic tests: PASS (9/9)
- Prefix/no-lookahead sample: PASS
- Historical replay: PASS as deterministic execution QA
- Provenance/availability: PASS
- Canonical production freeze: BLOCKED

## Freeze blockers
1. Production evaluator integration into the canonical rule adapter has not been verified.
2. A canonical production freeze commit for MURPHY_0033 has not been verified.
3. Historical QA is execution validation, not profitability validation.
