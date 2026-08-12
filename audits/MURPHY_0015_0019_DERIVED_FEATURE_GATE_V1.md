# Murphy 0015–0019 Derived Feature Gate V1

Date: 2026-08-12

## Scope

Close the next Murphy batch using existing Workspace evidence only. No rebuild and no invented features/operators.

## Current registry states

- 0015 = REQUIRES_DERIVED_FEATURE
- 0016 = NOT_YET_EVALUABLE / REQUIRES_DERIVED_FEATURE
- 0017 = REQUIRES_DERIVED_FEATURE
- 0018 = REQUIRES_DERIVED_FEATURE
- 0019 = REQUIRES_DERIVED_FEATURE

The current registry records zero dedicated evaluator artifacts for these rules. 0016 has three evidence conditions; 0017 has two; 0015, 0018, and 0019 each have one.

## Existing feature infrastructure verified

The project already contains Feature Engineering V2 and the Murphy mapping artifacts. The historical audit inventory explicitly contains:
- `MURPHY_0011_TO_0015_EXACT_MAPPING_V1.csv`
- `MURPHY_0011_TO_0015_EXACT_MAPPING_V2_RESET.csv`
- `MURPHY_0011_TO_0015_EXACT_MAPPING_V3.csv`
- `MURPHY_0016_TO_0020_EXACT_MAPPING_V1.csv`
- `MURPHY_0016_TO_0020_EXACT_MAPPING_V2_RESET.csv`
- `MURPHY_0016_TO_0020_EXACT_MAPPING_V3.csv`
- `MURPHY_51_EXACT_RULE_MAPPING_WORKSHEET_V1.csv`
- `MURPHY_51_EXACT_CONDITION_PREP_V1.csv`
- `MURPHY_51_RULE_TO_MTF_FUNCTION_MAP_V1.csv`
- `MURPHY_51_TIMEFRAME_MAPPING_AUDIT_V1.csv`
- `DYNAMIC_TIMEFRAME_SELECTION_EXAMPLES_V1.csv`

These prove that the mapping/feature-compatibility work was produced and preserved, but the current searchable excerpts do not expose the row-level Feature Engineering V2 schema or exact 0015–0019 operator contracts sufficiently to promote a specific derived feature to frozen status.

## Compatibility decision

Do not create a new derived feature yet.
Do not invent pattern measurements, thresholds, fixed lookbacks, or timeframe roles.
Do not create evaluators without an exact source-backed operator.

Current controlled state remains:
- 0015 = REQUIRES_DERIVED_FEATURE
- 0016 = NOT_YET_EVALUABLE / REQUIRES_DERIVED_FEATURE
- 0017 = REQUIRES_DERIVED_FEATURE
- 0018 = REQUIRES_DERIVED_FEATURE
- 0019 = REQUIRES_DERIVED_FEATURE

## What changed in this pass

The batch is now explicitly tied to the preserved Feature Engineering / mapping layer and the exact archived mapping files, rather than being treated as an undefined missing-feature problem.

This means the next unlock is narrow: expose/inspect the existing row-level schema for these five rules. If the required derived feature already exists, bind it; then close operator → evaluator → tests → historical QA. If it does not exist, keep the rule blocked until the authoritative source defines the feature.

## Controls

- 2025 remains OOS and untouched.
- Existing Decision Brain, Dynamic MTF, Pivot Sequence, Trendline Geometry, and Feature Engineering components are preserved.
- Similarity remains historical evidence only.
- No old historical counts are forced.

## Next action

Continue to the next actionable Murphy batch rather than waiting on a schema that is not currently exposed: resolve any rule whose blocker is already covered by an existing evaluator/market evidence module, while retaining 0015–0019 in this controlled gate until their exact feature schema can be inspected.
