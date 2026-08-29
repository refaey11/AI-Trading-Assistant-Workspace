# MTF -> Decision Brain Input Compatibility Audit
Date: 2026-08-29
Status: BLOCKED — EXISTING CONTRACT GAP, NO SYNTHETIC MAPPING AUTHORIZED

## Verified sources
- DECISION_BRAIN_V1 expects numeric inputs:
  M5_trend_regime, M15_trend_regime, M30_trend_regime, H1_trend_regime, H4_trend_regime, D1_trend_regime, mtf_trend_score, plus timeframe volume/volatility regimes.
- Existing Dynamic MTF infrastructure assigns roles from available evidence and explicitly does not synthesize BUY/SELL.
- Existing Market State Reader provides categorical context such as trend, structure_event, volume_state, volatility_state, support/resistance location and candlestick evidence.
- Existing historical MTF Reader V1 is H4/H1 research-only and explicitly does not fabricate M15 data.
- Existing Similarity V2 indexes contain 57 numeric feature dimensions and metadata including the Decision Brain trend-regime field names, but current-query producer lineage is not yet proven.
- FEATURE_ENGINEERING_V2 is present in Dropbox and is completed, but its schema contains 22 engineered features; it is not proven to be the exact 57D Decision Brain input vector.

## Exact blocker
We currently do not have a source-proven deterministic producer that converts the current multi-timeframe evidence streams into the Decision Brain's required six numeric trend-regime fields and mtf_trend_score.

Creating values such as UP=+1, DOWN=-1 or averaging categorical states here would invent strategy semantics and would violate the project's compatibility-first rule.

## Decision
Do not modify Decision Brain V1.
Do not invent a numerical MTF scoring formula.
Do not run the 2016-2024 unified backtest as if the missing fields were valid.

## Safe next action
Recover the exact producer/serialized feature matrix used to build Similarity V2, including current/query lineage and preprocessing. If the producer emits the exact 57D schema, build a wiring-only adapter that selects/renames those already-produced fields into the Decision Brain contract. Otherwise retain NOT_EVALUABLE for the affected fields until a source-backed producer is recovered.

## TIZ note
TIZ is not this blocker. TIZ remains optional/unverified when unavailable, process-only and direction-neutral. Risk remains a hard gate.

## Evidence
- Uploaded/project MTF blocker: MTF_BRAIN_INTERFACE_BLOCKER_V1.md
- Similarity recovery checkpoint: SIMILARITY_RECOVERY_CHECKPOINT_V1.json
- Similarity compatibility audit: SIMILARITY_COMPATIBILITY_AUDIT_RUN_026.json
- Similarity current-vector hunt: SIMILARITY_CURRENT_VECTOR_PROJECT_HUNT_RUN_034.json
- Similarity evidence extraction: SIMILARITY_CURRENT_VECTOR_EVIDENCE_EXTRACTION_RUN_035.json
- Dropbox FEATURE_ENGINEERING_V2_SCHEMA.json and FEATURE_ENGINEERING_V2_SUMMARY.csv
