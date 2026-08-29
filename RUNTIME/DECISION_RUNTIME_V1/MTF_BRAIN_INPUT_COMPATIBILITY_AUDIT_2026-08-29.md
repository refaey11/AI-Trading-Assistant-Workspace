# MTF -> Decision Brain Input Compatibility Audit
Date: 2026-08-29
Status: BLOCKED — EXISTING CONTRACT GAP, NO SYNTHETIC MAPPING AUTHORIZED

## Verified sources
- DECISION_BRAIN_V1 expects numeric inputs: M5_trend_regime, M15_trend_regime, M30_trend_regime, H1_trend_regime, H4_trend_regime, D1_trend_regime, mtf_trend_score, plus timeframe volume/volatility regimes.
- Existing Dynamic MTF infrastructure assigns roles from available evidence and does not synthesize BUY/SELL.
- Existing Market State Reader provides categorical context: trend, structure_event, volume_state, volatility_state, support/resistance location, and candlestick evidence.
- Existing historical MTF Reader V1 is H4/H1 research-only and does not fabricate M15 data.
- Existing Similarity V2 indexes contain 57 numeric dimensions and metadata naming the Decision Brain fields, but exact current/query producer lineage remains unproven.
- FEATURE_ENGINEERING_V2 exists in Dropbox and is marked completed, but its schema contains 22 engineered features, so it is not proven to be the exact 57D Decision Brain input vector.

## Exact blocker
We do not currently have source-proven deterministic producer lineage for the Decision Brain's six numeric trend-regime fields and mtf_trend_score.

Using arbitrary encodings such as UP=+1, DOWN=-1 or averaging categorical MTF states would invent strategy semantics and violate the project's compatibility-first rule.

## Decision
- Do not modify Decision Brain V1.
- Do not invent a numerical MTF scoring formula.
- Do not run the 2016-2024 unified backtest as if the missing fields were valid.

## Safe next action
Recover the exact producer or serialized feature matrix used to build Similarity V2, including current/query lineage and preprocessing. If it emits the exact 57D schema, build a wiring-only adapter selecting/renaming existing fields into the Brain contract. Otherwise affected fields remain NOT_EVALUABLE until source-backed producer evidence is recovered.

## TIZ note
TIZ is not this blocker. TIZ remains optional/unverified when unavailable, process-only, and direction-neutral. Risk remains a hard gate.

## Evidence
- MTF_BRAIN_INTERFACE_BLOCKER_V1.md
- SIMILARITY_RECOVERY_CHECKPOINT_V1.json
- SIMILARITY_COMPATIBILITY_AUDIT_RUN_026.json
- SIMILARITY_CURRENT_VECTOR_PROJECT_HUNT_RUN_034.json
- SIMILARITY_CURRENT_VECTOR_EVIDENCE_EXTRACTION_RUN_035.json
- Dropbox FEATURE_ENGINEERING_V2_SCHEMA.json
- Dropbox FEATURE_ENGINEERING_V2_SUMMARY.csv
