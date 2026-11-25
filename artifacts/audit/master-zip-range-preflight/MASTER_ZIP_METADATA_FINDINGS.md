# Master ZIP metadata findings — 2026-11-24

## Scope and safety
Read-only inspection of `/GBPUSD_M1_MASTER_2016_2026_V1.zip` using Dropbox HTTP byte ranges. Only ZIP directory metadata and the two allowlisted small documentation members were read. The monolithic CSV member was not opened or decompressed. No 2025/2026 candle rows were accessed.

## Archive structure
- Archive size: 43,120,568 bytes.
- ZIP contains exactly three members:
  - `README.md` (364 bytes uncompressed)
  - `VALIDATION_SUMMARY.json` (448 bytes uncompressed)
  - `GBPUSD_M1_MASTER_2016_2026.csv` (307,928,838 bytes uncompressed; DEFLATE)
- The market-data member is one monolithic CSV, not separate per-year members.

## Documentation claims (not independently authenticated)
README states:
- 2016–2019: historical M1, volume unavailable (source volume is zero).
- 2020–2026: Titan FX M1 with non-zero volume.
- Overlaps are deduplicated preferring TitanFX.
- No synthetic candles or gap filling.
- Timezone has not been assumed/converted without source metadata.

VALIDATION_SUMMARY states:
- raw_rows_combined: 5,022,012
- master_rows: 3,908,322
- unique_timestamps: 3,908,322
- duplicate_rows_before_dedup: 742,460
- invalid_ohlc_rows_before_dedup: 0
- missing_ohlc_master: 0
- missing_volume_master: 0
- volume_available_rows: 2,420,041
- volume_unavailable_rows: 1,488,281
- first_timestamp: 2016-01-03 17:00:00
- last_timestamp: 2026-06-30 23:59:00
- gaps_gt_1min: 5,621
- largest_gap_minutes: 4,326

These are archive-supplied assertions and summary counts; they do not independently prove TitanFX acquisition, source identity, timestamp clock semantics, or MTF producer lineage.

## Reconciliation with prior 2020 audit
The standalone HistData 2020 archive previously inspected has zero volume and does not reproduce the MTF volume. The master README's TitanFX claim is consistent with the historical worklog assertion, but targeted Dropbox searches for TitanFX GBPUSD 2020 raw exports, source manifests, and acquisition logs returned no matching files. Therefore TitanFX provenance remains unverified.

## Safe-read decision
The CSV is a single DEFLATE member spanning 2016–2026. There is no per-year member boundary or independent index in the ZIP directory. Extracting 2020 by ordinary streaming decompression would require consuming the compressed stream from its beginning, and chunked range reads could cross into compressed bytes containing later years. Under the current strict rule not to access any 2025/2026 data, do not attempt this extraction without a separately proven byte-level boundary/index that guarantees later-year bytes are not fetched or decompressed.

## Status
- Dropbox range support: verified.
- ZIP central directory: verified.
- Safe documentation extraction and CRC/size checks: passed.
- Master market-data CSV payload: not accessed.
- TitanFX 2020 provenance: unverified.
- 2020 master-vs-MTF source reconciliation: blocked pending independently verifiable source evidence or a safe, exact 2020-only data boundary.
- `main`: untouched; this report is on the isolated audit branch only.
