# MURPHY 0006/0007 — Fresh Replay Result V1

Date: 2026-08-14
Period: 2016–2024 only
Status: FRESH REPLAY PASS — GOVERNANCE/FREEZE STILL OPEN

## Source recovery
The three workspace transfer segments were reconstructed successfully:
- PART_01_OF_03.zip.part
- PART_02_OF_03.zip.part
- PART_03_OF_03.zip_part1..part4.bcut

The reconstructed archive validates with `unzip -t` and contains the canonical Pivot V2 and Trendline Geometry V1 outputs.

## Raw M1 → D1 validation
The uploaded `GBPUSD_M1_MASTER_2016_2026_V1.zip` was used as the raw source.
D1 was aggregated by calendar date using first open, max high, min low, last close.
For all 2,544 common 2016–2024 D1 dates, the reconstructed OHLC exactly matched the project's existing D1 OHLC carried by the DMI/Parabolic-SAR higher-timeframe outputs:
- max absolute open difference = 0
- max absolute high difference = 0
- max absolute low difference = 0
- max absolute close difference = 0

This establishes the exact M1→D1 aggregation used by the canonical 2016–2024 D1 data: calendar-date OHLC aggregation. No timezone/session adjustment was introduced.

## Fresh evaluator inputs
- Canonical `PIVOT_SEQUENCE_V2_OUTPUT/GBPUSD_D1_STRUCTURE_PIVOT_SEQUENCE_V2.csv`
- Canonical `TRENDLINE_GEOMETRY_V1_OUTPUT/GBPUSD_D1_STRUCTURE_TRENDLINES_V1.csv`
- Fresh D1 reconstructed from uploaded M1
- 2025 excluded
- Reference confirmation artifact was NOT read by the fresh runner

## Operational evaluator
- first eligible same-family pivot after line availability is the third-touch candidate; do not skip it if it fails the range-intersection test
- D1 range must intersect the line at the touch timestamp
- reaction is the next STRICTLY LATER opposite-family confirmed pivot with directional reaction
- completed D1 bars between touch and reaction are checked for line-hold/no-break
- confirmation availability = reaction pivot availability

## Fresh result
- MURPHY_0006 = 8
- MURPHY_0007 = 7
- TOTAL = 15

Fresh confirmations:
- 0006: LOW::55, LOW::59, LOW::80, LOW::106, LOW::205, LOW::214, LOW::216, LOW::239
- 0007: HIGH::104, HIGH::172, HIGH::236, HIGH::249, HIGH::256, HIGH::270, HIGH::288

These line IDs and event timestamps correspond to the existing confirmation artifact's provisional confirmations.

## Important boundary
This proves the data lineage and fresh replay reproduce 8 + 7 = 15 under the current operational candidate. It does NOT by itself convert the no-break operationalization into verbatim Murphy source semantics or declare production freeze.

Next gates remain:
1. formal production integration
2. provenance manifest
3. governance approval
4. production freeze decision

No 3%, 2-day, ATR, pip tolerance, hidden lookback, or 2025 tuning was used.
