# AI Trading Assistant — Complete Handoff / Project State — 2026-08-21

## Current stopping point
**Decision Brain Recovery & Compatibility Audit.**

## Core rule
This is an AI Trading Assistant / Decision Brain, not a trading indicator. Existing components must be recovered, audited, compatibility-checked, then integrated; they must not be rebuilt from scratch.

## Book status
- Murphy: 35/51 currently authoritative/frozen; 16 deferred/open.
- Steve Nison: 44/44 frozen.
- Trading in the Zone: 0/7 currently authoritative for integration; deferred.
- Current authoritative total: 79/102.
- Current non-authoritative/deferred total: 23/102.

## Fixed role boundaries
- Murphy = technical context / market structure.
- Nison = confirmation/contradiction only; cannot create direction alone.
- Trading in the Zone = psychology/process gate only.
- Similarity/Historical Memory = historical evidence only; never sole decision maker.
- Risk = hard gate.
- Decision Brain = synthesizing layer for current market evidence + book knowledge + historical memory + risk.
- 2025 = OOS and must never be used for tuning, calibration, optimization, or implementation selection.

## Completed milestones
1. 79-rule provenance/canonical governance audit: PASS.
2. Knowledge Alignment integration test: PASS 6/6.
3. Recovered Risk Engine spec classified as Research Prototype, not live execution.
4. Knowledge Alignment → Risk compatibility contract: compatible for research-boundary integration only.
5. Knowledge Alignment → Risk boundary integration test: PASS 8/8.
6. Milestone backups created and ZIP-verified.

## Risk status
The recovered RISK_ENGINE_SPEC_V1 contains research hard gates, research risk profiles, stop modes, position sizing formula, and a 1.5R research target. These are not automatically promoted to production constants. Current status is NOT_EXECUTION_READY because authoritative live handling for costs, spread, slippage, leverage, contract size, and broker-specific pip value remains unresolved.

## Next mandatory sequence
1. Recover the original Decision Brain from Workspace/File Library/project backup archives/release assets.
2. Identify implementation files and any Decision Brain V1/V1.1 artifacts.
3. Extract the real Input Contract and Output Contract.
4. Recover/audit any Run 070 or historical-evidence wrapper connected to it.
5. Run compatibility audit against Knowledge Alignment, Risk boundary, Historical Memory/Similarity, and book role boundaries.
6. Classify result as COMPATIBLE / COMPATIBLE_WITH_ADAPTER / CONFLICT / MISSING_INPUT_CONTRACT / MISSING_OUTPUT_CONTRACT.
7. Do not modify or rebuild the original Decision Brain before this audit is complete.

## After Decision Brain audit
Controlled integration → end-to-end scenario tests → historical validation → protected 2025 OOS validation → recovery/closure of remaining 16 Murphy + 7 Trading in the Zone rules → eventual execution-readiness review.

## Provenance commits
- Murphy reconciliation: 4be77bbb46dd6b2b97bc9b198416620af79e779d
- Nison freeze: 84257ada950ccd1ca5fca0357e0aa6f25d4eb8b3
- Rule Adapter mapping: e631e3f03a9ae52663e70f10272d98069f7baa29
- 79-rule audit: 29e01c8b328d689c96847bdbec2e0d61df944722
- Knowledge Alignment test 6/6: 759619ff1f43abf33f66285c5e1c677cfb917f3d
- Risk compatibility audit: 8cb2ae8553f4f79f652600884809d9b1c3fdf742
- Knowledge Alignment → Risk contract: 32f9a48c5859a261dee430ee4aef7994dbe0094b
- Knowledge Alignment → Risk test 8/8: 47ddd6a0c1637490e54fafc40a9ab14b262a9d47

## Backup policy
After every completed milestone: record status → commit authoritative artifacts → create backup containing actual changed files when retrievable + local artifacts + tests + manifest + commit pointers → verify ZIP contents → deliver backup.
