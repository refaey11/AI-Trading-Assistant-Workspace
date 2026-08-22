# GBPUSD Volume Source Audit — 2020-2024

## Finding
The project contains a derived GBPUSD MTF test dataset covering 2020-01-02 through 2024-12-31. The M5, M15, M30, H1, and H4 files all carry a `volume` field with positive values and identify their source as `M1_TitanFX_2020_2024`.

## Verified local artifacts
- `mtf_test2/M5.csv`: 373,465 rows; 2020-01-02 00:00 through 2024-12-31 23:55; all sampled/checked volume values are positive; source_timeframe=`M1_TitanFX_2020_2024`.
- `mtf_test2/M15.csv`: 124,764 rows; 2020-01-02 00:00 through 2024-12-31 23:45; volume present; source_timeframe=`M1_TitanFX_2020_2024`.
- `mtf_test2/M30.csv`: 62,513 rows; 2020-01-02 00:00 through 2024-12-31 23:30; volume present; source_timeframe=`M1_TitanFX_2020_2024`.
- `mtf_test2/H1.csv`: 31,385 rows; 2020-01-02 00:00 through 2024-12-31 23:00; volume present; source_timeframe=`M1_TitanFX_2020_2024`.
- `mtf_test2/H4.csv`: 8,039 rows; 2020-01-02 00:00 through 2024-12-31 20:00; volume present; source_timeframe=`M1_TitanFX_2020_2024`.

## Semantic interpretation
This confirms the project's statement that a separate 2020-2024 M1/TitanFX-derived pipeline supplies volume to M5+ derived bars. This is distinct from the uploaded 2025 HistData file, whose source volume column is zero throughout.

No synthetic volume was created. No rule, threshold, or 2025 data was modified.

## Consequence for OOS
The 2020-2024 volume source is suitable for development/context auditing. It does not by itself solve the 2025 OOS volume problem. A 2025 volume source with equivalent provenance is still required if volume is to be treated as usable evidence in the frozen 2025 stream.

## Next gate
Audit the existing 2020-2024 volume producer/contract and determine whether an authoritative 2025 continuation exists. Keep the raw 2025 HistData volume unchanged and treat it as unavailable unless a separate authoritative source is identified.