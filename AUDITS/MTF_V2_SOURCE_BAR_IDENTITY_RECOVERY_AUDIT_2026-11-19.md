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
