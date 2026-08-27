# Development Backtest Runner Plan V1

Status: IMPLEMENTATION STARTED

Development window: 2016-2024 only.
OOS 2025 remains locked and is not used for tuning.

Objective
Execute the current governed Decision Brain on historical development data without rebuilding or changing existing rule semantics.

Pipeline
1. Read authoritative GBPUSD H1 source.
2. Join currently available Murphy evidence, Nison evidence, MTF evidence, Historical Context Memory, Historical Outcome Memory, Similarity Memory metadata, Context-Aware Retrieval metadata, and TIZ process context by timestamp/as-of.
3. Pass market context into the recovered Decision Brain V1 assessment unchanged.
4. Apply the existing Three-Book Decision evaluator and frozen Risk/Execution contract.
5. Record every eligible/rejected event and the exact rejection reason.
6. For executable trades, apply the frozen SL/TP, position-size, cost/slippage and bar-by-bar outcome contract already present in the repository.
7. Produce development metrics only after timestamp/lookahead, MTF consumption, memory availability, execution-funnel, and cost checks pass.

Non-negotiable governance
- Murphy may provide directional context.
- Nison provides confirmation/contradiction, not independent direction.
- Similarity/Memory never generates direction.
- TIZ is process/psychology context only.
- Risk is a hard execution gate.
- 2025 cannot be used for calibration/tuning.
- Do not substitute legacy 2016-2018 backtest artifacts for the current 78-rule evaluation.

Required outputs
- unified_78_events_2016_2024.csv
- decision_events_2016_2024.csv
- executed_trades_2016_2024.csv
- execution_funnel_2016_2024.json
- backtest_metrics_2016_2024.json
- validation_manifest_2016_2024.json

Acceptance gate
No profitability claim is valid unless the validation manifest records PASS for timestamp/as-of, lookahead, MTF consumption, memory leakage, execution funnel, and frozen cost/slippage application.
