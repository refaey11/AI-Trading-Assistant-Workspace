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
4. Trading in the Zone = process/psychology context; never direction generation; unavailable TIZ must not be synthetically inferred.
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
Status: DONE/BASELINE PROTECTED.

## Phase 1 — CANONICAL CONNECT
Status: PASS — FIRST REAL E2E REPLAY VERIFIED (2026-08-29).
Evidence: RUNTIME/DECISION_RUNTIME_V1/CHECKPOINT_2026-08-29_GATE1.md; RUNTIME/DECISION_RUNTIME_V1/artifacts/E2E_2016_MANIFEST.json.

## Phase 2 — REAL DECISION REPLAY
Status: PASS FOR AVAILABLE 2016 ARTIFACTS (2026-08-29).
Verified: 401 events; 120 EXECUTABLE; 56 CANDIDATE; 225 NO_TRADE; 120/120 executable events matched the existing filtered execution outcome artifact; no unmatched executable events; no duplicate decision IDs after setup-aware identity fix.
Observed matched-outcome metrics: win rate 56.67%; PF 1.4554; expectancy +0.17286R; total +20.7432R; max DD -11.9262R.
These are 2016 artifact-level results, not the official full-period baseline or a claim of future/live profitability.

## Phase 3 — FULL BRAIN INTEGRATION + TRADE PLAN/RISK
Goal: route a real event through the recovered Decision Brain, governed Three-Book boundary, Risk, and frozen execution-plan adapter.
TIZ policy: TIZ is optional/unverified when unavailable in development/OOS; it remains process-only and direction-neutral. It is not a blocker for decision evaluation and must not be synthetically generated. Risk remains a hard execution gate.
Status: **GATE 3B PASS — EXECUTION ADAPTER ALIGNED; GATE 3C NEXT** (2026-08-29).
Evidence: RUNTIME/DECISION_RUNTIME_V1/full_brain_runtime_bridge_v1.py; OOS_2025/full_decision_brain_assembler_v1.py; RUNTIME/DECISION_RUNTIME_V1/execution_runtime_adapter_v2.py; RUNTIME/DECISION_RUNTIME_V1/test_execution_runtime_adapter_v2.py.
Verified locally: execution adapter compiles; 3/3 TIZ-optional/Risk-hard-gate tests pass. No GitHub Actions workflow was run.
Exit gate: one real pre-2025 snapshot reaches the recovered Decision Brain + Risk + Trade Plan path without bypass.

## Phase 4 — UNIFIED BACKTEST
Development: 2016–2024. OOS: 2025. No 2025 tuning.
Metrics: PF, expectancy, total R, max DD, win rate, trade count, losing streak, cost/slippage/ambiguity sensitivity.

## Phase 5 — PAPER RUNTIME
Same Decision Runtime on live market data with simulated execution.

## Phase 6 — MT5 DEMO EXECUTION
Real demo orders through execution boundary, fill/position tracking, retry/idempotency and broker rejection handling.

## Phase 7 — RECONCILIATION
Brain intent vs order vs fill vs position vs close vs P&L; broker reality authoritative for execution state.

## Phase 8 — n8n OPERATIONS
Triggers, alerts, monitoring, reports, journaling and failure notifications. n8n does not replace the Decision Brain.

## Phase 9 — CONTROLLED LIVE
Only after Backtest -> OOS -> Paper -> Demo -> Reconciliation gates pass; conservative risk and kill-switches.

## Definition of DONE
1. One current market snapshot enters the runtime.
2. All required evidence modules run on that same snapshot/as-of time.
3. Decision Brain outputs a final decision.
4. Risk approves/rejects it.
5. Trade plan is generated for approved trades.
6. Execution layer can hand it to MT5.
7. MT5 outcome is captured and reconciled.
8. Event is journaled for historical outcome/memory.
9. n8n can monitor the lifecycle.

## Progress log
2026-08-29:
- Protected existing project and created isolated build/decision-runtime-v1.
- Closed Gate 1 with a real 2016 GBPUSD integrated event stream.
- Closed Gate 2 for available 2016 artifacts after deterministic setup-aware identity fix and 120/120 reconciliation.
- Added canonical Full Brain bridge.
- Resolved TIZ policy: optional/unverified for development/OOS when no authoritative producer exists; no synthetic psychology; Risk remains hard gate.
- Added execution_runtime_adapter_v2 at the path required by the existing Full Brain assembler.
- Local adapter verification passed 3/3 tests without running GitHub Actions.
- Next: execute the first real Full Brain + Risk + Trade Plan event, then expand to unified 2016–2024 replay.

## Anti-loop rule
No new evaluator, audit, freeze, adapter, or strategy layer may be added unless it directly closes a named gap in this roadmap. After every completed task, record DONE; VERIFIED BY; ARTIFACT; REMAINING; NEXT SINGLE ACTION.
