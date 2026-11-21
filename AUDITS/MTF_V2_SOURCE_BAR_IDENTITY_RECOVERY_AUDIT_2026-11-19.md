# MTF Pivot V2 — Source-Bar Identity Recovery Audit

**Date:** 2026-11-19  
**Status:** BLOCKED — no authoritative stable source-bar ID contract recovered  
**Scope:** GitHub-only inspection of existing MT5 raw capture, six-timeframe source adapter, producer-to-feature lineage, and V2 evidence envelope contracts  
**Parent:** PR #141

## 1. Executive finding

The accessible repository contracts do not currently expose a canonical, immutable `source_bar_id` for each source candle across M5, M15, M30, H1, H4, and D1.

The approved Pivot V2 identity ingredients therefore cannot yet be populated from a verified upstream source identity contract. The new `mpv2_` reference encoder must remain isolated and must not be called with a fabricated source-bar ID.

This is a source-contract gap, not permission to invent a key from row order, an unverified timestamp, OHLC values, or a dataframe index.

## 2. Existing source contracts inspected

### 2.1 MT5 Raw Capture V1.3 — PR #131

Inspected:
- `RUNTIME/MT5_RAW_CAPTURE_V1_3/MT5_Raw_Capture_Only_V1_3.mq5`
- `RUNTIME/MT5_RAW_CAPTURE_V1_3/mt5_raw_capture_contract_v1_3.py`
- `RUNTIME/MT5_RAW_CAPTURE_V1_3/mt5_csv_ingest_v1_3.py`
- `RUNTIME/MT5_RAW_CAPTURE_V1_3/test_mt5_raw_capture_v1_3.py`

Observed fields include:
- `symbol`, `timeframe`;
- `bar_time_epoch_seconds_raw`;
- `bar_time_source_clock=MT5_MQLRATES_DATETIME_RAW`;
- `bar_time_utc_status=UNVERIFIED`;
- `broker_server_id`, `source_id`, `capture_version`;
- closed-bar flag and OHLC/volume/spread;
- row `payload_hash`.

Important distinctions:
- `source_id` is built from terminal name and terminal path. It identifies a capture environment, not one candle.
- The EA preserves raw `MqlRates.time` and explicitly labels it UNVERIFIED; it does not produce a verified UTC candle identity.
- CSV ingest deduplicates by (symbol, timeframe, raw epoch seconds), and rejects conflicting payload hashes for that key. This is a duplicate-detection key, not a separately governed source-bar identity contract.
- The payload hash covers the row payload, including observed capture metadata. It is an integrity digest, not a stable candle ID.
- The raw epoch cannot be treated as UTC or used as a globally canonical time identity under the current clock gate.

Conclusion: V1.3 does not supply the approved `source_bar_id`.

### 2.2 Six-Timeframe Source Adapter V1 — PR #136

Inspected:
- `BACKTEST/MTF_SIX_TF_SOURCE_ADAPTER_V1.py`
- `BACKTEST/test_mtf_six_tf_source_adapter_timestamp_v1.py`

Observed:
- Adapter inventories raw OHLC CSV sources for GBPUSD and M5/M15/M30/H1/H4/D1.
- It accepts timestamp/datetime or date+time columns only when timestamps carry explicit offsets, then normalizes them to UTC.
- It checks sampled duplicate timestamps, OHLC presence/numeric validity, source hashes, and source timeframe/symbol scope.
- It does not emit a stable per-bar ID or define source-bar identity serialization.
- The adapter's whole-file SHA-256 identifies a file artifact, not an individual source candle.

Conclusion: it validates timestamped OHLC source inventory but does not provide the required `source_bar_id`.

### 2.3 Producer-to-Feature Lineage V1 — PR #133

Inspected:
- `RUNTIME/MTF_PRODUCER_V1/producer_feature_lineage_contract_v1.py`
- `RUNTIME/MTF_PRODUCER_V1/MTF_PRODUCER_FEATURE_LINEAGE_CONTRACT_V1.md`

The lineage identity tuple is:
`symbol`, `timeframe`, `bar_time_utc`, `source`, `producer`.

It verifies aware timestamps, payload hashes, exact raw input references, and as-of causality. It does not include a `source_bar_id` field or define a canonical ID for one raw bar. The contract also explicitly does not turn V1.3 raw epoch values into UTC.

Conclusion: useful payload lineage, but no stable source-bar ID contract.

### 2.4 MTF V2 Evidence Envelope Gate — PR #140

Inspected:
- `RUNTIME/MTF_PRODUCER_V2/mtf_v2_evidence_envelope_gate_v1.py`

It checks envelope metadata, source and clock evidence SHA-256 shape, explicit-offset timestamps, row index continuity, bar open/close/availability ordering, and exact six-timeframe coverage.

It does not authenticate clock evidence, recompute the underlying source payload hash, or require a per-row stable source-bar ID.

Conclusion: structural evidence-envelope validation is not source-bar identity.

## 3. Compatibility with approved Pivot V2 identity encoding

The approved pivot identity requires six canonical fields:
- configuration fingerprint;
- detector version;
- pivot kind;
- original source-bar identity;
- canonical symbol;
- canonical timeframe.

