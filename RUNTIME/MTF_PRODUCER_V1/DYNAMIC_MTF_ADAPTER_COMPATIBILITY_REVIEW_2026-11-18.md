# Dynamic MTF Adapter Compatibility Review

**Date:** 2026-11-18  
**Parent:** PR #122 — MTF Producer V1 governed design and compatibility gates  
**Status:** READ-ONLY CODE REVIEW — NO RUNTIME OR DIRECTIONAL CHANGES

## 1. Files reviewed

- `compatibility/dynamic_mtf_binding_adapter_v1.py`
- `compatibility/dynamic_mtf_runtime_resolver_v1.py`
- `compatibility/dynamic_mtf_opportunity_ranker_v1.py`
- `tests/compatibility/test_dynamic_mtf_binding_adapter_v1.py`
- `compatibility/test_dynamic_mtf_runtime_resolver_v1.py`
- `compatibility/tests/test_dynamic_mtf_opportunity_ranker_v1.py`
- `AUDITS/DYNAMIC_MTF_RUNTIME_ADAPTER_GATE_2026-08-22.md`
- `AUDITS/DYNAMIC_MTF_RUNTIME_CONTRACT_TEST_2026-08-22.md`

The authoritative `DYNAMIC_MTF_BINDING_CONTRACT_V1.json` and examples are documented as recovered from the reconstructed workspace archive, but the contract JSON itself is not present as a standalone file in the inspected GitHub tree. This review therefore does not invent missing contract semantics.

## 2. What the current code supports

### Binding adapter

- Restricts timeframe labels to M5/M15/M30/H1/H4/D1.
- Requires explicit role assignments for the requested required roles.
- Enforces allowed timeframe candidates for each role.
- Rejects missing roles, unsupported timeframes, unavailable timeframes, and inverted higher-to-lower role ordering.
- Does not generate a direction; `final_trade_decision` remains unset.

### Runtime resolver

- Uses explicit upstream boolean evidence for context/setup/confirmation/risk completeness.
- Uses frozen candidate lists and deterministic higher-timeframe-first selection; no historical performance or 2025-derived weights are read.
- Fails closed with `NOT_EVALUABLE` when no execution candidate satisfies the implemented chain.
- Preserves an explicit upstream `CONFLICTED` alignment state.
- Does not itself inspect source timestamps, clock domains, producer lineage, or evidence freshness.

### Opportunity ranker

- Evaluates all six timeframe keys and only treats M30/M15/M5 as execution candidates.
- Requires explicit context, structure, setup, confirmation, non-contradiction, risk feasibility, and an upstream direction token.
- Returns the direction supplied by upstream evidence; it does not derive BUY/SELL from OHLC or MTF features itself.
- Uses deterministic M30 → M15 → M5 tie-breaking among complete execution candidates.
- Does not itself verify timestamp provenance or the upstream direction's evidence lineage.

## 3. Compatibility questions that remain open

These are audit findings, not authorization to change behavior.

1. **Repeated role assignments / alignment label:** the binding adapter labels repeated timeframe assignments as `MIXED` and unique assignments as `ALIGNED`. That is a role-assignment uniqueness test, not a demonstrated directional-alignment test. The authoritative contract definition must be checked before retaining or changing this meaning.
2. **Duplicate context selection:** the resolver independently selects macro context and context using the same candidate list and same `context_complete` boolean. It can select the same timeframe for both roles; an existing unit test expects D1/D1. Confirm whether the authoritative contract permits this or requires distinct role evidence.
3. **Resolver context requirement:** the resolver can select an execution timeframe when setup, confirmation, and risk flags are complete even if macro/context roles are unavailable. Confirm whether context completeness is a mandatory prerequisite under the recovered contract.
4. **Evidence trust boundary:** resolver and ranker accept caller-supplied booleans/direction values. They do not verify timestamps, `available_at`, source IDs, producer versions, freshness, or event identity. Those checks must be enforced at a trusted upstream boundary before these functions are allowed to influence the live runtime.
5. **Runtime wiring:** reviewed files do not establish that `bind_dynamic_mtf`, `resolve_mtf_event`, or `select_best_opportunity` are wired into `live_decision_runtime_v1.py`. Do not claim the Dynamic MTF path is live-integrated.
6. **Test scope:** existing tests use synthetic dictionaries and contract examples. Their existence does not prove current GitHub Actions execution, real aligned-row runtime behavior, timestamp causality, or broker/live feed readiness.

## 4. Required next compatibility gate

Before any adapter changes:

1. Attach or recover the exact authoritative `DYNAMIC_MTF_BINDING_CONTRACT_V1.json` content in a reviewable immutable project artifact.
2. Map each current adapter/resolver/ranker behavior to exact contract clauses.
3. Decide the semantics of role repetition, alignment, required context, and direction provenance from that contract—not from intuition.
4. Inspect actual historical aligned rows only within the permitted 2016–2024 development window, with timestamp limitations explicitly preserved.
5. Add deterministic tests only for approved contract requirements and run them through GitHub Actions.
6. Keep Time/Session Context separately blocked until its own authoritative contract is recovered.

## 5. Governance

- No code or runtime behavior changed.
- No formula, threshold, weight, directional rule, or session boundary was added.
- No 2025 OOS data was accessed or used.
- No orders or live execution were enabled.
- No merge to `main` is authorized.
- Documentation-only review; no automated tests were run by this commit.
