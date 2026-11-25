# Historical Source Manifest Recovery Audit — 2026-11-25

## Scope and method

GitHub-only, read-only source discovery for the Decision Brain V1 historical 2016-2024 vertical slice. Inspected:
- PR #118's pinned source manifest and Gate A reports;
- PR #97's workflow and historical replay;
- GitHub Actions run `35806971916` and its retained source artifact;
- the exact 2016-2024-only Murphy, Nison, and MTF payloads inside that artifact.

No Dropbox connection or API was used in this audit. The source artifact was retrieved through GitHub Actions. Only MTF annual payloads for 2016-2024, the 2016-2024 Murphy evidence CSV, and the 2016-2024 Nison evidence CSV were opened. H1 and Market State payloads were not opened because their source files include 2025; MTF 2025/2026 payloads were not opened. No source code, frozen rule semantics, or source data files were changed.

## Primary discovery: pinned source manifest

Recovered from PR #118 branch `audit/gate-a-input-preflight-2026-11-15`:

`BACKTEST/GOVERNED_SOURCE_INPUT_MANIFEST_2016_2024_2026-11-15.json`

The manifest pins seven source objects by Dropbox path, revision, byte size, and modified time:

| Key | Source role | Pinned object | Size (bytes) |
|---|---|---|---:|
| h1 | GBPUSD H1 bars | `/New 8/GBPUSD_H1_2016_2025_MASTER.zip` | 805,818 |
| murphy | Murphy 34-rule fan-in | `/New 8/MURPHY_HISTORICAL_34_RULE_FANIN_2016_2024.zip` | 314,490 |
| nison | Nison 44-rule evidence | `/New 8/NISON_2016_2024_FULL_EVIDENCE.csv` | 525,483,005 |
| market_state | GBPUSD Market State | `/New 8/GBPUSD_MARKET_STATE 6.csv` | 20,604,225 |
| mtf | Canonical GBPUSD MTF Alignment V1 | `/MTF_ALIGNMENT_GBPUSD_V1.zip` | 80,293,251 |
| historical_context | Historical Context Memory | `.../HISTORICAL_CONTEXT_MEMORY.csv` | 57,552,949 |
| historical_outcome | Historical Outcome Memory | `.../HISTORICAL_OUTCOMES.csv` | 63,287,758 |

The exact revision IDs remain in the manifest. Its `hashes.status` is `PENDING_ACTUAL_DOWNLOAD_AND_SHA256`; the manifest alone does not prove bytes or row semantics.

## GitHub Actions source artifact recovered

A historical GitHub Actions run contains the actual source bundle:

- Workflow run: `35806971916` — **Governed 78-Rule Development Backtest**, run #9
- Source commit: `333795a0a135317619af69fd11f191db595e86a7`
- Artifact: `governed-78-rule-development-backtest`
- Artifact ID: `10728885030`
- Artifact size: 150,865,980 bytes
- Retention expiry reported by GitHub: 2026-12-22
- Run URL: https://github.com/refaey11/AI-Trading-Assistant-Workspace/actions/runs/35806971916

The run's job steps show:
1. **Acquire authoritative governed inputs — SUCCESS**
2. **Validate governed 78-rule evidence envelope — SUCCESS**
3. **Run existing Decision Brain runner with real Murphy + real Nison + existing MTF — FAILURE**
4. **Upload results — SUCCESS**

PR #97 later retrieves this same artifact using `gh run download 35806971916 -n governed-78-rule-development-backtest` and re-uploads its replay package as another GitHub Actions artifact. This confirms a GitHub-only retrieval route exists; it does not require a new Dropbox connection.

### Artifact-to-manifest size reconciliation

The recovered source artifact contains copies of the following objects. Their stored byte sizes match the sizes in the PR #118 pinned manifest:

| Artifact member | Stored bytes | Manifest bytes | Match |
|---|---:|---:|---|
| `source/h1.zip` | 805,818 | 805,818 | YES |
| `murphy/murphy.zip` | 314,490 | 314,490 | YES |
| `nison/NISON_2016_2024_FULL_EVIDENCE.csv` | 525,483,005 | 525,483,005 | YES |
| `market_state.csv` | 20,604,225 | 20,604,225 | YES |
| `mtf/mtf_alignment.zip` | 80,293,251 | 80,293,251 | YES |

