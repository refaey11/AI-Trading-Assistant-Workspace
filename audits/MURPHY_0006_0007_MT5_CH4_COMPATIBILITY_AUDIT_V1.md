# Murphy 0006–0007 / MT5 Chapter 4 Compatibility Audit V1

Date: 2026-08-12
Status: PARTIALLY CLOSED / OPERATIONAL TOUCH STILL OPEN

## New source inspected

Uploaded archive: `MT5 Pro AI 2  2(1).zip`

Direct inspection recovered the structured Murphy Chapter 4 artifact:
`02_Books/01_John_Murphy_Technical_Analysis/Chapter_04_Basic_Concepts_Of_Trend/04_Trendlines_And_Filters.md/text.txt`

The artifact states:
- Up Trendline = connect successive reaction lows.
- Down Trendline = connect successive reaction highs.
- Tentative line = 2 points.
- Confirmed trendline = 3rd successful touch and reaction without breaking.
- Trendlines should enclose the entire daily price range (High to Low).
- Price filters can be used for break confirmation (3% major trend / 1% short-term example).
- Time filter = 2 consecutive daily closes beyond the trendline to confirm a valid breakout and avoid false signals.

The same archive's Chapter 4 JSON states:
- construction = connect lows for Uptrend / highs for Downtrend
- validity = 2 points tentative, 3 points confirmed
- price_filter = 3% closing price penetration
- time_filter = 2 consecutive daily closes beyond trendline

## Compatibility interpretation

### 1. No-break evidence is stronger than previously documented

The phrase `trendlines must enclose the entire daily price range (High to Low)` provides a source-backed geometric constraint for the line itself. This can support a no-break evidence layer at the daily-bar level without inventing ATR/pip/% touch tolerance.

For an uptrend, the trendline is below price action and the daily range must remain enclosed relative to that support line. For a downtrend, the trendline is above price action and the daily range must remain enclosed relative to that resistance line.

However, the source does NOT define a separate 0006/0007-specific touch-distance tolerance.

### 2. Break filters must remain separate from touch detection

The 3% price filter and 2-day time filter are source-backed as general trendline-break confirmation filters. They are NOT proven here as an automatic 0006/0007-specific binding.

Therefore:
- do not use 3% as a third-touch tolerance;
- do not use 2-day as a reaction definition;
- do not bind either filter to 0006/0007 without a project contract selecting that family.

### 3. Third touch is still the remaining deterministic gap

The source confirms the semantic requirement of a third touch followed by reaction, but does not give a numeric distance operator for when a pivot/bar is considered to have touched the line.

Therefore a production deterministic `third_touch_detected` predicate cannot be created from this source alone unless an existing project contract supplies the event representation or tolerance.

### 4. Reaction remains qualitative

The source confirms reaction/rebound away from the trendline, but does not specify a numeric reaction magnitude or fixed number of bars. Do not invent one.

## Reuse / implementation decision

Reuse:
- PIVOT_SEQUENCE_V2
- TRENDLINE_GEOMETRY_V1
- existing evaluator/test infrastructure

Add only an evidence adapter that can consume source-approved bar/pivot events.

Potential source-safe no-break evidence:
- evaluate the actual daily range against the line after line availability;
- classify confirmed breakout only through an explicitly selected price/time filter contract;
- otherwise keep `no_break_valid = NOT_EVALUABLE` when the project has not bound a break filter.

## Current status for 0006/0007

- source qualitative semantics: CLOSED
- working direction split: CLOSED in current project status
- geometry reuse: CLOSED
- daily-range enclosure evidence: SOURCE-BACKED
- general break filter definitions: SOURCE-BACKED
- 0006/0007-specific 3%/2-day binding: NOT PROVEN
- exact third-touch detector: OPEN
- exact reaction detector: OPEN
- evaluator: OPEN
- tests: OPEN
- historical QA: OPEN
- production freeze: OPEN

## Important control

The archive does not justify inventing a touch tolerance, reaction threshold, lookback, timeframe, or automatic 3%/2-day 0006/0007 binding. 2025 remains OOS.
