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

## Critical data-quality boundary
Across the audited Market State datasets, `volume` is zero for 100% of pre-2025 rows and `volume_ratio` is largely missing. Therefore volume-based reasoning is not deterministically evaluable from this dataset as supplied. The contract explicitly requires volume context, so volume evidence must remain unknown/unavailable rather than being inferred.

## Interpretation
- Market Reader source contract: PRESENT
- Market State dataset/provenance: PRESENT
- Market State runtime implementation: NOT FOUND in audited archive
- Market Scenario dataset/provenance: PRESENT
- Market Scenario runtime implementation: NOT FOUND in audited archive
- Volume context from supplied state data: NOT_EVALUABLE
- 2025: protected OOS / excluded

## Governance decision
Do not rebuild the Market Reader blindly.
First perform a compatibility audit against any existing runtime artifacts elsewhere in the project. If no runtime exists, build only the minimum contract-bound adapter/runtime needed to make the existing Market State and Scenario outputs executable, preserving the source semantics.

No numeric thresholds, new strategy rules, or volume semantics are invented by this audit.
