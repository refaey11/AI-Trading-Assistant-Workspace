# Gate A — Governed Source Input Preflight Implementation Audit
Date: 2026-11-15
Branch: audit/gate-a-input-preflight-2026-11-15
Base: current-stack-dev-backtest-2016-2024-v3
Scope: read-only input validation; no strategy, runtime, risk, or OOS changes.

## Result so far

- Added BACKTEST/GOVERNED_SOURCE_INPUT_PREFLIGHT_V1.py.
- Added deterministic unit tests in tests/test_governed_source_input_preflight_v1.py.
- Added a pinned Dropbox source manifest in BACKTEST/GOVERNED_SOURCE_INPUT_MANIFEST_2016_2024_2026-11-15.json.
- Added GitHub Actions workflow .github/workflows/gate-a-governed-source-input-preflight-2016-2024.yml.
- Final suite of 8 deterministic unit tests passed cleanly in PR validation run 43680131731 (no ResourceWarnings); the earlier 8-test run 43680047289 also passed before test-reader cleanup.
- The real-source acquisition step was blocked before downloading any source file because the repository Actions secret DROPBOX_ACCESS_TOKEN returned HTTP 401 Unauthorized.
- No real CSV rows were parsed by this run; no source SHA-256 values are claimed. The pinned Dropbox revision IDs and file sizes were independently confirmed through the connected Dropbox metadata API.

## Pinned sources verified in Dropbox metadata

| Source | Dropbox object | Revision | Size |
|---|---|---|---:|
| GBPUSD H1 master | /New 8/GBPUSD_H1_2016_2025_MASTER.zip | 0165a0f9940d06900000003796dcfe3 | 805,818 |
| Murphy 34 fan-in | /New 8/MURPHY_HISTORICAL_34_RULE_FANIN_2016_2024.zip | 0165a1138e757df00000003796dcfe3 | 314,490 |
| Nison 44 evidence | /New 8/NISON_2016_2024_FULL_EVIDENCE.csv | 0165a107ed6ebfb00000003796dcfe3 | 525,483,005 |
| GBPUSD Market State | /New 8/GBPUSD_MARKET_STATE 6.csv | 0165a0fa0988fbf00000003796dcfe3 | 20,604,225 |
| MTF Alignment V1 | /MTF_ALIGNMENT_GBPUSD_V1.zip | 01659665ff5a6d300000003796dcfe3 | 80,293,251 |
| Historical Context Memory | /AI_Trading_Assistant_FULL_PROJECT_V1/AI_Trading_Assistant_HISTORICAL_CONTEXT_MEMORY_V1/HISTORICAL_CONTEXT_MEMORY.csv | 0165968d9e8017000000003796dcfe3 | 57,552,949 |
| Historical Outcome Memory | /AI_Trading_Assistant_FULL_PROJECT_V1/AI_Trading_Assistant_HISTORICAL_OUTCOME_MEMORY_V1/HISTORICAL_OUTCOMES.csv | 0165968d6978be100000003796dcfe3 | 63,287,758 |

Dropbox metadata confirms these exact objects, revisions, sizes, and modified dates. It does not establish CSV content integrity; SHA-256 is generated only after an actual download.

## What the new preflight checks

- Exact required columns for H1, Market State, MTF, Murphy, Nison, Historical Context, and Historical Outcome.
- Full streaming row scan, not nrows=25.
- File size and SHA-256.
- Timestamp parseability, timezone-naive timestamp detection, chronology, and duplicate timestamps for bar/context sources where timestamps must be unique.
- H1 OHLC numeric/finite values and candle invariants.
- All seven canonical serialized MTF numeric fields; no recoding, imputation, or scaling.
- Development year coverage 2016-2024 for H1, Market State, and MTF.
- Any 2025 H1 rows are counted as excluded OOS rows; any 2025+ row in other development evidence blocks the gate.
- Manifest explicitly records checks not performed and keeps promotion disabled.

