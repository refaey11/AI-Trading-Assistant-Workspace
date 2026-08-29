# AI Trading Assistant — Decision Brain Execution Integration Audit

Date: 2026-08-29
Branch: governed-backtest-final-2026-08-29
Commit baseline: b552e611290ca8757de17e5cbb612abada54bcf8
Status: INTEGRATION AUDIT IN PROGRESS — NO OFFICIAL PROFITABILITY CLAIM

## Canonical project invariants
- Project is an AI Trading Assistant / Decision Brain, not a trading indicator.
- Murphy = technical context / directional context.
- Nison = confirmation / contradiction only; never independent direction.
- Trading in the Zone = process / psychology gate only; never direction.
- Historical / Similarity / Retrieval = evidence only; never direction or tuning.
- Risk = hard execution gate.
- Decision Brain V1 source remains unchanged.
- 2025 = OOS and LOCKED; no tuning, calibration, or optimization may use it.
- Missing evidence remains NOT_EVALUABLE / fail-closed.
- No semantic changes may be introduced merely to increase trade count.

## Current verified six-timeframe state
The project uses the six native timeframes:
M5, M15, M30, H1, H4, D1.
The current workstream preserves these six timeframes. The audit distinguishes between:
1. availability of six-timeframe source evidence, and
2. a frozen, source-backed transformation contract from those features into Decision Brain V1 numeric inputs.
The latter must not be invented.

## Current findings
### 1. CI / runner wiring
The recent CI repair work fixed trigger routing, stale 2025 assertion output, V4 wrapper recursion, and runner compatibility issues. CI success is not treated as proof of strategy profitability.

### 2. Decision events versus execution backtest
The prior governed run produced decision_events_2016_2024.csv but no executed_trades_2016_2024.csv. This proved that the current path can compile/replay decision events but did not by itself prove a valid execution/PnL path.

### 3. V4 compatibility wrapper
V4 now preserves multi-row Murphy/Nison evidence and calls the original V3 brain-row helper through a saved reference, avoiding recursion. Compatibility normalization must remain schema-only and cannot change rule semantics.

### 4. Six-timeframe Brain interface gap
Decision Brain V1 consumes mtf_trend_score plus six trend-regime fields. The current canonical MTF evidence establishes the six timeframes, but the exact authoritative feature-to-Brain numeric transformation is not fully frozen in the reviewed contract. Guessing weights/formulas would be a strategy change and is therefore blocked.

### 5. Murphy historical eligibility gap
The runtime allowlist contains 34 Murphy rules, but the current Murphy fan-in governance manifest identifies only 7 as decision-eligible historical directional evidence in the reviewed 2016-2024 recovery. The remaining rules retain their source-backed governance classifications (context/candidate/process/NOT_EVALUABLE/etc.) and must not be promoted without authoritative evidence.

### 6. Execution contract gap
The Risk Engine requires upstream numeric SL, TP, and ATR inputs. It does not invent SL/TP. The canonical integration plan explicitly rejects using the current runner's 0.75 ATR / 3R construction as an official execution method unless that convention is proven to be the project's frozen upstream execution contract.

### 7. Memory / Retrieval / TIZ boundaries
Current implementation notes identify remaining gaps around true timestamp/as-of consumption for Similarity V2 and Context-Aware Retrieval V2, true Historical Outcome as-of evidence, and the TIZ process boundary. Snapshot/presence metadata is not enough for an official E2E claim.

## Required engineering sequence
1. Trace the authoritative six-timeframe source artifacts and their existing mapping/binding policy into the Decision Brain interface. Do not invent transformation math.
2. Reconcile Murphy 34 runtime scope against source-backed 2016-2024 decision eligibility. Missing historical evidence stays NOT_EVALUABLE.
3. Trace the existing upstream execution contract for SL/TP/ATR, position sizing, cost, slippage, and bar-by-bar outcome. Do not reuse an unverified legacy convention as canonical.
4. Prove a deterministic real-source sample through: MTF → Murphy → Nison → memory/retrieval → TIZ boundary → Handoff → Decision Brain V1 → Risk → Execution.
5. Only after that real-source sample passes, run exactly one governed 2016-2024 development backtest.
6. 2025 remains locked and excluded from all tuning/calibration.

## Explicit non-actions
- Do not rebuild book knowledge.
- Do not modify Decision Brain V1 semantics.
- Do not manufacture evidence.
- Do not loosen gates to create trades.
- Do not substitute legacy profitability artifacts for the current governed 78-rule result.
- Do not claim profitability until timestamp/as-of, lookahead, MTF consumption, memory leakage, execution funnel, and frozen cost/slippage checks are proven.

## Current decision
FULL CANONICAL PROFITABILITY BACKTEST = BLOCKED pending closure of the above compatibility/execution evidence gaps.
This is an engineering integration status, not a statement that the strategy is profitable or unprofitable.
