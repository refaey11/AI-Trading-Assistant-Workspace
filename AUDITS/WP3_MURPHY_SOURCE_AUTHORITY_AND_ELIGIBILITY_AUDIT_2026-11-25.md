# WP3 — Murphy Source Authority and Eligibility Audit
Date: 2026-11-25
Branch: `audit/wp3-murphy-source-authority-2026-11-25`
Base: WP2 validated code/report head `931d0359c6c09667abcfb4c10399d0d3e16aff34`
Scope: GitHub-only static compatibility/governance audit. No market-data payloads were read.

## Executive conclusion
**Murphy-exclusive direction is implemented at the evaluator boundary, but the live Murphy input is not yet authenticated or fully governed. The live path must not be described as source-authenticated or production-eligible.**

The implementation now selects BUY/SELL from the top-level Murphy direction and ignores Brain/MTF/Volume direction. However, the runtime accepts caller-supplied claims of authority and producer identity, does not validate the Murphy pass rule against the canonical decision-eligibility manifest, and does not enforce a maximum event age or authenticated clock. A valid-looking input can therefore pass structural checks without proving that it came from the approved Murphy producer.

## Evidence reviewed
- `RUNTIME/DECISION_RUNTIME_V1/live_decision_runtime_v1.py`
- `evaluation/three_book_decision_evaluator_v1.py`
- `governance/DECISION_BRAIN_RULE_ALLOWLIST_V1.json`
- `BACKTEST/MURPHY_34_FANIN_CANONICAL_MANIFEST_V3.json`
- `BACKTEST/MURPHY_34_SOURCE_BACKED_FANIN_V2_2026-08-28.csv`
- `PROJECT_STATE/MURPHY_RUNTIME_ROUTING_REGISTRY_V1.json`
- `PROJECT_INDEX/MURPHY_CANONICAL_RECONCILIATION_REGISTRY_V1.json`
- `project_state/MURPHY_51_CANONICAL_RULE_STATUS_REGISTRY_V1.md`
- `audits/evidence/MURPHY_FROZEN_EVIDENCE_PROVIDER_EXACT_CONTRACT_CLOSURE_2026-08-22.md`
- `audits/MURPHY_0021_0023_RULE_ADAPTER_INTEGRATION_CONTRACT_V2.md`
- `RUNTIME/DECISION_RUNTIME_V1/gate3c_single_event_e2e_v1.py`
- `OOS_2025/build_single_event_risk_evidence_v1.py`
- `tests/evaluation/test_gate3c_murphy_direction_contract_v1.py`
- `RUNTIME/DECISION_RUNTIME_V1/test_live_decision_runtime_v1.py`

## Findings

### 1. Authority envelope is self-asserted, not authenticated — BLOCKER
Live Runtime `_require_source_envelope` checks:
- `authoritative is True`
- non-empty `source`
- non-empty `producer`
- parseable `available_at`
- `available_at <= query_as_of`

It does not bind the claimed producer/source to an approved producer registry, immutable artifact/version, code/config digest, signature/attestation, or authenticated clock. The caller supplies the fields being trusted. The runtime then constructs a new internal Murphy object with `authoritative: True` after those checks. This proves only that the input asserted authority and passed basic shape/time ordering; it does not authenticate provenance.

### 2. Runtime routing allowlist is being treated as directional eligibility — BLOCKER
`governance/DECISION_BRAIN_RULE_ALLOWLIST_V1.json` and `PROJECT_STATE/MURPHY_RUNTIME_ROUTING_REGISTRY_V1.json` describe the 34-rule runtime/routing scope. Routing state such as `ACTIVE_DISPATCHED` is not equivalent to directional decision eligibility.

The canonical `BACKTEST/MURPHY_34_FANIN_CANONICAL_MANIFEST_V3.json` explicitly states:
- runtime scope: 34 rules;
- decision-eligible rules: 7 only;
- eligible IDs: `MURPHY_0021`, `0022`, `0023`, `0025`, `0026`, `0028`, `0029`;
- candidate, provisional, context-only, and process-gate evidence cannot drive direction.

