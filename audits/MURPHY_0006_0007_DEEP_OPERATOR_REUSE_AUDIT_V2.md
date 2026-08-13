# Murphy 0006/0007 — Deep Operator Reuse Audit V2

Date: 2026-08-13
Status: AUDIT RESULT RECORDED / PRODUCTION OPERATOR STILL OPEN

## Sources inspected
- Reconstructed full GBPUSD_RULE_EVALUATOR_V2 workspace (241-file transfer lineage).
- TRENDLINE_GEOMETRY_CONTRACT_V1.json
- TRENDLINE_GEOMETRY_V1_OUTPUT/TRENDLINE_GEOMETRY_BUILD_CONTRACT_V1.json
- MURPHY_0006_TO_0010_EXACT_MAPPING_V1.csv
- MURPHY_51_COVERAGE_GAP_AUDIT_V1.csv
- MURPHY_51_EXACT_RULE_MAPPING_WORKSHEET_V1.csv
- MURPHY_EXACT_MAPPING_AUDIT_V2 artifacts
- Murphy 0006/0007 continuation/handoff files in File Library
- GitHub repository file search, commit search, and related break/no-break searches
- Murphy Chapter 4 source already reviewed and preserved as semantic source

## Findings
1. TRENDLINE_GEOMETRY_V1 is a geometry module only. It derives line_id, line_type, anchors, slope, direction, and availability from confirmed PIVOT_SEQUENCE_V2 pivots.
2. Geometry V1 explicitly excludes breakout detection and does not add tolerance, minimum-touch count, angle threshold, or breakout threshold.
3. The existing 0006/0007 mapping records the source-backed semantic chain but marks the third successful touch/reaction as NOT_YET_EVALUABLE because its operational definition is missing.
4. The existing 0008/0009 mapping references `break_structure_up/down` and an approved decisive-break condition, but the inspected workspace does not contain a standalone implementation/contract defining that decisive-break condition that can be safely reused for 0006/0007.
5. Murphy 0010 is explicitly NOT_EVALUABLE because the project-approved price/time filter has not been selected; therefore its general break-filter language cannot be silently reused as a 0006/0007 no-break predicate.
6. GitHub searches for `third_touch`, `reaction_bounce`, `no_break`, `break_structure_up`, `break_structure`, `trendline break`, and `consecutive closes` returned no direct reusable implementation in the repository search index.
7. The full workspace search also found no deterministic 0006/0007-specific touch tolerance, reaction threshold, lookback, or no-break operator.
8. Existing V4 historical candidate evidence provides raw observations (line/range intersection, subsequent directional reaction candidate, chronology/availability) but keeps `no_break_observation=OBSERVATION_ONLY` and `evidence_status=CANDIDATE_ONLY`.

## Important distinction
The project has a conceptual `break_structure_up/down` feature reference in mapping documents, but this audit did NOT find an authoritative executable contract for that primitive in the inspected Workspace/GitHub lineage. Therefore it cannot be promoted to a 0006/0007 no-break predicate without further provenance evidence.

## Decision
- Do not modify TRENDLINE_GEOMETRY_V1.
- Do not invent a touch tolerance or reaction threshold.
- Do not bind Murphy's general 3%/two-consecutive-close examples to 0006/0007.
- Do not reuse `break_structure_up/down` as a no-break operator unless its actual source-backed contract is recovered.
- Keep production 0006/0007 evaluation NOT_EVALUABLE until the missing upstream predicates are source-locked.

## Exact remaining gap
`TRENDLINE_GEOMETRY_V1 -> [third_touch, reaction_bounce, no_break] -> existing Murphy evaluator`

The missing layer is evidence generation/normalization, not Geometry and not the existing evaluator.

## Next authorized action
Search Git history/Workspace provenance for the actual implementation or contract behind `break_structure_up/down` and any source-backed touch/reaction detector. If found, perform compatibility audit and build only a minimal adapter. If not found, formally close the search gate and preserve NOT_EVALUABLE.