The encoder deliberately rejects missing/empty values and does not normalize source identity, symbol, or timeframe. That is correct fail-closed behavior. However, the upstream contracts currently inspected do not prove the required source identity field.

Do not fill `source_bar_id` with:
- MT5 terminal `source_id`;
- raw `MqlRates.time` while clock status is UNVERIFIED;
- row number, dataframe index, or file position;
- rounded OHLC/price;
- whole-file hash or per-row payload hash;
- a guessed concatenation of fields not yet approved as the source identity contract.

## 4. Required upstream contract before production IDs

A separate source-data contract must be proposed and approved before any production `mpv2_` IDs can be issued. At minimum it must define:

1. Authoritative source identity namespace and producer/version.
2. Canonical symbol and timeframe values, with no ambiguous aliases.
3. An immutable per-bar identity that survives file reordering and deterministic replay.
4. The relationship between the immutable bar identity and verified bar-time/clock evidence.
5. Uniqueness scope (at minimum source namespace + symbol + native timeframe).
6. Exact serialization and hash/version rules if the source identity itself is generated rather than supplied by the upstream platform.
7. Duplicate/revision behavior: whether a corrected candle is a new revision, a rejected mutation, or a separately versioned source record.
8. Six-timeframe conformance fixtures, including duplicate, reordered, missing, conflicting, and cross-source bars.

The contract must preserve the distinction between an immutable source-bar identity and a timestamp. A verified UTC timestamp may be part of lineage, but it must not silently replace a source identity unless that design is explicitly reviewed and approved.

## 5. Current eligibility decision

| Input | Current finding | Pivot identity use |
|---|---|---|
| MT5 V1.3 `source_id` | Terminal environment identifier | BLOCKED |
| MT5 V1.3 raw epoch | Explicitly UNVERIFIED clock value | BLOCKED |
| MT5 V1.3 payload hash | Whole row integrity digest | Not a source ID |
| MTF adapter timestamp | Explicit-offset UTC-normalized timestamp | Lineage only; not source ID |
| MTF adapter file SHA-256 | Whole file artifact digest | Not a source ID |
| Producer lineage identity tuple | Symbol/TF/UTC time/source/producer | Useful lineage tuple; no canonical source-bar ID |
| V2 evidence envelope | Structural row/clock checks only | Not a source ID |

**Decision:** keep production pivot identity generation blocked until an authoritative source-bar identity contract is available and reviewed. The isolated reference encoder and its synthetic test vectors remain valid as a serialization demonstration only; they do not establish upstream source identity.

## 6. Scope and safety

- GitHub repository content and existing PR branches only.
- No Dropbox, web, or external source access.
- No 2025 data or tuning.
- No change to legacy PIVOT_SEQUENCE_V2.
- No pivot detector implementation or L/R selection.
- No Decision Brain integration, signal generation, or order path.
- No PR merge and no main-branch change.


## 7. Follow-up source inspection — 2026-11-21

This follow-up re-fetched the exact implementation files from the head branches of PRs #131, #133, #136, and #140. The findings below are tied to the inspected branch content and blob SHAs so the conclusion is auditable.

| PR / file | Inspected blob SHA | Relevant lines / fields | Identity finding |
|---|---|---|---|
| #131 `RUNTIME/MT5_RAW_CAPTURE_V1_3/MT5_Raw_Capture_Only_V1_3.mq5` | `a79b173adf06c9caaf3a3288e5a3f8504a56e6f2` | 34, 61–72 | Uses `MqlRates`; writes raw epoch and explicitly labels it `UNVERIFIED`. No native per-bar ID field is emitted in this file. |
| #131 `RUNTIME/MT5_RAW_CAPTURE_V1_3/mt5_raw_capture_contract_v1_3.py` | `8474543c7465431a8a29fb1d106ec5621826e991` | 9, 30–31, 39–57, 73–75 | Defines row `payload_hash` and raw epoch; explicitly forbids UTC alignment fields and requires `UNVERIFIED`. No `source_bar_id` contract appears in this file. |
| #133 `RUNTIME/MTF_PRODUCER_V1/producer_feature_lineage_contract_v1.py` | `a4cb1c44d01725cc9e5f60ae1f1d83e9a049c0ee` | 11, 23–32, 43, 91–123 | Identity tuple is `symbol,timeframe,bar_time_utc,source,producer`; raw inputs are matched by payload hash and lineage tuple. No immutable per-bar ID field is defined. |
| #136 `BACKTEST/MTF_SIX_TF_SOURCE_ADAPTER_V1.py` | `c79c73851bd100990aa9ec18a462a028c819267b` | 6, 24, 57–86, 97–99, 217 | Rejects timezone-naive timestamps and normalizes explicit-offset timestamps to UTC; inventories timestamps and duplicate samples. No per-bar ID emission or serialization is present in this adapter. |
| #140 `RUNTIME/MTF_PRODUCER_V2/mtf_v2_evidence_envelope_gate_v1.py` | `c41eecd5b5c463857b2b81ac8b6a0b21a5dc2039` | 3, 29–30 | Gate describes envelope shape, aware timestamps, availability ordering, and explicit UTC offsets. It is not a source-ID authenticator or per-bar identity issuer. |

### 7.1 Search and scope limitations