Current live runtime verifies that Murphy row IDs exist, that `pass_rule_id` is among those row IDs, and that directional source IDs are among those row IDs. It does **not** check the canonical seven-rule decision-eligibility manifest. The Three-Book evaluator checks membership in the broad Murphy+Nison rule allowlist, not a separate Murphy directional allowlist.

The historical Gate3C risk builder has a registry-aware selector, and its tests reject a non-decision-eligible Murphy rule and a pass rule absent from source provenance. That protection is not equivalently enforced in the current Live Runtime.

### 3. Rule/provider scope is not reconciled for live direction — BLOCKER
The 2026-08-22 exact frozen-evidence provider closure documents an existing provider contract using `available=true`, `frozen=true`, direction, and source_rule_id, and records the 0006/0007 evidence scope. It explicitly says **active provider presence was not yet verified**.

Separately, the 34-rule historical fan-in manifest lists seven decision-eligible historical directional streams and states that the next step is to compile a real point-in-time Murphy evidence envelope and attach Rule Adapter/Knowledge Alignment/Agreement-Gate provenance before Decision Brain V1.

The 0021–0023 adapter integration contract is a proposal and explicitly says it is not production-frozen. The reviewed sources therefore do not establish one reconciled, currently active live Murphy provider contract. Do not assume the historical seven-rule eligibility manifest itself supplies a real-time producer.

### 4. Row-level evidence is not fully bound to the top-level direction — BLOCKER
Live Runtime checks:
- top-level Murphy status is `PASS`;
- top-level direction is BUY/SELL;
- pass_rule_id appears in row source IDs;
- directional_source_rule_id values appear in row source IDs.

It does not establish that:
- the pass row itself has `status=PASS`;
- the pass row's own directional field matches the top-level direction;
- every directional source row belongs to an approved decision-eligible rule;
- exactly one governed directional pass is selected where the producer contract requires uniqueness;
- row timestamps/event identity/source identity bind to this exact query event.

Thus the envelope can contain matching IDs while its row semantics do not independently substantiate the asserted direction.

### 5. No maximum event age or authenticated clock — BLOCKER
Live Runtime rejects years <=2025 and timestamps more than five minutes in the future. It does not impose a maximum age for 2026 events. `available_at <= query_as_of` is only an ordering check; it does not prove the event is recent or that either clock is authenticated. A stale 2026 event may pass the current date-year check.

No max-age value should be invented in this audit. It requires an approved live event freshness contract and clock provenance.

### 6. Current adversarial tests do not test source forgery/eligibility
WP2 tests establish that Brain/MTF/Volume and Similarity cannot reverse Murphy direction, and that TIZ/Risk contracts remain as specified. They do not yet test:
- forged `authoritative=true` with an unknown producer;
- unregistered source/producer;
- decision-ineligible Murphy IDs such as MURPHY_0003/0004;
- mismatch between top-level direction and the actual pass row direction/status;
- multiple competing directional PASS rows;
- stale 2026 source/event timestamps;
- producer/config/version digest mismatch;
- unverified clock or absent freshness evidence.

### 7. Existing Murphy evaluator files do not close the canonical live provider contract
A focused repository-tree inspection located these existing implementations:
- `src/murphy_0006_0007/evidence_adapter.py`
- `runtime/murphy/murphy_0006_0008_runtime_v1.py`
- `MURPHY_EVALUATORS_V1/murphy_0006_0007_runtime_v1.py`
- `bridges/murphy_0021_0023_evaluator_to_evidence_bridge.py`
- `MURPHY_EVALUATORS_V1/murphy_0021_0023_evaluator.py`

