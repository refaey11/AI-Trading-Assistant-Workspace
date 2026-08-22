# Nison Runtime Promotion Audit — 0001 / 0002 — 2026-08-22

## Source basis
- Canonical governance record: `NISON/NISON_CANONICAL_FREEZE_2026-08-18.md`
- C101 Bullish Engulfing source contract: formation rules + trading rules + JSON source.
- C102 Bearish Engulfing source contract: formation rules + trading rules + JSON source.

## Runtime implementation
Added `RUNTIME/NISON_EVALUATORS_V1/nison_0001_0002_engulfing.py`.

The evaluator preserves source semantics:
- Bullish Engulfing requires prior Downtrend, bearish first candle, bullish second candle, and second real body engulfing the first.
- Bearish Engulfing requires prior Uptrend, bullish first candle, bearish second candle, and second real body engulfing the first.
- Confirmation is mandatory and is supplied as source-compatible evidence: strong directional candle OR breakout of the engulfing extreme.
- Volume and location are retained as preferred evidence, not invented hard gates.
- No numeric thresholds were invented.
- No future candle data is required for signal formation.
- Output is a confirmation-layer candidate and does not independently form the final Decision Brain decision.

## Tests
Added `RUNTIME/NISON_EVALUATORS_V1/test_nison_0001_0002_engulfing.py`.

Local deterministic execution: **6/6 PASS**.

## Status
- 0001: Runtime evaluator implemented + deterministic tests PASS; unified project routing / CI verification still pending.
- 0002: Runtime evaluator implemented + deterministic tests PASS; unified project routing / CI verification still pending.
- These two rules are not yet counted as fully verified Runtime until routing and full-path verification are complete.

## Governance
2025 remains OOS and is excluded from tuning/selection. No profitability claim is made.
