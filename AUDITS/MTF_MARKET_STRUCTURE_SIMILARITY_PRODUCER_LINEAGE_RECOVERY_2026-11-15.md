# MTF / Market Structure / Similarity Producer Lineage Recovery
Date: 2026-11-15
Status: READ-ONLY RECOVERY AUDIT

## 1. Confirmed candle conversion
The GBPUSD raw M1 master was reconciled against the existing `MULTI_TF_MARKET_DATA_V1.zip` output for 2016-2024. All six timeframes matched 100% for OHLC, M1 row counts, volume availability flags, and available-volume sums:
- M5: 671,601 / 671,601
- M15: 223,978 / 223,978
- M30: 111,995 / 111,995
- H1: 55,998 / 55,998
- H4: 14,209 / 14,209
- D1: 2,544 / 2,544
No missing or extra output bars. 2025+ excluded. The conversion is closed for GBPUSD 2016-2024; do not rebuild it.

## 2. Existing six-timeframe output archives
Dropbox contains separate `MARKET_STRUCTURE_ALL_TF_V1.zip` archives for EURUSD, GBPUSD, USDJPY, USDCAD, and XAUUSD, and separate `MTF_ALIGNMENT_<SYMBOL>_V1.zip` archives for the same five instruments.
The GBPUSD structure archive has 36 CSV outputs (six timeframes x six years/coverage groups in the recovered inventory); the MTF alignment archive contains annual M5-aligned outputs, README/manifest, and six-timeframe fields.
The existing output artifacts are present. Their original executable feature-producer source is not in the archives' recovered file inventory.

## 3. MTF Architecture V2 is a plan/specification, not the producer
The Dropbox folder `AI_Trading_Assistant_FULL_PROJECT_V1/AI_Trading_Assistant_MTF_ARCHITECTURE_V2` contains:
- `MTF_READER_SPEC_V2.json`
- `READER_LOGIC.md`
- `DATA_REQUIREMENTS.md`
- `NEXT_STEP.md`

The specification describes a seven-timeframe reader (M5/M15/M30/H1/H4/D1/W1), role ordering, and intended market features. The docs explicitly describe future pipeline construction and data requirements; they contain no executable producer or formula for the existing six-timeframe trend regimes / score. This architecture is distinct from the already existing six-timeframe MTF Alignment output archive.

## 4. Existing project adapters are not producers
- `market_pipeline_evidence_adapter.py` normalizes existing Market Reader, Market State, Scenario, H4/H1 MTF, and Context-Aware Retrieval outputs into governed evidence. It does not compute the underlying Market Structure or six-timeframe alignment features.
- `MTF_SIX_TF_SOURCE_ADAPTER_V1.py` validates/loads existing MTF files; it does not resample candles or produce trend regimes/score.
- `mtf_brain_input_join_v1.py` performs strict point-in-time/as-of joining of the seven already-produced Brain input fields. It does not derive those fields.
- Dynamic MTF binding adapter validates explicit role assignments only; no numeric score or direction is generated.
- The H4/H1 Multi-Timeframe Reader V1 is a separate research-only component and must not be substituted for the six-timeframe alignment archive.

## 5. Similarity feature lineage is a separate path
### Feature Engineering V2
`FEATURE_ENGINEERING_V2_SCHEMA.json` defines 22 higher-level descriptive/memory features. It is marked completed and future outcomes are excluded as features. The H5/ZIP outputs and summary are present, but the original executable builder was not recovered in the inspected file inventory. It is not proven to be the original 57D raw feature builder or the six-timeframe Brain-field producer.

### Similarity V2 (57D)
The existing audit `MTF_57D_DEEP_LINEAGE_FINDINGS_2026-08-29.md` enumerates a 57D feature order and confirms persisted scaler/imputer metadata. It explicitly warns that standardized 57D index rows must not be injected into Decision Brain V1 fields without proving the original raw producer and preprocessing. Exact current/query raw-vector producer lineage remains open.

### Similarity V3 (71 features)
`SIMILARITY_ENGINE_V3.zip` contains a config with 22 feature names and 2024 retrieval result CSVs/summary. It does not contain a `.py` or notebook builder in the extracted text/file inventory. `SIMILARITY_57D_V3_AUDIT_RUN_039.md` says V3 uses a shared builder `v3_shared_builder.py`, but that builder was not located in the Dropbox project folder, V3 ZIP, recovered backups, or selected GitHub branch trees.
The V2 57D and V3 71D schemas are separate and must remain separate.

## 6. Other regime research artifacts are not the missing MTF producer
`AI_Trading_Assistant_REGIME_V2_SCORE.zip` contains a diagnostic Regime Engine V2 spec with continuous `trend_score`, `range_score`, `volatility_score`, and `uncertainty_score`, plus 2016-2018 GBPUSD score data and evaluation/calibration summaries. Its README labels it diagnostic-only; the fields are not the six per-timeframe `trend_regime` values or `mtf_trend_score` expected by the Decision Brain.
Regime discovery/diagnostic/filter artifacts likewise contain evaluation outputs/specifications, not the missing six-TF Market Structure producer.

## 7. Recovered GitHub source status
Selected branch trees inspected:
- `BACKUP_PRE_BRAIN_WIRING_2026-08-30`
- `build/decision-runtime-v1`
- `decision-brain-stable-2026-09-05`
- `canonical-decision-pipeline-v1`
- `feat/mtf-runtime-resolver-v1`
- `fix/mtf-import-clean-2026-08-30`
- `feature/edge-discovery-ledger-v1`

These contain MTF source adapters, as-of join/resolver logic, Similarity V2 boundary/governance adapters, and tests; no Market Structure feature producer or exact MTF score producer was found in those trees.

## 8. Reconciled conclusion
Confirmed:
1. Raw GBPUSD M1 -> M5/M15/M30/H1/H4/D1 candle aggregation output is fully reconciled for 2016-2024.
2. Five-symbol Market Structure and MTF alignment output archives exist.
3. MTF source adapters and Brain join contracts exist and are intentionally non-generative.
4. Similarity V2/V3 are distinct evidence-retrieval feature paths, not substitutes for the MTF-to-Brain raw semantic fields.

Still unproven / not recovered:
- Executable producer for Market Structure fields (trend_regime, pivots, structure breaks/candle features).
- Executable producer for the six-timeframe alignment output and exact `mtf_trend_score` formula.
- Exact raw/current-query producer and preprocessing for the 57D Similarity V2 representation.
- Actual V3 shared builder source (`v3_shared_builder.py`) despite the Run 039 checkpoint referencing it.

## 9. Next single safe action
Recover the original producer from the source environment that created the archives (likely the original analysis notebook/script or execution workspace), or recover the exact serialized pre-standardized feature matrix plus manifest/preprocessing metadata. Do not derive formulas from CSV columns, reverse-engineer approximate outputs, substitute Regime V2 scores, or rebuild from scratch.
Until recovered, preserve existing archives and keep affected semantic Brain fields `NOT_EVALUABLE` / blocked. Do not run a full governed backtest on guessed fields.

## Governance
- No runtime or source data changes.
- No feature formula, threshold, encoding, or scoring formula invented.
- No direction, risk, or trade semantics changed.
- 2025 remains frozen OOS; not used for tuning/calibration/selection.
- Audit-only branch/PR; no merge authorized.