Their exact compatibility status:
- The 0006/0007 evidence adapter explicitly emits `CANDIDATE_ONLY`; it does not create an approved successful-touch/no-break PASS predicate.
- The 0006/0007 runtime evaluators can emit `status=CONFIRMED` with a bullish/bearish direction after their line/reaction checks, but do not emit the canonical `available=true` and `frozen=true` provider record required by the recovered Knowledge Alignment contract.
- The 0006/0007 exact provider audit already states active provider presence is NOT VERIFIED and no synthetic frozen flag may be fabricated.
- The 0021–0023 evidence bridge normalizes an existing evaluator result into `available`, `direction`, `gate`, etc., but does not emit `frozen=true`; its integration contract is explicitly a proposal / not production-frozen.
- The canonical 34-rule fan-in manifest classifies 0006/0007 as provisional QA-only / not decision-eligible, while its seven decision-eligible rules are historical evidence streams. This reinforces that the 0006/0007 frozen-provider contract and the historical 7-rule eligibility list are distinct scopes and must not be silently conflated.

Therefore, the workspace contains Murphy evaluator artifacts, but the reviewed files do not yet provide a verified active producer that satisfies the exact frozen-provider contract and the current live decision contract simultaneously.

## Compatibility matrix — canonical status vs live producer wiring

The current canonical rule-status registry `project_state/MURPHY_51_CANONICAL_RULE_STATUS_REGISTRY_V1.md` is the authority for frozen status. It lists all seven manifest-eligible rules as PRODUCTION FROZEN and lists 0006/0007 as frozen at evaluator + Decision-Brain-evidence level. Older audit snapshots that disagree must be reported as historical conflicts, not used to downgrade the current status.

| Rule group | Canonical status / scope | Existing evaluator output | Live Decision Runtime compatibility | Verdict |
|---|---|---|---|---|
| 0006/0007 | Frozen at evaluator + Brain-evidence level; frozen provider contract explicitly requires available=true, frozen=true, direction, source_rule_id | Existing runtime returns status=CONFIRMED and direction=BULLISH/BEARISH; source-safe adapter returns CANDIDATE_ONLY | Runtime requires status=PASS and direction; it does not call these evaluators, and no verified adapter currently supplies the exact frozen envelope. Do not synthesize available/frozen flags | Frozen rule; provider wiring NOT CLOSED |
| 0021/0022/0023 | PRODUCTION FROZEN in canonical status registry; seven-rule fan-in manifest lists them decision-eligible | Evaluator returns PASS/FAIL/NOT_EVALUABLE plus directional_confirmation; 0022/23 require CME British Pound futures OI, not spot-FX proxy | Existing bridge normalizes to direction/gate/available, but integration contract V2 says proposal/not production frozen and does not emit frozen=true. Live Runtime still expects caller-supplied status=PASS + direction and does not call evaluator/bridge | Rule frozen; live producer-to-runtime envelope NOT CLOSED |
| 0025/0026 | PRODUCTION FROZEN in canonical status registry; decision-eligible in fan-in manifest | Runtime evaluator returns PASS/FAIL/NOT_EVALUABLE plus directional_confirmation using current_high/current_low vs preceding_4w_high/low | No verified live adapter/event producer or source-envelope binding found. Older four-week reconciliation contains close-vs-high/low contract conflict; do not reopen frozen semantics based on an old snapshot. Require canonical freeze artifact/manifest lookup before any use | Rule frozen; runtime source binding NOT CLOSED |
| 0028/0029 | PRODUCTION FROZEN in canonical status registry and individual freeze records | Evaluators return PASS/FAIL/NOT_EVALUABLE and directional_confirmation (0028 BEARISH_WARNING, 0029 BULLISH_WARNING) using confirmed divergence + pivot evidence | Live Runtime does not call these evaluators or bind their event availability/source identity to the current event. Warning semantics must not be silently upgraded to standalone trade direction | Rule frozen; live source binding NOT CLOSED |

### Important reconciliation of older conflicting records
- The 0021–0023 historical provenance audit and integration-gate documents contain older statements that integration/freeze remained open. The current canonical status registry supersedes those older snapshots for the rule's present freeze status. The historical records remain preserved; they are not rewritten.
- The 0021–0023 frozen snapshot records a clean 2020–2024 artifact with 9 raw 2025 rows excluded. The canonical status registry independently marks 0021–0023 PRODUCTION FROZEN. The separate raw-artifact contamination finding is not permission to re-open or retune the frozen rule.
- The 0025–0026 four-week reconciliation predates the current canonical status registry and says contract reconciliation was blocked. Current registry now marks 0025/0026 PRODUCTION FROZEN. Treat that old conflict as requiring canonical freeze-artifact provenance review, not a license to change the evaluator or choose a new price basis.
- 0028/0029 have individual production freeze records; the 0028 final provenance JSON still says freeze candidate, while its backup manifest and individual freeze markdown say PRODUCTION FROZEN. The canonical status registry is authoritative and says both are frozen.

