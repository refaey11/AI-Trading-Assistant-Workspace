# Rule Adapter Repair Contract V1
Date: 2026-08-15
Status: CONTRACT PROPOSAL — NOT PRODUCTION FROZEN

## Source basis
The uploaded canonical adapter contract requires normalized evidence plus gate, conflict, decision_hint, and bounded confidence_delta. The compatibility audit records that the existing implementation is missing decision_hint/confidence_delta and does not consume current_state despite declaring it as an input.

## Scope
Repair the existing Rule Adapter only. Do not rebuild the Decision Brain, registry, Murphy evaluators, Nison, TIZ, Similarity, or Risk Engine.

## Required output
The adapter output must contain:
- module
- source_rule_id
- statement
- direction
- strength
- available
- gate
- conflict
- decision_hint
- confidence_delta

## Governance
- Adapter normalizes evidence; it does not decide trades.
- Risk Engine remains the authoritative hard gate.
- Similarity remains historical evidence only and cannot override hard gates or create a trade from no-trade.
- Murphy remains primary technical context.
- Nison remains confirmation only.
- Trading in the Zone remains process/psychology gate only.
- 2025 remains OOS and cannot be used for tuning, selection, or parameter choice.

## Mapping constraints
1. `decision_hint` must not be inferred from ambiguous registry text.
2. Pattern polarity, market-context direction, and trade direction must remain distinct.
3. `confidence_delta` must default to a neutral bounded value when no authoritative confidence adjustment exists; the adapter must not fabricate confidence.
4. `current_state` must either be explicitly consumed according to an approved field-level contract or be removed/documented as an out-of-scope input. It must not be silently ignored while claiming state-aware normalization.
5. `available=false` must not be treated as PASS or FAIL.
6. `needs_review` is for insufficient/ambiguous evidence and must not be converted to a trade direction.

## 0021–0023 integration
The evaluator result boundary remains lossless. Do not directly equate evaluator status with canonical gate until the mapping is approved and tested. Preserve PASS/FAIL/NOT_EVALUABLE and directional_confirmation at the boundary.

## Required tests before implementation can be promoted
- existing adapter regression tests remain green;
- decision_hint mapping tests;
- confidence_delta bounds tests;
- ambiguous direction tests;
- availability/needs_review tests;
- Risk hard-gate precedence tests;
- Similarity cannot override hard gate tests;
- 0021–0023 evaluator boundary integration tests;
- no 2025-derived behavior.

## Freeze gate
This contract proposal does not grant production freeze. Production integration requires deterministic test execution and reconciliation against the canonical evidence artifacts.
