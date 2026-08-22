# Nison Runtime Batch 0001-0010 — 2026-08-22

## Scope
CANDLE_RULE_0001 through CANDLE_RULE_0010.

## Canonical source status
The Nison governance freeze states 38/38 candlestick pattern scopes and 6/6 methodology entries are source-contract frozen. This batch is therefore Runtime promotion work, not source re-freezing.

## Batch implementation
- 0001 Bullish Engulfing: existing evaluator retained and routed through batch router.
- 0002 Bearish Engulfing: existing evaluator retained and routed through batch router.
- 0003 Dark Cloud Cover: new source-mapped evaluator.
- 0004 Piercing Pattern: new source-mapped evaluator.
- 0005 On Neck: new source-mapped evaluator using categorical `near_previous_close` fact; no numeric tolerance invented.
- 0006 In Neck: new source-mapped evaluator using categorical `slightly_above_previous_close` fact; no numeric tolerance invented.
- 0007 Thrusting: new source-mapped evaluator using categorical `well_into_body` fact; no numeric tolerance invented.
- 0008 Morning Star: new source-mapped evaluator using categorical long/small/strong body facts.
- 0009 Evening Star: new source-mapped evaluator using categorical long/small/strong body facts.
- 0010 Morning Doji Star: new source-mapped evaluator using categorical doji/strong facts.

## Tests
Local execution:
- Positive batch: 10/10 PASS assertions.
- Wrong-trend rejection: 10/10 PASS assertions.
- Total deterministic assertions: 20/20 PASS.
- Unified router smoke for 0001/0002: 2/2 PASS.

## Lookahead/provenance
- Signal formation uses current/closed candle facts only.
- No future candle values are used for pattern formation.
- No invented numeric thresholds were introduced for qualitative Nison language.

## Promotion boundary
This batch is evaluator + unified-router verified locally. It is not represented as GitHub Actions CI PASS because the current connector cannot manually dispatch the repository workflow. The repository still requires the normal CI execution for final production verification.

## GitHub commits
- 0003-0010 evaluator: 947c6ebe9fc55a2299e9d841b5c2bca9c4fd98b5
- 0003-0010 tests: 47ff4bf6340e9f18de6e233c42aced1c6331f7c4
- 0001-0010 unified router: d0c7aa5f6e41c8c86a2bdc70f97b6669be8c643b

## 2025 policy
2025 remains OOS and is not used for tuning or selection.

## Next
Proceed to batch 0011-0020 after preserving this checkpoint.
