# AI Trading Assistant — Detailed Handoff / Resume Pack V1

## Exact stopping point
**Decision Brain Recovery & Compatibility Audit.**

Resume from this exact point. Do not rebuild or modify the existing Decision Brain before recovering the authoritative source and auditing its real contracts.

## Source-of-truth policy
- Workspace / File Library artifacts are the project source of truth.
- GitHub is the development/provenance mirror and must not silently replace Workspace truth.
- Existing components must be audited and integrated, not rebuilt.
- Compatibility audit is required before every new integration.
- 2025 is OOS and must never be used for tuning, calibration, optimization, or implementation selection.

## Current architecture rules
- Murphy = technical context / market structure evidence.
- Nison = confirmation / contradiction only; cannot create direction alone.
- Trading in the Zone = psychology / process gate only; cannot create direction.
- Similarity / Historical Memory = historical evidence only; never sole decision maker and cannot override hard gates.
- Risk = hard gate.
- Decision Brain = synthesis layer for current market evidence + book knowledge + historical evidence + risk.
- ABSTAIN is a valid outcome.

## Book-rule status
- Murphy: 35/51 authoritative/frozen; 16 deferred/open.
- Nison: 44/44 frozen.
- Trading in the Zone: 0/7 authoritative; 7 deferred.
- Current authoritative universe: 79/102 rules.
- Current deferred universe: 23/102 rules.

## Completed milestones
1. 79-rule provenance mapping / canonical governance checkpoint.
2. Rule Adapter -> Knowledge Alignment integration test: PASS 6/6.
3. Risk Engine artifact/spec recovered and classified as RESEARCH PROTOTYPE, not production/live.
4. Knowledge Alignment -> Risk Engine compatibility contract established.
5. Knowledge Alignment -> Risk Engine boundary integration test: PASS 8/8.
6. Complete milestone backup created before Decision Brain audit.

## Risk status
Research-only parameters remain research-only:
- risk profiles: 0.25%, 0.5%, 1%, 1.5%
- position sizing formula: risk_money / stop_distance
- stop modes: structure, 2x ATR, hybrid
- target: 1.5R
- drawdown tracked but not yet a trading halt

Do not promote these to production constants.

Unresolved live requirements include costs, spread, slippage, leverage, contract size, and broker-specific pip value. Current state: NOT_EXECUTION_READY.

## Required resume sequence
1. Recover original Decision Brain artifact(s) from Workspace/File Library/backups/project assets.
2. Identify exact implementation files, versions, and wrappers.
3. Extract actual Input Contract from source.
4. Extract actual Output Contract from source.
5. Recover and inspect Run 070 / Historical Evidence wrapper if present.
6. Verify Historical Memory/Similarity remains evidence-only.
7. Audit current market-evidence input.
8. Audit compatibility with completed Knowledge Alignment boundary.
9. Audit compatibility with Risk Hard-Gate boundary.
10. Classify each connection as COMPATIBLE / ADAPTER_REQUIRED / CONFLICT / MISSING_SOURCE.
11. Do not modify original Decision Brain during audit.
12. If needed, use the smallest boundary adapter possible.
13. Run tests only after real contracts are known.
14. Record governance result and commit it.
15. Create verified backup after milestone.

## Search locations
Workspace/File Library/backups first. Search terms:
- Decision Brain
- AI Decision Engine
- decision_brain.py
- Decision Brain V1 / V1.1
- Run 070
- Historical Evidence wrapper
- Historical Memory
- Similarity Memory
- 3_BOOK_INTEGRATION
- MASTER_KB
- MARKET_READER
- MARKET_STATE_READER
- MULTI_TIMEFRAME_READER
- MARKET_SCENARIO_ENGINE
- CONTEXT_AWARE_RETRIEVAL
- RISK_ENGINE_SPEC_V1

Known project archives include MASTER_KB_V1, 3_BOOK_INTEGRATION_V1, CONTEXT_AWARE_RETRIEVAL_V2, MARKET_READER_V1, MARKET_STATE_READER_V1, MARKET_SCENARIO_ENGINE_V1, MULTI_TIMEFRAME_READER_V1, HISTORICAL_CONTEXT_MEMORY_V1, HISTORICAL_OUTCOME_MEMORY_V1, SIMILARITY_MEMORY_V2, TRUE_BACKTEST_V2, TRADING_RULES_V2, NISON_CONTEXT_ENGINE_V1, NISON_CANDLE_CONFIRMATION_V1, plus rule_adapter_contract_v1.json, OFFICIAL_BASELINE_AUDIT_V1.txt, and VERSION_FREEZE_PLAN_V1.json.

## Key commit pointers
- Murphy canonical reconciliation: 4be77bbb46dd6b2b97bc9b198416620af79e779d
- Nison canonical freeze: 84257ada950ccd1ca5fca0357e0aa6f25d4eb8b3
- Rule Adapter mapping: e631e3f03a9ae52663e70f10272d98069f7baa29
- 79-rule audit: 29e01c8b328d689c96847bdbec2e0d61df944722
- Knowledge Alignment test: 759619ff1f43abf33f66285c5e1c677cfb917f3d
- Risk compatibility audit: 8cb2ae8553f4f79f652600884809d9b1c3fdf742
- Knowledge Alignment -> Risk compatibility contract: 32f9a48c5859a261dee430ee4aef7994dbe0094b
- Knowledge Alignment -> Risk boundary test: 47ddd6a0c1637490e54fafc40a9ab14b262a9d47

## Mandatory backup procedure
After every completed milestone: update governance, push GitHub, fetch actual latest GitHub artifacts when possible, include actual local/test artifacts, create manifest, ZIP, verify ZIP contents, provide SHA-256, and never claim a referenced commit pointer is the same as an included file snapshot.

## Instruction to the next chat
Start exactly from **Decision Brain Recovery & Compatibility Audit**. Recover the existing Decision Brain from Workspace/File Library/project backups first. Do not rebuild. Do not modify. Do not guess its contract. Extract the actual source contracts, then perform compatibility audit against the completed Knowledge Alignment and Risk boundaries.
