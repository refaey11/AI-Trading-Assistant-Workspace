# Trading Decision Brain — Source Registry V1
Updated: 2026-10-25
Status: initial verified source map; not proof that all sources are ingested or executable.

## Purpose
Single registry for ChatGPT analysis and the existing GitHub test/runtime. Link to canonical artifacts; do not copy large datasets or book text into this file. Update status only after reading or running the referenced source.

## Canonical architecture and governance
- Operator contract (same branch): `BRAIN/TRADING_DECISION_BRAIN_OPERATOR_V1.md`
- Existing runtime reconciliation audit (main): `audits/evidence/EXISTING_BRAIN_ADAPTER_RUNTIME_AND_GAP_RECONCILIATION_2026-08-21.md`
  URL: https://github.com/refaey11/AI-Trading-Assistant-Workspace/blob/main/audits/evidence/EXISTING_BRAIN_ADAPTER_RUNTIME_AND_GAP_RECONCILIATION_2026-08-21.md
- Brooks hypothesis catalog (research only): `research/AL_BROOKS_CANDIDATE_RULE_CATALOG_V1.md`
  URL: https://github.com/refaey11/AI-Trading-Assistant-Workspace/blob/codex/governed-backtest-gate-v1/research/AL_BROOKS_CANDIDATE_RULE_CATALOG_V1.md
- Related open PRs to reconcile before any merge: #60 runtime wiring, #97 governed backtest gate, #100 XAUUSD evidence pipeline. Do not assume they are merged or passing.

## Source inventory

### Market data
- Dropbox: `/XAUUSD_M1_MASTER_2016_2026_08_V1.zip` (ZIP, 52,349,241 bytes; modified 2026-08-20). Search found it; payload was not opened/validated in this registry pass.
- Intended development period: 2016–2024, subject to data completeness and timestamp/quality checks.
- 2025 is locked OOS: do not tune, select features, or change thresholds based on it.

### Murphy
- Dropbox: `/New 8/MURPHY_HISTORICAL_34_RULE_FANIN_2016_2024.zip` (ZIP, 314,490 bytes; modified 2026-08-28).
- Dropbox: `/AI_Trading_Assistant_FULL_PROJECT_V1/MURPHY_34_SOURCE_BACKED_FANIN_V2_2026-08-28.json` (JSON, 650 bytes).
- Dropbox: `/AI_TRADING_ASSISTANT_MURPHY_34_SOURCE_COVERAGE_LEDGER_2026-08-29.md`.
- Dropbox: `/New 8/AI_Trading_Assistant_MURPHY_34_BRAIN_INTEGRATION_STATE_V1.md`.
- Authority: 34 Murphy rules. `MURPHY_0008` remains blocked unless a newer verified source explicitly changes that status. Require all expected IDs and source attribution at the decision boundary; fail closed on incomplete coverage.

### Nison
- Dropbox: `/New 8/NISON_2016_2024_FULL_EVIDENCE.csv` (CSV, 525,483,005 bytes; modified 2026-08-28).
- Dropbox: `/New/NISON_2025_CANDIDATE_STREAM.csv` (CSV, 311,302 bytes; modified 2026-08-26).
- Dropbox: `/New 7/NISON_2025_FULL_EVIDENCE 9.csv` (CSV, 58,310,574 bytes; modified 2026-08-27; treat as OOS evidence only, not for tuning).
- Dropbox contains historical closure and compatibility notes under `/AI_Trading_Assistant_BACKUP_2026-08-22/`.
- Authority: 44 Nison rules. Nison is confirmation/contradiction only, not a standalone directional authority. Validate exact canonical rule coverage before runtime use.

### Mark Douglas — Trading in the Zone
- Role: process/discipline/uncertainty gate; not a price predictor.
- Source file not located in this Dropbox title search or verified in the repository during this pass. Prior conversation notes say the book/rules work is incomplete. Status: MISSING/UNVERIFIED as a centralized source.

