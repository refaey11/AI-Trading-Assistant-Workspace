# AI Trading Assistant — 2026-08-27 Development Run Started

## Locked truth
- Do not rebuild existing subsystems.
- Murphy: 34 governed rules existing.
- Nison: 44 governed rules existing.
- Governed package: 78 = 34 + 44.
- Similarity / Historical Memory = evidence only; never direction generation.
- Trading in the Zone = process/psychology gate only.
- 2025 remains OOS-LOCKED and is not used for tuning.

## Current execution target
Recover and validate the source-backed 2016-2024 development evidence using the existing runtimes, then continue toward the unified Decision Brain -> Risk/Execution -> Backtest path.

## Work started in this checkpoint
- Added `DEVELOPMENT_2016_2024/run_nison_development_2016_2024_v1.py`.
- The runner reuses the existing generic Nison historical runtime and the authoritative Dropbox `GBPUSD_H1_2016_2025_MASTER.zip` source.
- The runner is restricted to development years 2016-2024 and emits all 44 governed Nison rule rows per input H1 bar for each year.
- No new rule semantics, fabricated evidence, or 2025 tuning are introduced.
- Added GitHub Actions workflow `.github/workflows/development-nison-2016-2024.yml` to execute the development recovery and store the resulting artifacts.

## Next exact step
1. Verify the development Nison recovery job completes successfully.
2. Use the recovered 2016-2024 Nison evidence alongside the existing Murphy/runtime artifacts.
3. Assemble the unified 78-rule development Decision Events with MTF and memory evidence as evidence-only.
4. Run the real execution/backtest funnel and record trades, win rate, profit factor, expectancy, total R/P&L, and max drawdown.
5. Freeze development results before any 2025 OOS evaluation.

## Anti-loop rule
Do not return to rebuilding Murphy, Nison, Similarity, Memory, or the 78-rule package from scratch.