- GitHub code-search queries for `source_bar_id`, `bar_id`, `candle_id`, and `source identity` returned no indexed matches in the connected search surface.
- That search surface is limited to the default-branch code index; zero results do **not** prove that no identifier exists in every branch, historical commit, unindexed path, external provider, or uninspected artifact.
- The stronger positive findings above come from direct inspection of the exact PR-head files and their blob SHAs, not from treating zero search results as proof of absence.
- The four PRs' changed-file inventories were also checked. Their relevant changed-file sets contain the implementation/contract files listed in Sections 2 and 7; this does not constitute a complete repository-wide inventory of every historical or external data producer.

### 7.2 Updated conclusion

Within the directly inspected source contracts, no authoritative immutable upstream-native per-bar identifier has been demonstrated. This is sufficient to keep source identity blocked; it is **not yet sufficient to authorize Model B**. The Model A-first / conditional Model B policy remains unchanged.

Before Model B can be considered, the project must establish—through a bounded inventory of all relevant in-repository producers and source artifacts, plus source-backed evidence where available—that no suitable native identifier exists. Only then may the separate Model B prerequisites be specified, reviewed, tested, and explicitly approved.

No source identity implementation, timestamp promotion, pivot detector implementation, L/R selection, Brain integration, 2025 use, merge, or order path is authorized by this follow-up.


## 8. Expanded in-repository capture inventory — 2026-11-21

This pass extended the source-bar identity review to the earlier MT5 capture generations and reconciled the pre-existing GitHub-only branch-tree audit. It remains a GitHub-only inspection; no Dropbox/external archive retrieval or workflow that downloads external content was performed.

### 8.1 MT5 capture generations directly inspected

| Generation / PR | File | Inspected blob SHA | Relevant identity/clock evidence |
|---|---|---|---|
| Raw Capture V1 / PR #123 | `RUNTIME/MT5_RAW_CAPTURE_V1/MT5_Raw_Capture_Only_V1.mq5` | `7d0508bb7af3d0fbf89e114653f2ad72f5ec5c86` | Lines 15–48 track seen bars in memory by symbol/timeframe and datetime; lines 53–59 read MqlRates and form a symbol/timeframe key; lines 74, 97–100 expose terminal-derived `source_id` and bar-time column. No immutable native per-bar ID is emitted. |
| Raw Capture V1 / PR #123 | `RUNTIME/MT5_RAW_CAPTURE_V1/mt5_raw_capture_contract_v1.py` | `593b1648cb08604e8edf31436b7ac1484b4453bd` | Lines 3, 23, 30–38 parse the bar timestamp as UTC-aware; lines 54–66 define payload hash and capture fields; lines 119–128 deduplicate by (symbol, timeframe, timestamp) plus payload hash. No per-bar ID field is defined. The timestamp's UTC assertion is not independently authenticated by this contract. |
| Forex Capture V1.1 / PR #124 | `RUNTIME/MT5_FOREX_ONLY_CAPTURE_V1_1/MT5_Forex_Only_Raw_Capture_V1_1.mq5` | `0c20451c27c3f760876eb7b24d8d8a9687549d43` | Lines 16–58 track seen bar times; lines 63–68 read MqlRates and key symbol/timeframe; lines 84, 107–110 use terminal-derived `source_id` and timestamp field. No immutable per-bar ID is emitted. |
| Forex Capture V1.2 / PR #125 | `RUNTIME/MT5_FOREX_ONLY_CAPTURE_V1_2/MT5_Forex_Only_Raw_Capture_V1_2.mq5` | `c40d7df0b8c8ce09db474ba658f67a582b1e3712` | Lines 16, 77–100 track seen bar times; lines 113–118 read MqlRates and form symbol/timeframe key; lines 134, 157–160 use terminal-derived `source_id` and timestamp field. No immutable per-bar ID is emitted. |
| Raw Capture V1.3 / PR #131 | `RUNTIME/MT5_RAW_CAPTURE_V1_3/MT5_Raw_Capture_Only_V1_3.mq5` | `a79b173adf06c9caaf3a3288e5a3f8504a56e6f2` | Lines 13–37 track seen times per symbol/timeframe; lines 34–37 read MqlRates; lines 50, 61–65 emit terminal-derived `source_id` and raw epoch/status fields; lines 69–77 explicitly preserve raw time as UNVERIFIED. No immutable per-bar ID is emitted. |
| Raw Capture V1.3 / PR #131 | `RUNTIME/MT5_RAW_CAPTURE_V1_3/mt5_csv_ingest_v1_3.py` | `27262e0571de7163478d42ec234920a4b65f2d38` | Lines 42–46 use (symbol, timeframe, raw epoch) for duplicate detection and add `payload_hash`. This is an ingest dedup key plus integrity digest, not a separately governed immutable source-bar identity. |

### 8.2 Interpretation across capture generations

