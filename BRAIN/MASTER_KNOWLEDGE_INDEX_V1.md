# AI Trading Assistant — Master Knowledge Index V1
Updated: 2026-10-25
Status: WORKING INDEX — NOT YET COMPLETE; missing sources are explicitly marked.

## Purpose
This is the one entry point for the Decision Brain. When asked to analyze a market, consult this index first, then retrieve the actual data, book-derived rules, source provenance, runtime contract, and risk gate. Never treat a filename, manifest, or rule count as proof that its contents were ingested or tested.

## Canonical locations and roles
- **GitHub repository (code, governed rule definitions, tests, provenance, backtest artifacts):** https://github.com/refaey11/AI-Trading-Assistant-Workspace
- **Dropbox (large market-data files and source archives):** private source storage; use exact paths below.
- **ChatGPT analysis:** use only retrieved/verified sources available in the current analysis; if the relevant file cannot be retrieved, report NOT_EVALUABLE rather than pretending it was read.

## Decision contract — must not be bypassed
1. Murphy: market structure/trend context; authoritative set is 34 rules. MURPHY_0008 is blocked.
2. Nison: candlestick confirmation/contradiction only; authoritative set is 44 rules.
3. Mark Douglas, *Trading in the Zone*: discipline/process gate; source ingestion and operational mapping still need verification.
4. Al Brooks: trend/range, pullbacks, breakouts and failures. Treat candidate rules as research hypotheses until mapped to source-backed rules and tested.
5. Similarity/history/memory: supporting evidence only; never determine direction or override a hard gate.
6. Risk Engine: hard veto/gate. No risk pass means no trade candidate may be promoted.
7. No automatic BUY/SELL or live-readiness claim in V1. Final output must state direction/context, evidence, contradiction, invalidation, risk status, source timestamps and missing inputs.
8. 2025 is locked out-of-sample: do not tune parameters, select features or change thresholds based on 2025. Development/calibration is 2016–2023; 2024 is reserved as the development-period OOS check in the current XAU pipeline.

## Source inventory and verification state

### XAUUSD price data
- Dropbox path: `/XAUUSD_M1_MASTER_2016_2026_08_V1.zip` (52,349,241 bytes; modified 2026-08-20). Found by search; payload not yet validated here.
- XAU pipeline expected H1 archive path: `ns:14922141667//XAUUSD_H1_2016_2025_MASTER.zip`. Verify this exact path and the actual archive before running.
- Required checks: file schema, timestamp timezone/duplicates/gaps, OHLC validity, source/timeframe, coverage by year, and separation of development vs locked OOS.

### Multi-timeframe context
- Dropbox path: `ns:14922141667//ai_trading_assistant_full_project_v1/AI_Trading_Assistant_MULTI_TIMEFRAME_READER_V1/XAUUSD_MTF_H4_H1.csv` (8,453,520 bytes; modified 2026-08-19).
- This file was found, but its header/data have NOT yet been read because Dropbox text fetch has a 5 MB limit. Do not assume column aliases match until verified.
- Pipeline expects explicit H1 and H4 trend fields. Never synthesize trend labels from OHLC merely to make the test pass.

### Market-state context
- Dropbox path: `ns:14922141667//ai_trading_assistant_full_project_v1/AI_Trading_Assistant_MARKET_STATE_READER_V1/XAUUSD_MARKET_STATE.csv` (19,560,376 bytes; modified 2026-08-19).
- Found by search; payload not yet inspected. Validate schema, timestamps, provenance, and coverage before use.

### Murphy — 34 rules
- Dropbox: `/New 8/MURPHY_HISTORICAL_34_RULE_FANIN_2016_2024.zip`
- Dropbox: `/AI_Trading_Assistant_FULL_PROJECT_V1/MURPHY_34_SOURCE_BACKED_FANIN_V2_2026-08-28.json`
- Dropbox: `/AI_TRADING_ASSISTANT_MURPHY_34_SOURCE_COVERAGE_LEDGER_2026-08-29.md`
- Dropbox: `/New 8/AI_Trading_Assistant_MURPHY_34_BRAIN_INTEGRATION_STATE_V1.md`
- Known gap: a prior governed backtest attempt saw only 7 observed Murphy rules despite a 34-rule manifest. Resolve actual decision-boundary coverage; names in a manifest are not execution evidence.

