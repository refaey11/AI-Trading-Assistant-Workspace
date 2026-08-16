# Nison Source Sync V1 — 2026-08-16

Status: PREPARED / AWAITING BINARY SOURCE TRANSFER

The canonical source package was assembled locally from the uploaded project packages without changing semantics.

Included source roots:
- `01_Integrated_Knowledge/02_Nison_Candlesticks/` from `AI_Trading_Assistant_3_BOOK_INTEGRATION_V1.zip`
- `03_Rule_Registry/INTEGRATED_RULE_REGISTRY_V1.json` from `AI_Trading_Assistant_3_BOOK_INTEGRATION_V1.zip`
- `context_engine/` from `AI_Trading_Assistant_NISON_CONTEXT_ENGINE_V1.zip`
- `candlestick_engine/` from `AI_Trading_Assistant_NISON_CANDLE_CONFIRMATION_V1.zip`
- `rule_adapter_contract_v1.json` from the uploaded contract package

Local assembled archive:
- `NISON_SOURCE_SYNC_V1.zip`
- SHA-256: `5dbbdd276566e0b2f7db7e999125e157837d0c9acdeabe7820afeca9ed399e68`
- Nison knowledge files: 996
- Nison knowledge source size before archive: approximately 5.2 MB

Important governance:
- This package is source/evidence material, not an automatic freeze authority.
- Do not invent thresholds, tolerances, lookbacks, or scoring.
- Reuse compatible evaluators/primitives only.
- Unsupported clauses remain NOT_EVALUABLE/BLOCKED.
- 2025 remains OOS and must not be used for tuning, calibration, optimization, or operator selection.
- Nison remains confirmation/evidence only and does not generate standalone direction.

Next required infrastructure step: place the assembled binary archive or its extracted files into the GitHub branch so GitHub Actions can consume the actual source. This manifest does not claim that binary source transfer has completed.