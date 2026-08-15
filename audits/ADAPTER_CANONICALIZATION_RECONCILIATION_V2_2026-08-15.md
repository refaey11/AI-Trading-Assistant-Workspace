# Rule Adapter — Canonicalization Reconciliation V2
Date: 2026-08-15

## Finding
The project Workspace DOES contain the original Rule Adapter implementation at `024/rule_adapter.py`. The earlier claim that the file could not be found in the project source was incorrect.

The uploaded project handoff explicitly lists both `rule_adapter_contract_v1.json` and `rule_adapter.py` and states their purpose is to normalize existing book-rule outputs into Decision Brain evidence. The adapter is DESIGN_ONLY / initial implementation and requires validation.

## Implementation verified
`024/rule_adapter.py` currently defines `NormalizedEvidence` with:
- module
- source_rule_id
- statement
- direction
- strength
- available
- gate
- conflict

`adapt_rule()` accepts `rule`, `current_state`, and `similarity`, but the current implementation does not actually use `current_state`.

The implementation also does NOT provide:
- decision_hint
- confidence_delta

The adapter contains conservative direction parsing, role mapping, gate handling for Zone/unattributed rules, textual Murphy risk handling, and Similarity support/contradiction handling.

## Contract verified
`025/rule_adapter_contract_v1.json` requires:
- current market state inputs
- registry rule inputs
- historical/similarity inputs
- evidence fields
- gate
- conflict
- decision_hint
- bounded confidence_delta

Status remains DESIGN_ONLY.

## Governance conclusion
Do NOT replace the adapter. Do NOT rebuild it.
Do NOT silently promote it to production.
The correct next task is a minimal compatibility repair/extension, preserving its role as normalization-only and preserving Risk as the hard gate and Similarity as evidence only.

## 0021–0023 implication
The existing adapter is registry-oriented; it does not currently accept the `PASS/FAIL/NOT_EVALUABLE` evaluator-result boundary as a first-class input. Therefore the previously created lossless boundary remains useful, but the canonical evaluator-result → evidence mapping still requires an explicit contract and deterministic tests.

## Freeze status
0021–0023 remain QA PASS / FREEZE CANDIDATE, not Production Frozen.
Historical clean artifact remains the canonical 122,934-row 2020–2024 artifact with 2025 excluded.

## Next gate
1. Preserve current adapter implementation.
2. Define minimal evaluator-result bridge contract.
3. Add required contract fields without moving decision logic into adapter.
4. Deterministic tests.
5. Reconcile 0021–0023 against clean historical evidence.
6. Availability/no-lookahead audit.
7. Final freeze manifest.
