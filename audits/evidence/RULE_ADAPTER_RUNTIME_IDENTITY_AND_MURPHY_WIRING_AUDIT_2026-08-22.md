# Rule Adapter Runtime Identity and Murphy Wiring Audit — 2026-08-22

## Scope
Determine whether the recovered `RULE_ADAPTER_V1_*` artifacts are the missing runtime that can execute the 35 canonical frozen Murphy rules and feed the Knowledge Alignment Adapter.

## Sources inspected
- `rule_adapter_contract_v1.json`
- `RULE_ADAPTER_V1_LINEAGE_REGISTER.json`
- `RULE_ADAPTER_V1_RECOVERY_CONTRACT.json`
- `RULE_ADAPTER_KNOWLEDGE_ALIGNMENT_INTEGRATION_TEST_V1.json`
- `THREE_BOOK_RULE_ADAPTER_COMPATIBILITY_AUDIT_RUN_074.json`

## Finding 1 — The generic Rule Adapter Contract is design-only
The existing contract says its purpose is to normalize existing book-rule outputs into Decision Brain evidence without duplicating source rules. Its status is `DESIGN_ONLY`. Therefore the contract alone is not executable proof of a live book-rule runtime.

## Finding 2 — Recovered RULE_ADAPTER_V1_27D is NOT the Murphy rule evaluator
The recovered lineage/recovery artifacts identify a different adapter:
- source of truth: `FEATURE_ENGINEERING_V2.h5`
- schema: 27 fields
- purpose: reproducible similarity query vector
- next stage: training-only retrieval index

Therefore this recovered `RULE_ADAPTER_V1_27D` is a feature/similarity adapter, not an evaluator for the 35 frozen Murphy rules. It must not be wired as Murphy evidence runtime by name similarity alone.

## Finding 3 — Historical boundary test is PASS, but representative only
`RULE_ADAPTER_KNOWLEDGE_ALIGNMENT_INTEGRATION_TEST_V1.json` reports 6/6 PASS and explicitly limits scope to representative authoritative evidence shapes. It does not claim that all 79 rule evaluators executed live in one runtime.

## Finding 4 — Current safe Murphy state
- 35 canonical frozen Murphy rule IDs: RECOVERED.
- 16 non-frozen/deferred rules: EXCLUDED from canonical Murphy whitelist.
- Knowledge Alignment input shape: RECOVERED.
- Exact live Murphy evaluator/runtime producing those outputs: NOT YET RECOVERED/VERIFIED.

## Governance decision
Do NOT force the 35-rule whitelist through `RULE_ADAPTER_V1_27D`.
Do NOT rename the 27D similarity adapter as a Murphy evaluator.
Do NOT create a substitute evaluator before source/runtime recovery is exhausted and compatibility is audited.

## Next safe action
Search the remaining canonical runtime inventories, handoff backups, and reconstructed GBPUSD workspace specifically for a live rule-evaluation path that can emit source-linked book evidence. Search targets include evaluator functions, rule execution dispatch, `source_rule_id`, `direction`, `available`, `frozen`, and provenance mapping.

## OOS control
2025 remains OOS and is not used for tuning.