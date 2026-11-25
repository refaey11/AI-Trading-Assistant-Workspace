# Historical Memory Source Recovery and OOS Admission Audit — 2026-11-25

> **Correction / later discovery (2026-11-25):** The initial three-artifact search below was incomplete. A separate retained GitHub Actions artifact, run `33465775090` / artifact `9784863199`, was subsequently recovered. It contains the full `HISTORICAL_CONTEXT_MEMORY.csv` (57,552,949 bytes) and `HISTORICAL_OUTCOMES.csv` (63,287,758 bytes), exactly matching the byte sizes in the pinned source manifest. Therefore the two full memory sources **are present in GitHub Actions storage**. The earlier "NOT RECOVERED" finding below is superseded. However, this artifact also contains 2025/2026 payload members in other source families, and the successful workflow used load-then-filter for memory and extracted the complete MTF archive. No 2025/2026 payload was opened during this later audit. Source availability is now PASS at artifact-member/size level for all seven pinned source families; exact external revision binding remains unverified. Strict 2016-2024-only admission remains BLOCKED until a safe partition is created without reading OOS rows.

## Scope

GitHub-only inspection of the historical-context and historical-outcome source dependencies used by the 2016-2024 current-stack replay. This audit did not access Dropbox, did not open any 2025/2026 market or memory payload, and did not modify runtime code or source datasets.

Inspected:
- retained GitHub Actions artifact `10728885030` (`governed-78-rule-development-backtest`);
- retained GitHub Actions artifact `12577355039` (`decision-brain-backtest-2016-2024`);
- retained GitHub Actions artifact `12575929718` (`decision-brain-cost-stress-2016-2024`);
- current-stack workflow and provider implementation on `current-stack-dev-backtest-2016-2024-v5-1-fix`;
- historical context/outcome compatibility boundary and prior audit records.

Only archive member names and sizes were inspected in the two latter backtest artifacts; no 2025/2026 members were opened.

## 1. GitHub artifact search result

The following artifacts were checked:

| Run | Artifact | Size | Memory source CSVs present? |
|---|---|---:|---|
| 35806971916 | governed-78-rule-development-backtest | 150,865,980 bytes | No |
| 40135868895 | decision-brain-backtest-2016-2024 | 153,318,595 bytes | No |
| 40135868833 | decision-brain-cost-stress-2016-2024 | 2,468,402 bytes | No |
| 33465775090 | current-stack-development-backtest-2016-2024-v2 | 192,659,168 bytes | **Yes — both full memory CSVs** |

The first artifact contains H1, Murphy, Nison, Market State, and MTF source members, as documented in the companion source-admission manifest. The second contains replay outputs, H1, Market State, Murphy, Nison, and MTF members; it does not contain `HISTORICAL_CONTEXT_MEMORY.csv` or `HISTORICAL_OUTCOMES.csv`. The third contains only cost-stress replay outputs and metrics, not the original memory source datasets.

Therefore the first three artifacts do not recover the two full memory source CSVs; the subsequently recovered run 33465775090 does.

## 2. Exact intended source packages recovered from workflow configuration

The current-stack V2 workflow on `current-stack-dev-backtest-2016-2024-v5-1-fix` explicitly downloads these source packages:

- `/ai_trading_assistant_full_project_v1/AI_Trading_Assistant_HISTORICAL_CONTEXT_MEMORY_V1.zip`
- `/ai_trading_assistant_full_project_v1/AI_Trading_Assistant_HISTORICAL_OUTCOME_MEMORY_V1.zip`

After extraction, it expects:
- `HISTORICAL_CONTEXT_MEMORY.csv`
- `HISTORICAL_OUTCOMES.csv`

It also downloads Similarity Memory V2, Context-Aware Retrieval V2, and Market Scenario Engine V1 packages. Those packages are not part of the historical Context/Outcome source recovery and must remain evidence-only/NOT_EVALUABLE if their stored snapshots are OOS-2025.