## Live wiring result
The unified `MURPHY_EVALUATORS_V1/murphy_runtime_entrypoint_v1.py` dispatches the evaluator functions for these rules, but the inspected `RUNTIME/DECISION_RUNTIME_V1/live_decision_runtime_v1.py` does not import or call that entrypoint, any of the seven evaluators, or the 0006/0007 provider. Instead, it trusts the externally supplied `event["murphy_evidence"]` mapping after checking caller-provided authority/source/producer strings and basic rule-ID membership.

The live runtime's required top-level schema is:
- `status = PASS`
- `direction = BUY | SELL`
- `rows`, `pass_rule_id`, `directional_source_rule_id`
- `authoritative = true`, non-empty `source` and `producer`, `available_at <= query_as_of`

None of the inspected evaluators alone emits this complete envelope. Their native contract is `rule_id`, `status`, `directional_confirmation`, and rule-specific evidence fields; 0006/0007 emit `CONFIRMED` plus `direction`, while the frozen Knowledge Alignment contract expects `available`, `frozen`, `direction`, and `source_rule_id`.

**Therefore the correct next task is not to change Murphy rules or invent a provider. It is to locate the canonical, already-approved adapter/producer contract that converts existing frozen evaluator outputs into the Live Runtime's event-bound Murphy envelope, or explicitly keep live signals blocked if no such artifact exists.**

## Required next sequence
1. Reconcile the live directional source scope against the canonical registries and provider contracts. Keep separate: runtime routing, frozen rule status, historical decision eligibility, and live producer availability.
2. Identify an existing, active Murphy evaluator/adapter provider in the current repository and document its exact output contract. Do not build a duplicate Murphy evaluator or invent a new source.
3. Define a trusted producer identity/registry and source artifact/config/version binding using existing project evidence. If no authenticated mechanism exists, label source authority NOT_EVALUABLE and fail closed for live signals.
4. Define row-level binding: event timestamp/identity, pass status, pass rule, direction, directional source IDs, and eligible-rule membership must all reconcile.
5. Define an approved max event age and clock provenance before implementing freshness checks. Do not guess a numeric tolerance.
6. Add synthetic adversarial tests for all above cases; no market data is needed for these tests.
7. Only then implement the narrowest adapter/contract hardening on an isolated branch and run targeted GitHub Actions.

## WP2 validation retained
The prior WP2 code commit `567f4848e59c62b69b765931a1df5044dbade373` passed:
- Live Decision Runtime V1: 32 tests.
- TIZ Metadata-Only Compatibility: 65 tests.

Those tests validate the tested contracts, not upstream Murphy source authentication or the missing eligibility/freshness controls described here.

## Safety / non-actions
- Audit report only; no runtime or test code changed on this branch.
- No PR created from this audit branch.
- No merge, rebase, cherry-pick, main change, live execution, MT5 connection, or order submission.
- No Dropbox or CircleCI used.
- No historical market-data payloads or 2025/2026 datasets accessed.
- No test/workflow run was needed or performed for this report-only audit.

## Status
**MURPHY DIRECTION AUTHORITY: IMPLEMENTED AT DECISION LOGIC; CANONICAL RULE STATUS IS FROZEN FOR THE SEVEN ELIGIBLE RULES; LIVE PRODUCER-TO-RUNTIME WIRING NOT CLOSED.**
**LIVE SOURCE ENVELOPE / AUTHENTICATION: NOT CLOSED.**
**PRODUCTION / LIVE SIGNAL AUTHORIZATION: NOT GRANTED.**
