# Decision Brain — 2025 OOS Performance Audit

Date: 2026-08-22
Status: BLOCKED / NOT RUN

## Finding
The existing `TRUE_BACKTEST_V2` artifact is not accepted as the performance test of the frozen Decision Brain V1.

Reason 1: `DECISION_BRAIN_V1_SPEC.json` defines V1 as a structured market-state assessment and explicitly states no automatic BUY/SELL execution in V1.

Reason 2: `TRUE_BACKTEST_V2` contains a separate V2/V3 trading-engine backtest with its own signal/SL/TP configuration and states that costs were not yet applied. Those results cannot be attributed to the frozen Decision Brain V1.

Reason 3: The current Decision Brain V1 source contains legacy Similarity `predicted_return` directional behavior. The governed handoff adapter explicitly prevents that memory field from generating direction. Therefore the legacy source cannot be treated as an unchanged executable strategy for OOS profitability.

## OOS integrity rule
2025 may be evaluated only after a frozen Decision Brain-to-rule/execution evaluation path exists. During that evaluation:
- no 2025 tuning
- no threshold selection on 2025
- no calibration on 2025
- no implementation selection on 2025
- no future-data access
- historical/similarity memory remains evidence-only

## Accepted next step
Connect the frozen Decision Brain output to an existing Rule/Execution Evaluation contract without modifying the frozen Brain, then run the 2025 OOS evaluator for the first time.

## Explicitly not accepted as OOS proof
- TRUE_BACKTEST_V2 aggregate results
- old V2/V3 threshold searches
- any result with costs not applied
- any result whose signal logic differs from the frozen Decision Brain path
