# AI Trading Assistant — Master Execution Roadmap V1
Date: 2026-08-29
Status: ACTIVE — EXECUTION TRACK

## Mission
Build the existing AI Trading Assistant into one integrated Decision Brain that can:
Market Data -> Market State/MTF -> Murphy -> Nison -> TIZ -> Historical Memory -> Decision Brain -> Risk -> Trade Plan -> Execution -> MT5 -> Result -> Memory/n8n.

The project is NOT considered operational when modules pass individually. A gate is closed only when the relevant end-to-end chain works together on the same market snapshot/timestamp.

## Non-negotiable rules
1. Reuse existing project knowledge. Do not rebuild source knowledge from scratch.
2. Murphy = primary technical context/direction.
3. Nison = confirmation/contradiction only; never creates direction alone.
4. Trading in the Zone = process/psychology context; never direction generation.
5. Similarity and historical outcome memory = evidence only; never sole decision maker.
6. Risk is a hard gate.
7. 2025 is OOS and must never be tuned with.
8. No new strategy semantics during integration unless explicitly justified by a compatibility audit.
9. n8n is orchestration/automation/monitoring, not the trading brain.
10. MT5 is the broker/execution boundary.
11. One canonical Decision Event must carry the integrated result.
12. Backtest, Paper, Demo and Live must use the same decision runtime semantics.

## Master architecture
MARKET DATA -> MARKET SNAPSHOT -> MARKET STATE + MTF -> EVIDENCE ADAPTERS (Murphy, Nison, TIZ, Similarity, Historical Outcome) -> DECISION BRAIN -> HARD GATES -> RISK ENGINE -> TRADE PLAN -> EXECUTION ENGINE -> MT5 -> FILL/POSITION -> RESULT/P&L -> MEMORY + n8n.

## Phase 0 — FREEZE / PROTECT
Goal: protect existing intelligence and prevent accidental semantic drift.
Exit gate: current source/contracts/freeze boundaries documented; integration branch isolated.
Status: DONE/BASELINE PROTECTED.

## Phase 1 — CANONICAL CONNECT
Goal: connect existing modules through one orchestration boundary.
Deliverables: canonical MarketSnapshot; canonical Evidence objects; one Decision Runtime entry point; compatibility tests for every boundary; no hidden module-to-module dependencies.
Exit gate: one real snapshot can travel through the full evidence path.
Status: **PASS — FIRST REAL E2E REPLAY VERIFIED (2026-08-29)**
Evidence: `RUNTIME/DECISION_RUNTIME_V1/CHECKPOINT_2026-08-29_GATE1.md`, `RUNTIME/DECISION_RUNTIME_V1/artifacts/E2E_2016_MANIFEST.json`.

## Phase 2 — REAL DECISION REPLAY
Goal: run the integrated chain on real historical GBPUSD data.
Deliverables: chronological replay; one DecisionEvent per evaluated timestamp/setup; BUY/SELL/NO_TRADE; reason, evidence, gates, provenance; deterministic replay.
Exit gate: real data produces a coherent integrated event stream and executable events reconcile to existing outcomes.
Status: **PASS FOR AVAILABLE 2016 ARTIFACTS (2026-08-29)**
Verified: 401 events; 120 EXECUTABLE; 56 CANDIDATE; 225 NO_TRADE; 120/120 executable events matched the existing filtered execution outcome artifact; no unmatched executable events; no duplicate decision IDs after setup-aware identity fix.
Observed matched-outcome metrics: win rate 56.67%; PF 1.4554; expectancy +0.17286R; total +20.7432R; max DD -11.9262R.
Important: these are 2016 artifact-level results, not the official full-period baseline or a claim of future/live profitability.
Evidence: `RUNTIME/DECISION_RUNTIME_V1/CHECKPOINT_2026-08-29_GATE2.md`, `RUNTIME/DECISION_RUNTIME_V1/artifacts/GATE2_2016_REPLAY_SUMMARY.json`.

