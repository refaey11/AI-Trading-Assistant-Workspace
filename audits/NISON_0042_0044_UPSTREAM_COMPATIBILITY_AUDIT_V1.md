# Nison 0042–0044 Upstream Compatibility Audit V1

Date: 2026-08-17
Status: COMPATIBILITY MAPPING COMPLETE / E2E PENDING

## Existing canonical upstream artifact
The project already contains MARKET_STATE_READER_V1 outputs for GBPUSD, EURUSD, USDJPY, USDCAD and XAUUSD. Its contract explicitly describes market context including support/resistance location and structure events; it is a market-reading layer, not a trading strategy.

GBPUSD_MARKET_STATE.csv fields include:
- support_distance_atr
- resistance_distance_atr
- location
- structure_event
- bull_engulf
- bear_engulf
- hammer
- shooting_star

Observed structure_event vocabulary includes INSIDE_RANGE, BREAKOUT_UP and BREAKOUT_DOWN. Observed location vocabulary includes NEAR_SUPPORT, NEAR_RESISTANCE and MID_RANGE.

## Compatibility mapping
0042 Support/Resistance:
- location=NEAR_SUPPORT or NEAR_RESISTANCE can be consumed as upstream location evidence.
- Existing candlestick evidence fields can be passed to the Nison confirmation adapter.
- This does NOT establish a unique zone_id or numeric zone width; therefore the adapter must not invent one.
- Verdict: PARTIALLY EVALUABLE from existing Market State evidence.

0043 False Breakouts:
- BREAKOUT_UP / BREAKOUT_DOWN provides breakout-direction evidence.
- Existing artifact does not expose an explicit return_inside_range / failed_breakout event field.
- Therefore a false breakout cannot be declared solely from BREAKOUT_* without adding an unsupported inference.
- Verdict: NOT_EVALUABLE until an authoritative return/failure event is supplied.

0044 Polarity:
- BREAKOUT_* provides a break event, but the artifact does not expose an explicit successful_retest event or polarity-transition state.
- Therefore polarity cannot be declared from a break alone.
- Verdict: NOT_EVALUABLE until authoritative retest evidence is supplied.

## Governance decision
Reuse MARKET_STATE_READER_V1. Do not build a second support/resistance or breakout engine.
Do not convert support_distance_atr or resistance_distance_atr into a new zone tolerance.
Do not infer false breakout from a later candle merely because it looks like a return; an authoritative upstream event is required.
Do not infer polarity from a break without an explicit successful retest.
2025 remains OOS and is excluded from tuning/calibration.

## Next executable gate
Run the Nison adapter against the existing Market State evidence for 2016–2024 and record:
- 0042 cases with explicit NEAR_SUPPORT/NEAR_RESISTANCE + canonical candle confirmation.
- 0043 cases as NOT_EVALUABLE unless an explicit failed-breakout/return event is present.
- 0044 cases as NOT_EVALUABLE unless explicit successful-retest evidence is present.

This gate is intentionally fail-closed and does not create new market-structure semantics.
