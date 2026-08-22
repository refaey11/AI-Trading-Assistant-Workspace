# Work Scope Correction — 2026-08-22

## Active scope
The current implementation and integration scope is the project's 35 already Closed/Frozen Murphy rules.

## Parked scope
The remaining 16 Murphy rules are explicitly parked for the current phase. Do not begin new rule-development work on them during the 35-rule runtime/integration phase.

## Critical correction
Previous workstream notes that treated the 16 parked rules as the immediate implementation target were incorrect for the current project phase. In particular, do not start 0030-0032 merely because they are next numerically.

## Operating objective
Do not reopen frozen rule semantics. Instead:
1. Recover and verify existing evaluator/runtime artifacts for the 35 closed rules.
2. Normalize outputs through the existing Rule Adapter contract.
3. Preserve NOT_EVALUABLE and fail-closed behavior.
4. Integrate frozen Murphy evidence with Nison confirmation/context, historical/similarity evidence, Decision Brain, and Risk hard gates according to existing role boundaries.
5. Run end-to-end tests and produce a final runtime coverage matrix.

## Governance boundaries
- Murphy: technical context/evidence.
- Nison: confirmation/context; does not independently create direction.
- Trading in the Zone: psychology/process gate only; cannot create direction.
- Similarity: historical evidence only; never sole decision-maker.
- Risk: hard gate.
- 2025 remains OOS and must not be used for tuning or implementation selection.
- Do not rebuild existing frozen components without contradictory evidence or an approved semantic change.

This checkpoint corrects work scope only and does not modify any frozen rule definition or status.