This gate returns PASS_INPUT_PREFLIGHT_ONLY, never a backtest PASS. It does not prove producer lineage, as-of join correctness, runtime consumption, risk execution, costs, or profitability.

## Test evidence

PR #118: https://github.com/refaey11/AI-Trading-Assistant-Workspace/pull/118

Final clean 8-test PR validation run: https://github.com/refaey11/AI-Trading-Assistant-Workspace/actions/runs/43680131731

Initial push run (unit tests passed, Dropbox acquisition returned 401): https://github.com/refaey11/AI-Trading-Assistant-Workspace/actions/runs/43679881054

- Run deterministic preflight unit tests: SUCCESS.
- Covered clean source fixture, H1 2025 exclusion, 2025 leakage in non-H1 data, missing MTF numeric field, duplicate H1 timestamp, naive timestamp, invalid OHLC, and correct min/max timestamp bounds for unordered source rows.
- Acquire exact pinned source revisions: FAILURE — HTTP 401 from Dropbox API.
- The failure happened at the first Dropbox metadata request. No source downloads or real-data validation were performed.

## Important upstream blockers found

1. BACKTEST/CIRCLECI_ACQUIRE_GOVERNED_SOURCES.py and .github/workflows/governed-integration-gate-2026-08-28.yml point to an old/non-canonical MTF ZIP path:
   /AI_Trading_Assistant_FULL_PROJECT_V1/AI_Trading_Assistant_MULTI_TIMEFRAME_READER_V1.zip
   The currently verified canonical GBPUSD artifact is:
   /MTF_ALIGNMENT_GBPUSD_V1.zip
   The source-acquisition path must be corrected and the archive contents resolved before the integration gate can be run.
2. BACKTEST/mtf_source_contract_gate_v1.py confirms the seven numeric MTF fields must already be serialized; it deliberately forbids categorical conversion, imputation, and scaling.
3. BACKTEST/DEV_BACKTEST_RUNNER_V1.py currently conflicts with that MTF contract: build_row() converts categorical trend labels to numeric values and initializes missing MTF fields to 0.0. It must not be used as a canonical runner until this conflict is reconciled against the original producer contract.
4. The same runner writes timestamp_asof, lookahead, mtf_consumption, and memory_leakage as literal True, while the inspected implementation does not prove those claims. It also marks costs_applied: false and official_claim_allowed: false. These are diagnostic-only outputs, not validated profitability evidence.
5. BACKTEST/REAL_SOURCE_E2E_SMOKE_CHECK_V2.py reads only the first 25 rows. Its prior result explicitly states that the Nison byte-level join was not executed and that real TIZ boundary execution remained outstanding.

## Next actions

1. Renew the Dropbox API token stored in GitHub Actions repository secret DROPBOX_ACCESS_TOKEN. Do not paste the token into code, chat, workflow YAML, or repository files.
2. Re-run the Gate A workflow so it can validate the pinned Dropbox revisions and calculate actual SHA-256 values.
3. Review the resulting source-input manifest and resolve any real data blockers (timestamp timezone, missing years, duplicate bars, schema drift, 2025 leakage).
4. Correct the MTF acquisition path in a separate reviewed change, without changing MTF feature semantics.
5. Only after Gate A passes, continue the existing real-source Integration Gate and reconcile the MTF producer and canonical risk contract. Do not run the full backtest before those gates pass.

## Governance

- 2025 remains locked OOS and is never used for tuning/calibration/feature selection.
- Similarity V3 remains isolated; no replacement builder is introduced.
- Murphy is technical context; Nison confirmation/contradiction only; TIZ process gate only; memory/retrieval evidence only; risk is a hard gate.
- No changes to Decision Brain V1, risk runtime, SL/TP, position sizing, or existing source archives were made by this Gate A implementation.
- PR #116 remains open and unmerged.
- PR #117 remains a separate documentation-only roadmap.
