# Murphy 0006–0007 Successful Bounce Upstream Audit V1

Date: 2026-08-13
Status: UPSTREAM REVIEW COMPLETE / PRODUCTION GATE STILL OPEN

## What the existing runner actually derives
`run_murphy_0006_0007_real_data_candidates.py` already derives, from completed Pivot V2 + Geometry V1 + D1 OHLC:
- first same-type pivot after anchor 2 and line availability;
- mathematical line price at the candidate pivot;
- daily high/low and whether the line lies inside that day's range;
- first opposite-type pivot after the candidate;
- `reaction_directionally_consistent` based on opposite pivot price relative to the candidate pivot.

The runner deliberately labels the output `CANDIDATE_ONLY` and `no_break_observation = OBSERVATION_ONLY`.

## Important semantic finding
Murphy source contract says the third test becomes confirmation only when the third test is successful and price bounces away from the trendline in the original trend direction. The project source contract explicitly says the third touch alone is not the confirmation event.

The current runner has enough raw observations to represent a candidate bounce sequence, but the project has not frozen an explicit production predicate that maps `daily_range_intersects_line` + first opposite pivot directional consistency into Murphy's phrase "successful test + bounce".

Therefore do not silently promote those fields to PASS/FAIL.

## Confirmation timestamp defect found
`confirmation_evidence_layer.py` requires a `confirmation_available_timestamp`, but the real-data runner currently uses `line_availability_timestamp` for that field in its output schema. That is semantically wrong if the timestamp is intended to mean the time at which the successful third test + bounce becomes known.

The source contract states that confirmation availability must be the event timestamp at which the successful third test + bounce is known from completed data, not merely the line availability timestamp.

This is a real implementation gap and should be corrected before any production evaluator is attempted.

## No-break
No approved 0006/0007 production no-break predicate was found in the reviewed upstream path. Keep `no_break = UNKNOWN` for production.

## Decision
1. Preserve the existing candidate runner and evidence adapter.
2. Do not promote daily-range intersection or directional consistency to confirmation without an explicit approved binding.
3. Correct confirmation timestamp semantics before production use.
4. Continue searching only for an already-approved semantic binding; do not invent a tolerance, magnitude, duration, percentage, ATR, or lookback.
5. 2025 remains excluded from implementation selection/tuning.
