# Canonical Master Map → Runtime Compatibility Audit
Date: 2026-08-28
Branch: backtest-only-2026-08-28

## Purpose
Reconcile the original project architecture against the actual artifacts on the current branch and the recovered workspace. This is an audit/controls document, not a redesign.

## Source-of-truth hierarchy
1. Workspace/File Library artifacts for component existence/content.
2. Current branch runtime files for what CI can actually execute.
3. Older status snapshots remain historical when they conflict with current runtime evidence.

## Canonical architecture under audit
Market Data → Market Reader → Market State → Market Structure → Dynamic MTF / Time Context → Murphy → Nison → TIZ → Historical/Similarity Evidence → Rule Adapter / Master Evidence → Knowledge Alignment → Agreement / Contradiction Gate → Knowledge/Decision Handoff → Decision Brain V1 → Risk Gate → Position Sizing → Execution Contract.

## Compatibility matrix
| Layer | Evidence found | Current runtime status | Classification | Required next action |
|---|---|---|---|---|
| H1 Market Data | Authoritative GBPUSD H1 2016-2025 source is referenced by the current governed workflow | Runtime input | COMPATIBLE | Use only 2016-2024 in this development run; keep 2025 locked |
| Market Reader | Project archive contains MARKET_READER_V1 artifacts | No dedicated current-branch Reader runtime module identified by repository search | ADAPTER_REQUIRED | Mount existing Reader output; do not rebuild it |
| Market State | GBPUSD market-state source and contract exist in project workspace | Runtime-connected | COMPATIBLE | Preserve point-in-time joins |
| Market Structure | Workspace audit contains all 51 Murphy rows as SUPPORTED_PRIMITIVE using existing S/R primitives | Standalone producer not established in current runner | ADAPTER_REQUIRED | Mount existing structure primitives; do not invent operators |
| Dynamic MTF / Time Context | DYNAMIC_MTF_BINDING_CONTRACT_V1 + selection examples + 51-rule MTF map exist | Current runner has MTF input; rule-level timeframe mapping is explicitly unresolved/not-expressed for many rules | ADAPTER_REQUIRED / GOVERNANCE BLOCK | Apply only explicit MTF policy; unresolved mappings remain NOT_EVALUABLE |
| Murphy | Current routing registry / adapter allowlist contains 34 active rules | Routing connected | COMPATIBLE at routing level; historical fan-in incomplete | Build source-backed 2016-2024 evidence for current 34 scope; never fabricate |
| Nison | 44-rule runtime/bridge and frozen scope exist | Runtime-connected | COMPATIBLE | Confirmation/contradiction only |
| TIZ | RUNTIME/TIZ_PROCESS_GATE_V1/tiz_process_gate_v1.py exists and implements READY/NOT_READY | Runtime module exists | ADAPTER_REQUIRED | Feed real process-state inputs; never synthesize PASS |
| Historical Context Memory | HISTORICAL_CONTEXT_MEMORY.csv + index/contract exist | Runtime artifact exists | ADAPTER_REQUIRED | Pass actual as-of context evidence, not presence-only |
| Historical Outcome Memory | HISTORICAL_OUTCOMES.csv + stats/index exist | Runtime artifact exists | ADAPTER_REQUIRED | Pass actual outcome evidence as-of |
| Similarity V2 | Summary/reads/method artifacts exist | Evidence artifact exists | ADAPTER_REQUIRED | Carry matches/results through Handoff as evidence only |
| Context-Aware Retrieval V2 | Summary/reads artifacts exist | Evidence artifact exists | ADAPTER_REQUIRED | Carry retrieved context through Handoff; no directional authority |
| Rule Adapter | ADAPTERS/rule_adapter_execution_bridge_v1.py exists and enforces allowlist and conflict normalization | Runtime module exists | COMPATIBLE at boundary | Use it as the normalization boundary |
| Knowledge Alignment | Detailed handoff records Rule Adapter → Knowledge Alignment PASS 6/6 and KA → Risk PASS 8/8 | Existing integration milestone; canonical runner does not expose a dedicated alignment stage | ADAPTER_REQUIRED | Reuse existing contract/test boundary |
| Agreement / Contradiction Gate | Nison contradiction handling exists; no standalone canonical gate identified | Partially represented | ADAPTER_REQUIRED | Make gate explicit before Handoff |
| Knowledge/Decision Handoff | compatibility/knowledge_decision_handoff.py exists and is fail-closed | Runtime-connected | COMPATIBLE | It must receive the complete evidence envelope |
| Decision Brain V1 | Recovered at RECOVERED_SOURCES/DECISION_BRAIN_V1/decision_brain.py | Runtime-connected | PROTECTED | Do not modify semantics |
| Risk | RUNTIME/RISK_ENGINE_INTEGRATION_V1/risk_engine_integration_v1.py exists | Runtime-connected | ADAPTER_REQUIRED | Use upstream execution inputs; no invented SL/TP method; hard gate remains real |
| Position Sizing / Execution | Existing bridge exposes execution contract; live broker/cost assumptions remain unresolved | Not production-ready | NOT_EXECUTION_READY | Preserve research-only status |
| 2025 | Governance explicitly marks 2025 OOS | Locked | COMPATIBLE | Never tune/calibrate/select with 2025 |

## Reconciliation findings

### Murphy count conflict
The project contains historical governance snapshots with different counts: 33 frozen in the 2026-08-19 master-state snapshot, 35/51 authoritative in the detailed 2026-08-21 handoff, and 34 active/dispatched in the current runtime registry/adapter allowlist. These are not interchangeable concepts. The current branch runtime integration scope is 34. Do not alter semantics to force counts to match.

### Dynamic MTF conflict
The recovered 51-rule mapping explicitly labels rule-level timeframe resolution as UNRESOLVED_BY_RULE / NOT_EXPLICIT and says resolution must come from an explicit MTF policy, not from guessed rule-name semantics. Therefore current code must not claim complete Dynamic MTF closure until the policy is actually mounted.

### Historical Murphy evidence conflict
The 2026-08-27 handoff records that the recovered normalized 2016-2024 Murphy historical artifact covers only 7 rules of the current 34-rule runtime scope. The correct state for uncovered rules is NOT_EVALUABLE / governed-unavailable, not fabricated historical evidence.

### Contract-test conflict
The current Integration Contract Test uses synthetic evidence and synthetic Risk inputs; it proves module compatibility only. It does not prove real source-backed E2E integration and must not be treated as a substitute for real-source validation.

## Gate decision
FULL CANONICAL INTEGRATION = BLOCKED until the items classified ADAPTER_REQUIRED / GOVERNANCE BLOCK are closed with source-backed artifacts and deterministic tests.

## Next engineering sequence
1. Compile real source-backed evidence into one canonical point-in-time envelope.
2. Mount existing Market Structure and explicit Dynamic MTF policy artifacts.
3. Run existing Rule Adapter → Knowledge Alignment → Agreement/Contradiction → Handoff on a small real-data sample.
4. Feed real TIZ process inputs; unresolved inputs stay NOT_READY/NOT_EVALUABLE.
5. Verify Risk can genuinely PASS and FAIL using existing execution inputs; do not invent SL/TP logic.
6. Only after deterministic sample validation, consume one governed 2016-2024 backtest run.

## Governance lock
2025 remains OOS and locked. Decision Brain V1, Murphy semantics, Nison semantics, Similarity/Memory authority, and Risk hard-gate semantics are protected.
