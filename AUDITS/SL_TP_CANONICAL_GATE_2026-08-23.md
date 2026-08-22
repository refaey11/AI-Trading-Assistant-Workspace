# SL/TP Canonical Gate — 2026-08-23

## Finding
The project contains a frozen **candidate baseline execution protocol** for Similarity Engine V2 + 4H:
- threshold: 0.52
- SL: 0.75 ATR
- RR / TP: 2.0R

Source evidence: `UNIFORM_OOS_AGGREGATION_V1.json` and `OFFICIAL_BASELINE_EXECUTION_GATE_V1.json`.

## Important boundary
This protocol is **frozen for the candidate baseline execution gate**, but the V2 + 4H baseline is still **NOT OFFICIAL** until the required uniform end-to-end walk-forward and leakage audit pass.

Therefore:
- Do NOT use the older TRUE_BACKTEST_V2 mechanical config (1x H1 ATR / 1.5R) as the canonical candidate baseline.
- Do NOT tune SL/TP on 2025.
- Do NOT claim the stored 2025 aggregation as a fresh OOS result.
- Use the candidate frozen protocol consistently for the official walk-forward when the full raw-data execution path is available.

## Next gate
Run one fresh, identical protocol across all five assets:
- Calibration 2016–2023 -> OOS 2024
- Calibration 2016–2024 -> OOS 2025
- same signal, threshold, SL/TP, ambiguity policy, and costs
- no OOS tuning
- leakage/availability audit

## Current status
SL/TP canonical candidate = **0.75 ATR stop + 2R target**.
Official baseline status = **NOT YET FROZEN**.
