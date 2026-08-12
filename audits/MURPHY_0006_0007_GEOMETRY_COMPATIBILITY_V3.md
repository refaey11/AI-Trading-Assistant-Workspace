# Murphy 0006–0007 Trendline Geometry Compatibility V3
Date: 2026-08-12

## Sources checked
1. Uploaded John Murphy archive: `01_John_Murphy_Technical_Analysis(1).zip`
2. Workspace/File Library current-state and Trendline Geometry artifacts
3. Existing project handoff and rule-status records

## Chapter 4 source evidence
The uploaded Chapter 4 source explicitly states:
- Up Trendline = straight line up/right connecting successive reaction lows.
- Down Trendline = straight line down/right connecting successive reaction highs.
- Tentative line = 2 points.
- Confirmed trendline = 3rd successful touch and reaction without breaking.
- More successful tests without breaking increase validity.
- Trendline must enclose the entire daily High-to-Low range.
- Break filters are separate: example price filters (3% major / 1% short-term) and a 2-consecutive-trading-day close filter.

The JSON and SQL companions in the same uploaded chapter independently confirm 2-point tentative / 3-point confirmed construction and separate breakout filters.

## Existing Workspace geometry evidence
The Workspace confirms `TRENDLINE_GEOMETRY_V1` already exists with:
- `TRENDLINE_GEOMETRY_BUILD_CONTRACT_V1.json`
- `TRENDLINE_GEOMETRY_QA_V1.csv`
- `TRENDLINE_GEOMETRY_MANIFEST_V1.csv`
- timeframe-specific trendline outputs

The project handoff also confirms `PIVOT_SEQUENCE_V2` with confirmed pivots, two confirming bars, availability at pivot timestamp + 2 bars, and no lookahead before availability.

## Compatibility result
The source semantics now match the existing geometry conceptually:
- 0006 → LOW reaction anchors + UP line + third successful touch/reaction → BULLISH
- 0007 → HIGH reaction anchors + DOWN line + third successful touch/reaction → BEARISH

However, the currently searchable Workspace representation exposes the existence of the geometry contracts/outputs but does not expose row-level schema fields that prove the machine evaluator can directly consume all of:
- third-touch identity;
- successful-reaction measurement;
- no-break event at confirmation;
- exact availability timestamp for the completed confirmation event.

Therefore the correct gate is:
**SOURCE-LOCKED SEMANTICS / GEOMETRY COMPATIBLE / EVALUATOR CONTRACT NOT YET PROVEN**

## No invented parameters
Do NOT convert Murphy's separate breakout filters into touch/reaction tolerances. No ATR, percentage touch tolerance, reaction-distance threshold, lookback, or execution timeframe is invented.

## Next action
Expose/inspect the actual row-level Trendline Geometry V1 contract/output schema from the project archive. If those fields already exist, bind the Murphy evaluator to them. If not, keep the missing operational field explicitly NOT_EVALUABLE rather than inventing it.

## Book note
The uploaded archive already contains the full Chapter 4 source package (`04_Trendlines_And_Filters.md`, JSON, SQL, plus adjacent Chapter 4 material). A separate Chapter 4 upload is not required for the semantic question currently under review unless the user wants the remaining Chapter 4 material examined for additional context.

## Controls
2025 OOS; no tuning. Existing components preserved. Similarity remains historical evidence only.