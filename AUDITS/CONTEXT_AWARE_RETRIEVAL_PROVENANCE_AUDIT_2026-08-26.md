# Context-Aware Retrieval Provenance Audit — 2026-08-26

## Scope
Read-only provenance audit of the existing `AI_Trading_Assistant_CONTEXT_AWARE_RETRIEVAL_V2` package. No rule semantics are copied, modified, or regenerated.

## Observed package structure
`CONTEXT_AWARE_READINGS.json` contains five precomputed readings. Each reading contains:
- a current market state with timestamp;
- context terms used for retrieval;
- retrieved chunks with `score`, `chunk_id`, `book`, and `source_file`;
- source text derived from the project rule registry.

## Provenance finding
The retrieved chunks explicitly identify `03_Rule_Registry/INTEGRATED_RULE_REGISTRY_V1.json` as the source file and retain rule IDs such as `CANDLE_RULE_0002` / `CANDLE_RULE_0005` inside the returned text.

This establishes **source provenance of the stored retrieval snapshots**.

It does **not** establish runtime consumption by the current Decision Brain. The current event producer does not pass a retrieval payload into `historical_evidence`, and the current handoff path has no runtime retrieval callable exposed by this package.

## Result

| Test | Status |
|---|---|
| Stored retrieval artifact exists | PASS |
| Retrieved content identifies source file | PASS |
| Retrieved content retains source-rule identity | PASS |
| Runtime retrieval callable exposed by package | NOT PROVEN |
| Current Decision Brain consumes retrieval payload | NOT WIRED |
| Retrieval can generate direction | MUST REMAIN FALSE |

## Governance boundary
Context-Aware Retrieval is evidence/provenance only. It cannot create direction, override Murphy, bypass Nison/TIZ/Risk gates, or become a sole decision maker. 2025 remains locked and must not be used for tuning.

## Required next implementation
Build a shadow-only retrieval provenance/consumption probe for 2016–2024 that takes an as-of market context, records the retrieved chunk IDs/source rule IDs, attaches the result to the single historical-evidence envelope, and verifies downstream direction remains unchanged. Do not alter the production 2025 path until this structural proof passes.
