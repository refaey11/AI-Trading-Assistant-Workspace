# Murphy 0006–0007 Evidence Adapter Contract V1

Date: 2026-08-12
Status: CONTRACT-ONLY / NO PASS-FAIL

## Purpose

Define the smallest adapter that consumes existing canonical artifacts and preserves observable evidence for 0006/0007 without inventing a successful-touch or reaction threshold.

## Inputs

1. PIVOT_SEQUENCE_V2 canonical D1 output.
2. TRENDLINE_GEOMETRY_V1 canonical D1 output.
3. Completed D1 OHLC evidence for the same historical window.

## Rule mapping

- MURPHY_0006: LOW pivot family + UP trendline.
- MURPHY_0007: HIGH pivot family + DOWN trendline.

## Candidate selection

For each available geometry line, identify the next confirmed same-type pivot after the second defining anchor and after line availability. This event is a `third_touch_candidate`, not a confirmed successful touch.

## Evidence fields

The adapter must preserve, when available:
- rule_id
- line_id
- line_type
- direction
- anchor_1_timestamp / price
- anchor_2_timestamp / price
- line_availability_timestamp
- candidate_timestamp
- candidate_pivot_type
- candidate_pivot_price
- line_price_at_candidate
- signed_distance
- absolute_distance
- daily_high
- daily_low
- daily_range_intersects_line
- reaction_candidate_timestamp
- reaction_candidate_type
- reaction_directionally_consistent
- no_break_observation
- evidence_status

## Status rules

Allowed evidence statuses:
- `CANDIDATE_ONLY`
- `NOT_EVALUABLE`
- `INSUFFICIENT_DATA`

`PASS` and `FAIL` are explicitly forbidden in this adapter.

## Reaction evidence

The adapter may record a subsequent completed event that moves away from the line in the expected Murphy direction as `reaction_candidate`. It must not impose a fixed number of bars, pip amount, percentage, ATR, or close threshold.

## No-break evidence

The adapter may record raw D1 range/line integrity observations after line availability. A potential penetration is an observation only. A confirmed break requires a separately approved break/no-break contract.

The Murphy 3% and 2-consecutive-day filters remain source evidence for general break confirmation and are not automatically bound to 0006/0007.

## Lookahead control

Only data at or after the line/pivot availability timestamp may be used. 2025+ is excluded from any selection/tuning and is not an input to this contract.

## Non-goals

Do not modify PIVOT_SEQUENCE_V2 or TRENDLINE_GEOMETRY_V1.
Do not introduce touch tolerance.
Do not introduce reaction magnitude/duration.
Do not introduce hidden lookbacks.
Do not promote working rule mappings to Source-Locked.

## Acceptance gate

This contract is accepted only as an evidence-preservation adapter. It does not close the production evaluator gate. Production PASS/FAIL remains blocked until an authoritative/operator-approved definition of successful third touch + reaction and the required no-break binding is available.
