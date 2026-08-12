# Murphy 0006–0007 Confirmation Layer Contract V1
Date: 2026-08-12
Status: DESIGN-CONTRACT / NOT-FROZEN

## Purpose
Implement Murphy's source-defined third-test confirmation as a separate evidence layer over the existing PIVOT_SEQUENCE_V2 + TRENDLINE_GEOMETRY_V1 outputs.

The existing Geometry layer remains unchanged and continues to own two-point trendline construction, slope/direction, and anchor availability.

## Source-backed semantics
From John Murphy Chapter 4 and the recovered Master Rule Database records:

### MURPHY_0006
- confirmed uptrend line
- successive reaction lows
- upward slope
- two points form tentative line
- third test/touch confirms validity when the test is successful and price rebounds from the line without a meaningful break
- direction = BULLISH

### MURPHY_0007
- confirmed downtrend line
- successive reaction highs
- downward slope
- two points form tentative line
- third test/touch confirms validity when the test is successful and the line holds without a meaningful break
- direction = BEARISH

## Layer inputs
Required upstream evidence:
1. `line_id`
2. `line_type` / family (LOW or HIGH)
3. `direction` (UP or DOWN)
4. `point_1_timestamp`, `point_1_price`
5. `point_2_timestamp`, `point_2_price`
6. `availability_timestamp`
7. completed-bar market data after the line availability timestamp, restricted to the evaluator's allowed event window
8. approved project trendline-break semantics, if an existing contract is found

## Layer outputs
The layer may emit:
- `third_touch_timestamp`
- `third_touch_price`
- `third_touch_detected`
- `reaction_detected`
- `no_break_valid`
- `confirmation_timestamp`
- `confirmation_available_timestamp`
- `rule_id`
- `status` = PASS / FAIL / NOT_EVALUABLE

## Rule binding
- MURPHY_0006 accepts only LOW-family + UP geometry and outputs BULLISH when confirmed.
- MURPHY_0007 accepts only HIGH-family + DOWN geometry and outputs BEARISH when confirmed.

## Operational constraints
This layer MUST NOT invent:
- ATR thresholds
- percentage touch tolerances
- fixed lookbacks
- fixed execution timeframes
- alternate trendline geometry

The source's 3% price filter and 2-consecutive-day close filter are general trendline-break examples in Chapter 4. They are NOT automatically assigned to 0006/0007.

## Touch/reaction rule
The implementation must use source-visible structure first:
- a later completed-bar interaction with the existing trendline after both anchors are available;
- the interaction is the candidate third test;
- the test is successful only when subsequent/associated completed-bar evidence shows price rebounding away from the line in the original trend direction;
- the event cannot be confirmed using data that occurs before the third-test timestamp.

Because the source does not prescribe one universal numerical distance tolerance for 'touch', the first implementation should expose the touch test as a deterministic adapter over existing project-approved Geometry/price fields. A numeric tolerance may only be added after an explicit project/source contract is found.

## No-break rule
`no_break_valid` must be delegated to an existing project-approved trendline-break contract if one exists.
If no such contract exists, the layer may only record the source-semantic state `NO_BREAK_NOT_OPERATIONALIZED` and return NOT_EVALUABLE for production evaluation. It must not silently choose 3%, 2 days, ATR, or another proxy.

## Availability / no-lookahead
- The two-anchor line cannot be used before its `availability_timestamp`.
- Third-test confirmation can only become available on/after the completed bar where the successful third test/reaction is knowable.
- Historical evaluation must not consume bars after `confirmation_available_timestamp` to decide the event itself.
- 2025 remains OOS and is never used for tuning/selection.

## Acceptance tests required
1. 0006 valid LOW+UP, two anchors, successful third test/reaction, approved no-break -> PASS/BULLISH.
2. 0007 valid HIGH+DOWN, two anchors, successful third test/reaction, approved no-break -> PASS/BEARISH.
3. Wrong rule-direction binding -> NOT_EVALUABLE.
4. Fewer than two anchors -> NOT_EVALUABLE.
5. No third test -> FAIL/NOT_EVALUABLE according to approved evaluator convention.
6. Third test without successful reaction -> FAIL.
7. Third test with meaningful break -> FAIL.
8. Missing break contract -> NOT_EVALUABLE, not guessed.
9. Availability timestamp leakage -> NOT_EVALUABLE/test failure.

## Gate
This is a contract for a NEW derived evidence layer, not a modification to the existing Geometry engine.

PRODUCTION FREEZE remains blocked until the exact no-break operational contract and deterministic touch/reaction implementation are validated against the source and project architecture.
