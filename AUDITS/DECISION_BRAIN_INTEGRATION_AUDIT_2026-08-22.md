# Decision Brain Integration Audit — 2026-08-22

## Current verified baseline
- Murphy active scope: 35 Frozen/Closed rules.
- Murphy Runtime verified: 34/35 under the corrected rule-by-rule audit.
- Murphy 0008 remains BLOCKED pending an approved source-bound operational definition for `decisively broken`.
- No Murphy rule semantics are reopened by this audit.

## Three-book contract
The existing `THREE_BOOK_DECISION_CONTRACT_V1` establishes the intended decision hierarchy:
- Murphy supplies technical context and a valid setup.
- Nison may provide directional confirmation.
- Trading in the Zone may only permit/block execution and may not generate or override direction.
- Strong confirmation requires Murphy setup + Nison confirmation + risk pass + Zone process pass.
- Contradictory Nison, invalid Murphy structure, failed risk, or failed Zone process reject the trade.
- Future data is forbidden and psychology features must be known before entry.

## Nison status
- Existing Nison candle-confirmation engine and outputs are present in the source packages.
- Current operational Nison spec explicitly states that its deterministic definitions are only inspired by common candlestick taxonomy and that exact Steve Nison textual criteria/context must be mapped before treating the spec as canonical.
- Therefore Nison is **INTEGRATION-READY / CANONICAL-MAPPING-GAP**, not frozen as an authoritative runtime producer solely from this package.
- Do not add or tune pattern thresholds in this audit.

## Trading in the Zone status
- The repository contains `THREE_BOOK_RUNTIME_BOUNDARY_TIZ_PRODUCER_SPEC_CANDIDATE_V1`.
- It is explicitly `CANDIDATE_NOT_AUTHORITATIVE` and requires an authoritative producer, deterministic evaluator, adapter integration, historical QA, 2025 OOS protection, and cross-file consistency before freeze.
- Therefore TIZ is **PROCESS-ROLE DEFINED / RUNTIME-PRODUCER GAP**.
- Direction generation and technical override remain forbidden.

## Historical / Similarity Memory status
- Context-aware retrieval provides structured historical reads.
- Historical Context Memory is outcome-free and explicitly `not_a_strategy`.
- Historical Outcome Memory provides descriptive forward-return statistics at 6/12/24/48 H1 horizons and explicitly states these are historical descriptions, not guaranteed probabilities or trade rules.
- Similarity Memory uses weighted categorical agreement + robust numeric closeness + candlestick similarity, top_k=20, and explicitly marks `not_a_strategy=true`.
- Therefore these memory layers are **EVIDENCE SOURCES**, not independent decision makers.

## Decision engine status
- `DECISION_SCHEMA_V1` already separates Murphy, Nison, Trading in the Zone, risk, final decision, and audit provenance.
- The schema permits `BUY|SELL|NO_TRADE`, but the integration contract constrains how those fields may be populated.
- The next engineering task is to implement/verify the producer boundaries into this schema without allowing TIZ or memory to generate direction.

## Integration gaps to close
1. Establish an authoritative Nison producer contract from the existing source-mapped knowledge; do not replace it with the candidate generic taxonomy.
2. Establish an authoritative TIZ producer contract/evaluator from the existing project source; keep output neutral and execution-gating only.
3. Build a single cross-book adapter that consumes Murphy evidence, optional Nison confirmation, TIZ process state, risk output, and historical evidence without allowing memory or psychology to become directional.
4. Add deterministic no-lookahead / provenance tests at the cross-book boundary.
5. Preserve 2025 as OOS and prohibit tuning or threshold selection from the final test set.

## Decision
Do not rebuild the three knowledge bases. Integrate the existing artifacts through explicit producer contracts and a single Decision Brain boundary. Keep unresolved components blocked rather than inventing semantics.
