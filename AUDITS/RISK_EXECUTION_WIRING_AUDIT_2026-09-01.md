# Risk / Execution Wiring Audit — 2026-09-01

## Purpose
Document the first confirmed compatibility defects before any full 2016-2024 replay. No trading-rule semantics are changed by this audit.

## Confirmed defect 1 — RR contract mismatch
- `RUNTIME/DECISION_RUNTIME_V1/execution_runtime_adapter_v2.py` defines the frozen execution plan as `SL_ATR = 0.75` and `TP_R = 2.0`.
- `RUNTIME/RISK_ENGINE_INTEGRATION_V1/test_risk_engine_integration_v1.py` explicitly requires the exact 2.0R boundary to pass and sub-2R to fail.
- `RUNTIME/RISK_ENGINE_INTEGRATION_V1/risk_engine_integration_v1.py` on `main` currently defines `CURRENT_CANONICAL_MIN_RR = 3.0`, which contradicts both the execution adapter and its own tests.
- Dropbox reconciliation checkpoint dated 2026-08-30 records 2.0R as the reconciled frozen candidate execution level and says not to run the full backtest until a real event passes through the reconciled boundary.

## Confirmed defect 2 — current development runner bypasses the Risk Engine contract
- `BACKTEST/DEV_BACKTEST_RUNNER_V1.py` computes `stop_distance = 0.75 * atr` and `tp_distance = 2.0 * stop_distance` inside the runner and simulates outcomes directly.
- The same runner reports `costs_applied = False` and `official_claim_allowed = False`.
- Therefore its current outputs are diagnostic and cannot establish an official profitability result.

## Confirmed defect 3 — Brain input loss risk
The current development runner builds a Brain row with zero defaults for MTF/trend-regime fields and `volume_available=False` unless those fields happen to exist in the context input. The recovered Brain uses those fields to construct directional evidence. This must be traced against the actual upstream MTF/context schema before code is changed.

## Confirmed semantic policy
TIZ `NOT_EVALUABLE` is not itself a development hard block. It must remain visible/unverified while Risk remains the hard execution gate. This is already reflected by `execution_runtime_adapter_v2.py` and by the current project state checkpoints.

## Safe change order
1. Reconcile the RR constant to the existing frozen 2R execution/test contract.
2. Run the Risk integration tests.
3. Trace one real pre-2025 event through Execution -> Risk.
4. Only after that, wire the governed 2016-2024 replay to the existing execution/risk path.
5. Apply frozen costs/slippage and then evaluate profitability.

## Governance
- Do not modify Murphy, Nison, Similarity, Memory, TIZ semantics, or Decision Brain direction logic during this repair.
- Do not tune on 2025.
- Do not synthesize missing evidence to force trades.
