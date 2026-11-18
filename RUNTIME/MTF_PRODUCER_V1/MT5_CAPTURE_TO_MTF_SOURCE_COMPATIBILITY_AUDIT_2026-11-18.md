# MT5 Capture to MTF Source Contract — Compatibility Audit

**Date:** 2026-11-18  
**Scope:** Read-only audit of the existing MT5 Raw Capture V1 / Forex-Only V1.2 implementation against the MTF Producer V1 Stage A/B contract.  
**Status:** RAW CAPTURE EVIDENCE PARTIAL — FEATURE PRODUCTION AND HISTORICAL PARITY REMAIN BLOCKED.

## 1. Files inspected

- `RUNTIME/MT5_RAW_CAPTURE_V1/MT5_Raw_Capture_Only_V1.mq5`
- `RUNTIME/MT5_RAW_CAPTURE_V1/mt5_raw_capture_contract_v1.py`
- `RUNTIME/MT5_RAW_CAPTURE_V1/mt5_csv_ingest_v1.py`
- `RUNTIME/MT5_RAW_CAPTURE_V1/test_mt5_csv_ingest_v1.py`
- `RUNTIME/MT5_RAW_CAPTURE_V1/test_mt5_raw_capture_contract_v1.py`
- `RUNTIME/MT5_FOREX_ONLY_CAPTURE_V1_2/MT5_Forex_Only_Raw_Capture_V1_2.mq5`
- `RUNTIME/MT5_FOREX_ONLY_CAPTURE_V1_2/README.md`

The V1.2 capture is the user's demonstrated capture path; the V1 ingest/contract remains the shared 20-column validation contract.

## 2. What is already supported by code and tests

- Six native MT5 periods are enumerated: M5, M15, M30, H1, H4, D1.
- The EA requests CopyRates shift 1, i.e. the latest closed bar, and writes `is_closed=true`.
- Raw OHLC, tick volume, real volume, spread, symbol, timeframe, broker server identity, source identity, capture version, and separate clock observations are serialized.
- The raw contract rejects naive timestamps, non-finite numeric values, invalid OHLC geometry, unsupported timeframes, unfinished bars, and conflicting duplicates.
- The ingest adapter enforces an exact 20-column header and computes a canonical payload hash during ingestion.
- V1.2 applies two independent forex filters: MT5 FX calculation mode and base/profit currency allowlist.

These checks establish a useful raw-bar capture and validation layer. They do not establish any of the seven derived Brain MTF feature semantics.

## 3. Exact schema gaps against Stage A/B

| Required evidence | Current implementation | Finding |
| --- | --- | --- |
| `bar_time_server` (raw server wall-clock bar label) | Not emitted as a separate bar field; `bar_time_mt5_utc` is emitted | Missing as a distinct raw field |
| `bar_time_utc` | `bar_time_mt5_utc` is emitted from `MqlRates.time` and labelled with Z | Semantics rely on the documented MT5 UTC contract; the EA does not perform a conversion |
| `bar_close_time_utc` | Not emitted | Missing; do not synthesize by adding timeframe duration |
| `retrieved_at_utc` | No retrieval timestamp field; `host_gmt_estimate_utc` is a host-derived clock observation | Missing; host clock estimate is not an independently verified UTC clock |
| `timezone_policy_id` | Not emitted | Missing explicit versioned policy identifier |
| `broker_server_id`, `source_id`, `capture_version` | Emitted | Present |
| `payload_hash` | Computed by ingest and added to JSONL, not included in original EA CSV | Present only after ingestion |
| Closed-bar flag | `is_closed=true` after CopyRates shift 1 | Present; deterministic close-boundary tests across all six periods still need evidence |
| Volume type | tick/real fields plus `volume_type` | Present and kept distinct |

## 4. Timestamp interpretation — do not overclaim

- `bar_time_mt5_utc` is formatted from `MqlRates.time`; the EA's `IsoUtc()` helper formats the supplied datetime with a trailing Z and does not itself convert a broker wall-clock timestamp.
- The project guide attributes UTC semantics to the MT5 MqlRates time contract. This should remain explicitly documented as the source contract; it must not be generalized to the legacy historical archive, whose timezone remains unresolved.
- `terminal_time_server` is a current server-time estimate, not the historical bar timestamp.
- `terminal_time_current_server` is the last known quote time.
- `host_gmt_estimate_utc` comes from TimeGMT and depends on host clock/settings; it is diagnostic only.
- `observed_server_minus_host_gmt_seconds` is a contemporaneous diagnostic, not a historical broker timezone/DST conversion rule.
- An explicit ISO offset alone does not prove source lineage or the correctness of the clock that produced it.

## 5. Safe next changes — require a versioned capture contract

Do not silently add fabricated values to the existing V1.2 CSV or relax the current ingest contract. A future capture version should make each additional clock field's source explicit and should only emit a close/availability timestamp when its semantics are proven by MT5 API behavior and deterministic tests.

Before a new capture version is accepted, require:
1. A documented source for each timestamp field and its clock domain.
2. A stable `timezone_policy_id` tied to the documented MqlRates UTC semantics, not inferred from server-minus-host offsets.
3. A retrieval/observation timestamp whose clock source and uncertainty are explicit.
4. A defensible closed-bar availability contract; no blind timeframe-duration arithmetic.
5. Tests for all six timeframes, weekend/session gaps, stale feeds, restart/replay, duplicates, and no-future availability.
6. A schema version bump and compatibility tests proving the old V1/V1.2 CSV remains readable without reinterpretation.

## 6. Gates that remain blocked

- Original historical archive timezone / broker-clock / DST provenance: **BLOCKED**.
- Seven Brain MTF feature formulas and semantics: **BLOCKED**.
- Stage B capture-to-provenance completeness: **PARTIAL**.
- Stage C derived feature producer: **NOT AUTHORIZED**.
- Stage D 2016–2024 historical parity: **BLOCKED** until historical timestamp provenance and feature semantics are established.
- 2025 OOS: **LOCKED / NOT TOUCHED**.
- Live orders: **NOT AUTHORIZED**.

## 7. Decision

Keep the current raw capture and ingest as a useful data-collection layer. Do not treat its successful schema validation as proof that all Stage B provenance requirements are met. The next implementation must be a separately versioned capture-contract upgrade, after the timestamp semantics are agreed and testable. No derived MTF fields, formulas, direction, imputation, scaling, or trading behavior are added by this audit.
