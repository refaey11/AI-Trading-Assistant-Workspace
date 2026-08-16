# Rule Factory V1 × Rule Adapter V1 Compatibility Audit

Date: 2026-08-16
Branch: `pilot/rule-factory-v1`
Status: BLOCKED_FOR_INTEGRATION

## Scope
Determine whether the existing Rule Adapter can be safely placed after Rule Factory V1 without changing canonical rule meaning or Decision Brain precedence.

## Existing source-of-truth findings
The existing Rule Adapter contract is `rule_adapter_contract_v1.json`. It is explicitly DESIGN_ONLY and is intended to normalize existing book-rule outputs into Decision Brain evidence; it must not duplicate the 102 rules or make trading decisions.

The existing implementation is `rule_adapter.py`.

## Compatibility result
### Compatible
- Adapter remains an evidence/normalization layer.
- Murphy remains primary technical context.
- Nison remains confirmation only.
- Trading in the Zone remains process gate only.
- Similarity remains historical evidence only.
- Risk remains a hard gate.
- 2025 remains OOS.
- Factory orchestration does not alter canonical evaluator meaning.

### Blocking mismatches
1. Contract requires `decision_hint`; current adapter output does not expose it.
2. Contract requires bounded `confidence_delta`; current adapter output does not expose it.
3. Contract declares `current_market_state` as adapter input, but current implementation accepts `current_state` without using it.
4. Existing adapter uses a heuristic base strength value. This is engineering evidence and must not be presented as source-author strength or as a canonical rule threshold.
5. The current registry has stale/parallel attribution issues; the adapter must not replace canonical Murphy rule governance with the old registry.

## Frozen-rule protection
MURPHY_0003 and MURPHY_0004 are protected by the 2026-08-15 production freeze artifact. They must not be changed to accommodate the Factory/Adapter integration.

## Decision
Do not integrate Factory V1 with the Adapter as a production path yet.

First close the Adapter contract mismatch in a separate versioned change, with tests proving:
- canonical direction is preserved;
- gate precedence is preserved;
- `decision_hint` cannot create a trade from no-trade;
- `confidence_delta` is bounded and cannot override hard gates;
- provenance/source_rule_id is preserved;
- availability is preserved;
- Similarity cannot override a hard gate.

Only after those tests pass should one frozen rule be used as a read-only integration regression.

## Non-negotiables
- Do not modify frozen Murphy rules.
- Do not invent thresholds/operators.
- Do not tune on 2025.
- Do not let Adapter or Factory generate a trade independently.
- If required evidence is unavailable, return NOT_EVALUABLE/BLOCKED.