### Nison — 44 rules
- Dropbox: `/New 8/NISON_2016_2024_FULL_EVIDENCE.csv` (large file, ~525 MB).
- Dropbox: `/New/NISON_2025_CANDIDATE_STREAM.csv` and `/New 7/NISON_2025_FULL_EVIDENCE 9.csv` are OOS-only evidence; do not use to tune.
- Validate actual 44-rule coverage, timestamps, direction normalization, confirmation timing, and leakage.

### Risk Engine
- Dropbox: `/ENGINE_AUDIT/AI_Trading_Assistant_RISK_ENGINE_V1/RISK_ENGINE_EVENTS.csv`
- Dropbox: `/ENGINE_AUDIT/AI_Trading_Assistant_RISK_ENGINE_V1/RISK_ENGINE_RESULTS.csv`
- Dropbox archive: `/ENGINE_AUDIT/AI_Trading_Assistant_RISK_ENGINE_V1.zip`
- Must prove that the existing authoritative Risk Engine is actually invoked at the final decision boundary; adapter-only risk logic is insufficient.

### Books — required knowledge sources
- John J. Murphy, *Technical Analysis of the Financial Markets*: source file/location and ingestion into governed rule mapping not yet verified in this index.
- Steve Nison candlestick source: exact source edition/file and mapping to the 44 rules must be recorded.
- Mark Douglas, *Trading in the Zone*: Dropbox search returned no match; source availability and ingestion remain unverified.
- Al Brooks, *Trading Price Action Trends* and *Trading Price Action Trading Ranges*: local conversation uploads were previously present (EPUB and PDF), but they are not yet proven to be in the repository or fully indexed into source-backed candidate rules.
- Do not copy entire copyrighted books into a public GitHub repository. Keep lawfully held full-text files in private storage; put concise rule mappings, citations/page references, source hashes, and testable derived logic in GitHub.

## Existing runtime and current work
- Existing Brain/Rule Adapter and structural tests are confirmed by: https://github.com/refaey11/AI-Trading-Assistant-Workspace/blob/main/audits/evidence/EXISTING_BRAIN_ADAPTER_RUNTIME_AND_GAP_RECONCILIATION_2026-08-21.md
- PR #60: runtime wiring; open/unmerged status must be checked before relying on it.
- PR #97: governed backtest gate; open/unmerged status must be checked before relying on it.
- PR #100: XAUUSD evidence pipeline prototype; full workflow has not been confirmed as executed.
- PR #101: pivot look-ahead timing and MTF explicit-column normalization/tests; proposed change only until checks pass and the PR is reviewed.
- Pipeline workflow: manual dispatch only; it is not proof of a completed backtest. Dropbox credential previously returned HTTP 401.

## Required ingestion ledger
For every source, record: stable source ID, exact private path or repository URL, edition/version, file size/hash where feasible, page/row/time coverage, date retrieved, extraction status, rule IDs derived, source citations, tests, and last verified commit.
Use these statuses only: FOUND_NOT_READ, READ_SCHEMA_ONLY, EXTRACTED, RULES_MAPPED, TESTED, APPROVED_FOR_ANALYSIS.
Never promote a source's status without actual evidence.

## Analysis response contract
For every request for a market decision, report:
- Instrument, timeframe, data source and last candle timestamp/freshness.
- Murphy context and which of the 34 rules actually evaluated.
- Nison confirmation/contradiction and which of the 44 rules actually evaluated.
- Brooks evidence only if mapped to a cited source and testable condition.
- Trading-in-the-Zone process/discipline gate.
- Risk Engine result and explicit invalidation.
- Conflicts, missing sources, and status: EVALUABLE or NOT_EVALUABLE.
- Scenario/decision with rationale; never promise certainty or profitability.
