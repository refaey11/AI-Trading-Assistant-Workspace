# Rule Factory V1 — Isolated Pilot

## Safety boundary
This pilot is on `pilot/rule-factory-v1`, based on `main`. It does not modify production and does not redefine any source rule.

## Purpose
Automate the repeated orchestration around existing rule contracts so one blocked rule does not block unrelated rules.

## Gate order
1. Canonical evaluator
2. Deterministic tests
3. Historical QA
4. No-lookahead gate
5. OOS protection gate
6. Governance status

## Allowed outcomes
- FROZEN: all registered gates pass.
- CANDIDATE: rule remains usable for research/evidence but is not production frozen.
- BLOCKED: a required safety/availability/evaluability gate prevents promotion.
- FAIL: a defined rule violates an explicit test.

## Explicit non-goals
- No rule semantics are invented.
- No automatic threshold optimization.
- No 2025 tuning or selection.
- No trade direction generation.
- No automatic merge to main.

## Next validation
Run the factory against existing, already-validated rules as regression controls before connecting it to unresolved Murphy batches. A factory failure must not alter those rules.
