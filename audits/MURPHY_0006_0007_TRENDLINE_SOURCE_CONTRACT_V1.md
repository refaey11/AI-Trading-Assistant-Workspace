# Murphy 0006–0007 Trendline Source Contract V1

Date: 2026-08-12
Status: SOURCE-SEMANTICS-RESOLVED / ID-BINDING-PENDING

## Source evidence

John Murphy, *Technical Analysis of the Financial Markets*, Chapter 4, Trendlines, defines:

- Up trendline: a straight line drawn upward to the right along successive reaction lows.
- Down trendline: a straight line drawn downward to the right along successive rally peaks.
- Two points establish a tentative trendline.
- The third test is the validity-confirming test.
- The confirming third test is a successful test where price bounces off the line.
- After the third point is confirmed and the trend continues in its original direction, the trendline is considered valid/useful.

External source verification used for this audit: Murphy Chapter 4, Figures 4.6a–c and the "Tentative Versus the Valid Trendline" section.

## Frozen semantic operator

The evaluator must NOT calculate a touch tolerance, ATR threshold, percentage threshold, or lookback. Those would be invented parameters unless explicitly supplied by the existing Trendline Geometry V1 contract.

The evaluator consumes the already-derived upstream geometry evidence:

1. `trendline_type` = `UP` or `DOWN`.
2. Two valid anchor points exist.
3. The third test/touch exists.
4. The third test is successful and price bounces away from the trendline in the original trend direction.
5. The confirmation/availability timestamp is the timestamp at which the successful third test + bounce is known from completed data.

PASS requires all five conditions. Missing any required upstream evidence => `NOT_EVALUABLE`.

## No-lookahead

The evaluator is event-based. It must never use bars after the upstream `confirmation_available_timestamp`.
The third touch alone is not the confirmation event; the successful test/bounce is the confirmation event because Murphy explicitly describes the successful test as confirming validity.

## Rule-ID binding

The source proves two distinct trendline variants (up and down), but the currently available project Rule Registry does not explicitly bind `MURPHY_0006` versus `MURPHY_0007` to those variants.

Therefore this contract intentionally does NOT freeze the ID mapping. A later authoritative Rule Registry record must bind:

- `MURPHY_0006` -> one trendline variant
- `MURPHY_0007` -> the other trendline variant

Until that binding is recovered, the generic evaluator is valid as an upstream-compatible primitive but the two rule IDs remain `NOT_YET_EVALUABLE`.

## Compatibility gate

This contract reuses existing Trendline Geometry V1 output and does not rebuild geometry. It only evaluates the source-defined confirmation semantics over that existing output.

2025 is OOS and is not used for implementation selection or tuning.
