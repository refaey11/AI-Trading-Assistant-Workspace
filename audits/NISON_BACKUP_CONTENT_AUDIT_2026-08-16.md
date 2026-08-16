# Nison Backup Content Audit — 2026-08-16

Status: AUDIT ONLY — no Nison source files copied into the repository by this audit.

## Backup packages inspected

- AI_Trading_Assistant_NISON_CONTEXT_ENGINE_V1.zip
- AI_Trading_Assistant_NISON_CANDLE_CONFIRMATION_V1.zip
- AI_Trading_Assistant_3_BOOK_INTEGRATION_V1.zip
- rule_adapter_contract_v1.json

## Verified contents

### Nison Candle Confirmation V1
- candlestick_engine/CANDLESTICK_SPEC_V1.json
- candlestick_engine/CANDLE_FILTER_RESULTS_2016.csv
- candlestick_engine/FILTERED_TRADES_2016.csv
- candlestick_engine/PATTERN_SIGNALS_WITH_CANDLE_CONFIRMATION.csv

The specification currently lists 9 operational pattern names and explicitly warns that the definitions are engineering definitions inspired by common candlestick taxonomy and must be mapped to exact Steve Nison textual criteria before being treated as canonical.

### Nison Context Engine V1
- context_engine/CONTEXT_SPEC_V1.json
- context_engine/CANDLES_WITH_CONTEXT.csv
- context_engine/CONTEXT_FILTER_RESULTS_2016.csv
- context_engine/CONTEXT_FILTERED_TRADES_2016.csv

The specification uses EMA20/EMA50 trend filtering, a 40-bar S/R location window with a 0.75 ATR distance, body/range >= 0.35, and bar range <= 3 ATR. It explicitly labels these as engineering filters rather than verbatim Nison rules.

### Three-Book Integration V1
- 01_Integrated_Knowledge/04_Integration_Layer/THREE_BOOK_INTEGRATION.json
- 02_Decision_Engine/DECISION_SCHEMA_V1.json
- 02_Decision_Engine/THREE_BOOK_DECISION_CONTRACT_V1.json
- 03_Rule_Registry/INTEGRATED_RULE_REGISTRY_V1.json

The registry contains Nison-sourced confirmation records. The inspected records are marked UNTESTED and retain source-file references.

### Rule Adapter Contract V1
- Normalizes existing book-rule outputs into Decision Brain evidence.
- Explicitly states Nison is confirmation-only and 2025 is OOS.
- Status is DESIGN_ONLY.

## Critical integration finding

This backup is useful and valuable, but it is NOT yet a canonical 44-rule executable Nison source package.

The backup contains operational/engineering artifacts and an integrated registry, but the candle/context specifications themselves explicitly disclaim canonical Steve Nison equivalence. Therefore the backup MUST NOT be copied into production CI and treated as canonical 44-rule semantics without a compatibility/source audit.

## CI implication

GitHub Actions can run deterministic tests and audits once the required executable source/tests are present in the repository. The current backup should first be treated as an evidence/source package. Only files that pass the compatibility/source audit should be promoted into the Nison CI workspace.

## Safety gates

- Do not invent missing Nison definitions.
- Do not promote engineering thresholds to canonical Nison thresholds.
- Do not use 2025 for tuning/calibration/selection/optimization.
- Do not let Nison generate independent direction.
- Do not auto-freeze from test success alone.