This is a strong size-level reconciliation, not cryptographic proof that the artifact bytes correspond to the exact Dropbox revision IDs recorded later in the manifest. The original source acquisition run predates the November manifest and its workflow downloads by path; no immutable Dropbox revision ID is embedded in that run's acquisition step. Exact revision-to-artifact binding therefore remains unverified.

## 2016-2024-only payload checks

The following checks were performed directly against the recovered GitHub artifact. No 2025/2026 payload was opened.

### MTF 2016-2024

Only the nine annual files from 2016 through 2024 were opened:
- Total rows: **671,601**
- Timestamp strings: **671,601 / 671,601 timezone-naive**
- Time range: 2016-01-03 17:00:00 through 2024-12-31 23:55:00
- All seven Brain MTF field names are present:
  `M5_trend_regime`, `M15_trend_regime`, `M30_trend_regime`, `H1_trend_regime`, `H4_trend_regime`, `D1_trend_regime`, `mtf_trend_score`
- Blank cells: M15=26, M30=53, H1=107, H4=371, D1=1,955; total **2,512**

SHA-256 values for the nine 2016-2024 annual files were calculated and are preserved in this audit's source verification record (the hashes are listed below). The MTF producer/formula semantics remain unresolved; field presence and observed values do not authorize recoding, imputation, scaling, or a replacement formula.

### Murphy 2016-2024

The recovered evidence CSV was opened:
- Rows: **87,225**
- Distinct source rule IDs: **7** — 0021, 0022, 0023, 0025, 0026, 0028, 0029
- Status counts: FAIL=55,493; PASS=30,678; NOT_EVALUABLE=1; CONFLICT=1,053
- Timestamp strings: **32,400 naive**, with 54,825 offset-aware

The CSV SHA-256 is `4ecd91b02047d817b5ceeb239e5d76f7d0c8f1c0aefd3de15f38f6bebbd2cfc7`. It exactly matches the `integrity.fan_in_sha256` value embedded in `MURPHY_2016_2024_MANIFEST.json`.

The manifest describes 34 runtime rule IDs, but the evidence CSV contains only seven IDs. Its own per-rule coverage metadata classifies the other histories as unavailable, provisional, or not decision-eligible. The filename and declared runtime rule count must not be mistaken for 34 complete historical evidence streams.

### Nison 2016-2024

The recovered Nison evidence CSV was opened:
- Rows: **2,428,448**
- Distinct rule IDs: **44**
- Timestamp strings: all offset-aware
- Time range: 2016-01-03 17:00:00+00:00 through 2024-12-31 16:00:00+00:00
- SHA-256: `8487d24664de68ad7947ea66e1686437a46cc1a7a433fff930198d531c990a0e`

### SHA-256 for MTF annual files (2016-2024 only)

| Year | SHA-256 |
|---|---|
| 2016 | `677c5d5fc9ce28e4c8067cf08318685e4215e9192c11d6bb0d29b11400a19aca` |
| 2017 | `b5ceebf0cd5f3a662f0d80d4b4334af714e70d4a07182ed4d064d170153102bd` |
| 2018 | `3b6aaf581c5d687d7fcabf482ba50e3512094645a93dc03ec802881e4344340b` |
| 2019 | `c19b23002fa1b3346685fb938346588b54d81f79f16e6429b56c1a20fcf9be9a` |
| 2020 | `ec2e7beb0ffedae1226ee1f6f4039b89f773102da2075081e707aaccb0562521` |
| 2021 | `d397ccd36c2720dfc1a00a9173d803d10724ac6bbc0a2d1d735553bdb4c0a856` |
| 2022 | `6fa1d3a38c7b1141dbfcd547fb6c16db6e3c14a050a76f094298215b8e7617b4` |
| 2023 | `e4b13a9a23e1728e5381e90f73c1fdaae03c01edee78fd3f42b775593ccb0ef8` |
| 2024 | `d108d29afde393ff7f68dcece6e3bc19e861673182ce80d88c67a5c8d32ef7dd` |

