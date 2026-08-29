# Risk / Execution Contract Reconciliation — 2026-08-29

## Decision
The canonical minimum reward:risk requirement remains **3:1**.

## Source-backed basis
- The Master Knowledge Base Murphy Chapter 16 source states that the risk/reward ratio must be at least 3:1.
- The current `RUNTIME/RISK_ENGINE_INTEGRATION_V1/risk_engine_integration_v1.py` already encoded `CURRENT_CANONICAL_MIN_RR = 3.0` and described it as the current project Decision Contract.
- The older `RISK_ENGINE_SPEC_V1.json` describes a 1.5R research prototype and is not the final execution contract.
- Historical P&L/evaluator evidence used a 2R target. That is preserved as legacy/observed execution behavior and is not promoted over the source-backed Murphy contract.

## Build_59 failures reconciled
### RiskResult API
Build_59 expected `stop_loss` and `take_profit`, while the active integration `RiskResult` exposed only `risk_pass`, `risk_percent`, `stop_distance`, `rr`, `position_size`, and `reason`.

Resolution: add `stop_loss` and `take_profit` to `RiskResult` while preserving every existing field and behavior.

### Exact 3R boundary
Build_59 produced `rr = 2.999999999999852` for the mathematically exact 3R example and rejected it with `RR_BELOW_CURRENT_CANONICAL_MINIMUM`.

Resolution: preserve the 3.0R threshold and permit only a negligible IEEE-754 representation error using absolute tolerance `1e-12`. Materially sub-3R values still fail.

## Guardrails
- No Murphy rule changes.
- No Nison rule changes.
- No Decision Brain V1 changes.
- No Memory/Retrieval changes.
- No 2025 changes.
- No new SL/TP generation logic.
- No backtest promotion from this repair alone.

## Verification
The exact build_59 values now produce:
- `rr = 2.999999999999852`
- `risk_pass = True`
- `reason = RISK_GATE_PASS`
- original `stop_loss` and `take_profit` preserved on `RiskResult`

A materially lower target (`take_profit = 1.2544` for entry 1.25 / stop 1.2485) still returns `RR_BELOW_CURRENT_CANONICAL_MINIMUM`.

Next governance step: run the governed integration gate on the corrected branch. Do not run the expensive 2016–2024 backtest until that gate passes.
