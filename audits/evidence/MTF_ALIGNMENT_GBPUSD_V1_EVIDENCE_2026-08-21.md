# Evidence Pack — MTF Alignment GBPUSD V1

**Date:** 2026-08-21
**Purpose:** Raw/source-derived evidence supporting the MTF Alignment gate checkpoint.

## Evidence source A — README.json from reconstructed archive

Source archive metadata states:
- version: V1
- asset: GBPUSD
- base_timeframe: M5
- aligned_timeframes: M5, M15, M30, H1, H4, D1
- status: complete_2016_2026
- purpose: Market Intelligence / Market Reading, not a strategy or indicator
- anti_leakage: Higher-timeframe features are joined only after source candle close
- next: Volume + volatility evidence, then Historical Similarity / Memory

This is direct source metadata from the reconstructed MTF archive.

## Evidence source B — FINAL_MANIFEST.csv

The manifest lists 11 annual files:

| Year | File | Rows | From | To |
|---|---|---:|---|---|
| 2016 | GBPUSD_M5_MTF_ALIGNMENT_2016.csv | 74677 | 2016-01-03 17:00:00 | 2016-12-30 16:55:00 |
| 2017 | GBPUSD_M5_MTF_ALIGNMENT_2017.csv | 74478 | 2017-01-02 02:00:00 | 2017-12-29 16:55:00 |
| 2018 | GBPUSD_M5_MTF_ALIGNMENT_2018.csv | 74696 | 2018-01-01 17:00:00 | 2018-12-31 16:55:00 |
| 2019 | GBPUSD_M5_MTF_ALIGNMENT_2019.csv | 74473 | 2019-01-01 00:00:00 | 2019-12-31 23:55:00 |
| 2020 | GBPUSD_M5_MTF_ALIGNMENT_2020.csv | 74681 | 2020-01-01 00:00:00 | 2020-12-31 23:55:00 |
| 2021 | GBPUSD_M5_MTF_ALIGNMENT_2021.csv | 74573 | 2021-01-01 00:00:00 | 2021-12-31 23:50:00 |
| 2022 | GBPUSD_M5_MTF_ALIGNMENT_2022.csv | 74523 | 2022-01-03 00:00:00 | 2022-12-30 23:50:00 |
| 2023 | GBPUSD_M5_MTF_ALIGNMENT_2023.csv | 74496 | 2023-01-02 00:00:00 | 2023-12-29 23:50:00 |
| 2024 | GBPUSD_M5_MTF_ALIGNMENT_2024.csv | 74825 | 2024-01-01 00:00:00 | 2024-12-31 23:55:00 |
| 2025 | GBPUSD_M5_MTF_ALIGNMENT_2025.csv | 74684 | 2025-01-01 00:00:00 | 2025-12-31 23:55:00 |
| 2026 | GBPUSD_M5_MTF_ALIGNMENT_2026.csv | source artifact present; partial year | 2026-01-01 00:00:00 | 2026-06-30 23:55:00 |

Note: 2026 row count was not used as a gate criterion in this evidence pack. The gate development/QA window remains 2016–2024.

## Evidence source C — Direct CSV schema inspection

Direct inspection of extracted annual CSV files (2017, 2018, 2020, 2022, 2026) found a 106-column schema containing the six explicit prefixes:

- M5_
- M15_
- M30_
- H1_
- H4_
- D1_

Representative per-timeframe fields include:
- trend_regime
- pivot_high
- pivot_low
- break_structure_up
- break_structure_down
- dist_pivot_high
- dist_pivot_low
- dist_resistance_20
- dist_support_20
- dist_resistance_50
- dist_support_50
- doji
- hammer_like
- shooting_star_like
- bullish_engulfing
- bearish_engulfing

Aggregate MTF fields directly present in the inspected schema:
- mtf_trend_score
- mtf_bullish_count
- mtf_bearish_count
- mtf_neutral_count
- mtf_context
- higher_tf_bullish_breaks
- higher_tf_bearish_breaks
- higher_tf_bullish_candles
- higher_tf_bearish_candles

## Evidence interpretation

PASS for existence/structure of the six-timeframe MTF input artifact is supported by the source README, annual manifest, and direct CSV schema inspection.

The anti-leakage statement is source metadata: higher-timeframe features are joined only after source candle close. Downstream runtime tests must preserve this boundary and should independently test AS-OF behavior at their own input boundary.

This evidence pack does NOT claim that every downstream reader has already passed runtime testing. It only supports closing the repeated question of whether the GBPUSD MTF Alignment input artifact exists and is structurally six-timeframe aligned.

## Official gate conclusion

**MTF Alignment GBPUSD V1 = PASS / EXISTING EVIDENCED INPUT ARTIFACT**

Next gate: **Market State / Market Reader standalone runtime test on the existing aligned artifact, using 2016–2024 only.**
