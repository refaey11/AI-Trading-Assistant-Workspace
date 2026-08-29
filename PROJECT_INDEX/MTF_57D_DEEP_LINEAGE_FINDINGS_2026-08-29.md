# Six-TF / 57D Deep Lineage Findings
Date: 2026-08-29
Status: DEEP SEARCH COMPLETE — RAW PRODUCER LINEAGE STILL OPEN

## What is now proven
The project contains an explicit, source-backed V2 57-dimensional schema for the similarity candidate/index path. The feature order is explicitly enumerated and includes:
- mtf_trend_score
- mtf_bullish_count
- mtf_bearish_count
- mtf_neutral_count
- higher_tf_bullish_breaks
- higher_tf_bearish_breaks
- higher_tf_bullish_candles
- higher_tf_bearish_candles
- per-timeframe features for M5, M15, M30, H1, H4, D1 including relative_volume_20, atr_14, atr_50, range_to_atr14, atr_pct, trend_regime, volume_regime, volatility_regime
- mtf_context_code

The V2 artifacts also persist scaler_mean, scaler_scale, and median_impute metadata, and future outcomes are explicitly excluded from retrieval features.

## Six canonical timeframes
M5 -> M15 -> M30 -> H1 -> H4 -> D1.
Existing as-of/no-lookahead evidence for 2020-2024 is already closed.

## Critical compatibility distinction
The recovered Decision Brain V1 consumes semantic numeric fields such as the six trend_regime values and mtf_trend_score directly as Brain inputs. The V2 similarity indexes are standardized matrices. Therefore the standardized 57D candidate matrix must NOT be injected directly into the Brain without proving the original raw-feature producer and preprocessing contract.

## Deep-search result
Search across the uploaded workspace, File Library, Dropbox artifacts, GitHub repository files/history, and reconstructed evaluator workspace did not recover a definitive source-proven producer that emits the exact current/query 57D raw vector in the exact order and preprocessing used by Similarity V2.

The reconstructed workspace DOES contain the existing DYNAMIC_MTF_BINDING_CONTRACT_V1 and MURPHY_51_RULE_TO_MTF_FUNCTION_* contracts. These confirm that six timeframes are available and that role selection is dynamic, higher-timeframe-first, and must not synthesize BUY/SELL. They do not define a new numeric scoring transform into Brain fields.

## Important reusable evidence
- SIMILARITY_LINEAGE_AUDIT_RUN_027: explicit 57D feature list and metadata.
- SIMILARITY_ENGINE_V2_INDEX_COMPATIBILITY_RUN_028: five asset indexes at 150000 x 57; exact feature order/scaler/query lineage not fully proven end-to-end.
- SIMILARITY_RUNTIME_MAPPING_RUN_038: only fields with runtime producer + explicit semantics + explicit numeric encoding may enter similarity vectors.
- SIMILARITY_57D_V3_AUDIT_RUN_039: V2 57D and V3 engineered schema are separate; do not manually rebuild V2.
- FEATURE_ENGINEERING_V2_SCHEMA.json: completed 22-feature leakage-safe schema; not proven identical to V2 57D.
- DYNAMIC_MTF_BINDING_CONTRACT_V1: six timeframe availability and dynamic role semantics.

## Safe decision
Do NOT modify Decision Brain V1.
Do NOT invent UP=+1/DOWN=-1 or averaged MTF scoring.
Do NOT feed standardized V2 index rows directly into the Brain.
Do NOT run the unified 2016-2024 backtest on an unproven Brain input contract.

## Remaining single objective
Recover the exact existing producer or serialized raw/pre-standardized feature matrix for the V2 query/current vector, including feature order and preprocessing lineage. If recovered, create a wiring-only adapter into the existing Brain contract. If not recoverable, keep the affected Brain fields NOT_EVALUABLE rather than invent semantics.

## Anti-loop rule
No new evaluator, strategy layer, or replacement Brain is authorized by this finding. The work remains audit -> recover -> wire -> one pre-2025 Gate 3C event.
