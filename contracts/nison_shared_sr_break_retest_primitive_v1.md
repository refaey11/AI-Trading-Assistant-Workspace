# Nison Shared S/R Breakout-Retest Primitive V1

Status: CONTRACT ONLY — NO EXECUTION ENGINE

Purpose: provide one shared evidence interface for Nison 0042 Support/Resistance, 0043 False Breakouts, and 0044 Polarity Principle without inventing a new market-structure algorithm.

## 1. S/R Zone Evidence
Required fields:
- zone_id
- zone_type: support | resistance
- source_id / provenance
- created_at
- available_at
- validity: active | inactive | unknown

No numeric zone width/tolerance is defined here. The producer must supply an authoritative zone; this contract does not derive one.

## 2. Breakout Evidence
Required fields:
- zone_id
- break_direction: above_resistance | below_support
- event_at
- available_at
- close_relation: above | below | inside | unknown
- source_id / provenance

A breakout is not inferred from a configurable percentage, ATR, pip distance, or lookback in this contract.

## 3. Return / Retest Evidence
Required fields:
- zone_id
- return_or_retest_at
- available_at
- outcome: returned_inside | successful_retest | failed_retest | unknown
- source_id / provenance

The primitive only consumes an authoritative event. It does not manufacture a retest threshold.

## 4. Nison bindings
0042: active S/R zone + qualifying test/rejection evidence + Nison candlestick confirmation.
0043: support/resistance boundary + break beyond boundary + return/close back inside + Nison directional confirmation.
0044: break of S/R + successful retest demonstrating polarity change + Nison directional confirmation.

## 5. Chronology / availability
Required ordering:
zone.created_at <= breakout.event_at <= return_or_retest_at <= confirmation.available_at

Any violation => NOT_EVALUABLE.
Missing provenance or unavailable evidence => NOT_EVALUABLE.
No future event may be used to establish an earlier event.

## 6. Governance
This is a shared evidence contract, not a new S/R/breakout/retest engine. Existing canonical producers must populate it. If no canonical producer exists, these rules remain NOT_EVALUABLE rather than silently creating a new algorithm.
2025 remains OOS and is excluded from tuning, calibration, threshold selection, and operator selection.