### Al Brooks — Trading Price Action Trends
- User-provided local EPUB previously available in conversation: `dokumen.pub_trading-price-action-trends-technical-analysis-of-price-charts-bar-by-bar-for-the-serious-trader-original-retailnbsped-1118066510-978-1118066515 2.epub`.
- Repository hypothesis catalog: `research/AL_BROOKS_CANDIDATE_RULE_CATALOG_V1.md`.
- Dropbox canonical book copy not located in title search. Local EPUB content has not been fully ingested into the runtime. Status: candidate source exists in conversation history; persistent repository/storage linkage unverified.

### Al Brooks — Trading Price Action Trading Ranges
- User-provided local PDF previously available in conversation: `dokumen.pub_trading-price-action-ranges-technical-analysis-of-price-charts-bar-by-bar-for-the-serious-trader-9781118172315.pdf`.
- Repository hypothesis catalog: `research/AL_BROOKS_CANDIDATE_RULE_CATALOG_V1.md`.
- Dropbox canonical book copy not located in title search. Local PDF content has not been fully ingested into the runtime. Status: candidate source exists in conversation history; persistent repository/storage linkage unverified.

### Risk Engine
- Dropbox: `/ENGINE_AUDIT/AI_Trading_Assistant_RISK_ENGINE_V1/RISK_ENGINE_EVENTS.csv`
- Dropbox: `/ENGINE_AUDIT/AI_Trading_Assistant_RISK_ENGINE_V1/RISK_ENGINE_RESULTS.csv`
- Dropbox: `/ENGINE_AUDIT/AI_Trading_Assistant_RISK_ENGINE_V1.zip`
- These are discovered artifacts, not proof the current runtime uses the authoritative risk gate. Missing risk inputs must yield NOT_EVALUABLE.

### Existing runtime / tests
- Archived workspace inventory previously confirmed `decision_brain.py`, `decision_brain_v1_1.py`, Rule Adapter, specs, structural tests, precedence tests and attribution artifacts. Current authoritative paths and exact commit alignment still need live verification.
- Known historical gaps to re-test: `current_state` accepted but not consumed; unsafe legacy 102-rule direction semantics; adapter risk logic not a true Risk Engine gate; incomplete final decision-hint/confidence layer.
- Current code must enforce the 79-rule provenance boundary where applicable and preserve `source_rule_id`; do not treat legacy 102-rule registry as active strategies.

## Runtime contract
1. For ChatGPT analysis, use only market bars/screenshots actually supplied or fetched from an authorized current source. State data timestamp, timezone, timeframe and freshness. Do not invent live prices.
2. Record the exact source artifacts read during each analysis separately from this registry.
3. Apply Murphy context -> Nison confirmation/contradiction -> Brooks exploratory lens -> historical memory as evidence only -> Trading in the Zone process gate -> Risk Engine hard gate.
4. If critical bars, costs, contract/tick values, timestamps, or rule coverage are missing, report NOT_EVALUABLE / NO TRADE rather than guessing.
5. Backtest candidate development on 2016–2024 only; preserve 2025 as locked OOS.
6. No automatic BUY/SELL and no profitability/live-readiness claim without reproducible governed tests.

## Verification checklist
- [ ] Fetch and inspect the ZIP manifests and bar schema; verify coverage, duplicates, gaps, timezone, symbol and timeframe.
- [ ] Inspect Murphy fan-in manifest and prove 34/34 IDs (including blocked status) at decision boundary.
- [ ] Inspect Nison canonical 44-rule registry and prove coverage; separate development evidence from 2025 OOS.
- [ ] Locate/attach the source for Trading in the Zone and both Brooks books; extract only permitted working notes/hypotheses, not reproduce book text.
- [ ] Fetch current runtime/adapter files from the active branch; test source authority, current_state consumption, unknown rule rejection, and Risk Engine hard gate.
- [ ] Reconcile PR #60/#97/#100 without merging automatically.
- [ ] Run deterministic tests on development data only, report results and blockers; do not use 2025 for tuning.
