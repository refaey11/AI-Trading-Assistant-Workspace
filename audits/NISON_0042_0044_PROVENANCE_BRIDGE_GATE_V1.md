# Nison 0042–0044 Provenance Bridge Gate V1

Date: 2026-08-17
Status: BRIDGE CONTRACT IMPLEMENTED / E2E PENDING

## Purpose
Bind existing MARKET_STATE_READER_V1 evidence to the shared Nison 0042–0044 primitive without creating a second market-structure engine.

## Accepted upstream fields
Existing Market State provides:
- `location`: `NEAR_SUPPORT | NEAR_RESISTANCE | MID_RANGE`
- `structure_event`: `INSIDE_RANGE | BREAKOUT_UP | BREAKOUT_DOWN`
- candle evidence fields including `bull_engulf`, `bear_engulf`, `hammer`, `shooting_star`
- `support_distance_atr`, `resistance_distance_atr`

These fields are accepted as raw upstream evidence only. Distance fields are NOT converted into a new zone tolerance.

## Provenance gate
A row may become Nison-evaluable only when the upstream evidence carries:
- source identifier
- event timestamp
- availability timestamp
- canonical zone identifier for S/R-dependent rules
- canonical candle evaluator provenance for the confirmation candle

Missing provenance => `NOT_EVALUABLE`.

## 0042 bridge
Accepted sequence:
1. authoritative S/R zone evidence
2. completed test of the zone
3. canonical Nison candle confirmation after the test

`NEAR_SUPPORT/NEAR_RESISTANCE` alone remains `CANDIDATE`, not PASS, because it does not identify a unique authoritative zone.

## 0043 bridge
Accepted sequence:
1. authoritative prior S/R boundary/zone
2. penetration/break event
3. authoritative close/return back inside the boundary
4. canonical Nison directional confirmation

`BREAKOUT_UP/DOWN` alone is insufficient. A later candle is not treated as a return event unless the upstream artifact explicitly identifies it as such.

## 0044 bridge
Accepted sequence:
1. authoritative prior S/R zone
2. confirmed break
3. authoritative successful retest/rejection proving polarity transition
4. canonical Nison directional confirmation

A break without an explicit successful retest remains `NOT_EVALUABLE`.

## Causal gate
All events must be received in causal order. No sorting is permitted before validation. No future row may establish an earlier event.

## 2025 isolation
The bridge accepts only evaluation rows dated 2016–2024 for the current historical gate. 2025 is OOS and cannot be used for tuning, calibration, or operator selection.

## Verdict
0042 = bridge-ready but provenance-gated.
0043 = bridge-ready but return-event gated.
0044 = bridge-ready but successful-retest gated.
No PASS or FREEZE is emitted by this bridge itself.
