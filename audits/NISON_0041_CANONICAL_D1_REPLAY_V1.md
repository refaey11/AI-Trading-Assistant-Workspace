# Nison 0041 — Canonical D1 Replay V1

Date: 2026-08-17
Dataset: uploaded D1(2).csv
Period: 2016-01-03 through 2024-12-31
Rows: 2,544
2025 rows consumed: 0

## Upstream structural events
Consumed the existing 15 provisional Murphy 0006/0007 structural confirmations as upstream evidence: 8 UP-trendline events and 7 DOWN-trendline events. No new trendline engine was created.

UP / 0006 third-touch dates:
- 2017-04-18
- 2017-05-16
- 2017-11-28
- 2018-07-13
- 2021-02-04
- 2021-04-16
- 2021-05-03
- 2021-12-15

DOWN / 0007 third-touch dates:
- 2018-07-16
- 2020-01-24
- 2021-10-11
- 2022-02-10
- 2022-04-21
- 2022-09-13
- 2023-03-07

## Canonical Nison source binding
The recovered Trend Lines source binds:
- UP trend line -> Hammer / Morning Star / Bullish Engulfing
- DOWN trend line -> Shooting Star / Evening Star / Bearish Engulfing

The exact source pattern records were recovered for C002, C005, C101, C102, C108 and C109.

## Deterministic replay boundary
Only the Bullish Engulfing (C101) and Bearish Engulfing (C102) conditions were promoted to deterministic replay because their recovered source contracts specify an exact two-candle body relationship without a qualitative size/tolerance comparator.

Hammer, Shooting Star, Morning Star and Evening Star were not converted into numeric predicates. Their source contracts contain qualitative conditions such as "very small", "long", "strong", and "closes well into". Those remain NOT_EVALUABLE rather than being thresholded.

For C101/C102, source confirmation is required. Confirmation was checked on the next D1 candle using the source-defined break-above-high / break-below-low entry condition. Availability is the completion of that next candle; no future candle after the confirmation candle is used.

## Results
Exact canonical engulfing confirmations:

UP / C101 Bullish Engulfing:
- 2018-07-13 -> PASS; next candle broke above pattern high.
- 2021-02-04 -> PASS; next candle broke above pattern high.

DOWN / C102 Bearish Engulfing:
- 2022-09-13 -> PASS; next candle broke below pattern low.

Counts:
- 0006 structural events consumed: 8
- 0007 structural events consumed: 7
- Canonical C101/C102 PASS: 3
- Remaining structural events with no deterministic C101/C102 confirmation: 12
- Those 12 are NOT_EVALUABLE overall because the remaining four source-bound pattern families contain qualitative conditions that were deliberately not converted into invented numeric rules.

## Availability / leakage
- Structural event precedes candle confirmation: PASS for all consumed events.
- Confirmation uses only the event candle and the immediately following candle: PASS.
- 2025 rows consumed: 0.
- No threshold, tolerance, ATR, pip, percentage, lookback, or trend proxy introduced.

## Verdict
SOURCE/CONTRACT BINDING = PASS
CANONICAL DETERMINISTIC SUBSET REPLAY = PASS (3 confirmations)
FULL NISON 0041 EVALUATION = NOT_EVALUABLE
PRODUCTION FREEZE = NOT YET

Reason for remaining NOT_EVALUABLE: four of the six source-bound confirmation families still contain qualitative formation conditions that the supplied source does not make numerically deterministic. The project rule is to preserve those as NOT_EVALUABLE rather than invent thresholds.
