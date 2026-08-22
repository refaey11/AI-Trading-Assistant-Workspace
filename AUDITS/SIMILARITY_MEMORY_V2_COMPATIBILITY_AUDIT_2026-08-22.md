# Similarity Memory V2 Compatibility Audit — 2026-08-22

## Source reviewed
`AI_Trading_Assistant_SIMILARITY_MEMORY_V2.zip`

## Source contract preserved
- Method: weighted categorical agreement + robust numeric closeness + candlestick similarity
- top_k: 20
- Purpose: historical context memory
- not_a_strategy: true

## Important source observation
The supplied `SIMILAR_CONTEXT_READS.json` contains 2025 current-context examples and also includes some 2025 similar matches. Those examples cannot be used for development retrieval or tuning because 2025 is locked OOS.

## Runtime boundary
`compatibility/similarity_memory_v2_boundary.py`

The boundary:
- accepts development retrieval only through 2024
- blocks current-context 2025
- blocks 2025 similar matches
- blocks future data
- preserves declared top_k=20
- fails closed when more than 20 matches are supplied
- emits evidence only; no direction and no final trade decision

## Governance
No similarity thresholds, scoring weights, directional rules, or scenario classification policy are invented by this adapter.

## Verification status
Implementation + tests + CircleCI job added. CI verification pending.
