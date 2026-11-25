# Historical Source Manifest Recovery Audit — 2026-11-25

## Scope and method

GitHub-only, read-only source discovery for the Decision Brain V1 historical 2016-2024 vertical slice. Inspected the repository tree and the existing Gate A source manifest / audit artifacts on PR #118, plus the historical backtest checkpoint and PR #97 / #118 / #137 records.

No Dropbox connection or API was used. No market-data payloads were opened. No 2025/2026 market-data payloads were read. No source code, frozen rule semantics, or data files were changed.

## Primary discovery: a pinned source manifest exists

Recovered from PR #118 branch `audit/gate-a-input-preflight-2026-11-15`:

`BACKTEST/GOVERNED_SOURCE_INPUT_MANIFEST_2016_2024_2026-11-15.json`

The manifest pins seven external source objects by Dropbox path, revision, byte size, and modified time:

| Key | Source role | Pinned object | Size (bytes) |
|---|---|---|---:|
| h1 | GBPUSD H1 bars | `/New 8/GBPUSD_H1_2016_2025_MASTER.zip` | 805,818 |
| murphy | Murphy 34-rule fan-in | `/New 8/MURPHY_HISTORICAL_34_RULE_FANIN_2016_2024.zip` | 314,490 |
| nison | Nison 44-rule evidence | `/New 8/NISON_2016_2024_FULL_EVIDENCE.csv` | 525,483,005 |
| market_state | GBPUSD Market State | `/New 8/GBPUSD_MARKET_STATE 6.csv` | 20,604,225 |
| mtf | Canonical GBPUSD MTF Alignment V1 | `/MTF_ALIGNMENT_GBPUSD_V1.zip` | 80,293,251 |
| historical_context | Historical Context Memory | `.../HISTORICAL_CONTEXT_MEMORY.csv` | 57,552,949 |
| historical_outcome | Historical Outcome Memory | `.../HISTORICAL_OUTCOMES.csv` | 63,287,758 |

The exact revision IDs are preserved in the source manifest. They are not repeated here to avoid creating a second mutable source of truth; the manifest is the canonical pinned record.

**Important distinction:** these are external-source pins recorded in GitHub, not GitHub-hosted data assets. The manifest explicitly records `hashes.status = PENDING_ACTUAL_DOWNLOAD_AND_SHA256`. The metadata pins do not prove file bytes, row contents, source semantics, or current retrievability.

## GitHub-only availability result

The repository's recursive `main` tree contains no raw historical market-data archive matching the seven source objects. The inspected PR #97 head tree likewise contains no raw H1/MTF/Murphy/Nison historical source package; its CSV files are small memory fixtures and rule/audit summaries, not the canonical market series.

PR #118's implementation audit records that the acquisition workflow failed at its first Dropbox API request with HTTP 401. It explicitly says no source files were downloaded, no real CSV rows were parsed, and no SHA-256 values were calculated. Therefore the external pinned source objects cannot be treated as available within the agreed GitHub-only workflow.

## What existing evidence says about the pinned sources

### Gate A input preflight (PR #118)

The existing remediation report states:
- Historical Context: 273,387 rows retained for 2016-2024; 30,805 rows from 2025 excluded.
- Historical Outcome: 273,183 rows retained; 30,805 rows from 2025 excluded; 204 additional late-2024 rows excluded because the 48-hour outcome horizon was not mature by 2025-01-01 UTC.
- Market State: 55,192 rows retained; 6,225 rows from 2025 excluded.
- H1 and Nison passed the recorded input preflight.
- Gate A remained BLOCKED on MTF and Murphy.

These are reported outputs from the historical Gate A run, not a new validation performed by this audit.

### MTF

The existing report records 671,601 rows for 2016-2024, with 2025/2026 annual files excluded. All 671,601 timestamps are timezone-naive and remain `NAIVE_UNRESOLVED`. It records 2,512 blank cells across five regime fields. No timezone normalization, imputation, categorical recoding, or scaling is authorized.

The exact producer/formula lineage for the seven Brain MTF fields remains unresolved. The canonical MTF archive is identified, but its producer semantics are not.

### Murphy

The existing report records 32,400 naive timestamps and 54,825 offset-aware timestamps in the 87,225-row fan-in. The naive records are associated with MURPHY_0021, 0022, 0023, 0028, and 0029; offset-aware records with 0025 and 0026. The manifest's archive creation time does not prove the timezone semantics of event timestamps.

Separately, the historical backtest checkpoint reports that the recovered historical Murphy evidence contained only seven rule IDs (0003, 0004, 0021, 0022, 0023, 0028, 0029), totaling 402,710 normalized rows. PR #97 independently states that the available Murphy fan-in artifact represented only 7/34 decision-eligible rules and correctly failed the official completeness gate. The manifest's filename describing a 34-rule fan-in is not proof that all 34 eligible rule histories are present.

### Historical aggregation

Existing repository records state that GBPUSD 2016-2024 candle aggregation reconciliation has already been completed. This audit does not rebuild or alter that aggregation.

## Source-admission decision

| Gate | Current evidence | Disposition |
|---|---|---|
| Pinned historical source manifest | Exact external paths, revisions, sizes recorded | IDENTIFIED; not GitHub-hosted |
| Actual source bytes / SHA-256 | No source download in Gate A; hash status pending | NOT VERIFIED |
| GitHub-only source availability | No canonical raw source package found in inspected repository trees | BLOCKED |
| H1 input shape | Historical Gate A reports PASS | Prior preflight only; no fresh source verification |
| Nison input shape | Historical Gate A reports PASS | Prior preflight only; no fresh source verification |
| Murphy 34-rule coverage | Historical evidence reports 7/34 eligible rule histories | BLOCKED |
| Murphy timestamp semantics | Mixed naive/offset-aware; authoritative timestamp contract absent | BLOCKED |
| MTF timestamp semantics | 671,601 naive timestamps | BLOCKED |
| MTF producer/formula semantics | Seven Brain fields unresolved | BLOCKED |
| 2025 OOS separation | Manifest and Gate A reports preserve exclusion | KEEP LOCKED |

## Next safe action

Do not write a new historical-source adapter, do not rerun the backtest, and do not reconstruct the candle aggregation.

The next work should remain on GitHub and focus on one of these source-preserving routes:
1. Locate an already committed, authoritative GitHub artifact/Actions artifact containing the exact pinned 2016-2024 source bytes and a verifiable digest; or
2. If no such GitHub artifact exists, record the source-data dependency as an explicit external blocker and proceed only with code/contract tests that do not claim real historical validation.

Before any real-data replay, separately close Murphy 34-rule completeness, MTF producer semantics, and timestamp/availability provenance. Keep 2025 excluded from development, tuning, calibration, and feature selection.

## Governance

- Audit-only; no runtime code, data, frozen knowledge, or risk contracts changed.
- No merge, no main changes, no PR retargeting.
- No Dropbox or CircleCI use.
- No 2025/2026 market-data payloads accessed.
- No live orders or trading authorization.
