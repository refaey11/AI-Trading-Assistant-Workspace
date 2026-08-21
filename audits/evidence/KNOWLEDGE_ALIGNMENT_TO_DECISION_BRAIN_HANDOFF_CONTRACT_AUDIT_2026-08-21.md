# Knowledge Alignment → Decision Brain Handoff Contract Audit

Date: 2026-08-21
Status: HANDOFF GAP CONFIRMED; NO BRAIN REBUILD REQUIRED

## Source evidence reviewed
1. `knowledge_alignment_adapter.py` from the milestone backup.
2. `RULE_ADAPTER_PROVENANCE_MAPPING_V1.json` from the same governed backup.
3. Existing `decision_brain.py` runtime previously recovered from Dropbox.

## Canonical knowledge output contract
The existing adapter returns evidence-alignment fields including:
- `alignment_state`
- `candidate_direction`
- `contradiction_gate`
- `process_gate`
- `book_evidence_status`
- optional `market_evidence_status`
- `similarity_record_count`
- `final_trade_decision: None`
- `next_layer: risk_engine_then_existing_decision_brain`

Critical semantics:
- Murphy provides candidate context/direction only from available + frozen evidence.
- Conflicting frozen Murphy directions produce `NEEDS_REVIEW` and no manufactured direction.
- Nison can confirm or contradict an existing Murphy direction; it does not create direction alone.
- Trading in the Zone `FAIL` produces `PROCESS_BLOCKED`.
- Similarity is counted as evidence only.
- The adapter intentionally emits no final trade decision.

## Authority evidence
`RULE_ADAPTER_PROVENANCE_MAPPING_V1.json` records:
- 35 closed/frozen Murphy rules.
- 44 closed/frozen Nison rules.
- 79 authoritative rules now.
- 23 unavailable/deferred.

The authority is governed by canonical provenance/commit pointers upstream of the adapter. The adapter itself is not an independent generic 79-ID allow-list.

## Decision Brain compatibility finding
The recovered `decision_brain.py` is an evidence/market assessment runtime using market and historical/similarity inputs. It is not a complete knowledge-aware orchestrator by itself.

Therefore the required change is a narrow handoff/compatibility boundary, not a Decision Brain rewrite.

## Minimum required handoff semantics
1. `PROCESS_BLOCKED` must remain a hard block and cannot be overridden downstream.
2. `NISON_CONTRADICTION` must remain visible as a contradiction and cannot become confirmation by transformation.
3. `candidate_direction` may enter as attributed book context, not as an automatic BUY/SELL command.
4. `final_trade_decision` remains outside the Knowledge Alignment adapter.
5. Similarity remains historical/evidence-only and cannot override a hard process or contradiction gate.
6. Risk remains an independent hard gate according to the existing risk contract.
7. 2025 remains protected OOS and is not used for tuning.

## Exact next implementation task
Recover or define only the narrow compatibility handoff that maps the above alignment output into the existing Decision Brain assessment input/evidence structure. Do not duplicate the 79 rules, rebuild the Decision Brain, or move risk authority into the adapter.

## Test cases required after handoff
- Aligned Murphy + Nison → context can pass to assessment, no automatic trade.
- Murphy-only → context passes with weaker/explicit status, no automatic trade.
- Nison contradiction → contradiction survives handoff.
- TIZ/process fail → hard block survives handoff.
- Insufficient book evidence → abstain/review state survives handoff.
- Similarity cannot override a hard gate.
- Risk failure blocks final eligibility.
- No 2025 tuning or leakage.
