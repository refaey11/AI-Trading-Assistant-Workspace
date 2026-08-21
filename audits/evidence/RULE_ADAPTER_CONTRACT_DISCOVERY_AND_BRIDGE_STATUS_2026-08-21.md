# Rule Adapter Contract V1 — Discovery and Decision-Brain Bridge Status

Date: 2026-08-21
Status: EXISTING CONTRACT LOCATED / DESIGN-ONLY / NO RUNTIME BRIDGE PROVEN

## Question audited
Does the project already contain an integration contract for the missing bridge between market/knowledge evidence, Decision Brain synthesis, and downstream risk gating?

## Evidence located
Dropbox file: `/rule_adapter_contract_v1.json`
Server modified: 2026-08-19T13:18:07Z.

## Contract purpose
The existing contract explicitly states its purpose is to normalize existing book-rule outputs into Decision Brain evidence **without duplicating source rules**.

Its declared sources of truth are:
- AI_Trading_Assistant_MASTER_KB_V1
- AI_Trading_Assistant_3_BOOK_INTEGRATION_V1
- AI_Trading_Assistant_KB_AUDIT_V1_CONFIRMED

## Preserved hard boundaries
The contract explicitly preserves:
- do not copy/rewrite registry rules into the Brain;
- Murphy = primary technical context;
- Nison = confirmation only;
- Trading in the Zone = process/psychology gate only;
- Similarity = historical memory/evidence only;
- Risk = hard gate;
- 2025 = OOS and not for tuning.

## Adapter inputs
- Current market state: market structure, MTF context, volatility regime, volume availability, current price action.
- Rule metadata/output: rule_id, primary_source, integration_role, rule_type, source metadata and setup/conditions/confirmation/trade-plan/risk/decision fields.
- Historical memory: similarity direction/strength, neighbor count, best distance.

## Adapter outputs
- Evidence records: module, statement, direction, strength, availability, source_rule_id.
- Gate: pass/fail/needs_review.
- Conflict: supports/contradicts/neutral/insufficient.
- Decision hint: bullish/bearish/neutral/no_trade.
- Confidence delta: bounded adjustment only and cannot create a trade from no-trade.

## Explicit precedence
1. Process gate failure blocks all execution.
2. Risk failure blocks all execution.
3. Murphy invalidation blocks directional setup.
4. Nison may confirm or contradict but never create direction alone.
5. Similarity may support or weaken but never override a hard gate.
6. Decision Brain synthesizes; the adapter only normalizes.

## Critical status finding
The contract status is explicitly `DESIGN_ONLY`.

Therefore this file is the strongest located evidence for the intended integration architecture, but it is **not proof of an implemented runtime adapter**.

## Reconciliation with previous audits
This contract explains the intended modern bridge much more precisely than the legacy fixed-weight AI Decision Engine V1 experiment. It supports:

`Market State + existing rule outputs + historical evidence -> Rule Adapter normalization -> Decision Brain synthesis`

while preserving downstream hard gates.

It does not prove the old AI Decision Engine V1 should be merged into Decision Brain V1. The legacy candidate layer remains historical research/runtime evidence unless separately adopted by a current implementation.

## Final verdict
- Existing integration design contract: PASS / LOCATED.
- Role boundaries: PASS.
- Agreement/contradiction semantics: PRESENT IN CONTRACT.
- Hard-gate precedence: PRESENT IN CONTRACT.
- Runtime implementation of adapter: UNPROVEN.
- Direct Brain -> CANDIDATE -> Risk runtime bridge: UNPROVEN.

## Next safe action
Do not rebuild any completed module.

The next work item is a compatibility audit between this DESIGN_ONLY contract and the current authoritative 79-rule state before any implementation. The audit must resolve whether the contract's legacy reference to the 102-rule registry conflicts with, or can be safely mapped to, the later authoritative 79-rule provenance boundary.

Only after that compatibility check should the smallest implementation/adapter work begin, followed by historical testing with 2025 preserved as final OOS.
