# AI Trading Assistant — Decision Brain
## Final 2025 Evaluation Start — 2026-08-25

### Gate status before final evaluation
- Nison 2025 production: PASS
- Murphy 0021 fresh 2025: PASS
- Murphy 0022/0023 PIT 2025: PASS
- 78-rule coverage: PASS
- Decision Brain integration: PASS
- Final E2E readiness: PASS
- Risk execution runtime: PASS
- Three-Book evaluator: PASS
- TIZ optional execution adapter: PASS
- Memory/integration and rule allowlist gates: PASS

### Final evaluation objective
Run the authoritative 2025 OOS inputs through the existing governed Full Decision Brain path, then evaluate execution eligibility and only afterward promote an official profitability result if the existing profitability-readiness gate is satisfied.

### Governance preserved
- 2025 is evaluation-only; no tuning or threshold selection.
- Existing project knowledge and frozen contracts are reused.
- Murphy is the direction source.
- Nison is confirmation/context and contradiction handling only.
- Trading in the Zone is a process/psychology gate and never a direction generator.
- Historical memory is evidence only and never the sole direction source.
- Missing evidence remains NOT_EVALUABLE.
- No profitability number is promoted merely from coverage or eligibility output.

### Final-event producer already present
`OOS_2025/full_decision_brain_historical_event_producer_v1.py`

This producer requires governed context, Murphy, Nison, risk and execution inputs and emits `FINAL_2025_DECISION_EVENTS.csv` plus a manifest.

### Final-evaluation producer already present
`OOS_2025/run_final_2025_full_evaluation_v1.py`

It constructs fresh 2025 Murphy 0021 and 0022/0023 evidence, builds the governed 78-rule event stream, builds context/risk evidence, runs the existing Full Decision Brain producer, and emits core profitability eligibility output. It explicitly records `profit_number_promoted: false` until a governed outcome/backtest artifact exists.

### Current execution note
The existing CircleCI `.circleci/config.yml` currently runs the production/coverage jobs but does not yet define a dedicated final Decision Brain profitability job. Therefore this checkpoint records the final-evaluation start and required wiring; it does NOT claim that the final P&L run has completed.

### Next execution step
Add a dedicated CircleCI final-evaluation job that uses the existing `DROPBOX_ACCESS_TOKEN`, acquires the authoritative H1/M1/market-state inputs, runs `run_final_2025_full_evaluation_v1.py`, stores the generated Decision Brain events, manifests and core profitability eligibility artifacts, and then runs the existing governed profitability/backtest path. No strategy changes are allowed during this step.