These exact source package paths are useful provenance references. Run 33465775090 records the same Dropbox paths in its resolved-source manifest and preserves the extracted CSVs inside GitHub Actions artifact 9784863199. The source CSV member sizes match the pinned manifest exactly:
- Historical Context CSV: 57,552,949 bytes.
- Historical Outcome CSV: 63,287,758 bytes.

The original source acquisition was still Dropbox-backed, but the retained GitHub artifact provides a GitHub-only recovery/download route from this point forward. The exact immutable Dropbox revision IDs are not recorded by the September workflow; byte-size match is not cryptographic revision binding.

## 2A. Exact retained artifact recovery and run evidence

The later-discovered artifact is:
- Workflow run: `33465775090` — Current Stack Development Backtest 2016-2024 V2
- Run commit: `7fd6cb8810b63844e0b17a6ef818981d25dc8371`
- Artifact ID: `9784863199`
- Artifact name: `current-stack-development-backtest-2016-2024-v2`
- Artifact size: 192,659,168 bytes
- GitHub run URL: https://github.com/refaey11/AI-Trading-Assistant-Workspace/actions/runs/33465775090

The GitHub job completed successfully. Its logs explicitly show successful source acquisition, memory path resolution, replay invocation, replay-manifest validation, and artifact upload. The resolved paths point to the two full memory CSVs named above.

Archive-member metadata shows:
- `source/memory/historical_context/HISTORICAL_CONTEXT_MEMORY.csv`: 57,552,949 bytes.
- `source/memory/historical_outcome/HISTORICAL_OUTCOMES.csv`: 63,287,758 bytes.
- Both sizes exactly match the pinned November source manifest.

Only archive member names, byte sizes, README/contract metadata, and CSV headers were inspected. No memory CSV payload rows were opened. The context index metadata includes last-seen dates in 2025, confirming that the full source spans the locked OOS year; no index rows were used as strategy evidence.

The artifact also contains extracted MTF annual members for 2016 through 2026. The 2025/2026 members were not opened. This makes the artifact a recoverable source container, not a clean 2016-2024-only dataset.

## 3. Critical 2025 read-boundary finding

The current-stack V2 workflow and its replay code do not enforce the strongest form of the user's 2025 lock:

- The workflow downloads and unzips the full H1 source named `GBPUSD_H1_2016_2025_MASTER.zip`.
- It downloads and unzips the full Historical Context and Historical Outcome packages.
- The current-stack replay loader calls `read_csv` on the full context and outcome files, parses all timestamps with `pd.to_datetime(..., utc=True)`, and only afterward filters rows to `timestamp.dt.year <= 2024`.
- The H1 runner likewise loads the source before applying its 2016-2024 year filter.

Consequently, the code's final replay window may be 2016-2024, but the loader still reads the full source files before excluding 2025. That is not equivalent to never reading 2025 payload rows. This audit did not run that workflow or inspect the excluded rows.

**Disposition:** do not dispatch the current-stack V2 workflow under the strict 2025 no-read requirement. Do not use it as proof of OOS isolation.

A future approved implementation must select 2016-2024 source partitions before opening payload rows, or use an upstream source package that is physically partitioned to 2016-2024. A post-load DataFrame filter is insufficient.

## 4. Timestamp provenance issue

The current-stack memory provider and replay loaders use `pd.to_datetime(..., utc=True)`. This converts timezone-naive timestamps by assigning UTC semantics. The current source manifest does not establish that naive context/outcome timestamps are UTC or provide broker/session timezone provenance.

Do not normalize naive memory timestamps to UTC unless the source contract independently establishes their meaning. A strict source admission gate must reject unresolved naive timestamps or retain them as unresolved without joining them to UTC event streams.

## 4A. What the successful replay actually proves

Run `33465775090` completed all current-stack workflow steps successfully, including:
- component completeness gate;
- runtime wiring gate;
- governed source acquisition;
- Murphy and MTF source resolution;
- memory source resolution;
- replay invocation;
- validation-manifest check;
- artifact upload.

