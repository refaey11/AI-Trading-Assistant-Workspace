# Nison 0041 — D1 Canonical Candle Gate V1

## Execution input
- Uploaded D1(2).csv
- 2,544 rows
- 2016-01-03 through 2024-12-31
- 2025 rows: 0
- timestamps unique and monotonic

## Upstream structural population
Existing Murphy 0006/0007 confirmation artifact provides 15 provisional structural confirmations:
- 0006: 8
- 0007: 7

Third-touch dates used for the Nison confirmation scan:
- 0006: 2017-04-18, 2017-05-16, 2017-11-28, 2018-07-13, 2021-02-04, 2021-04-16, 2021-05-03, 2021-12-15
- 0007: 2018-07-16, 2020-01-24, 2021-10-11, 2022-02-10, 2022-04-21, 2022-09-13, 2023-03-07

## Source-locked Nison confirmation families
The available project Nison source material explicitly associates support/bullish confirmation with Hammer, Morning Star, and Bullish Engulfing, and resistance/bearish confirmation with Shooting Star, Evening Star, Bearish Engulfing, and Dark Cloud Cover. Candlestick confirmation is intended to increase confidence when it occurs directly at the relevant level/area.

## Deterministic scan boundary
Only exact relational candlestick geometry that does not require an invented numeric tolerance is allowed to be counted as an objective candidate in this pass. Qualitative long-shadow patterns such as Hammer/Shooting Star are recorded as candidate/needs-review, not canonical PASS, because no project-approved numeric comparator is source-locked.

## Objective observations at third-touch date
0006 bullish-side structural events:
- 2018-07-13: Bullish Engulfing geometry observed.
- 2021-02-04: Bullish Engulfing geometry observed.
- 2017-11-28: Hammer-like qualitative candidate (not canonical).
- 2021-12-15: Hammer-like qualitative candidate (not canonical).

0007 bearish-side structural events:
- 2022-09-13: Bearish Engulfing geometry observed.
- 2021-10-11: Shooting-Star-like qualitative candidate (not canonical).
- 2022-02-10: Shooting-Star-like qualitative candidate (not canonical; bullish-engulfing geometry is opposite polarity and therefore not confirmation for 0007).

The remaining structural events do not have an exact, source-locked reversal-pattern geometry at the third-touch date under this conservative gate.

## Current result
- Exact source-compatible candlestick candidates: 3
  - 0006 bullish: 2
  - 0007 bearish: 1
- Qualitative long-shadow candidates requiring unresolved comparator: 3
- Remaining third-touch events: no canonical candlestick confirmation observed under the conservative gate

## Governance
This is NOT a production PASS count and does not freeze Nison 0041. It is a conservative evidence gate over the uploaded D1 data.
No ATR, pip, percentage, body-size, shadow-ratio, lookback, timeframe, or 2025 tuning was introduced.
Nison remains confirmation-only and cannot create direction.

## Next gate
Resolve the existing Nison canonical candlestick pattern contracts for the confirmation families, then rerun the same 15 third-touch events. Do not promote qualitative Hammer/Shooting Star candidates without an approved comparator.
