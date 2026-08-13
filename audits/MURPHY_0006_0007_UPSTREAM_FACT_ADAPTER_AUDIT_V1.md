# Murphy 0006–0007 Upstream Fact Adapter Audit V1

Date: 2026-08-13
Status: CORRECTION REQUIRED / DO NOT PROMOTE TO PRODUCTION

## Finding
The frozen source contract defines confirmation as:
1. two valid anchors;
2. a third test/touch exists;
3. the third test is successful AND price bounces away from the trendline in the original trend direction;
4. confirmation becomes known at the completed-data timestamp of that successful test + bounce.

The current `src/murphy_0006_0007/upstream_fact_adapter.py` is more aggressive than the source contract. It currently maps:
- `daily_range_intersects_line` -> `third_touch=True`
- `reaction_directionally_consistent` -> `reaction_bounce`

Those mappings are not sufficient to establish Murphy's successful test + bounce semantics. The source contract explicitly says the evaluator must consume already-derived successful third-test/bounce evidence and must not invent thresholds. Therefore these booleans must remain candidate observations unless a source-approved upstream predicate exists.

## Correct interpretation
- `third_touch`: candidate only from same-family third pivot + line interaction evidence.
- `reaction_bounce`: candidate only from directional reaction observation; not a production confirmation by itself.
- `no_break`: unknown until an approved operator/binding exists.
- `confirmation_available_timestamp`: unknown until the successful third-test + bounce event is actually established from completed data.

## Existing safe layer
`evidence_adapter.py` correctly remains candidate-only and calculates geometry/intersection without deciding successful touch.

## Decision
Do not use `upstream_fact_adapter.py` as a production evaluator. Correct it or keep its outputs explicitly candidate/observation status. Do not promote any field to PASS/FAIL based only on intersection or directional consistency.

## Next action
Search the remaining project artifacts for an already-approved successful-test/bounce predicate. If none exists, the production rule remains `NOT_EVALUABLE` despite having rich candidate evidence.

2025 remains OOS.
