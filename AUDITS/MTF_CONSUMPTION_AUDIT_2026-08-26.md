# MTF Consumption Audit — 2026-08-26

## Scope
Read-only structural audit following the current handoff. No MTF rule semantics, thresholds, or 2025 OOS parameters are changed.

## Source evidence
- `AI_Trading_Assistant_MULTI_TIMEFRAME_READER_V1` contains H4/H1 aligned datasets for EURUSD, GBPUSD, USDJPY, XAUUSD, and USDCAD.
- `CONTRACT.json` explicitly defines H4 as higher-timeframe context and H1 as local structure, and says the layer does not generate trade decisions.
- The existing `compatibility/dynamic_mtf_binding_adapter_v1.py` can validate role assignments, but it requires explicitly supplied MTF role assignments; it does not retrieve MTF data by itself.
- `OOS_2025/full_decision_brain_historical_event_producer_v1.py` currently calls `assemble_decision_event()` with market-state `row=_pick_context(market_context, ts)` and does not supply an MTF evidence object.

## Result

| Layer | Status | Evidence |
|---|---|---|
| MTF source datasets | WORKING / PRESENT | H4/H1 datasets exist and cover the five project assets |
| Dynamic MTF binding adapter | PRESENT / READY FOR EXPLICIT INPUT | Contract-bound adapter exists and fail-closes on invalid role assignments |
| Current Decision Brain MTF ingestion | NOT WIRED | Current event producer has no MTF evidence field at the decision boundary |
| MTF influence on direction | NOT PROVEN | No downstream receipt showing MTF evidence was consumed by the recovered Brain |

## Boundary conclusion
MTF is **not missing**. It is a wiring gap at the Decision Brain boundary, consistent with the existing component wiring audit. The correct next action is to add a shadow-only MTF consumption probe for development years (2016–2024), using the existing MTF datasets and existing binding adapter, without changing the production/OOS decision path.

## Governance
2025 remains locked and is excluded from all tuning. No MTF thresholds or directional semantics are changed by this audit.
