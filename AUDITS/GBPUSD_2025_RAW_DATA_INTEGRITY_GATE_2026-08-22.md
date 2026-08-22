# GBPUSD 2025 Raw Data Integrity Gate — 2026-08-22

## Source
- Uploaded artifact: `HISTDATA_COM_MT_GBPUSD_M12025.zip`
- Local SHA-256 of uploaded ZIP: `0ead9b4df326b5248bea59f1ad09878e8240227f36d250d1f17a3252af9d11fc`
- ZIP entries:
  - `DAT_MT_GBPUSD_M1_2025.csv`
  - `DAT_MT_GBPUSD_M1_2025.txt`

## Parsed CSV integrity
- Rows: 371,091
- First timestamp: 2025-01-01T17:01:00Z
- Last timestamp: 2025-12-31T16:57:00Z
- Invalid timestamps: 0
- Duplicate timestamp groups: 60
- Rows participating in duplicate timestamp groups: 120
- Non-positive OHLC values: 0
- High < Low rows: 0
- OHLC consistency violations: 0
- Provided volume values equal to zero: 371,091 / 371,091

## Source status-report observations
- The companion `.txt` reports 2,535 timestamp gaps.
- Reported gap sizes range from 60 seconds to 3,594 seconds.
- These gaps are preserved as source-quality metadata; no synthetic bars are inserted at this gate.

## Important interpretation
- Duplicate timestamps are preserved as a source-quality finding. No rows were silently deduplicated.
- The source volume column is entirely zero. It is therefore **not treated as usable volume evidence** for the OOS stream unless an existing project contract explicitly maps this field to a valid volume interpretation.
- No 2025 tuning, threshold selection, calibration, or implementation selection was performed.
- No trading result was calculated from this gate alone.

## Gate result
`RAW_DATA_SOURCE_VALIDATED_WITH_WARNINGS`

The OHLC data is structurally valid, but the duplicate timestamp block, source-reported gaps, and zero-volume condition must be resolved by the existing source-derived feature/market-state contracts before a final frozen decision-event stream is accepted.

## Next gate
Use the existing project preprocessing/Market-State/MTF contracts to establish the authoritative timestamp handling and volume-availability semantics without inventing new rules. Do not alter the raw 2025 file, and do not create synthetic volume. Only after that may the 2025 stream proceed to the frozen 78-rule Decision Brain evaluation path.
