# CHECKPOINT — GATE 2 REAL DECISION REPLAY
Date: 2026-08-29

## DONE
- Gate 1 E2E event stream replay preserved: 401 GBPUSD events for 2016.
- Fixed deterministic event identity bug: timestamp alone was not unique when multiple setups occurred on the same bar; setup_id is now included in the identity hash.
- Re-ran the real 2016 replay successfully.
- All 120 EXECUTABLE decision events matched an existing execution outcome artifact.
- No unmatched executable events remain.
- Chronological ordering verified.
- No duplicate decision IDs remain.
- No new strategy semantics introduced.
- 2025 remained untouched for tuning.

## VERIFIED RESULT
- Decision events: 401
- EXECUTABLE: 120
- CANDIDATE: 56
- NO_TRADE: 225
- BUY: 70
- SELL: 106
- Matched executable outcomes: 120/120
- Win rate on matched executable outcomes: 56.67%
- Profit factor: 1.4554
- Expectancy: +0.17286R
- Total: +20.7432R
- Max drawdown: -11.9262R

## IMPORTANT INTERPRETATION
This is a real integrated replay result for the available 2016 project artifacts. It is not yet the official full-period baseline, not a proof of future profitability, and not a live-trading result.

## ARTIFACTS
- `e2e_artifact_runtime.py` — corrected deterministic event identity.
- `artifacts/GATE2_2016_REPLAY_SUMMARY.json` — replay metrics.
- `artifacts/GBPUSD_2016_E2E_DECISION_EVENTS.csv` — integrated event stream.
- `artifacts/GBPUSD_2016_E2E_EXECUTABLE_OUTCOMES.csv` — executable events reconciled to existing outcomes.

## REMAINING
- Extend the same canonical path across the available development period (2016–2024) using the existing governed artifacts.
- Then run the frozen OOS 2025 verification.

## NEXT SINGLE ACTION
Build the full 2016–2024 canonical replay on the same runtime semantics, without tuning.
