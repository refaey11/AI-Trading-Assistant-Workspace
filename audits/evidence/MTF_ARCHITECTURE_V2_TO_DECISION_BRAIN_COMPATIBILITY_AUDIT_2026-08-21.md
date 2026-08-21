# MTF Architecture V2 → Decision Brain V1 Compatibility Audit — 2026-08-21

## Evidence basis
This audit compares the recovered Dropbox `MTF_READER_SPEC_V2.json` / `AI_Trading_Assistant_MTF_ARCHITECTURE_V2` contract with the active GitHub `decision_brain.py` runtime.

## Source contract
The recovered MTF specification defines a context-aware reading stack:

- W1: macro context
- D1: major context
- H4: higher-timeframe context
- H1: primary intraday structure
- M30: local pullback / continuation
- M15: short-term structure / setup development
- M5: execution confirmation

The specified reading order is top-down: Weekly/Daily → H4 → H1 → M30 → M15 → M5. The source also requires handling contradictions and explicitly states that a single indicator/candle/pattern cannot create a trade decision.

The data policy prohibits fabricating M5/M15/M30 from H1.

## Active Decision Brain contract
`decision_brain.py` currently reads these direct fields:

- `mtf_trend_score`
- `M5_trend_regime`
- `M15_trend_regime`
- `M30_trend_regime`
- `H1_trend_regime`
- `H4_trend_regime`
- `D1_trend_regime`

It aggregates them as evidence and returns:

- `market_state`
- `directional_bias`
- `confidence`
- `evidence`
- `contradictions`
- `no_trade_reasons`

It is explicitly an evidence aggregator rather than a trading signal generator.

## Compatibility result

### Directly compatible
- M5 through D1 trend-regime field family: YES
- Aggregate MTF trend context: YES
- Evidence aggregation rather than automatic BUY/SELL: YES
- Contradiction/no-trade output: PARTIALLY represented

### Not yet represented directly
- W1 macro context
- Explicit timeframe roles in the runtime output
- Explicit top-down reading-order trace
- Pullback/countertrend interpretation as a named context state
- Selected-timeframe / Dynamic-MTF runtime field

## Important governance conclusion
The absence of a standalone file named `Dynamic MTF Binding` does not justify rebuilding the MTF system. The recovered V2 specification already provides the architectural contract. However, the current active `decision_brain.py` is a narrower implementation and does not yet expose every architectural field/role.

Therefore the correct next action is a narrow compatibility adapter or contract extension only after runtime evidence confirms which V2 fields are actually required by the downstream chain. No new directional rule is authorized by this audit.

## Status
- Six-timeframe MTF source: CLOSED / confirmed
- MTF Architecture V2 contract: RECOVERED / confirmed
- Direct M5–D1 Decision Brain field compatibility: SUPPORTED
- W1 / role / reading-order trace in active Brain: GAP IDENTIFIED
- Full runtime integration: PENDING EXECUTION TEST
- Time/Session standalone module: NOT ESTABLISHED by this audit

## OOS boundary
2025 remains locked Out-of-Sample and must not be used for tuning or compatibility-driven optimization.
