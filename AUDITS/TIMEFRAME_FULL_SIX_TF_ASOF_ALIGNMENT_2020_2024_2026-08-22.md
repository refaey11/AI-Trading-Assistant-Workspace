# Full Six-Timeframe As-Of Alignment — 2026-08-22

## Scope
Standalone Timeframe Layer alignment evidence for the recovered six-timeframe family:
`M5 -> M15 -> M30 -> H1 -> H4 -> D1`

## Dataset window
2020-01-02 through 2024-12-31 only.
2025 is excluded completely.

## Rows observed
- M5: 373,465
- M15: 124,764
- M30: 62,513
- H1: 31,385
- H4: 8,039
- D1: 1,554

## Structural checks
- All six timestamp series are strictly increasing.
- No duplicate timestamps were observed in any timeframe.
- Median timestamp spacing matches the expected timeframe cadence: 5m / 15m / 30m / 60m / 240m / 1440m.

## As-of mapping checks
For each adjacent pair, the higher-timeframe row was selected using the latest timestamp <= the lower-timeframe timestamp.

Results:
- M5 -> M15: 0 future mappings, 0 missing mappings
- M15 -> M30: 0 future mappings, 0 missing mappings
- M30 -> H1: 0 future mappings, 0 missing mappings
- H1 -> H4: 0 future mappings, 0 missing mappings
- H4 -> D1: 0 future mappings, 0 missing mappings

## Interpretation
The recovered six-timeframe source passes the standalone timestamp/alignment and as-of no-future mapping checks for the 2020–2024 development window.

This closes the six-timeframe alignment evidence layer only. It does NOT by itself certify:
- Dynamic Timeframe Selection runtime producer
- Time/Session Context runtime producer
- Full Decision Brain E2E
- 2025 OOS performance

## Governance
- No source semantics were invented.
- No thresholds were added.
- 2025 remains untouched for tuning/calibration/selection.
