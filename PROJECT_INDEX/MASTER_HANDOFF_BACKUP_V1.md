# AI Trading Assistant — Decision Brain
## MASTER HANDOFF & RECOVERY BACKUP V1

**Current checkpoint:** Decision Brain Recovery & Compatibility Audit.

### Governance
- Workspace/File Library artifacts are source of truth.
- GitHub is development/provenance mirror.
- Never rebuild existing components before recovery + compatibility audit.
- 2025 remains OOS and cannot be used for tuning.
- Murphy = technical context/market structure evidence.
- Nison = confirmation/contradiction only; cannot create direction alone.
- Trading in the Zone = psychology/process only; cannot create direction.
- Similarity/Historical Memory = historical evidence only; never sole decision maker.
- Risk = hard gate.

### Canonical book status
- Murphy: 35/51 authoritative/frozen; 16 deferred.
- Nison: 44/44 authoritative/frozen.
- Trading in the Zone: 0/7 authoritative currently; 7 deferred.
- Total authoritative: 79/102.
- Total deferred: 23/102.

### Completed
- Rule provenance mapping / 79-rule governance.
- Knowledge Alignment integration test: PASS 6/6.
- Recovered RISK_ENGINE_SPEC_V1: research prototype, not execution ready.
- Knowledge Alignment → Risk compatibility contract.
- Knowledge Alignment → Risk boundary test: PASS 8/8.
- Last clean milestone backup created before Decision Brain audit.

### Key commit pointers
- Murphy reconciliation: 4be77bbb46dd6b2b97bc9b198416620af79e779d
- Nison freeze: 84257ada950ccd1ca5fca0357e0aa6f25d4eb8b3
- Rule Adapter mapping: e631e3f03a9ae52663e70f10272d98069f7baa29
- 79-rule audit: 29e01c8b328d689c96847bdbec2e0d61df944722
- Knowledge Alignment test: 759619ff1f43abf33f66285c5e1c677cfb917f3d
- Risk compatibility contract: 32f9a48c5859a261dee430ee4aef7994dbe0094b
- Risk boundary test: 47ddd6a0c1637490e54fafc40a9ab14b262a9d47

### Current mandatory next sequence
1. Recover original Decision Brain / AI Decision Engine from Workspace, File Library, backups and project assets.
2. Search for decision_brain.py, Decision Brain V1/V1.1, Run 070 wrapper, I/O contracts, tests and integration records.
3. Extract real inputs and outputs; do not infer missing semantics.
4. Audit compatibility with Knowledge Alignment, Risk boundary, Murphy, Nison, Similarity/Historical Memory and process gate.
5. Classify results: COMPATIBLE / ADAPTER_REQUIRED / BLOCKED_PENDING_SOURCE / CONFLICT.
6. Do not modify or rebuild original Decision Brain before audit.
7. After milestone: GitHub commit → verified full backup with manifest → continue.

### Project assets to search
MASTER_KB, 3_BOOK_INTEGRATION, MARKET_READER, MARKET_STATE_READER, MARKET_SCENARIO_ENGINE, MULTI_TIMEFRAME_READER, HISTORICAL_CONTEXT_MEMORY, HISTORICAL_OUTCOME_MEMORY, SIMILARITY_MEMORY, TRUE_BACKTEST_V2, CONTEXT_AWARE_RETRIEVAL, TRADING_RULES, OFFICIAL_BASELINE_AUDIT, VERSION_FREEZE_PLAN, GBPUSD workspace archives and AI Decision Engine/project backup assets.

### Live execution status
NOT EXECUTION READY. Risk prototype still lacks governed costs, spread, slippage, leverage, contract size and broker-specific pip value handling.

### Backup policy
Every completed milestone: commit authoritative artifacts, include actual available snapshots/local artifacts, manifest, commit pointers, SHA-256 and ZIP verification. Never claim a file was fetched when only a pointer is available.
