# AI Trading Assistant — Continuation Checkpoint
Date: 2026-08-29

## Current conclusion
The project must continue on the existing architecture. No new Decision Brain, no rebuilt Murphy/Nison modules, and no invented MTF numeric semantics.

## Six canonical timeframes
M5, M15, M30, H1, H4, D1.
Existing six-timeframe as-of/no-lookahead evidence is already closed for 2020–2024. The verified chain is M5 -> M15 -> M30 -> H1 -> H4 -> D1 with zero future mappings and zero missing mappings in that validation.

## Existing components preserved
- Murphy: 34 runtime-verified rules. 0008 remains blocked/not evaluable and is not part of the 34.
- Nison: 44 governed rules.
- Historical/Similarity Memory: evidence only; PIT required; cannot generate direction.
- TIZ: process/psychology evidence only; optional/unverified outside production when unavailable; never generates direction.
- Decision Brain V1: existing recovered runtime; do not rewrite.
- Three-Book evaluator, Risk, and Execution adapter: existing governed path.

## Important compatibility finding
Six-timeframe alignment itself is not the blocker. The unresolved point is source-proven lineage for the numeric Decision Brain inputs: M5_trend_regime, M15_trend_regime, M30_trend_regime, H1_trend_regime, H4_trend_regime, D1_trend_regime, and mtf_trend_score. Arbitrary encodings such as UP=+1/DOWN=-1 or averaging categorical states are prohibited.

## Source recovery path
Existing Dropbox artifacts include FEATURE_ENGINEERING_V2 schema/H5 and Similarity V2/V3 artifacts. FEATURE_ENGINEERING_V2 is completed and leakage-safe, but its documented schema contains 22 engineered features; it is not yet proven to be the exact 57D Decision Brain vector. Similarity runtime mapping records that only fields with runtime producer + explicit semantics + explicit numeric encoding may enter the similarity vector.

## Next execution gate
Recover the exact producer or serialized feature matrix used to build the 57D Similarity representation, prove current/query lineage and preprocessing, and then make only a wiring/selection adapter into the Decision Brain contract. After that, run one real pre-2025 Gate 3C event through:
Market + six-TF MTF -> Murphy 34 -> Nison 44 -> PIT Memory -> TIZ process evidence -> existing Decision Brain -> Risk -> Trade Plan.

## Guardrails
- 2025 remains OOS and is never used for tuning.
- Do not run the 2016–2024 unified backtest until the Brain input lineage is proven.
- Do not claim full-34/full-44 E2E until the canonical event proves the rule envelope is source-backed.
- Record each completed execution checkpoint in GitHub and Dropbox.

## Evidence references
- GitHub commit f5e0e59b46f2b79a0e28405713955cb7f18720d1: six-timeframe as-of alignment final evidence.
- GitHub commit dd011d02b158fefd3de0a5f3fd3488e90878115c: MTF -> Brain input compatibility audit.
- Dropbox FEATURE_ENGINEERING_V2_SCHEMA.json: completed, 22-feature leakage-safe feature engineering schema.
- Dropbox SIMILARITY_RUNTIME_MAPPING_RUN_038.md: contract-driven mapping path; no guessed feature insertion.
- Dropbox project checkpoint 2026-08-25: final OOS assembly/profitability stage and governed full-event-stream requirement.
