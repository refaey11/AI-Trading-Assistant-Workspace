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
