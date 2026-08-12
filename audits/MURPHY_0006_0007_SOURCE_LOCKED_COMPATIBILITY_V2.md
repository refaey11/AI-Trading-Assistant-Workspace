# Murphy 0006–0007 Source-Locked Compatibility V2
Date: 2026-08-12

## Authoritative rule records recovered

The actual uploaded `AI_Trading_Assistant_TRADING_RULES_V2.zip` was extracted and its `MASTER_TRADING_RULES_V2.json` directly inspected.

### MURPHY_0006
- status: INCOMPLETE_NEEDS_RULE_DEFINITION
- source: Technical Analysis of the Financial Markets, John J. Murphy, Chapter 4, Trendlines
- setup name: Confirmed uptrend line
- conditions:
  1. Connect successive reaction lows with an upward-sloping line.
  2. Two points create a tentative line.
  3. A third successful touch and reaction confirms the trendline.
- trade direction: BULLISH
- decision logic: Use the third successful test as confirmation of trendline validity.
- missing registry field: `confirmation` (empty)

### MURPHY_0007
- status: INCOMPLETE_NEEDS_RULE_DEFINITION
- source: Technical Analysis of the Financial Markets, John J. Murphy, Chapter 4, Trendlines
- setup name: Confirmed downtrend line
- conditions:
  1. Connect successive reaction highs with a downward-sloping line.
  2. Two points create a tentative line.
  3. A third successful touch and reaction confirms the trendline.
- trade direction: BEARISH
- decision logic: Use the third successful test as confirmation of trendline validity.
- missing registry field: `confirmation` (empty)

## John Murphy book cross-check
The uploaded book archive's Chapter 4 Trendlines source states:
- Up Trendline connects successive reaction lows.
- Down Trendline connects successive reaction highs.
- Tentative line requires 2 points.
- Confirmed trendline requires a 3rd successful touch and reaction without breaking.
- More successful tests without breaking increase validity.
- Break filters are described separately (e.g. 3% closing penetration and 2 consecutive daily closes).

## Result
The original Rule Database records have now been recovered. The semantic distinction between 0006 and 0007 is no longer an unresolved provenance problem:
- 0006 = confirmed uptrend line = reaction lows + upward slope = bullish.
- 0007 = confirmed downtrend line = reaction highs + downward slope = bearish.
- both require the third successful touch/reaction confirmation.

## Compatibility gate
Existing project artifacts already contain:
- `TRENDLINE_GEOMETRY_V1`
- Pivot Sequence V2
- trendline output/QA/manifest artifacts
- refreshed rule-level coverage showing:
  - 0006 feature path: `pivot_low sequence + touch/reaction`
  - 0006 operator note: `third touch followed by reaction away from line`
  - 0007 feature path: `pivot_high sequence + touch/reaction`
  - 0007 operator note: `third touch followed by reaction away from line`

These existing artifacts establish a compatible feature path, but the refresh artifact still labels both rules `NOT_YET_EVALUABLE` because an approved operational definition of successful touch/reaction is not yet frozen.

## Remaining missing fields
Source semantics are now source-locked, but the machine-level evaluator still needs an approved operational contract for:
- numerical/tolerance definition of a successful touch;
- operational measurement of reaction away from the line;
- exact no-break condition at the event;
- exact evaluator availability timestamp using the existing Pivot/Geometry availability lineage.

The book's 3% and 2-day values are breakout filters and must not automatically be converted into touch/reaction thresholds.

## Gate decision
**0006–0007 = SOURCE-LOCKED SEMANTICS / OPERATIONAL COMPATIBILITY PENDING**

Do not invent the remaining tolerance/threshold fields.

## Next action
Inspect the existing Trendline Geometry V1 contract/output schema directly. If it already contains the required touch/reaction/no-break fields, bind the evaluator to those exact existing fields. Only implement the missing adapter/evaluator layer, then unit test and run 2016–2024 historical QA. Keep 2025 untouched.
