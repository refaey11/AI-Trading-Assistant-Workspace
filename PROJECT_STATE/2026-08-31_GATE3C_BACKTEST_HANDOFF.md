# AI Trading Assistant — Decision Brain
## Project State / Handoff — 2026-08-31

### Current verified state
- Gate 3C bounded event discovery completed successfully.
- GitHub Actions run: `33352436711`.
- Discover job: `99368252868`.
- The job conclusion is `success`.
- The full `Brain -> Risk -> Trade Plan E2E` step completed successfully.
- Result artifact `gate3c-auto-discovery-result` was uploaded successfully.
- A valid event was discovered at `2024-12-31T16:00:00Z`.
- Earlier failures encountered during development included Dropbox 401/409 responses, timestamp/H1 mismatch, and an unbounded event search that was cancelled after ~20 minutes. These are historical debugging events, not current Gate 3C failures.

### Current Gate 3C interpretation
- Gate 3C single-event operational E2E is working.
- The discovered event produced a valid pipeline execution; `NO_TRADE` is an allowed decision and is not itself a pipeline failure.
- Nison `NOT_EVALUABLE` observations must not trigger rule rewriting or tuning. They are to be interpreted through the existing governed contracts and available source facts.

### Existing backtest implementation found
- Official development runner already exists at `BACKTEST/DEV_BACKTEST_RUNNER_V1.py`.
- Official plan already exists at `BACKTEST/DEV_BACKTEST_RUNNER_PLAN_V1.md`.
- Development window is strictly `2016-2024`.
- 2025 remains locked as OOS and must not be used for calibration/tuning.
- The plan requires joining authoritative H1, Murphy, Nison, MTF, Historical Context Memory, Historical Outcome Memory, Similarity metadata, Context-Aware Retrieval metadata and TIZ context, then applying the current Decision Brain and frozen Risk/Execution contract.
- Required development outputs: `unified_78_events_2016_2024.csv`, `decision_events_2016_2024.csv`, `executed_trades_2016_2024.csv`, `execution_funnel_2016_2024.json`, `backtest_metrics_2016_2024.json`, `validation_manifest_2016_2024.json`.
- No profitability claim is allowed unless timestamp/as-of, lookahead, MTF consumption, memory leakage, execution funnel, and frozen cost/slippage checks pass.

### Governance / non-negotiables
- Do not rebuild existing project components.
- Murphy provides directional context.
- Nison provides confirmation/contradiction, not independent direction.
- Similarity/Memory is historical evidence only and never generates direction.
- TIZ is process/psychology context only.
- Risk is a hard execution gate.
- 2025 OOS is never used for tuning.
- Do not substitute legacy backtest artifacts for the current governed 78-rule evaluation.

### Next action
Run the existing governed development backtest for `2016-2024` using authoritative sources. Do not create a parallel backtest implementation unless the existing runner is proven unusable. Review the validation manifest first; only after a clean validation gate should the project move to freeze and then 2025 OOS.

### Important correction to avoid future confusion
A prior exploratory runner/launcher was identified as potentially diagnostic rather than official because it explicitly marks profitability claims as not allowed and uses a simplified execution model. Do not treat its metrics as official project performance. Use the existing governed backtest path and its acceptance gate.
