# Murphy 0006/0007 — TRENDLINE_GEOMETRY_V1 Field Reconciliation

Date: 2026-08-13
Status: RECONCILED / OPERATOR GAP CONFIRMED

## Actual Geometry V1 contract
From the canonical workspace artifact `TRENDLINE_GEOMETRY_BUILD_CONTRACT_V1.json`:
- input: PIVOT_SEQUENCE_V2
- line generation: consecutive pivots of the same type only
- slope: exact price change / elapsed seconds
- availability: later confirmation timestamp of the two defining pivots
- pattern classification: excluded
- breakout detection: excluded
- thresholds added: false
- 2025 used: false
- lookahead control: line cannot be available before both defining pivots are confirmed

## Actual D1 output fields
`GBPUSD_D1_STRUCTURE_TRENDLINES_V1.csv` contains:
- line_id
- line_type
- point_1_timestamp / price
- point_2_timestamp / price
- slope_price_per_second
- direction
- availability_timestamp
- point_1_availability
- point_2_availability
- source_file

## Compatibility with Murphy Confirmation Layer
Available directly:
- line identity: YES
- LOW/HIGH family: YES
- UP/DOWN direction: YES
- two anchors: YES
- line availability: YES
- exact line geometry: YES
- post-availability completed-bar input is available upstream in the workspace: YES

Not produced by Geometry V1:
- third_touch_detected: NO
- third_touch_timestamp/price: NO
- reaction_detected: NO
- no_break_valid: NO
- confirmation_timestamp: NO

## Critical interpretation
Geometry V1 explicitly excludes breakout detection and does not add thresholds. Therefore it cannot be treated as the producer of `no_break_valid`.

Because Geometry V1 creates lines from consecutive same-type pivots, a later same-type pivot can be used as a candidate observation, but that does NOT by itself prove a successful third touch. A successful touch still requires a source-backed relation between the observed price action and the projected line. No such tolerance/predicate is defined in the Geometry V1 contract.

Similarly, a later opposite-type pivot can be recorded as a reaction candidate, but `reaction_candidate` / directional consistency is not equivalent to the source-level `successful reaction/rebound` predicate without an approved operator.

## Conclusion
The smallest safe integration is NOT a replacement Geometry implementation. The existing Geometry output is sufficient as the geometric input to a separate Confirmation Evidence Layer, but the three confirmation predicates remain upstream/open:
1. third_touch
2. reaction_bounce
3. no_break

The current candidate dataset may continue to record raw observations, but those observations must not be promoted to confirmation booleans without a source/project contract.

## Next exact action
Search all existing project artifacts for an approved break/no-break contract and any source-backed touch/reaction operator. If none exists, keep the three predicates NOT_EVALUABLE and do not create a guessed adapter.
