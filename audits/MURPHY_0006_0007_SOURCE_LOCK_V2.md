# Murphy 0006–0007 Source Lock V2

Date: 2026-08-12
Status: PARTIALLY RESOLVED — MAPPING SOURCE-LOCKED / REACTION OPERATOR OPEN

## Purpose

Close the source-semantic ambiguity for Murphy rules 0006 and 0007 without rebuilding existing components or inventing an operational threshold.

## Authoritative Murphy source recovered

Source archive:
`01_John_Murphy_Technical_Analysis.zip`

Source file:
`Chapter_04_Basic_Concepts_Of_Trend/04_Trendlines_And_Filters.md`

The source explicitly defines:

- Up Trendline = a line drawn up and to the right connecting successive reaction LOWS.
- Down Trendline = a line drawn down and to the right connecting successive reaction HIGHS.
- Tentative line = 2 points.
- Confirmed trendline = a 3rd successful touch and reaction without breaking.

Therefore the semantic mapping is now source-supported:

`MURPHY_0006 → Uptrend Line → reaction LOWS → UP → BULLISH`

`MURPHY_0007 → Downtrend Line → reaction HIGHS → DOWN → BEARISH`

## What is now resolved

1. 0006 is the uptrend-line rule.
2. 0007 is the downtrend-line rule.
3. Uptrend geometry uses LOW anchors.
4. Downtrend geometry uses HIGH anchors.
5. Confirmation requires a third successful touch and reaction without breaking.
6. Existing Trendline Geometry V1 must be reused.

## What remains unresolved

The source does NOT provide a numeric operational definition for:

- touch tolerance;
- reaction-distance threshold;
- ATR tolerance;
- percentage tolerance for defining a successful touch/reaction;
- exact event timestamp for confirmation beyond the conceptual third successful touch + reaction;
- an additional availability rule specific to this evaluator.

The source does contain breakout filters (3% price filter / 2-day closing filter), but those are breakout filters and MUST NOT be repurposed as a touch/reaction threshold.

## Compatibility decision

The existing architecture already provides:

- PIVOT_SEQUENCE_V2
- TRENDLINE_GEOMETRY_V1
- existing Rule Evaluator V2 infrastructure

No new Geometry component is required.

The correct implementation path is:

`source-locked mapping`
`→ existing Geometry V1`
`→ determine whether Geometry already emits third-touch/reaction/no-break evidence`
`→ if yes, build only the evaluator adapter`
`→ if no operational reaction field exists, return NOT_EVALUABLE for that condition`

## Prohibited actions

- No new threshold.
- No ATR invention.
- No percentage invention.
- No lookback invention.
- No 2025 tuning.
- No modification of Murphy 0003/0004.
- No Geometry rebuild.

## Gate status

Mapping gate: **PASS / SOURCE-LOCKED**

Third-touch/reaction operational-evidence gate: **OPEN / NOT_YET_EVALUABLE**

Evaluator implementation gate: **BLOCKED only on the unresolved reaction operator**

## Next exact action

Audit the existing Trendline Geometry V1 contract/output for these fields:

- line family: LOW/HIGH
- direction: UP/DOWN
- anchor count/order
- third touch
- reaction evidence
- break/no-break evidence
- availability timestamp
- chronology/no-lookahead

If all required evidence exists, implement and test the 0006/0007 evaluator adapter using only those fields.
If successful reaction is absent, keep that condition NOT_EVALUABLE rather than inventing a threshold.

Validation remains 2016–2024 only. 2025 remains OOS and untouched.