- Across the directly inspected V1, V1.1, V1.2, and V1.3 MQL5 capture implementations, no authoritative upstream-native immutable per-bar identifier is emitted.
- The `source_id` in these capture generations is derived from terminal name/path and identifies the capture environment, not an individual candle.
- The in-memory `g_seen_bar_times` / symbol-timeframe key prevents repeated writes during capture; it is not a persistent source identity contract.
- V1/V1.1/V1.2 use a timestamp-shaped field and a timestamp-based duplicate key. Their UTC labeling is not itself proof of broker timezone/DST lineage. V1.3 deliberately corrects this uncertainty by preserving raw MqlRates time as UNVERIFIED; it must not be silently promoted to verified UTC.
- Payload hashes are integrity/conflict evidence. They are not stable candle IDs and remain Model C-rejected for identity purposes.
- Forex-only filtering in V1.1/V1.2 changes symbol selection, not per-bar identity semantics.

### 8.3 Prior branch-tree audit reconciliation

PR #137's GitHub-only audit records recursive branch-tree inspection of 16 named branches, including the historical MTF producer search, MTF archive audit, MTF V1 design/contract, MT5 V1 capture, runtime integration, and older decision-stack branches. It found readers/adapters/validators/specifications but no executable Market Structure / six-timeframe numeric feature producer. This follow-up additionally inspected the exact MT5 V1, V1.1, V1.2, and V1.3 capture files above.

The branch inventory was bounded to named branches and PR heads relevant to MTF/MT5/source/capture work. It is not a claim that every branch, every historical Git object, every unindexed artifact, or every external data provider has been exhaustively enumerated. PR #137 itself notes that its code-search zero-results are not proof of global absence. No Dropbox-based workflow was run.

### 8.4 Updated Model A / Model B gate

**Current result:** No suitable upstream-native immutable per-bar ID has been demonstrated in the directly inspected MT5 V1–V1.3 capture implementations or the previously audited MTF source contracts. This strengthens the evidence that the current MT5 capture path does not provide Model A, but it does not prove that every possible upstream/provider-native ID is unavailable.

Therefore:
1. Keep Model A preferred; if the eventual upstream data source exposes an authoritative native bar ID, recover and validate it before considering a composite.
2. Do not treat terminal `source_id`, `g_seen_bar_times`, timestamp dedup keys, payload hashes, row indices, OHLC, or the V1.3 raw epoch as native IDs.
3. Model B remains **NOT AUTHORIZED** until the actual source/provider boundary and clock evidence are established, the absence of a suitable native ID is proven for that selected source, and the full Model B contract is separately reviewed, tested, and explicitly approved.
4. No concrete composite ID, source timestamp promotion, or pivot identity generation is implemented by this inventory.

No 2025 use, tuning, source/runtime change, Pivot Detector implementation, Brain integration, merge, or order path is authorized by this follow-up.



## 9. Recovered original workspace archive — provider/source lead (2026-11-21)

A previously committed read-only GitHub Actions workflow in PR #116 was located and its completed run and artifact were inspected:

