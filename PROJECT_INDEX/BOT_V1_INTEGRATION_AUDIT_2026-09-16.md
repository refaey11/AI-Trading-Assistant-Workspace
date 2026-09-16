# BOT V1 Integration Audit — 2026-09-16

## Purpose
Start the executable Bot V1 workstream without rebuilding the Decision Brain or changing frozen trading semantics.

## Current verified architecture
- Decision Brain V1 recovered source exists at `RECOVERED_SOURCES/DECISION_BRAIN_V1/decision_brain.py`.
- Governed handoff adapter exists at `compatibility/decision_brain_v1_handoff_adapter.py`.
- Governed development backtest runner exists at `BACKTEST/DEV_BACKTEST_RUNNER_V1.py`.
- Execution adapter exists at `BACKTEST/EXECUTABLE_TRADING_ADAPTER_V1.py`.
- Six-timeframe source adapter exists at `BACKTEST/MTF_SIX_TF_SOURCE_ADAPTER_V1.py`.
- Existing ATB V1 backtest results are diagnostic only and explicitly disallow an official profitability claim.

## Critical finding #1 — current runner does not feed Murphy/Nison direction into Brain V1
`BACKTEST/DEV_BACKTEST_RUNNER_V1.py` aggregates `murphy_direction` and `nison_confirmation`, but `build_brain_row()` only copies MTF trend, timeframe trend regimes, and volume fields into the recovered Brain input. The recovered Brain V1 itself derives `directional_bias` from MTF/Structure/Volume (and optional similarity) and does not consume `murphy_direction` or `nison_confirmation` fields.

Therefore the current runner can compare Brain bias against Murphy direction, but it does not prove that the canonical Murphy/Nison directional evidence actually reaches Brain V1. This is a semantic integration gap to investigate, not a reason to invent direction.

## Critical finding #2 — handoff adapter treats TIZ NOT_EVALUABLE as execution-ineligible
`compatibility/decision_brain_v1_handoff_adapter.py` currently adds `TIZ_PROCESS_GATE_NOT_EVALUABLE` to `needs_review`, and `execution_eligible` requires `not needs_review`. The current Gate 3C checkpoint states that TIZ NOT_EVALUABLE was non-authoritative and did not block the tested event. This is a contract mismatch that must be reconciled against the canonical Gate 3C runtime before any change.

## Critical finding #3 — Murphy historical fan-in is incomplete
The 2026-08-27 development checkpoint states that only 7 Murphy rule IDs currently have source-backed historical evidence in the recovered 2016–2024 stream, while the development allowlist contains 34 Murphy + 44 Nison verified runtime rules. The source-preserving recovered slice contains 402,710 rows. The remaining Murphy histories must be recovered/generated from authoritative source material and existing evaluator contracts; no synthetic evidence is allowed.

## Safe execution plan
1. Freeze current successful Gate 3C behavior; do not change Decision Brain V1 source.
2. Trace one successful Gate 3C event from Murphy evidence -> canonical bundle -> handoff adapter -> Brain input.
3. Trace Nison 44/44 evidence -> confirmation mapping -> canonical bundle -> Brain input.
4. Reconcile TIZ NOT_EVALUABLE semantics against the actual canonical runtime contract.
5. Recover/generate source-backed Murphy historical evidence for the remaining development rules.
6. Run the existing governed runner unchanged on 2016–2024 after the evidence fan-in is complete.
7. Apply frozen Risk/Execution and produce the required event/trade/funnel/metrics/validation artifacts.
8. Only after development validation is frozen, run 2025 as locked OOS evaluation.
9. Do not tune on 2025 and do not loosen fail-closed behavior to increase trade count.

## External architecture reference
Current open-source trading frameworks emphasize one event-driven execution model spanning research/backtest/live, with explicit risk/execution layers and minimized backtest/live divergence. NautilusTrader documents this design directly. Walk-forward tooling likewise emphasizes untouched chronological OOS evaluation and explicit overfitting checks.

## Status
`BOT_V1_INTEGRATION_STARTED`

No trading logic, frozen rules, 2025 data, or Decision Brain source was modified by this audit.
