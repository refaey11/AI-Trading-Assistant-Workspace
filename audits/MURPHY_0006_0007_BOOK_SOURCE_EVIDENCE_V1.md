# Murphy 0006–0007 — John Murphy Book Source Evidence V1
Date: 2026-08-12

## Uploaded source
`01_John_Murphy_Technical_Analysis(1).zip`

## Exact source files inspected
- `Chapter_04_Basic_Concepts_Of_Trend/04_Trendlines_And_Filters.md`
- `Chapter_04_Basic_Concepts_Of_Trend/05_JSON.json`
- `Chapter_04_Basic_Concepts_Of_Trend/06_SQL.sql`

## Source-derived semantics
The uploaded Chapter 4 material states:
- Up Trendline: straight line drawn up/right connecting successive reaction lows.
- Down Trendline: straight line drawn down/right connecting successive reaction highs.
- Tentative line: 2 points.
- Confirmed trendline: a 3rd successful touch and reaction without breaking.
- More successful tests without breaking increase validity.
- Trendlines must enclose the entire daily High-to-Low range.
- Break filters in the supplied source include a 3% closing-price penetration example and a 2-consecutive-daily-close time filter.

The JSON source independently states:
- construction = connect lows for Uptrend, connect highs for Downtrend;
- validity = 2 points tentative, 3 points confirmed;
- filters = 3% closing price penetration and 2 consecutive daily closes beyond trendline.

The SQL source states:
- trendlines require 3 touches to confirm;
- valid breakouts use price filters (3% rule) or time filters (2-day closing rule).

## Impact on Murphy 0006–0007
This uploaded book source now provides direct source evidence for the core semantics previously missing:
- 0006 can be source-mapped to an Up Trendline constructed from successive reaction lows.
- 0007 can be source-mapped to a Down Trendline constructed from successive reaction highs.
- Confirmation requires the third successful touch + reaction without breaking.

This materially strengthens the existing working mapping:
- 0006 = LOW + UP → BULLISH
- 0007 = HIGH + DOWN → BEARISH

## Important limits
The uploaded source does NOT by itself define a complete machine evaluator for the project. It does not specify a numerical tolerance for what counts as a touch/reaction, nor does it specify a project-specific execution timeframe. The 3% and 2-day values are presented as breakout filters in the supplied Chapter 4 source; they must not automatically be repurposed as a touch tolerance or confirmation threshold for 0006/0007.

Therefore:
- Source semantics are now substantially resolved.
- The exact operational feature/tolerance contract still requires compatibility audit against existing Trendline Geometry V1.
- No new threshold or timeframe is invented.

## Next action
Run a compatibility audit between these book semantics and the existing Trendline Geometry V1 outputs/contracts. If the existing component already represents successive reaction lows/highs, third touch/reaction, no break, and availability, bind 0006/0007 to it rather than rebuilding anything. Then define evaluator/tests only from the compatible existing contract.

## Controls
2025 remains OOS. Similarity remains historical evidence only. Existing project components are reused; no rebuild.