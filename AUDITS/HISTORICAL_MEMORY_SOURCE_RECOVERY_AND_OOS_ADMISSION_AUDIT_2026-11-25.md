# Historical Memory Source Recovery and OOS Admission Audit — 2026-11-25

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

The first artifact contains H1, Murphy, Nison, Market State, and MTF source members, as documented in the companion source-admission manifest. The second contains replay outputs, H1, Market State, Murphy, Nison, and MTF members; it does not contain `HISTORICAL_CONTEXT_MEMORY.csv` or `HISTORICAL_OUTCOMES.csv`. The third contains only cost-stress replay outputs and metrics, not the original memory source datasets.

Therefore the GitHub Actions artifacts inspected do not recover the two full memory source CSVs.

## 2. Exact intended source packages recovered from workflow configuration

The current-stack V2 workflow on `current-stack-dev-backtest-2016-2024-v5-1-fix` explicitly downloads these source packages:

- `/ai_trading_assistant_full_project_v1/AI_Trading_Assistant_HISTORICAL_CONTEXT_MEMORY_V1.zip`
- `/ai_trading_assistant_full_project_v1/AI_Trading_Assistant_HISTORICAL_OUTCOME_MEMORY_V1.zip`

After extraction, it expects:
- `HISTORICAL_CONTEXT_MEMORY.csv`
- `HISTORICAL_OUTCOMES.csv`

It also downloads Similarity Memory V2, Context-Aware Retrieval V2, and Market Scenario Engine V1 packages. Those packages are not part of the historical Context/Outcome source recovery and must remain evidence-only/NOT_EVALUABLE if their stored snapshots are OOS-2025.

These exact source package paths are useful provenance references, but because they are external Dropbox paths and no corresponding full source bytes are in the inspected GitHub artifacts, they are not a GitHub-only recoverable source today.

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
| Full Context CSV in inspected GitHub artifacts | NOT RECOVERED |
| Full Outcome CSV in inspected GitHub artifacts | NOT RECOVERED |
| Context/Outcome source SHA-256 | NOT AVAILABLE |
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
