# Murphy 0006-0007 Source Resolution V2

Date: 2026-08-12

## Source-of-truth finding

The project Master Knowledge Base contains authoritative candidate rule records in `02_Trading_Rules/MASTER_CANDIDATE_RULES_V1.json`.

### MURPHY_0006

- Rule name: Confirmed uptrend line
- Chapter/section: Technical Analysis of the Financial Markets, Chapter 4, Trendlines
- Conditions:
  1. Connect successive reaction lows with an upward-sloping line.
  2. Two points create a tentative line.
  3. A third successful touch and reaction confirms the trendline.
- Decision direction: BULLISH

### MURPHY_0007

- Rule name: Confirmed downtrend line
- Chapter/section: Technical Analysis of the Financial Markets, Chapter 4, Trendlines
- Conditions:
  1. Connect successive reaction highs with a downward-sloping line.
  2. Two points create a tentative line.
  3. A third successful touch and reaction confirms the trendline.
- Decision direction: BEARISH

## Primary-source cross-check

The uploaded John Murphy Chapter 4 source independently states:
- Up Trendline = successive reaction lows.
- Down Trendline = successive reaction highs.
- Tentative line = 2 points.
- Confirmed trendline = a 3rd successful touch and reaction without breaking.

Therefore the project mapping is resolved:

- `MURPHY_0006` -> `LOW` + `UP` -> `BULLISH`
- `MURPHY_0007` -> `HIGH` + `DOWN` -> `BEARISH`

## Compatibility boundary

Do not rebuild Trendline Geometry V1. The existing geometry remains the geometry provider.

The source resolves the semantic mapping and confirmation concept, but it does not supply a numeric touch/reaction tolerance. No ATR, percentage, lookback, or other invented threshold is permitted.

The evaluator may only return PASS for the third-touch condition when the existing geometry/evidence artifact explicitly supplies the required third successful touch/reaction and no-break evidence. Otherwise that portion remains `NOT_EVALUABLE`.

## Availability / leakage

The rule must consume only confirmed pivot/geometry evidence available at the artifact's availability timestamp. PIVOT_SEQUENCE_V2 availability remains authoritative; no future bars may be used before availability. 2025 remains OOS and is not used for tuning or implementation selection.

## Status

- 0006 semantic mapping: RESOLVED
- 0007 semantic mapping: RESOLVED
- Third-touch/reaction source semantics: RESOLVED at qualitative level
- Numeric touch tolerance: intentionally unspecified
- Existing Geometry V1 compatibility: pending direct schema/evidence verification
- Evaluator freeze: NOT YET FROZEN
