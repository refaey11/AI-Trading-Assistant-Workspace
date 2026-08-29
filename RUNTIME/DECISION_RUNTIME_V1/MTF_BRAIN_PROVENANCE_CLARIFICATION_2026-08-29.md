# MTF -> Decision Brain Provenance Clarification
Date: 2026-08-29
Status: ACTIVE — DO NOT CONFLATE ALIGNMENT PASS WITH BRAIN INPUT PROVENANCE

## What is already proven
The six-timeframe as-of alignment chain M5 -> M15 -> M30 -> H1 -> H4 -> D1 is closed for the tested 2020-2024 window. The evidence proves zero future mappings and zero missing mappings in that alignment validation.

## What is not proven by that evidence
The alignment artifact does not prove that the Decision Brain's numeric inputs were produced by a source-backed deterministic producer. In particular, the following remain a separate lineage question:
- M5_trend_regime
- M15_trend_regime
- M30_trend_regime
- H1_trend_regime
- H4_trend_regime
- D1_trend_regime
- mtf_trend_score
- timeframe volatility/volume numeric fields required by Decision Brain V1

## Why this distinction matters
The existing Decision Brain contract consumes numeric fields. The current Market State / Dynamic MTF evidence is not authorization to invent a numeric encoding such as UP=+1/DOWN=-1, to average categorical states, or to zero-fill missing fields.

## Canonical interpretation
- Six-TF alignment PASS = source/time alignment and no-lookahead evidence.
- Numeric Brain producer PASS = separate producer/schema/semantics/preprocessing proof.
- Full Brain E2E PASS = canonical timestamped event carrying complete source-backed Brain inputs through Handoff -> Brain -> TIZ boundary -> Risk/Execution.

These are separate gates and must remain separate in reports and execution scripts.

## Current safe action
Recover the exact producer or serialized feature matrix used for the 57D Similarity representation, including field order, current/query lineage, imputation/scaling, and raw-to-feature semantics. If it matches the Decision Brain contract, wire by selection/rename only. Otherwise keep affected fields NOT_EVALUABLE and fail closed.

## References
- f5e0e59b46f2b79a0e28405713955cb7f18720d1: six-TF as-of alignment evidence.
- dd011d02b158fefd3de0a5f3fd3488e90878115c: explicit MTF -> Brain numeric input compatibility gap.
- AI_Trading_Assistant project handoff 2026-08-29: canonical governed execution sequence.