## Phase 3 — FULL BRAIN INTEGRATION + TRADE PLAN/RISK
Goal: route a real event through the recovered Decision Brain, governed Three-Book boundary, authoritative TIZ/Risk evidence, and frozen execution-plan adapter.
Deliverables: Runtime -> full Decision Brain assembler bridge; fail-closed TIZ/Risk authorization; mechanical Entry/SL/TP/R:R/size contract; integration tests.
Exit gate: one real pre-2025 snapshot can reach a fully assembled decision event without bypassing the production assembler; any missing authoritative TIZ/Risk producer blocks execution.
Status: **IN PROGRESS — BRIDGE ADDED (2026-08-29)**
Evidence: `RUNTIME/DECISION_RUNTIME_V1/full_brain_runtime_bridge_v1.py`, `RUNTIME/DECISION_RUNTIME_V1/test_full_brain_runtime_bridge_v1.py`.
Known compatibility issue being resolved: the Three-Book evaluator documents TIZ as audit/process context while the existing execution adapter requires a READY/PASS/AVAILABLE TIZ process state. No semantic change is authorized; the bridge currently fails closed until the authoritative contract is resolved.

## Phase 4 — UNIFIED BACKTEST
Goal: evaluate the actual integrated Decision Runtime, not isolated modules.
Development: 2016–2024. OOS: 2025. No 2025 tuning.
Metrics: PF, expectancy, total R, max DD, win rate, trade count, losing streak, cost/slippage/ambiguity sensitivity.
Exit gate: reproducible results + no leakage + correct provenance.

## Phase 5 — PAPER RUNTIME
Goal: same Decision Runtime on live market data with simulated execution.
Exit gate: stable real-time event timing, no lookahead, correct state transitions.

## Phase 6 — MT5 DEMO EXECUTION
Goal: send real demo orders through the execution boundary.
Deliverables: order submission, order result, fill tracking, position tracking, retry/idempotency handling, broker rejection handling.
Exit gate: Brain decision and MT5 state reconcile correctly.

## Phase 7 — RECONCILIATION
Goal: make broker reality authoritative for execution state.
Compare Brain intent vs order vs fill vs position vs close vs P&L.
Exit gate: deterministic reconciliation and safe fail-closed behavior.

## Phase 8 — n8n OPERATIONS
Goal: automate scheduling, alerts, monitoring, journaling and reporting.
n8n responsibilities: triggers, calls to Decision Runtime, alerts/Telegram, monitoring, daily reports, trade journal, failure notifications. It must not replace the Decision Brain.

## Phase 9 — CONTROLLED LIVE
Goal: controlled real-money deployment only after Backtest -> OOS -> Paper -> Demo -> Reconciliation gates pass.
Start with conservative risk limits and explicit kill-switches.

## Definition of DONE
The project is operational only when:
1. One current market snapshot enters the runtime.
2. All required evidence modules run on that same snapshot/as-of time.
3. Decision Brain outputs a final decision.
4. Risk approves/rejects it.
5. Trade plan is generated for approved trades.
6. Execution layer can hand it to MT5.
7. MT5 outcome is captured and reconciled.
8. The event is journaled for historical outcome/memory.
9. n8n can monitor the lifecycle.

## Progress log
2026-08-29:
- Confirmed project is not to be rebuilt.
- Created isolated branch: build/decision-runtime-v1.
- Created canonical Decision Runtime boundary and contract tests.
- Closed Gate 1 with a real 2016 GBPUSD integrated event stream.
- Closed Gate 2 for the available 2016 artifact set after fixing setup-aware deterministic event identity and reconciling 120/120 executable decisions to existing outcomes.
- Added the canonical Full Brain Runtime bridge and tests; it now fails closed when authoritative TIZ/Risk producers are absent.
- Next execution gate: resolve the existing TIZ/Execution contract boundary, then run the full 2016–2024 canonical replay using the same runtime semantics, without tuning.

## Anti-loop rule
No new evaluator, audit, freeze, adapter, or strategy layer may be added unless it directly closes a named gap in this roadmap. After every completed task, record: DONE; VERIFIED BY; ARTIFACT; REMAINING; NEXT SINGLE ACTION.
