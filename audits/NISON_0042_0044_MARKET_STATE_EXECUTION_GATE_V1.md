# Nison 0042–0044 Market State Execution Gate V1

Date: 2026-08-17
Dataset: existing GBPUSD_MARKET_STATE.csv from MARKET_STATE_READER_V1
Evaluation period: 2016-01-03 through 2024-12-31
2025 rows consumed: 0
Rows evaluated: 55,192

## 0042 — Support/Resistance
The existing Market State artifact exposes `location` with NEAR_SUPPORT / NEAR_RESISTANCE and exposes candle evidence flags. A compatibility scan found 2,790 rows where location and a directional candle flag coexist:
- NEAR_SUPPORT + (bull_engulf or hammer)
- NEAR_RESISTANCE + (bear_engulf or shooting_star)

These are compatibility candidates, NOT Nison PASS counts, because the current artifact does not expose provenance proving that each candle flag was produced by the canonical Nison pattern evaluator, nor does it expose a unique S/R zone_id. Therefore the adapter must keep these as CANDIDATE rather than PASS until canonical provenance is attached.

## 0043 — False Breakouts
The artifact exposes BREAKOUT_UP / BREAKOUT_DOWN, but no explicit failed-breakout / return-inside-range event. No PASS count is emitted.
Verdict: NOT_EVALUABLE.

## 0044 — Polarity
The artifact exposes BREAKOUT_UP / BREAKOUT_DOWN, but no explicit successful-retest / polarity-transition event. No PASS count is emitted.
Verdict: NOT_EVALUABLE.

## 2025 isolation
The source file contains 2025 rows, but the execution gate explicitly filtered them out. No 2025 row was consumed for candidate selection, tuning, calibration, or threshold selection.

## Verdict
0042: CANDIDATE-READY, NOT FROZEN
0043: NOT_EVALUABLE
0044: NOT_EVALUABLE

Next required artifact is provenance-bearing canonical S/R zone evidence plus explicit failed-breakout/return and successful-retest events. No new market-structure engine should be created merely to make these rules evaluable.
