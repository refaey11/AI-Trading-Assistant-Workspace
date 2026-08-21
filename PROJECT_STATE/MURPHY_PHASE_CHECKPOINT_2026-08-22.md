# Murphy Phase — Comprehensive Project Record — 2026-08-22

## Record purpose
This is the comprehensive Murphy project record, not merely a rollback checkpoint. It preserves the reconciled state, scope decisions, recovered closure evidence, authority boundaries, integration status, unresolved scope, and the exact next work so later project phases can continue without repeating the reconciliation.

## Canonical project context
- The project is an AI Trading Assistant / Decision Brain, not a trading indicator.
- Existing project knowledge and artifacts are the starting point; do not rebuild existing knowledge from scratch.
- Before new integration, perform compatibility audit first.
- John Murphy provides technical context / market structure.
- Steve Nison provides confirmation and must not independently generate direction.
- Trading in the Zone is a psychology/process gate and cannot generate direction.
- Similarity Engine is historical memory/evidence only and can never be the sole decision maker.
- Risk remains a hard gate/veto.
- 2025 is out-of-sample and must never be used for tuning.

## Murphy universe and scope decision
- Total Murphy rules: 51.
- Active closed/frozen project scope: 35 rules.
- Separate Open Rules register: 16 rules.
- MURPHY_0046 belongs to the Open Rules register and is outside the active 35-rule closed scope.
- The project must not stop on 0046 when progressing through the closed-rule integration scope.

## Reconciled closed/frozen groups
Recovered direct closure/freeze evidence established the following groups for the active closed/frozen scope:

### Group A — early closed batch
- 0003
- 0004
- 0006
- 0007
- 0008
- 0021
- 0022
- 0023
- 0025
- 0026
- 0028
- 0029

### Group B
- 0030–0032: production frozen.

### Group C
- 0033: locally frozen/closed in the recovered reconciliation artifacts.

### Group D
- 0034–0045: production frozen through the recovered batch freeze evidence.

### Group E
- 0047–0049: closed batch.
- 0050–0051: process-gate frozen.

### Scope handling note
0046 is explicitly excluded from the active closed-scope list because it is part of the separate Open Rules register. Do not treat it as the missing member of the 35-rule closed scope.

## What the reconciliation did and did not establish
Established:
- The active project phase has a reconciled 35-rule closed/frozen Murphy scope.
- Closure/freeze governance artifacts were recovered across the listed groups.
- The project does not need to reopen or rebuild those rules merely to continue.

Not yet claimed:
- Complete executable end-to-end runtime integration of all 35 rules.
- Runtime PASS for adapter coverage or integration tests that have not yet been executed.
- Any trading profitability claim.

Therefore, remaining Murphy work is an adapter/integration validation task, not a rule-rebuild task.

## Murphy authority boundary
Murphy is the technical context / market-structure layer. Murphy output must not independently become the final BUY/SELL decision.

## Preserved system authority model
1. Murphy -> primary technical context / market structure.
2. Nison -> confirmation only.
3. Trading in the Zone -> psychology/process gate only; no direction generation.
4. Similarity Engine -> historical evidence only; never sole decision maker.
5. Historical Context/Outcome Memory -> historical evidence under provenance/availability rules.
6. Risk -> hard gate/veto.
7. Final Decision Brain -> combines authorized evidence and gates; no single non-risk evidence source has unilateral final-decision authority.

## Existing Rule Adapter starting point
The existing Rule Adapter contract/architecture must be audited and reused before creating anything new.

The normalized integration contract requires the project to handle:
- rule_id
- status
- evidence
- current_state
- decision_hint
- confidence_delta

Required behavior:
- insufficient evidence must fail closed as NOT_EVALUABLE, not invented PASS;
- missing data must not be silently replaced with an unverified proxy;
- Murphy alone must not leak into a final BUY/SELL decision;
- decision_hint is evidence/interpretation support, not a standalone trade order;
- confidence_delta cannot create a trade from no_trade;
- current_state handling must be compatible with the contract;
- provenance/availability constraints must remain enforceable;
- Risk hard veto must remain enforceable regardless of other evidence;
- process-gate failure can block execution but cannot generate direction.

