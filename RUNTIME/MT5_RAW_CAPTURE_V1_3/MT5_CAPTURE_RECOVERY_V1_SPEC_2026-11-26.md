# MT5 Capture Recovery V1 — Specification Draft

**Date:** 2026-11-26  
**Status:** SPECIFICATION DRAFT — REVIEW ONLY — NOT AN IMPLEMENTATION AUTHORIZATION  
**Target:** MT5 Raw Capture V1.3  
**Branch:** `spec/mt5-capture-recovery-v1-2026-11-26`

## 1. Purpose

Define a fail-closed recovery contract so a capture process can resume after terminal restart, disconnection, delayed history availability, or interrupted writes without silently skipping closed bars or creating duplicate records.

This specification is limited to capture completeness and recovery. It does not approve a source-bar identity implementation, timestamp normalization, MTF joins, feature production, Decision Brain integration, trading signals, or orders.

## 2. Existing V1.3 baseline and compatibility

The inspected V1.3 EA:
- requests only the latest closed bar using `CopyRates(symbol, timeframe, 1, 1, rates)`;
- keeps seen-bar keys/times in process memory;
- loses that seen-state on terminal/EA restart;
- does not backfill every intermediate bar after an outage;
- labels raw `MqlRates.time` as `MT5_MQLRATES_DATETIME_RAW` with UTC status `UNVERIFIED`.

Recovery must be additive and separately versioned. Do not silently change the V1.3 raw timestamp meaning or rewrite historical rows.

## 3. Three distinct identities/state concepts

These MUST NOT be conflated:

1. **Capture cursor:** mutable operational checkpoint for one capture stream. It records how far durable capture has progressed.
2. **Ingest deduplication key:** an idempotency aid used to recognize a previously ingested record. It is not proof of source identity.
3. **Canonical source_bar_id:** immutable identity of the upstream candle. Model A (authoritative native ID) remains preferred. Model B remains conditional and unauthorized until all source, clock, uniqueness, revision, and conformance evidence is approved. Model C (payload/OHLC-derived identity) remains rejected.

Neither terminal `source_id` nor `payload_hash` is a canonical source_bar_id.

## 4. Stream partitioning

Recovery state is isolated per capture stream. At minimum, the stream namespace must distinguish:
- source/provider namespace (currently unresolved for the general OHLC feed);
- canonical instrument/symbol identity (contract not yet approved);
- native timeframe;
- capture schema/version.

A terminal environment identifier may be retained as observation metadata, but it must not silently become the provider namespace or canonical bar identity.

Until canonical symbol and source namespace contracts are approved, cross-terminal or cross-provider cursor reuse is prohibited. A cursor from one stream must never advance another stream.

## 5. Cursor contract

The cursor is persistent and versioned. Its logical record must include:
- cursor schema version;
- stream key and capture schema version;
- last durably committed source position;
- last committed record reference/integrity metadata;
- update/commit status;
- recovery generation or equivalent audit marker.

The exact serialization and storage technology are implementation decisions and are not selected here.

### 5.1 Commit ordering

For every recovered batch:
1. request a bounded batch after the committed cursor;
2. validate schema and closed-bar status;
3. establish deterministic source ordering under the approved source ordering contract;
4. write records durably and idempotently;
5. verify durable write completion;
6. only then advance the persistent cursor atomically or through a recoverable journal protocol.

If data writing succeeds but cursor persistence fails, replay the batch safely; deduplication must prevent duplicate durable rows. If cursor persistence appears ahead of durable data, stop and mark the stream inconsistent. Never skip forward to repair it automatically.

### 5.2 Cursor loss or corruption

Missing, unreadable, malformed, or incompatible cursor state must produce `RECOVERY_REQUIRED`, not an assumed latest position. A conservative rescan/reconciliation procedure must be specified and bounded before implementation. No blind initialization at the latest closed bar is allowed after an established stream has lost its cursor.

## 6. Catch-up acquisition

The recovery producer must request all available closed bars strictly after the last committed source position, using bounded batches. It must continue until the source reports that no further bars are currently available or a configured safety bound is reached.

- Partial `CopyRates` results are partial, not success for the requested range.
- `-1`, history-not-ready, timeout, or unavailable history must leave the cursor unchanged and schedule a retry.
- Returned arrays must be normalized into deterministic chronological order only after the API's ordering behavior is explicitly tested.
- Do not assume that a successful request proves all expected bars were returned.
- Do not advance based on the newest returned bar if earlier positions in the requested range are unresolved.
- The first bootstrap of a new stream requires an explicitly approved start boundary. It must not silently mean “start now” if historical completeness is expected.

## 7. Time, ordering, and market gaps

V1.3 raw time remains `UNVERIFIED`. It may not be converted to UTC, used for UTC MTF joins, or used to infer broker timezone/DST.

A raw source position may be considered for same-stream resume ordering only after a separate conformance test proves its monotonicity, uniqueness, stability across restart, and behavior under history corrections for the exact source/API/broker combination. Until then, automatic cursor advancement based on raw epoch is blocked.

### 7.1 Gap classification