## Why the historical backtest run failed

The original run's log records:
- Governed expected rule count: 78
- Nison observed: 44
- Murphy observed: 7
- Missing Murphy rule IDs: 27
- The runner then raised: `ValueError: artifacts/mtf/extracted: no source-backed timeframe trend columns found`

The first failure is an actual data-coverage gap: only 7 of the expected 34 Murphy IDs are present. The second is a runner/source schema incompatibility. The source annual MTF files do contain the seven named fields, but the old runner did not recognize the source layout as a valid timeframe trend input. Neither issue is solved by renaming fields or inventing a conversion.

## Existing source blockers that remain

- **Murphy:** 7/34 expected rule IDs are represented; 27 are missing. The historical evidence must remain limited to the source-backed IDs and cannot be padded.
- **Murphy time:** mixed naive and offset-aware event timestamps; authoritative event timestamp semantics are not established.
- **MTF time:** every 2016-2024 timestamp is naive; broker/session timezone provenance remains unresolved.
- **MTF meaning:** seven serialized Brain fields exist, but exact producer/formula/encoding semantics remain unresolved.
- **H1 and Market State:** matching artifact member sizes are confirmed from ZIP metadata only; their payloads were not opened because they include 2025.
- **Exact external revision binding:** artifact sizes match the later pinned manifest, but the older run acquired by path, so exact Dropbox revision IDs are not independently bound to this artifact.
- **Historical aggregation:** existing GBPUSD 2016-2024 candle aggregation reconciliation is preserved and will not be rebuilt.

## Source-admission decision

| Gate | Current evidence | Disposition |
|---|---|---|
| Pinned source manifest | Exact paths, revisions, sizes recorded in PR #118 | IDENTIFIED |
| GitHub-only artifact availability | Retained GitHub Actions artifact recovered | AVAILABLE |
| Artifact/source size reconciliation | Five principal source objects match manifest byte sizes | PASS_SIZE_ONLY |
| Exact source revision binding | Older run downloads by path, not immutable revision | UNVERIFIED |
| Murphy content integrity | CSV SHA matches embedded manifest SHA | PASS_INTEGRITY |
| Nison content digest | SHA calculated for 2016-2024 evidence CSV | RECORDED |
| MTF 2016-2024 integrity | Annual-file SHA values calculated | RECORDED |
| Murphy 34-rule coverage | Only 7 of 34 IDs present | BLOCKED |
| Murphy timestamp semantics | Mixed naive/offset-aware | BLOCKED |
| MTF timestamp semantics | 671,601 naive timestamps | BLOCKED |
| MTF producer/formula semantics | Seven fields present, producer meaning unresolved | BLOCKED |
| 2025 OOS separation | 2025/2026 payloads not opened in this audit | KEEP LOCKED |

## Next safe action

Do not rebuild candle aggregation and do not run the full backtest yet.

The recovered GitHub Actions artifact removes the prior source-availability blocker for the files it contains. The next work should use this exact GitHub artifact as the immutable working input, preserve its SHA-256 values, and create a separate source-admission manifest on GitHub that:
1. pins the original workflow run, source commit, artifact ID, and expiry;
2. records only the 2016-2024 file hashes above;
3. records H1/Market State as present but not payload-inspected under the 2025 lock;
4. keeps Murphy at 7/34 and MTF time/semantics fail-closed;
5. does not claim a successful strategy backtest or profitability.

Only after these source gates are closed should a separate compatibility patch be considered. The immediate MTF error must be resolved against the actual producer/schema contract, not by guessing field mappings. The Murphy gap requires recovery of approved historical rule sources, not synthetic evidence.

## Governance

- Audit-only; no runtime code, source data, frozen knowledge, or risk contracts changed.
- No merge, no main changes, no PR retargeting.
- No Dropbox or CircleCI use.
- No 2025/2026 market-data payloads opened.
- No live orders or trading authorization.