- Workflow: **MTF Producer Lineage - Recovered Workspace Archive**
- Run: [43676124722](https://github.com/refaey11/AI-Trading-Assistant-Workspace/actions/runs/43676124722)
- Result: completed / SUCCESS; all six workflow steps completed successfully.
- Artifact: `recovered-workspace-mtf-producer-lineage`, artifact ID `14146273673`.
- Artifact SHA-256: `6d364bc7c5f0bcbd78a29c870468d8dcab0e9de9df2097947f76c912258103e8`.
- The workflow downloaded and reassembled the three-part `GBPUSD_RULE_EVALUATOR_V2_WORKSPACE` backup from the repository's `workspace-v1` release, then scanned the extracted workspace read-only.

### 9.1 Inventory result

The generated report records:
- 241 files in the recovered workspace;
- 211 text files scanned;
- 94 candidate files containing relevant MTF / structure / timeframe / OHLCV terms;
- only four Python files in the recovered workspace inventory, all named Murphy evaluator modules:
  - `MURPHY_EVALUATORS_V1/murphy_0003_0004_evaluator.py`
  - `MURPHY_EVALUATORS_V1/murphy_0021_0023_evaluator.py`
  - `MURPHY_EVALUATORS_V1/murphy_0027_0029_evaluator.py`
  - `MURPHY_EVALUATORS_V1/murphy_0050_evaluator.py`

The inventory is primarily contracts, manifests, evaluation outputs, and precomputed indicator/structure files. It does not identify the original general Market Structure / six-timeframe MTF numeric producer or its exact `mtf_trend_score` formula. This is bounded to the contents of this recovered workspace backup; it is not an exhaustive inventory of every separately released data archive or external source.

### 9.2 Provider clue — strictly scoped

The recovered file-search report contains this exact line from `OBV_V1_OUTPUT/OBV_CONTRACT_V1.json` (line 5):

```json
"source_volume": "TitanFX M1-derived timeframe volume, 2020-2024"
```

This is positive evidence that the OBV contract attributes its M1-derived timeframe-volume input for 2020–2024 to **TitanFX**. It is a useful upstream-provider lead, but its scope is explicitly the OBV volume path. It does **not** prove that:
- all historical M1 OHLC candles in the separately released master archives came from TitanFX;
- the current/live MT5 feed uses TitanFX;
- the broker server, symbol mapping, timezone/DST policy, or immutable per-bar ID is established;
- TitanFX exposes a provider-native immutable candle ID.

The recovered-workspace workflow did not download or inspect the separately released `GBPUSD_M1_MASTER_2016_2026_V1.zip` asset or the live MT5 source boundary. The provider identity for the canonical historical OHLC master and live capture therefore remains UNRESOLVED.

### 9.3 Updated source-identity decision

1. Record TitanFX as a **documented volume-source lead for the OBV 2020–2024 path only**, not as the proven canonical source for every M1 OHLC archive or live MT5 capture.
2. Do not promote this clue into a source namespace, clock policy, native candle ID, or Model B composite key.
3. Continue to prefer Model A if the selected upstream source exposes an authoritative native per-bar ID.
4. Before any Model B consideration, identify the actual provider/feed and source boundary for the selected historical OHLC master and live capture separately; then establish clock provenance, native-ID availability/absence, uniqueness, revisions, and serialization under the previously approved gates.
5. The recovered workspace scan is read-only and does not change the existing 2016–2024 candle aggregation reconciliation.

No 2025 data was used for tuning, calibration, feature selection, or evaluation. No source/runtime change, ID generation, pivot detector implementation, Brain integration, merge, or order path is authorized by this follow-up.


## 10. Direct inspection of annual HistData GBPUSD M1 release archives — 2026-11-21

A bounded, read-only GitHub Actions inspection downloaded only the explicitly named annual GBPUSD M1 release assets for 2016–2019 and 2021–2024. It did not download or inspect 2025/2026 data and did not download the separate combined master archive.

### 10.1 Exact assets and integrity

Workflow: [MTF Producer V2 Prototype Tests — run 44869552965](https://github.com/refaey11/AI-Trading-Assistant-Workspace/actions/runs/44869552965), job `histdata-archive-forensics`, completed SUCCESS. The workflow verified each downloaded archive against the release API's SHA-256 digest before inspecting it.

| Year | Release asset | SHA-256 |
|---|---|---|
| 2016 | `HISTDATA_COM_MT_GBPUSD_M12016.zip` | `f9cc08e01cb7d4bc65fbcb8783b6bca6b57d7ab5891c4b2899c39514a82cd326` |
| 2017 | `HISTDATA_COM_MT_GBPUSD_M12017.zip` | `39758f62fdd7c9760950541fa119c0bac2f0a0c3eb1645b9e71ac1034844aabe` |
| 2018 | `HISTDATA_COM_MT_GBPUSD_M12018.zip` | `a1c66aca1aeec78e60c9aba633953f28c268b209015e786d7bef705ab59d03a1` |
| 2019 | `HISTDATA_COM_MT_GBPUSD_M12019.zip` | `1f0b275f21fba5cdc230a6a436aceaf039b11139b16e22814ad2b18dfc2c3bda` |
| 2021 | `HISTDATA_COM_MT_GBPUSD_M12021.zip` | `3a4c2f5ac875f20bbee6891370a6a85163f2f1d76ddfe0b3dcaa704e8b83e07c` |
| 2022 | `HISTDATA_COM_MT_GBPUSD_M12022.zip` | `dc8848671a1c3b757aa9fcc9e81c8b94f9f950badf8aeb751d516ec239c95cfa` |
| 2023 | `HISTDATA_COM_MT_GBPUSD_M12023.zip` | `a15a061d5f6f58fa9119ca9f134bab5203c554a84d1f0adf43aa7f633eec347f` |
| 2024 | `HISTDATA_COM_MT_GBPUSD_M12024.zip` | `323137222c00e071e706863ab587234dbc6ba305ffbf6d01e0f36a468347f68e` |

For each year, the archive contains a `DAT_MT_GBPUSD_M1_<year>.csv` file and a companion `.txt` metadata file. The CSV files contain seven comma-separated fields in the inspected first/last records: date, time, OHLC, and volume; no separate per-row immutable identifier field appears in that observed record format. The companion metadata files begin with `HistData.com (c) 2012`, directly attributing these annual archives to HistData.com.

The metadata scan searched all non-empty companion-text lines for provider, GMT/UTC, timezone, DST, offset, server, broker, date/time, format, and tick-interval terms. It found the HistData attribution and average/maximum tick interval summaries, but no explicit GMT/UTC timezone, DST, broker-server, or clock-offset declaration. This is a bounded text/keyword finding, not proof about every HistData product or provider interface.

### 10.2 Clock and identity findings

- The observed CSV records are date/time + OHLC + volume only; no native immutable per-bar ID is exposed in this file format.
- The timestamps have no explicit UTC offset in the inspected CSV record representation. The companion metadata scan did not recover an authoritative timezone/DST/clock contract.
- The varying first-record wall-clock times across years (for example 17:00, 02:00, and 18:04) are observations only; they must not be interpreted as UTC or used to infer a timezone/DST rule.
- Therefore these annual archives establish a HistData.com provenance label for the inspected files, but do not authenticate their clock or supply Model A native per-bar IDs.
- A timestamp-based Model B composite remains blocked because verified clock lineage, namespace/timeframe canonicalization, uniqueness, and duplicate/revision semantics have not been established and approved.

### 10.3 Relationship to the combined M1 master — still unresolved

The release inventory separately lists `GBPUSD_M1_MASTER_2016_2026_V1.zip` (asset ID `510583969`, size 43,120,568 bytes, release SHA-256 `edb39db9c91dcfd2f3b5b11fa25734810d50cf501be37555d5ec9951715d8202`). Its release metadata identifies the asset and upload, but not its internal provenance.

For the **Section 10 annual HistData archive forensics run**, that combined archive was deliberately not downloaded or inspected, because it includes the locked 2025 OOS period. A separate, older PR #116 workflow had previously downloaded and performed a bounded scan of the combined archive; the exact scope and limitation of that earlier scan are documented in Section 11 below. Accordingly, this audit still does not establish that the combined master was assembled exclusively from the inspected HistData annual files. The release inventory has no matching named HistData GBPUSD M1 asset for 2020; that gap also prevents assuming one uninterrupted provider lineage across the whole master. The earlier TitanFX OBV clue remains scoped to the OBV volume path for 2020–2024 only.

### 10.4 Updated eligibility decision

1. HistData.com is now directly evidenced as the provenance label for the eight inspected annual GBPUSD M1 archives.
2. Those CSV rows do not expose a native per-bar ID in the inspected format; no provider-native ID is established by this evidence.
3. No verified UTC/timezone/DST lineage was recovered; do not use their date/time values as authenticated UTC.
4. Do not attribute the combined GBPUSD M1 master or live MT5 feed to HistData without separate source-backed evidence.
5. Model A remains preferred if the eventual selected upstream provider/feed exposes an authoritative native ID. Model B remains **NOT AUTHORIZED** until the selected source boundary, clock evidence, and all composite-key semantics are independently established, reviewed, tested, and explicitly approved.
6. No source ID, composite ID, timestamp promotion, or pivot identity was generated.

No 2025/2026 data was downloaded or inspected. No tuning, calibration, feature selection, or OOS evaluation was performed. No legacy producer, aggregation, runtime, Brain, detector, or order path was changed.

## 11. Reconciliation of earlier PR #116 combined-master scan — 2026-11-21

A further source-code review of the earlier PR #116 workflow (`audit/mtf-archive-producer-lineage`, commit `e19ac4482666d6c0dfde55de369f5c0dfe5fa537`) found that the historical workflow did download `/GBPUSD_M1_MASTER_2016_2026_V1.zip` from Dropbox. Therefore, the broader statement that the combined archive had never been downloaded or inspected would be inaccurate. This section supersedes any such global interpretation in earlier notes.

### 11.1 Exact scope of the old workflow

The workflow `.github/workflows/mtf-archive-producer-lineage-audit.yml` downloaded the combined archive and passed it to `tools/audit_mtf_archive_producer_lineage_v1.py` and `tools/validate_m1_to_mtf_candle_reconciliation_v1.py`.

The audit script:
- enumerated ZIP member names and metadata;
- read a 256 KiB preview from CSV members to inspect headers and sample rows;
- for the exact member `GBPUSD_M1_MASTER_2016_2026.csv`, iterated the CSV with `csv.DictReader` and used the timestamp year to count only 2016–2024 rows, grouped by year/source-period/volume-availability;
- did not include 2025+ rows in its reported M1 summary, and its report explicitly described the summary as restricted to 2016–2024.

The separate reconciliation script read the combined CSV into a dataframe, then filtered both M1 and existing MTF frames to the half-open interval 2016-01-01 through 2025-01-01 before aggregation/comparison. It reported 2016–2024 only.

### 11.2 OOS handling qualification

The older scanner did traverse/parse CSV records from the combined file while applying its year filter. In addition, the reconciliation helper called `pandas.read_csv` on the complete M1 CSV member before applying its date filter, so the 2025+ rows and columns were loaded into memory by that historical workflow. It is therefore not correct to claim that no 2025+ record bytes, timestamps, or OHLCV fields were ever read. However, the inspected source code shows that:
- 2025+ rows were excluded from the reported row counts and M1-to-MTF reconciliation results;
- the scanner used the timestamp to decide the year bucket and did not aggregate 2025 OHLC or volume into the audit summary;
- the reconciliation filtered the loaded dataframe to dates before 2025-01-01 before computing expected OHLCV aggregation and comparisons;
- no 2025 tuning, calibration, feature selection, threshold selection, or performance evaluation was performed by these scripts.

This is a bounded source-code finding about what the scripts did. It is not a claim that the archive was untouched at the byte/read or in-memory loading level: the old workflow did read and load 2025 records, then excluded them before reported calculations. The protected 2025 OOS rule remains: no future inspection, analysis, tuning, or evaluation of 2025 data.

### 11.3 Provenance conclusion unchanged

The old workflow's scan did not recover an internal source manifest or producer lineage proving which provider generated every year of the combined master. The later direct annual HistData inspection remains limited to the eight annual files from 2016–2019 and 2021–2024. The missing 2020 annual HistData GBPUSD asset and the separate combined archive's unresolved assembly history mean that HistData provenance must not be generalized to the full combined master or live MT5 feed.

No source ID, composite ID, timestamp promotion, pivot identity, detector implementation, Brain/runtime change, or merge is authorized by this correction.

## 12. GBPUSD 2020–2024 TitanFX label and historical M1/H1 clock-assumption follow-up — 2026-11-21

### 12.1 What the GitHub history actually establishes

Two historical commits were reviewed:
- Commit `30318c5fdc59f117e5ec1162fa345da885e459ef` added `AUDITS/GBPUSD_VOLUME_SOURCE_AUDIT_2020_2024_2026-08-22.md`. It records GBPUSD derived M5/M15/M30/H1/H4 files in `mtf_test2/` for 2020-01-02 through 2024-12-31 with `source_timeframe=M1_TitanFX_2020_2024` and nonzero/positive volume in the inspected outputs.
- Commit `4b8f52438925684501fb7d54d3c8136888a4838e` changed the Market State fixture from zero-volume examples to a small number of GBPUSD sample rows dated 2020-01-02 through 2024-12-31. The commit provides fixture values, not the upstream raw M1 source archive or its provider manifest.
- Commit `44dff967b3dc7c40f7f1a170f3fd4429892e165b` changed the Market State adapter to treat an explicitly non-null volume as evaluable even if `volume_ratio` is unavailable. It is a downstream normalization change, not a raw-volume producer or provenance record.

These records corroborate a **TitanFX-labelled derived volume path** for the 2020–2024 GBPUSD development artifacts. They do not identify the original raw M1 OHLC provider, establish that all OHLC fields came from TitanFX, authenticate the provider boundary, or provide a native per-bar ID. The exact source archive/manifest and executable M1-to-derived-volume producer were not recovered in the inspected GitHub history. Do not promote the label `M1_TitanFX_2020_2024` into a canonical source namespace without its source-side evidence.

### 12.2 Existing annual HistData inventory cross-check

The `workspace-v1` release inventory contains named annual GBPUSD M1 HistData MT archives for 2016–2019 and 2021–2025, but no matching named GBPUSD M1 HistData MT archive for 2020. This is a release-inventory gap only; it does not prove that HistData supplied no 2020 data by another route, nor that TitanFX necessarily supplied all 2020 OHLC. The annual files directly inspected in Section 10 remain attributable to HistData only for their own years.

### 12.3 PR #114 timestamp audit code has an explicit UTC assumption

PR #114 (`audit/m1-h1-completeness-timestamp-audit`, head `1d76594115ccaf0b8df2c7d0dd989cf0dc18195a`) was reviewed at source level. Its workflow downloads `/GBPUSD_M1_MASTER_2016_2026_V1.zip` and `/GBPUSD_H1_2016_2025_MASTER.zip`. In `tools/audit_m1_h1_completeness_timestamp_v1.py`, `_timestamps()` calls `pd.to_datetime(frame["timestamp"], utc=True, errors="coerce")` (function near the top of the file). For timezone-naive source timestamps, pandas localizes them as UTC; the code does not independently authenticate the source clock, broker timezone, DST policy, or UTC offset before doing so.

Also, `_read_csv_from_zip()` loads the selected full CSV into a dataframe before `_timestamps()` parses timestamps and before the audit filters rows to years 2016–2024. Thus the PR #114 workflow read/loaded the full M1/H1 CSV members, including 2025 rows from the named 2016–2026/2016–2025 archives, then excluded 2025+ before reported development-period measurements. The old audit statement that 2025 was excluded before all measurements is true for its reported calculations but must not be read as meaning 2025 rows were never read or loaded. No 2025 tuning, calibration, feature selection, threshold selection, or performance evaluation is evidenced in this code path.

Consequently, the PR #114 finding that timestamps equal UTC hour boundaries is conditional on its `utc=True` interpretation and is not independent proof that the raw provider timestamps were UTC. Do not reuse that audit's UTC-normalized values as authenticated clock lineage or as permission to construct Model B source-bar IDs.

### 12.4 Current conclusion and next evidence gate

1. TitanFX is supported as a source label for the separate 2020–2024 derived GBPUSD volume path only; raw M1 OHLC provider identity remains unresolved.
2. HistData is directly evidenced for the eight annual files in Section 10 only; the release inventory has no named 2020 GBPUSD M1 HistData MT asset.
3. The 2020 provider gap is not solved by either label. Require the original source-side archive/manifest, acquisition record, or producer contract that explicitly binds the 2020 M1 OHLC/volume records to a provider and source namespace.
4. The timestamp audit's `utc=True` conversion is an assumption for naive timestamps, not clock authentication. Require source-native timezone/UTC-offset/DST/server-clock documentation or independently verified capture metadata.
5. No provider-native immutable per-bar ID has been evidenced for the 2020–2024 TitanFX-labelled derived path. Model A remains preferred; Model B remains NOT AUTHORIZED until the selected source boundary, clock lineage, uniqueness/revision semantics, and serialization are separately evidenced and approved.
6. Do not inspect or analyze 2025 data further. Historical workflows that loaded complete source CSVs before filtering are documented as past scope corrections, not a precedent for future access.

No source ID or composite ID was generated. No clock was promoted to UTC. No runtime, producer, pivot detector, Decision Brain, OOS, or order-path change was made.

## 13. Historical source-manifest recovery status — 2026-11-21

This section records the first historical-source recovery pass after the user approved the sequence "historical source first, live MT5 second." It uses only existing GitHub repository/PR evidence and the previously completed, bounded annual HistData archive forensics. It does not download, reopen, or inspect any 2025/2026 market data.

### 13.1 Positive source evidence currently recovered

| Artifact / period | Evidence | What it establishes |
|---|---|---|
| Eight annual GBPUSD M1 MT archives: 2016–2019 and 2021–2024 | Release asset names, per-asset SHA-256 values, internal CSV member names, and companion metadata inspected in Section 10 | HistData.com provenance label for each of those eight annual archives |
| Annual CSV row schema | Date, time, OHLC, volume; no separate per-row immutable identifier in the inspected format | No Model A native candle ID demonstrated by this CSV representation |
| Annual companion metadata | HistData attribution and tick-interval summaries; no explicit UTC/GMT, timezone, DST, broker-server, or clock-offset declaration recovered | File provenance label only; no authenticated clock lineage or source publication-time semantics |
| 2020 GBPUSD M1 | No matching named annual HistData M1 asset in the inspected release inventory | A source-inventory gap; provider is unresolved, not inferred |
| Combined GBPUSD M1 master | Earlier PR #116 workflow downloaded and parsed it; Section 11 documents that full CSV rows were traversed/loaded before 2016–2024 filters | Historical presence of the archive in a prior workflow, but not a per-year source manifest; 2025 handling remains frozen and must not be repeated |
| TitanFX-labelled 2020–2024 volume artifacts | Existing GBPUSD volume-source audit records derived timeframe volume as M1_TitanFX_2020_2024 | Volume-path label only; not raw M1 OHLC provider identity or clock authority |
| PR #114 timestamp audit | Workflow source shows it acquired the combined M1/H1 archives; helper applies pd.to_datetime(..., utc=True) to timestamps | A historical code-path assumption, not independent source-clock authentication |

### 13.2 Recovery of an authoritative manifest

The reviewed GitHub evidence does **not** contain a recovered authoritative manifest that maps each year/file in the canonical historical OHLC master to:
- actual upstream provider/feed and source namespace;
- exact acquisition/export method and immutable archive/member identity;
- canonical symbol mapping and native timeframe;
- timestamp meaning (bar open vs bar close), timezone/offset and DST history;
- provider publication/availability-time semantics;
- duplicate, correction, revision, and backfill policy;
- native per-bar immutable ID availability and uniqueness scope;
- reproducible producer/transform version and parameters linking raw M1 to each derived output.

PR #116's archive scanner was designed to find candidate documents/code and inspect archive members/schema/previews; its own interpretation explicitly says a filename/keyword is a lead, not proof of output lineage. Its recovered-workspace scan did not find the original general Market Structure/six-TF producer. PR #114's timestamp audit does not repair this gap because it localizes naive timestamps to UTC by software assumption, not by source evidence. The eight annual HistData files are direct provenance evidence for those files only; they do not authenticate the combined master or fill the 2020 gap.

### 13.3 Historical source-manifest disposition

**AUTHORITATIVE_HISTORICAL_SOURCE_MANIFEST: NOT RECOVERED.**

Current bounded state:
- HistData annual provenance: **PARTIALLY ESTABLISHED** for 2016–2019 and 2021–2024 only.
- 2020 raw OHLC provider: **UNRESOLVED**.
- Combined master per-year lineage: **UNRESOLVED**.
- Historical timestamp UTC/timezone/DST lineage: **NOT AUTHENTICATED**.
- Provider source publication/available-at semantics: **NOT RECOVERED**.
- Native immutable per-bar ID (Model A): **NOT DEMONSTRATED**.
- Model B composite identity: **NOT AUTHORIZED**.
- Historical source suitability for production Pivot V2: **BLOCKED**.

Do not label the entire 2016–2024 development dataset as HistData or TitanFX. Do not infer 2020 from adjacent years. Do not treat the old utc=True normalization as source-clock evidence. Do not create source IDs or production available_at values from these records.

### 13.4 Evidence required to close the historical gate

The next admissible recovery item is the original source-side manifest/acquisition record or provider documentation for the exact raw OHLC files used to build the canonical 2016–2024 M1 master, including an explicit 2020 resolution. If no such manifest exists, a newly authored declaration from memory is not equivalent to contemporaneous source evidence; it must be marked as an owner attestation and independently corroborated where possible.

The evidence package must also include:
1. exact archive/member names and cryptographic digests for each development-year source file;
2. provider/source namespace and canonical symbol mapping;
3. native timestamp semantics and authoritative timezone/DST/UTC mapping;
4. provider publication/availability semantics, distinct from capture and ingestion time;
5. revision/backfill/duplicate policy;
6. whether native immutable candle IDs exist and their uniqueness scope;
7. reproducible transformation lineage from raw M1 to derived OHLC/timeframes, with code/version and configuration;
8. explicit exclusion of the locked 2025 OOS dataset from all new retrieval, inspection, and processing.

### 13.5 Next step

The historical source-manifest recovery pass is complete as a bounded GitHub evidence review and has reached a fail-closed result: **the authoritative manifest was not found**. Before any historical clock or identity contract can be promoted, the project needs the original acquisition/source manifest or equivalent provider-issued evidence. Once that historical gate is resolved, proceed to the separately governed live MT5 broker-clock workstream; do not combine their policies.

Read-only documentation update. No 2025/2026 data access, no tuning/calibration/feature selection/performance evaluation, no timestamp promotion, no source ID generation, no production runtime change, no Decision Brain integration, no main-branch change, no merge, and no order path.
