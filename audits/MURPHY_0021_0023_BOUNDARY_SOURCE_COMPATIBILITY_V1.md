# Murphy 0021–0023 — Boundary Source Compatibility V1

Date: 2026-08-13
Scope: 0021–0023 only
Status: SOURCE-COMPATIBILITY CHECK — NO PRODUCTION FREEZE

## Actual evaluator output
The Workspace evaluator `MURPHY_EVALUATORS_V1/murphy_0021_0023_evaluator.py` returns:
- `rule_id`
- `status`
- `directional_confirmation`
- `reason`

For unavailable evidence it returns `status=NOT_EVALUABLE` and `directional_confirmation=UNKNOWN`.

The evaluator contract names the canonical rule IDs as `MURPHY_0021`, `MURPHY_0022`, and `MURPHY_0023`.

## Compatibility result
The Boundary implementation's accepted rule IDs match the evaluator's canonical IDs.
Its status vocabulary includes all three evaluator statuses: PASS, FAIL, NOT_EVALUABLE.
Its directional field can preserve the evaluator's `UNKNOWN` value because it is transported as an opaque optional string.

The boundary also carries `confirmation_available_timestamp`, but this field is not currently emitted by the 0021–0023 evaluator implementation. Therefore the boundary must treat it as optional metadata, not as a required evaluator field.

## Important correction
The earlier generic test example using `directional_confirmation=null` for NOT_EVALUABLE is not source-exact. The source evaluator actually emits `directional_confirmation="UNKNOWN"` for NOT_EVALUABLE.

The test contract must therefore assert exact source behavior:
`NOT_EVALUABLE + UNKNOWN` must survive unchanged.

## Semantic constraints
- Do not convert UNKNOWN to null, NONE, FAIL, or PASS.
- Do not infer direction from status.
- Do not synthesize strength, conflict, or gate.
- Do not require a timestamp that the source evaluator does not emit.
- Do not modify evaluator semantics.
- Do not use 2025.

## Gate
After source-exact boundary tests pass, perform the separate mapping compatibility test against the canonical Rule Adapter. Until that mapping is explicitly approved and reconciled, Production Freeze remains blocked.
