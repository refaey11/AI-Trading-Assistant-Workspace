# Nison Source Sync Manifest V1 — 2026-08-16

## Purpose
Prepare the Nison source packages for GitHub Actions without treating engineering outputs as canonical Nison definitions.

## Verified local source packages
- `AI_Trading_Assistant_NISON_CONTEXT_ENGINE_V1.zip`
  - SHA-256: `b18b62313a77454abc64f361cbc1a2122daff648becc449bd4edda7ab761c7b9`
- `AI_Trading_Assistant_NISON_CANDLE_CONFIRMATION_V1.zip`
  - SHA-256: `f46525d262463e87df61233d3088cefbcfcaaf546b4f1dad7be993d36519c7de`
- `AI_Trading_Assistant_3_BOOK_INTEGRATION_V1.zip`
  - SHA-256: `31ad1d22a2d9ed3c897fece30da4da5934955114302226b20177cac0a1a45509`

## Important source finding
The 3-book integration archive contains the integrated rule registry and decision/integration contracts, but it does not contain a standalone `01_Integrated_Knowledge/02_Nison_Candlesticks/` subtree. The separate Nison context/candle packages contain the engineering artifacts used by the current Nison implementation.

## Current sync state
- GitHub branch: `feature/nison-hybrid-44-batch-v1`
- `main`: untouched
- Nison source payload: **NOT YET COPIED**
- Reason: the connected GitHub write interface available here supports text blobs/files, but the local uploaded CSV/ZIP payloads must not be replaced by placeholders or invented content.

## Required next sync
Copy the exact Nison package files into a dedicated branch subtree, preserving bytes/content and checksums, then wire GitHub Actions to that subtree. The sync must include the canonical integrated rule registry from the 3-book package plus the separate Nison context/candle artifacts required by their evaluators.

## Governance constraints
- No invented Nison thresholds, tolerances, lookbacks, or semantics.
- Reuse compatible primitives only.
- `NOT_EVALUABLE` when required operationalization is absent.
- Nison remains confirmation/evidence-only and cannot generate direction.
- 2025 remains OOS and cannot be used for tuning/calibration/selection.
- No automatic freeze from CI; governance freeze remains a separate gate.