The artifact's runtime-wiring record states that the historical memory provider was invoked and historical evidence injected. This proves the old replay had a memory-wiring path for GBPUSD; it does not prove strict OOS source isolation or production readiness.

The replay's own output reports:
- 30,678 candidate events;
- 29,163 evaluated events;
- 66 simulated trades;
- 29 wins / 37 losses;
- 43.94% win rate;
- 1.57 profit factor;
- +0.318 R expectancy;
- +21 R total;
- -19 R max drawdown.

These figures are **diagnostic-only historical output**, not an official backtest or a profitability claim. The same output explicitly records `costs_applied=false`, `official_profitability_claim=false`, and only **7 source-backed Murphy rules observed** despite a 34-rule registry. It also records that the replay used a GBPUSD-only path.

The validation JSON's `window_2016_2024_only=true` and `future_data_used=false` are output assertions. They do not override the code-level finding that full source files were loaded before the 2025 filter. Consequently these metrics cannot be promoted as evidence of a compliant 2016-2024 OOS-isolated evaluation.

## 5. Existing memory semantics preserved

The existing Historical Outcome Memory compatibility audit says:
- Historical Outcome Memory is descriptive forward-return evidence at 6, 12, 24, and 48 H1-bar horizons.
- It is not a probability guarantee, trade rule, or direction source.
- 2025 is protected OOS.
- Outcome-to-Scenario BULL/BASE/BEAR boundaries and uncertainty formula are not frozen and must not be invented.

The existing memory provider also documents:
- Historical Context uses strictly prior observations.
- Historical Outcome evidence requires the full 48-hour horizon to have elapsed.
- Similarity, retrieval, and scenario snapshots are stored OOS-2025 snapshots and are explicitly returned as NOT_EVALUABLE in the 2016-2024 replay.

Those semantics should be preserved; this audit does not authorize new scenario labels or direction generation.

## 6. Source-admission status

| Gate | Result |
|---|---|
| Exact Historical Context package path | IDENTIFIED |
| Exact Historical Outcome package path | IDENTIFIED |
| Full Context CSV in retained GitHub artifact 9784863199 | RECOVERED; exact manifest byte-size match |
| Full Outcome CSV in retained GitHub artifact 9784863199 | RECOVERED; exact manifest byte-size match |
| Context/Outcome source SHA-256 | NOT CALCULATED — would require opening full files containing OOS records |
| Physical 2016-2024-only memory partitions | NOT VERIFIED |
| 2025 no-read behavior in current-stack V2 | FAIL — load-then-filter |
| Naive timestamp timezone provenance | UNRESOLVED |
| Outcome horizon maturity rule | EXISTING 48-hour gate; preserve |
| Outcome-to-Scenario policy | NOT FROZEN; do not infer |
| Similarity/Retrieval/Scenario 2025 snapshots | NOT_EVALUABLE for development replay |

## 7. Next safe action

The next step is not to rerun or patch the old workflow. It is to recover a **physically 2016-2024-only** Context Memory and Outcome Memory source through an already retained GitHub artifact or a new approved GitHub-hosted source artifact, with:
1. exact source identity and immutable revision provenance;
2. SHA-256 calculated over the exact 2016-2024 source files;
3. timestamp semantics explicitly established (no silent UTC assignment);
4. a source manifest proving that 2025 rows were not included in the opened payload;
5. schema and 48-hour outcome maturity checks.

If no such GitHub-hosted source exists, record the two memory datasets as external source blockers. Do not use Dropbox, CircleCI, synthetic fixtures, or the old load-then-filter workflow to claim the source gate is closed.

## Governance

- Audit/report only; no source code or data files changed.
- No Dropbox or CircleCI used.
- No 2025/2026 payload rows opened.
- No main changes, no merge, no live trading or order execution.
