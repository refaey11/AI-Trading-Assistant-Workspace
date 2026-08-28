# Canonical Master Map Compatibility Audit — 2026-08-28

Branch: `backtest-only-2026-08-28`

Purpose: compare the original Master Project Map with the current runtime implementation before any full 2016–2024 backtest.

## Source architecture

Market Data → Market Reader → Market State → Market Structure → Dynamic MTF / Time Context → Current Market Evidence → Murphy → Nison → TIZ → Historical Evidence → Similarity → Historical Context + Historical Outcome → Rule Adapter + Master Evidence → Knowledge Alignment → Evidence Agreement / Contradiction Gate → Knowledge/Decision Handoff → Decision Brain V1 → LONG/SHORT/NO TRADE → Risk Gate → Position Sizing → Execution Contract.

## Runtime audit

| Layer | Existing artifact/evidence | Runtime status | Required action |
|---|---|---|---|
| H1 Market Data | governed H1 master source | PRESENT | consume point-in-time |
| Market Reader | project/runtime source stack | PARTIAL / not separately represented in current canonical runner | identify canonical adapter before full run |
| Market State | acquired `market_state.csv` | CONNECTED | verify fields actually consumed |
| Market Structure | Master Map requires explicit layer | NOT PROVEN in current runner | locate existing canonical artifact; do not fabricate |
| Dynamic MTF / Time Context | MTF H4/H1 runtime artifact | PARTIAL | verify dynamic role vs static H4/H1 join |
| Murphy 34 | frozen allowlist / evidence | CONNECTED | preserve primary directional role |
| Nison 44 | frozen allowlist / evidence | CONNECTED | confirmation/contradiction only |
| TIZ | `RUNTIME/TIZ_PROCESS_GATE_V1/tiz_process_gate_v1.py` | PRESENT AND RUNTIME-ABLE | wire real inputs; never hardcode PASS |
| Historical Context | `HISTORICAL_CONTEXT_MEMORY.csv` | CONNECTED | point-in-time consumption |
| Historical Outcome | `HISTORICAL_OUTCOMES.csv` | CONNECTED | use actual outcome evidence, not only signature/timestamp |
| Similarity V2 | packaged V2 artifacts | PRESENT | evidence-only; no direction generation |
| Context-Aware Retrieval V2 | packaged V2 artifacts | PRESENT | retrieval/context evidence; no direction generation |
| Rule Adapter / normalization | compatibility + allowlist | PRESENT | normalize existing outputs; do not copy registry into Brain |
| Knowledge Alignment | Master Map layer | NOT PROVEN as independent runtime stage | recover/use existing canonical adapter if present |
| Agreement / Contradiction Gate | Handoff + Nison contradiction logic | PARTIAL | ensure it is an explicit pre-Brain gate |
| Knowledge/Decision Handoff | `compatibility/knowledge_decision_handoff.py` | PRESENT | canonical boundary before Brain |
| Decision Brain V1 | recovered source | PRESENT / PROTECTED | do not modify semantics/source |
| Risk Gate | `risk_engine_integration_v1.py` | PRESENT | hard gate; upstream supplies SL/TP/ATR |
| Position Sizing | Risk engine computes size | PRESENT | consume real execution inputs |
| Execution Contract | current runner simulates execution | PARTIAL | must not invent a new SL/TP policy inside orchestrator |
| 2025 | governance | LOCKED | never used for tuning/calibration |

## Critical blockers before full backtest

1. Prove the canonical Market Structure runtime artifact.
2. Prove Dynamic MTF / Time Context is actually dynamic/contextual and not only an H4/H1 static join.
3. Recover/verify the canonical Knowledge Alignment stage instead of collapsing it into the Handoff.
4. Make Agreement / Contradiction an explicit pre-Brain gate.
5. Wire real TIZ process inputs to `evaluate_tiz_gate`; `UNRESOLVED_OPTIONAL` must not be converted into PASS.
6. Pass Similarity V2 and Retrieval V2 as governed evidence to the Handoff without allowing either to generate direction.
7. Replace the runner's invented fixed SL/TP method with the existing canonical execution contract/input source. Risk validates; it does not invent execution policy.
8. Only after these checks pass should the 2016–2024 full backtest consume compute.

## Governance invariants

- Murphy remains primary technical/context direction source.
- Nison remains confirmation/contradiction only.
- TIZ remains process/psychology only.
- Historical memory and Similarity remain evidence only.
- Retrieval remains contextual evidence only.
- Decision Brain V1 remains unchanged.
- Risk remains a hard gate.
- 2025 remains completely locked from tuning/calibration/selection.
- No historical or OOS artifact is silently rewritten to make integration appear complete.

## Decision

The current canonical runner is **not yet authorized for a full 2016–2024 backtest**. The correct next step is a compatibility-only implementation pass that closes the seven blockers above, followed by a small E2E contract sample. Full backtest is authorized only after that sample and the Integration Gate both pass.
