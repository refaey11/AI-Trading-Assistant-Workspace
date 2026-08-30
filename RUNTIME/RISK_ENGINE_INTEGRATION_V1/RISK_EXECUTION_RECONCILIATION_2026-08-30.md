# Risk / Execution Reconciliation — 2026-08-30

## Source-of-truth finding
- Recovered `RISK_ENGINE_SPEC_V1.json` in Dropbox defines `1.5R` as a **research prototype** target only.
- Existing frozen execution adapter defines `0.75 ATR` stop and **2R target**.
- `CHECKPOINT_2026-08-29_GATE3_BRIDGE.md` explicitly records the 0.75 ATR / 2R levels as the frozen candidate execution levels.
- The previously added `CURRENT_CANONICAL_MIN_RR = 3.0` in the integration wrapper is not supported by the recovered Risk Engine specification; it created the 2R-vs-3R contract mismatch.

## Reconciliation
The active Risk integration boundary is now aligned to **2.0R minimum RR**. Exact-boundary comparison uses a very small tolerance so binary floating-point representation cannot reject a mathematically exact 2R trade.

`RiskResult` now exposes `stop_loss` and `take_profit` as optional fields so the existing downstream evaluator/execution boundary can consume the validated levels without an API mismatch.

## Protected components
No changes to Murphy, Nison, Decision Brain V1, historical memory/retrieval semantics, TIZ direction boundary, or 2025 OOS governance.

## Validation added
- Exact 2R case must PASS.
- Sub-2R case must FAIL with `RR_BELOW_CURRENT_CANONICAL_MINIMUM`.

## Next gate
Run the narrow risk/contract tests and then a single real pre-2025 Gate 3C event. Do not start the full 2016–2024 profit replay until the single-event path is proven end-to-end.