## Integration work status at this record
Completed at the governance/reconciliation level:
- closed/open scope distinction;
- 0046 classification for this project phase;
- recovered closed/frozen groups across the active scope;
- authority boundaries;
- OOS/tuning boundary;
- decision that existing adapter files must be audited before patching;
- decision to patch only verified compatibility gaps.

Still pending runtime validation:
1. Locate/audit the existing adapter implementation against the contract.
2. Identify only verified gaps; do not invent a parallel adapter architecture.
3. Confirm 35/35 registry coverage for the active closed scope.
4. Run normalized contract tests.
5. Run authority-boundary tests.
6. Run conflict/precedence tests.
7. Run NOT_EVALUABLE / fail-closed tests.
8. Run process-gate tests.
9. Run risk hard-veto tests.
10. Run end-to-end wiring tests.
11. Validate on 2016–2024 under availability rules.
12. Preserve 2025 exclusively for final OOS testing; do not tune on it.

## Test expectations
The integration test suite must be able to establish at minimum:
- Murphy alone != final BUY/SELL.
- Nison alone != direction generator.
- Similarity alone != final decision.
- Trading in the Zone alone != direction generator.
- Risk failure = NO TRADE / veto regardless of other evidence.
- Insufficient evidence = NOT_EVALUABLE, not fabricated PASS.
- Strong confidence evidence cannot override a no_trade state by itself.
- Historical data must respect point-in-time availability.
- 2025 must remain isolated from tuning and operator selection.

## Historical validation boundary
- Development/validation window: 2016–2024, subject to project availability/provenance rules.
- 2025: final out-of-sample only.
- Do not use 2025 to tune thresholds, select operators, repair rules, or choose logic.

## Open Murphy rules
The 16-rule Open Rules register remains separate from the active closed-scope integration work. It is not silently converted into closed knowledge and is not used as a reason to rebuild the reconciled 35-rule scope.

MURPHY_0046 remains in this Open Rules scope for its own future recovery/review path.

## Handoff to the next major engine
Murphy does not need another rule-count reconciliation before moving forward. The project can progress to the Nison engines while the remaining Murphy adapter/runtime validation is handled as an explicit integration gate.

The Nison audit should begin from existing artifacts, especially:
- Nison Context Engine.
- Nison Candle Confirmation.
- Existing closure/freeze evidence and registries.
- Existing integration contracts and Decision Brain boundaries.

The Nison audit must answer:
1. What is already closed/frozen?
2. What exists but is not wired?
3. What is a genuine runtime/contract gap?
4. What can be integrated without rebuilding existing knowledge?

## GitHub recording discipline
Every completed project milestone must be recorded in GitHub as a substantive project artifact, including:
- what was completed;
- exact scope/IDs where applicable;
- evidence/source basis;
- status (implemented, frozen, validated, pending, blocked);
- compatibility decisions;
- tests run and actual results when tests exist;
- unresolved gaps and why they remain unresolved;
- exact next step.

A status note alone is not sufficient when there is a concrete artifact, contract, code change, test result, registry, or reconciliation output that can be stored.

## Project discipline
- Audit and integrate existing artifacts first.
- Do not rebuild existing Murphy knowledge from scratch.
- Do not silently invent operators, thresholds, proxies, or missing evidence.
- Keep closed/frozen, open, candidate, and runtime-validated states distinct.
- Do not claim runtime PASS without executed evidence.
- Preserve the authority boundaries of the Decision Brain.
- Record completed work comprehensively in GitHub before or when moving to the next major milestone.

## Current canonical next work
1. Treat this record as the comprehensive Murphy handoff/state record.
2. Continue with Nison audit from existing files and closure evidence.
3. In parallel or as the next Murphy integration gate, audit the existing Rule Adapter implementation and run only verified compatibility patches/tests.
4. Record actual test outputs and implementation artifacts in GitHub when completed.
