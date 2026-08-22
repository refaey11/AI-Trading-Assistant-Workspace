# Market / MTF Standalone Compatibility Audit — 2026-08-22

## Scope
Audit the existing Market Reader V1, Market State Reader V1, and Market Scenario Engine V1 artifacts before any new integration or rebuild.

## Source artifacts reviewed
- `AI_Trading_Assistant_MARKET_READER_V1.zip`
  - `MARKET_READER_ARCHITECTURE.json`
  - `MARKET_READER_SCHEMA.md`
  - `MARKET_READING_OUTPUT_TEMPLATE.json`
  - `FLOW.md`
  - `BUILD_ROADMAP.md`
- `AI_Trading_Assistant_MARKET_STATE_READER_V1.zip`
  - `CONTRACT.json`
  - `STATE_READER_COVERAGE.csv`
  - five symbol market-state datasets
  - `LATEST_MARKET_READINGS.json`
- `AI_Trading_Assistant_MARKET_SCENARIO_ENGINE_V1.zip`
  - `SCENARIO_SUMMARY.csv`
  - `MARKET_SCENARIOS.json`
- Recovered six-timeframe source data used by the project's MTF alignment evidence (`M5/M15/M30/H1/H4/D1`, 2020-2024).

## Verified data observations (development window only)
2025 was excluded from this audit.

The five Market State datasets are timestamp-ordered and contain no duplicate timestamps in 2016-01 through 2024-12:
- EURUSD: 55,210 rows
- GBPUSD: 55,192 rows
- USDJPY: 55,191 rows
- USDCAD: 55,195 rows
- XAUUSD: 52,599 rows

All required contract fields are present in the pre-2025 rows.

The EMA20/EMA50/EMA200 columns exactly reproduce a causal pandas EWM(span=N, adjust=False) calculation from the close series within floating-point precision for all five symbols.

Trend-state internal consistency checked against EMA ordering:
- all `BULL_TREND` rows satisfy EMA20 > EMA50 > EMA200;
- all `BEAR_TREND` rows satisfy EMA20 < EMA50 < EMA200;
- no violations were observed in the audited 2016-2024 rows.

## Critical dependency gap
The Market Reader V1 archive contains architecture/schema/flow documentation but no executable Market Reader runtime implementation.

The Market State Reader archive contains precomputed state datasets and a reading contract, but no executable runtime module was present in the archive.

The Market Scenario Engine archive contains precomputed scenario outputs and documentation, but no executable runtime module was present in the archive.

Therefore these artifacts must not be labeled Runtime/CI Verified merely from the presence of datasets or documentation.

## Corrected volume data boundary
The earlier audit statement that volume was unavailable across the whole development window was too broad and is corrected here.

The supplied Market State Reader datasets themselves contain zero/blank volume fields. Separately, the recovered six-timeframe source data used for MTF alignment contains explicit nonzero volume for the 2020-2024 development window across all six timeframes:
- M5: 373,465 rows, all with nonzero volume
- M15: 124,764 rows, all with nonzero volume
- M30: 62,513 rows, all with nonzero volume
- H1: 31,385 rows, all with nonzero volume
- H4: 8,039 rows, all with nonzero volume
- D1: 1,554 rows, all with nonzero volume

For the GBPUSD H1 compatibility join between the Market State Reader rows and the six-timeframe source data, 28,441 pre-2025 timestamps overlap, and all 28,441 joined rows have nonzero source volume.

Therefore the project has source-backed volume evidence for the 2020-2024 development window. Pre-2020 volume is not represented in the recovered six-timeframe source files used here and must remain unavailable rather than inferred.

## Interpretation
- Market Reader source contract: PRESENT
- Market State dataset/provenance: PRESENT
- Market State runtime implementation: NOT FOUND in audited archive
- Market Scenario dataset/provenance: PRESENT
- Market Scenario runtime implementation: NOT FOUND in audited archive
- Six-timeframe source volume 2020-2024: AVAILABLE / source-backed
- Pre-2020 volume from recovered six-timeframe source: NOT AVAILABLE
- 2025: protected OOS / excluded

## Governance decision
Do not rebuild the Market Reader blindly.
Use the existing Market State contract and normalize source-derived state rows with volume from the recovered six-timeframe source where timestamps overlap. Keep pre-2020 volume unavailable and fail closed for any rule that requires it.

No numeric thresholds, new strategy rules, or volume semantics are invented by this audit.
