# Murphy Freeze Batch 0015–0020 Gate V1

Date: 2026-08-12

## Source reviewed

Authoritative Workspace status registry: `MURPHY_RULE_WORKSPACE_STATUS_V1.csv`.

## Results

| Rule | Workspace status | Dedicated evaluator | Freeze result |
|---|---|---|---|
| 0015 | REQUIRES_DERIVED_FEATURE | False | NOT_EVALUABLE — derived feature/operator not closed |
| 0016 | REQUIRES_DERIVED_FEATURE | False | NOT_EVALUABLE — derived feature/operator not closed |
| 0017 | REQUIRES_DERIVED_FEATURE | False | NOT_EVALUABLE — derived feature/operator not closed |
| 0018 | REQUIRES_DERIVED_FEATURE | False | NOT_EVALUABLE — derived feature/operator not closed |
| 0019 | REQUIRES_DERIVED_FEATURE | False | NOT_EVALUABLE — derived feature/operator not closed |
| 0020 | NOT_YET_EVALUABLE | False | NOT_EVALUABLE — operator/evaluator not closed |

## Decision

No rule in this batch is promoted to FROZEN. The existing Workspace evidence does not contain a verified evaluator/test/historical chain for these six rules. Creating one without recovering the exact source-backed derived-feature/operator contract would violate the project freeze controls.

## Controls

- Reuse existing feature modules where a source-backed compatibility mapping exists.
- Do not invent derived features, thresholds, operators, timeframes, or proxies.
- 2025 remains OOS and is not used for tuning or implementation selection.
- This batch is separate from the 0003–0004 provenance issue and 0006–0007 trendline reaction gate.

## Next action

Continue the freeze audit with 0024–0026 and then the remaining Murphy rules, prioritizing any existing evaluator artifacts and source-backed operators.