A fixed timeframe interval alone is not sufficient to classify missing bars. Weekends, holidays, exchange sessions, broker trading sessions, daylight-saving changes, and instrument-specific closures can create legitimate time gaps.

Gap states:
- `CONTIGUOUS_CONFIRMED`: continuity is established by approved source/session evidence.
- `EXPECTED_SESSION_GAP`: a recognized closure is supported by an approved calendar/source rule.
- `MISSING_DATA_SUSPECTED`: evidence indicates an expected bar or source position is absent.
- `GAP_UNKNOWN`: available evidence cannot distinguish a normal closure from missing data.

No synthetic bars may be fabricated. `GAP_UNKNOWN` and `MISSING_DATA_SUSPECTED` block a completeness claim and must prevent downstream consumers from treating the stream as complete. No guessed tolerance, session calendar, or broker offset is introduced by this draft.

## 8. Duplicate and revision handling

- An exact replay of an already committed record must be idempotent.
- A repeated dedup key with different payload must be recorded as a conflict/revision candidate, not silently overwritten or discarded.
- Historical broker corrections must be represented as an explicit revision event only after a source revision contract is approved.
- Payload hashes remain integrity evidence only.
- A dedup key based on `(symbol, timeframe, raw_epoch)` remains a bounded ingest aid; it is not promoted to canonical source identity and cannot support cross-provider identity.

## 9. Fail-closed stream states

The recovery state machine must expose, at minimum:
- `BOOTSTRAP_REQUIRED`
- `RECOVERING`
- `CAUGHT_UP_CURRENTLY`
- `INCOMPLETE_PARTIAL_READ`
- `RETRYABLE_SOURCE_UNAVAILABLE`
- `RECOVERY_REQUIRED`
- `GAP_UNKNOWN`
- `MISSING_DATA_SUSPECTED`
- `IDENTITY_CONFLICT`
- `CURSOR_DATA_INCONSISTENT`
- `BLOCKED_UNVERIFIED_ORDERING`

Only a stream with approved source identity/order, durable cursor consistency, and resolved continuity may be described as complete. “Caught up currently” is not the same as “historically complete.”

## 10. Required acceptance tests

All tests must use deterministic synthetic fixtures or an explicitly approved non-OOS demo source. They must not read or import `OOS_2025` or mixed-year archives.

1. Restart after several closed bars: recover every available missing bar.
2. Long disconnection: recover in bounded batches without skipping.
3. Partial `CopyRates` response: do not advance cursor; retry remaining range.
4. History unavailable/not ready: preserve cursor and report retryable state.
5. Data write succeeds, cursor write fails: replay safely without duplicate rows.
6. Cursor advances only after durable data write.
7. Cursor corruption/loss: enter `RECOVERY_REQUIRED`; never jump to latest.
8. Duplicate identical batch: idempotent replay.
9. Same dedup key with changed payload: explicit conflict/revision candidate.
10. Out-of-order API result: deterministic ordering or fail closed.
11. Weekend/session closure: do not report a missing bar without calendar evidence.
12. In-session missing source position: mark suspected/unknown and block completeness.
13. Broker/server clock or DST change: do not reinterpret raw timestamp as UTC.
14. Terminal restart and terminal-path change: do not reuse an unproven stream namespace.
15. Bootstrap boundary: enforce explicit approved start boundary.
16. Durable storage interruption at every commit step: recover without cursor/data divergence.
17. History correction/re-download: preserve prior evidence and expose conflict.
18. Multi-symbol and six-timeframe isolation: no cursor crossover.

## 11. Required evidence before implementation

Implementation remains blocked until review establishes:
- authoritative upstream/provider boundary for the live OHLC feed;
- canonical symbol and timeframe identity;
- a source ordering/resume-position contract for the exact MT5 API and broker;
- source-bar identity decision under the already-approved Model A preference / conditional Model B fallback;
- durable storage and atomic/recoverable cursor semantics;
- approved session/calendar evidence or an explicit policy to leave continuity unknown;
- deterministic fixtures and acceptance criteria for all failure modes.

The MQL5 documentation distinction between raw `MqlRates.time`, terminal server-time observations, and Python API UTC statements must be resolved for the exact acquisition path. Do not infer a universal timezone rule from one API surface.

## 12. Explicit non-goals and governance

- No code or runtime changes are authorized by this document.
- No PR is created by this specification alone; implementation and PR require separate explicit approval.
- No change to Murphy, Nison, TIZ, Similarity, Decision Brain, or Risk Engine.
- No production MTF/pivot eligibility is granted.
- No live orders or auto-execution.
- No 2025 OOS access, import, filtering, tuning, calibration, feature selection, or evaluation.
- No merge to `main`.

## 13. Review decision checklist

The draft is ready for review, not approval. Reviewers must explicitly resolve:
1. What exact source/API constitutes the live OHLC provider?
2. What native source position can safely resume a stream without claiming UTC?
3. What durable store and atomic cursor commit mechanism are permitted?
4. What evidence can distinguish session closures from missing bars?
5. How should source corrections/revisions be represented?
6. What is the approved bootstrap start boundary and historical completeness claim?

Until these are answered, production capture completeness remains **BLOCKED / NOT PROVEN**.
