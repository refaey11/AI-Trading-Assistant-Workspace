# AI Trading Assistant — Chat Handoff Checkpoint — 2026-08-21

## Current stopping point
**DECISION BRAIN RECOVERY & COMPATIBILITY AUDIT**

Do not implement or rebuild the Decision Brain before recovering the existing/original artifact and auditing its real contracts.

## Completed
- Murphy: 35/51 currently authoritative/frozen; 16 deferred/open.
- Steve Nison: 44/44 frozen; confirmation/contradiction only; cannot create direction alone.
- Trading in the Zone: 0/7 currently authoritative/frozen; psychology/process only; cannot generate direction.
- Total currently authoritative: 79/102; deferred/not currently frozen: 23.
- Rule provenance/canonical mapping completed.
- Rule Adapter -> Knowledge Alignment integration test: PASS 6/6.
- RISK_ENGINE_SPEC_V1 recovered and classified as research prototype, not execution ready.
- Knowledge Alignment -> Risk Engine compatibility contract completed.
- Knowledge Alignment -> Risk Engine boundary integration test: PASS 8/8.
- Full milestone backup created before Decision Brain audit.

## Architecture boundaries
- Murphy = technical context / market structure evidence.
- Nison = confirmation/contradiction only.
- Trading in the Zone = psychology/process gate only.
- Similarity/Historical Memory = historical evidence only, never sole decision maker.
- Risk = hard gate.
- Decision Brain = current market evidence + book knowledge + historical memory + risk.
- 2025 = OOS and must never be used for tuning, calibration, optimization, or implementation selection.

## Exact next sequence
1. Recover original/existing Decision Brain from Workspace/File Library/project backup assets.
2. Locate decision_brain.py or equivalent, V1/V1.1 records, input/output contracts, and Run 070/historical wrapper if present.
3. Inspect actual implementation.
4. Extract actual input/output contract.
5. Audit compatibility with Knowledge Alignment and Risk boundaries.
6. Classify mismatches as COMPATIBLE / ADAPTER_REQUIRED / CONFLICT / MISSING_SOURCE.
7. Do not edit the original Decision Brain during the audit.
8. After audit, create only the smallest required adapter.
9. Run representative tests.
10. Record result, sync provenance, and create a verified backup.

## Risk research boundary
Research-only hard gates: positive stop; 0.5–4 ATR when ATR reference is used; defined take profit; risk budget fixed before entry.
Research parameters are not production constants: 0.25/0.5/1/1.5% profiles, risk_money/stop_distance sizing formula, structure/2xATR/hybrid stops, 1.5R target.
Live requirements still unresolved: costs, spread, slippage, leverage, contract size, broker-specific pip value.

## Provenance pointers
- Murphy reconciliation: 4be77bbb46dd6b2b97bc9b198416620af79e779d
- Nison freeze: 84257ada950ccd1ca5fca0357e0aa6f25d4eb8b3
- Rule adapter mapping: e631e3f03a9ae52663e70f10272d98069f7baa29
- 79-rule audit: 29e01c8b328d689c96847bdbec2e0d61df944722
- Knowledge Alignment test: 759619ff1f43abf33f66285c5e1c677cfb917f3d
- Risk compatibility contract: 32f9a48c5859a261dee430ee4aef7994dbe0094b
- Risk boundary test: 47ddd6a0c1637490e54fafc40a9ab14b262a9d47

## Working policy
Workspace/File Library artifacts are the project source of truth. GitHub is the development/provenance mirror and must not silently replace Workspace truth. Existing components must be audited and integrated, not rebuilt. Compatibility audit is required before every new integration. After each completed milestone, create a verified backup with actual artifacts where available, manifest, provenance pointers, and ZIP-content verification.
