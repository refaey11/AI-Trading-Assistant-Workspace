# AI Trading Assistant — Execution Integration Plan
Date: 2026-08-30

## Objective
Move the existing Decision Brain project from governed integration proof to a real 2016–2024 profit test, then development freeze, 2025 OOS, and eventually MT5 demo. Do not rebuild the project.

## Protected components
- Murphy 34 governed runtime; no semantic rewrite.
- Nison 44 governed runtime; confirmation/contradiction only.
- Decision Brain V1; source unchanged.
- Historical Context / Historical Outcome / Similarity V2 / Context-Aware Retrieval V2; evidence only and point-in-time.
- TIZ; process/psychology only, never direction.
- Risk/Execution; hard gate; no synthetic SL/TP.
- 2025 remains locked and cannot be used for tuning.

## Proven current state
- CANONICAL_E2E_INTEGRATION_V1 = PASS.
- GOVERNED_INTEGRATION_GATE_V3 = PASS.
- Decision Brain V1 executes.
- Memory/Retrieval do not generate direction.
- 2025 is locked.
- Canonical runner generated 55,192 events.
- Current events include bullish and bearish Brain outputs, so the Brain is executing.
- Risk pass = 0 and trade_allowed = 0 because the runner reports MISSING_UPSTREAM_EXECUTION_INPUT.

## Immediate blocker
Execution inputs are not reaching Risk from an authoritative upstream producer. Required inputs include the project-defined entry / stop / target / ATR / account-state fields. Do not invent these values.

## Execution plan
1. Locate the authoritative existing producer/contract for execution inputs in GitHub and Workspace.
2. Audit its schema against the existing Risk/Execution and RiskResult interfaces.
3. Make the smallest compatibility/wiring change only; do not modify Brain V1 or strategy semantics.
4. Prove one real 2016–2024 event end-to-end: Market -> MTF -> Murphy -> Nison -> Memory -> Handoff -> Brain -> TIZ -> Execution -> Risk.
5. Require Risk to return a real PASS/FAIL when required upstream inputs exist; missing inputs remain NOT_EVALUABLE.
6. Run unit/contract checks and governed integration validation.
7. Only after proof, run the governed 2016–2024 profit test and inspect funnel/P&L.
8. Freeze development before touching 2025 OOS.
9. Only after all gates and OOS proof, move to MT5 demo.

## MTF rule
Use source-backed six-TF Brain inputs (M5/M15/M30/H1/H4/D1). No synthetic timeframe generation, no invented encodings, no zero-fill. Preserve source values for provenance where applicable.

## Preservation rule
Every implementation change must be committed to the governed branch and documented in the master worklog. Never reset main or replace existing project components.

## Current target
The next concrete proof is NOT a large backtest. It is ONE real event reaching Risk with real upstream execution inputs. Once that passes, scale the exact same path to 2016–2024 and calculate the real profit metrics.
