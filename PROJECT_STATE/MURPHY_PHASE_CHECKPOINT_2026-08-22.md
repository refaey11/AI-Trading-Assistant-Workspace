# Murphy Phase Checkpoint — 2026-08-22

## Purpose
Canonical checkpoint after reconciliation of Murphy closure artifacts, GitHub history, workspace archives, and status registries. This checkpoint records what is established and what remains an integration task. It does not reopen closed rules and does not claim unverified runtime completion.

## Scope
- 51 Murphy rules total.
- 35-rule closed/frozen candidate set is the active closed-rule scope for the current project phase.
- 16 rules remain in the separate Open Rules register.
- Rule 0046 belongs to the Open Rules register and is outside the current 35-rule closed scope.

## Murphy authority boundary
Murphy is technical context / market structure. It must not independently generate the final BUY/SELL decision.

## Preserved project boundaries
- Nison: confirmation only.
- Trading in the Zone: psychology/process gate only; cannot generate direction.
- Similarity Engine: historical memory/evidence only; never the sole decision maker.
- Risk: hard gate/veto.
- 2025: final out-of-sample period; never use it for tuning.

## Reconciliation result
Direct closure/freeze evidence was recovered across the closed-rule scope, including the previously reconciled groups:
- 0003, 0004, 0006, 0007, 0008
- 0021, 0022, 0023
- 0025, 0026, 0028, 0029
- 0030–0032
- 0033–0045
- 0047–0051

0046 is explicitly excluded from this closed-scope list because it belongs to the Open Rules register.

## Important distinction
CLOSED/FROZEN rule knowledge and governance are not automatically equivalent to complete executable end-to-end runtime integration. The remaining Murphy work is an integration/adapter validation task, not a rule-rebuild task.

## Rule Adapter checkpoint
Existing adapter contract/architecture is treated as the starting point. The required normalized integration fields/checks include:
- rule_id
- status
- evidence
- current_state
- decision_hint
- confidence_delta

Required behavior:
- fail closed when evidence is insufficient: NOT_EVALUABLE, not invented PASS;
- no direction leakage from Murphy alone;
- confidence_delta cannot create a trade from no_trade;
- authority boundaries above must remain intact;
- Risk hard veto must remain enforceable.

## Next phase
1. Audit existing adapter implementation against its contract.
2. Reuse existing files; patch only verified gaps.
3. Run 35/35 coverage and contract tests.
4. Run authority, conflict, fail-closed, process-gate, and risk-veto integration tests.
5. Validate historical behavior on 2016–2024.
6. Preserve 2025 for final OOS testing only.
7. Record each completed milestone in GitHub before moving to the next major engine.

## Project discipline
Do not rebuild existing Murphy knowledge from scratch. Audit and integrate existing artifacts first. Do not silently invent operators, thresholds, proxies, or missing evidence.
