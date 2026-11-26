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


## 14. Compatibility review addendum — 2026-11-26

This addendum records a second-pass compatibility review against the existing V1.3 EA, Python contract, and Source-Bar Identity Proposal V1. It does not approve implementation.

### 14.1 Confirmed compatibility constraints

1. **Current V1.3 is a latest-bar poller, not a recovery reader.** The EA calls `CopyRates(symbol, tf, 1, 1, rates)`, and its seen-key arrays exist only in process memory. A recovery implementation must not claim completeness by merely persisting the current `g_seen_bar_times` value.
2. **Current CSV output is append-oriented.** The EA opens the Common Files CSV, seeks to end, writes a header only for an empty file, writes one row, calls `FileFlush`, closes the file, and then updates in-memory seen state. A future cursor must be reconciled against the actual durable CSV contents, not treated as an independent truth.
3. **FileFlush is not yet an approved crash-durability guarantee.** The current code's successful `FileWrite` plus `FileFlush` is not sufficient evidence for atomic multi-record batch commits, power-loss durability, or atomic coordination between CSV rows and a separate cursor file. The implementation design must state its exact failure model and prove recovery under process crash, terminal crash, OS crash, and storage interruption. If the selected storage cannot provide the required guarantee, the state must remain incomplete rather than overclaim durability.
4. **Existing Python ingest normalization is not canonical identity.** The V1.3 validator uppercases symbol and timeframe values and the current ingest dedup key is `(symbol, timeframe, bar_time_epoch_seconds_raw)`. The Source-Bar Identity Proposal explicitly treats this as an ingest aid, not immutable source identity. Recovery must not promote either normalization or this tuple into a canonical source_bar_id without a separate approved symbol/identity contract.
5. **Source-Bar Identity remains unresolved.** Model A requires evidence of a native immutable identifier; none is emitted by the inspected V1.3 MqlRates capture. Model B requires verified UTC bar-open time and approved namespace/symbol/timeframe/revision semantics. Current raw time is UNVERIFIED, so Model B is presently blocked. Model C remains rejected.
6. **Raw-time ordering is a separate proof obligation from UTC.** A same-stream resume cursor might eventually use a raw source position without claiming UTC, but only if exact API/broker tests prove stable ordering, uniqueness, and repeatability across restarts and history refreshes. This is not currently proven.

### 14.2 Additional acceptance tests required

19. CSV row is truncated/torn during process or terminal interruption: detect and quarantine the incomplete tail; never advance cursor past it.
20. CSV append succeeds but process crashes before cursor update: replay/reconcile without losing or duplicating committed logical records.
21. Cursor update succeeds but CSV data is absent/truncated: detect `CURSOR_DATA_INCONSISTENT` and stop.
22. FileFlush returns but simulated OS/power-loss failure occurs: validate the declared durability boundary; otherwise do not claim durable commit.
23. Existing CSV contains duplicate keys with identical payloads: reconcile idempotently while preserving an audit count.
24. Existing CSV contains duplicate keys with different payloads: preserve both evidence records or a conflict record according to an approved revision policy; never silently overwrite.
25. Symbol case/suffix/alias differences (for example broker-specific suffixes) do not merge streams without an approved canonical symbol mapping.
26. Recovery batch spans more records than one bounded request: all pages are fetched in deterministic order; no cursor leap occurs after a partial page.
27. History refresh changes an older bar while the cursor is ahead: detect the revision/conflict under an approved lookback/reconciliation policy; do not assume all earlier bars are immutable.
28. CSV header/schema mismatch, reordered columns, or unsupported capture version: block recovery rather than append incompatible rows.

### 14.3 Revised storage decision gate

No storage backend or cursor-file layout is selected by this draft. Before implementation, choose one explicit transaction/reconciliation strategy and document its guarantees:

- **Single append log with recoverable journal/checkpoint:** cursor is derived from and validated against the committed log boundary; partial trailing records are detected and quarantined.
- **Transactional store:** data rows and cursor advancement share one atomic transaction, with a defined uniqueness/conflict model.
- **Separate CSV plus cursor file:** allowed only if a crash-safe two-phase/journal protocol is demonstrated; simple sequential writes to two files are not sufficient.

The implementation must not describe a row as durably committed merely because an API call returned success. Define what “durable” means for the selected platform and failure model.

### 14.4 Compatibility disposition

- Existing V1.3 capture contract: **COMPATIBLE ONLY AS RAW INPUT**, not as proof of recovery completeness.
- Existing V1.3 CSV dedup tuple: **INGEST AID ONLY**, not canonical identity.
- Source-Bar Identity Model A: **PREFERRED, EVIDENCE NOT FOUND IN V1.3**.
- Source-Bar Identity Model B: **BLOCKED**, because verified UTC and namespace/symbol semantics are not established.
- Persistent cursor implementation: **NOT APPROVED** until storage/reconciliation and source-ordering gates pass.
- Production completeness claim: **BLOCKED / NOT PROVEN**.

No source files, runtime code, tests, workflows, or OOS data were changed or executed during this compatibility review.


## 15. Storage architecture research addendum — 2026-11-26

This section records an official-documentation discovery made during the storage comparison. It is an architecture candidate, not implementation approval.

### 15.1 New finding: MQL5 has a native SQLite API

The earlier storage comparison treated SQLite mainly as a possible Python-side store. Official MQL5 documentation confirms that MQL5 itself exposes SQLite database operations, including DatabaseOpen / DatabaseClose; SQL execution and prepared statements; DatabaseTransactionBegin, DatabaseTransactionCommit, and DatabaseTransactionRollback; and DATABASE_OPEN_COMMON for a database file in the common folder shared by terminals.

Official references:
- https://www.mql5.com/en/docs/database
- https://www.mql5.com/en/docs/database/databaseopen
- https://www.mql5.com/en/docs/database/databasetransactionbegin
- https://www.mql5.com/en/docs/database/databasetransactioncommit
- https://www.mql5.com/en/articles/7463

This is materially different from a Python-only SQLite proposal: the MT5 EA may be able to write both captured bars and its capture cursor into the same SQLite database and the same transaction, avoiding a non-atomic handoff between a CSV file and a separate cursor file.

### 15.2 Candidate architecture A — one MQL5 SQLite database

Proposed transaction boundary (candidate only):
1. Read a bounded closed-bar batch from the source.
2. Validate each row and the approved stream identity/order contract.
3. Begin one SQLite transaction.
4. Insert raw bar evidence using a uniqueness/dedup policy that does not claim canonical source identity.
5. Update the corresponding stream cursor in the same database transaction.
6. Commit; if any operation fails, roll back and do not report the batch as committed.
7. On restart, read the cursor and reconcile it against committed rows before requesting the next batch.

This can make the logical data-row update and cursor update atomic with respect to the database transaction. It also enables SQL constraints and indexes for stream isolation, replay detection, and conflict reporting.

Important limits still unproven:
- MQL5 documentation confirms SQLite transactions, but this review has not yet proven the exact crash/power-loss durability mode available through the MQL5 wrapper or whether required SQLite PRAGMA settings are accepted and effective.
- A successful transaction commit must not be equated automatically with the strongest power-loss guarantee until the actual MQL5/SQLite build, filesystem, journal mode, and synchronous behavior are tested.
- DATABASE_OPEN_COMMON confirms a common-folder location, not a complete multi-terminal writer-coordination policy. Start with one designated writer per database/stream unless concurrency is separately tested.
- Python interoperability, concurrent read behavior, backup/restore, schema migration, disk-full behavior, and database corruption recovery require explicit tests.
- A transaction only protects records already returned by CopyRates; it does not solve missing history, unverified timestamps, source-bar identity, ordering, or session-gap classification.

### 15.3 Candidate architecture B — append-only file plus journal/checkpoint

This remains viable if a text/binary audit log is a hard requirement, but it needs explicit record framing, sequence numbers, checksums, torn-tail detection, and a recoverable checkpoint protocol. A simple CSV append plus separate cursor file remains rejected. MQL5 FileFlush flushes the file's I/O buffer, but the official description does not define a complete atomic transaction spanning a CSV record and a separate cursor file.

Official references:
- https://www.mql5.com/en/docs/files/fileflush
- https://www.mql5.com/en/docs/files/filewrite
- https://www.mql5.com/en/docs/files

### 15.4 Candidate architecture C — Python SQLite after CSV export

The existing Python V1.3 adapter reads a CSV and writes JSONL; it does not currently participate in the EA's write transaction. Therefore a Python-side SQLite database would be downstream of capture and could not atomically commit the MT5 source rows and MT5 cursor unless the architecture changes to make Python the authoritative capture writer. That alternative would require a separately designed IPC/ownership protocol and is not assumed here.

Python's sqlite3 supports explicit transaction control, but that alone does not close the cross-process transaction gap between an MT5 CSV writer and a Python database writer.
Official reference: https://docs.python.org/3/library/sqlite3.html

### 15.5 Provisional comparison and disposition

| Criterion | MQL5 SQLite, bars + cursor in one DB | Append log + journal | CSV + Python SQLite |
|---|---|---|---|
| Same transaction for bars and cursor | Potentially yes | Must be designed | No, not with current handoff |
| Native support in current EA language | Official MQL5 API exists | MQL5 file API exists | Requires separate Python process |
| Torn-tail handling | SQLite recovery/transaction behavior must be tested | Must be implemented and tested | CSV tail still needs repair before import |
| Human-readable raw archive | Export view can be generated | Yes, depending on format | CSV retained |
| Multi-terminal coordination | Not yet proven | Not yet proven | Not yet proven |
| Power-loss durability | Not yet proven for actual wrapper/config | Not yet proven | Depends on both stages |

Provisional recommendation for the next design review: prioritize a proof-of-concept review of MQL5-native SQLite with bars and cursor in the same database transaction. Do not implement it yet. Keep CSV as a derived export/audit format rather than the authoritative transactional store if the proof succeeds.

### 15.6 Mandatory proof tests before selection

29. Confirm the deployed MT5 build supports all required database APIs and DATABASE_OPEN_COMMON.
30. Verify schema creation, prepared inserts, uniqueness constraints, and rollback behavior in a Demo terminal.
31. Inject a failure after bar inserts but before cursor update; confirm neither is committed.
32. Inject a failure after cursor update but before commit; confirm neither is committed.
33. Terminate EA/terminal at each transaction stage; verify database integrity and cursor/data agreement after restart.
34. Test OS crash and controlled power-loss simulation on the actual storage environment; document what durability claim is justified.
35. Verify whether required SQLite journal/synchronous configuration is accepted and effective through MQL5 DatabaseExecute; if unavailable, document the resulting durability limit.
36. Test disk-full, locked database, busy timeout, corrupted database, backup/restore, and schema migration.
37. Test one-writer enforcement and read-only Python access while the EA is active; test multi-terminal access only if required.
38. Confirm that CSV export is reproducible from committed database rows and is never treated as an independent cursor authority.

### 15.7 Updated storage gate

- MQL5-native SQLite: PREFERRED CANDIDATE FOR PROOF-OF-CONCEPT; NOT APPROVED.
- Append log + journal: VALID FALLBACK CANDIDATE; DESIGN NOT COMPLETE.
- CSV + separate cursor file: REJECTED WITHOUT A PROVEN JOURNAL/TWO-PHASE PROTOCOL.
- Python SQLite after current CSV export: DOWNSTREAM ONLY; CANNOT ATOMICALLY COMMIT MT5 CAPTURE + CURSOR.

No source/runtime code, tests, workflows, or OOS data were changed or executed in this research step. The specification remains review-only; implementation and PR creation still require separate explicit approval.


## 16. SQLite logical schema and transaction protocol — review proposal only

This section narrows the preferred proof-of-concept without selecting source identity, timestamp semantics, or authorizing implementation. Names below are conceptual; they are not committed SQL or code.

### 16.1 Logical tables

1. **capture_streams** — one row per approved stream partition. Holds stream identifier, provider namespace, canonical symbol identifier, timeframe, schema version, bootstrap boundary, current recovery state, cursor kind/value, cursor generation, and update observation. The canonical fields remain unresolved; do not populate them from terminal path or broker display text by assumption.
2. **raw_bars** — immutable capture observations. Holds an internal ingestion record ID, stream reference, raw source position as-is, raw clock label/status, OHLC, volume fields, spread, capture version, payload hash, and observation metadata. Preserve raw source fields; do not normalize raw time to UTC.
3. **capture_batches** — one row per bounded acquisition batch, including stream, requested source range/position, returned count, validation outcome, batch state, and commit generation. This supports audit of partial reads and retries.
4. **capture_conflicts** — links a previously stored observation to a later conflicting payload or source revision candidate. Never silently overwrite prior evidence.
5. **capture_events** — append-only state-transition/audit events for recovery-required, retryable source failure, gap-unknown, identity conflict, cursor inconsistency, and operator-approved bootstrap/reconciliation decisions.

### 16.2 Constraints that can be considered now

- Primary keys should be internal database record IDs, not claims of upstream source-bar identity.
- Foreign keys should isolate each raw bar, batch, and event to exactly one stream record.
- A uniqueness constraint on source position must remain disabled until same-stream position uniqueness/stability is proven for the exact source path.
- The current tuple (symbol, timeframe, raw epoch) may be indexed for diagnostics/reconciliation but must not be promoted to a canonical identity key.
- Conflicting payloads must be preserved and surfaced; conflict resolution policy is still open.
- Every stream cursor must explicitly carry its position kind and clock status. An UNVERIFIED raw timestamp must never be labelled UTC.

### 16.3 Transaction protocol

For each fully validated bounded batch, the intended transaction is:
1. Begin database transaction.
2. Insert batch audit row in a pending/in-progress state.
3. Insert all accepted raw bar observations; write conflict evidence rather than overwrite when a duplicate candidate differs.
4. Update only the matching stream cursor and generation after all batch rows are accepted.
5. Mark the batch committed and append the corresponding capture event.
6. Commit the transaction; only a successful commit permits the runtime to report the batch as database-committed.
If any step fails, roll back the transaction, retain the previous cursor, and expose a retryable or blocked state. If commit outcome is uncertain after a process/terminal interruption, reopen the database and reconcile batch state, rows, and cursor before requesting new data. Never infer success from a log message alone.

### 16.4 Important boundary

This protocol makes database rows, batch status, and cursor a single logical transaction candidate. It does not prove that CopyRates returned every expected candle, that the returned ordering is stable, that historical bars cannot be revised, or that the source position is a canonical immutable bar ID. Those remain independent gates. The recovery system must not report CAUGHT_UP_CURRENTLY or complete continuity until source ordering and completeness evidence are approved.

### 16.5 Review disposition

Logical schema: **DRAFTED FOR REVIEW**.
SQLite transaction pattern: **PREFERRED PROOF-OF-CONCEPT DESIGN**.
Source position / source_bar_id: **UNRESOLVED**.
Timestamp normalization: **UNRESOLVED; raw V1.3 remains UNVERIFIED**.
Implementation, MetaEditor changes, Demo capture, and PR: **NOT AUTHORIZED BY THIS DOCUMENT**.


## 17. Official MQL5 API compatibility review — 2026-11-26

This section records official MQL5 API behavior relevant to the proposed recovery design. It does not authorize implementation.

### 17.1 SQLite support confirmed at API level

The official MQL5 database reference confirms that the built-in database functions use SQLite and support database files on disk, SQL execution, prepared queries, parameter binding, and explicit transaction begin/commit/rollback. `DatabaseOpen` documents `DATABASE_OPEN_COMMON` for a database file in the common folder shared by terminals.

References:
- https://www.mql5.com/en/docs/database
- https://www.mql5.com/en/docs/database/databaseopen
- https://www.mql5.com/en/docs/database/databaseexecute
- https://www.mql5.com/en/docs/database/databaseprepare
- https://www.mql5.com/en/docs/database/databasebind
- https://www.mql5.com/en/docs/database/databasetransactionbegin
- https://www.mql5.com/en/docs/database/databasetransactioncommit
- https://www.mql5.com/en/docs/database/databasetransactionrollback

This confirms that an MQL5-native SQLite proof of concept is technically plausible without adding a Python process to the capture write path. It does not prove the deployed terminal build, storage configuration, power-loss durability, or multi-terminal writer behavior.

### 17.2 Important transaction limitation

MQL5 documents successful transaction commit as completion/application of the changes accumulated since transaction begin. The API documentation does not, by itself, specify the exact filesystem-level power-loss guarantee, SQLite journal mode, synchronous setting, or durability after sudden OS/power failure for the target terminal build.

Therefore:
- Treat transaction atomicity as a database-level property to validate with rollback/crash tests.
- Do not claim power-loss durability solely from `DatabaseTransactionCommit()` returning true.
- Test actual restart and fault-injection behavior on the target MT5 build and storage medium.
- If the strongest durability mode cannot be configured or verified through the MQL5 wrapper, narrow the durability claim accordingly.

The official API example also checks and handles transaction begin, execute, rollback, and commit outcomes; the recovery implementation must check every return value rather than log and continue.

### 17.3 Prepared statements and value binding

`DatabasePrepare` supports parameter placeholders and `DatabaseBind` binds supported scalar values. The recovery implementation should use prepared statements for all variable row values. Dynamic table/column names are not value parameters and must remain fixed, allowlisted schema identifiers.

This reduces SQL quoting/injection risk and avoids brittle string formatting for symbols, source metadata, and payload fields. It does not solve canonical symbol identity or source-bar identity.

### 17.4 CopyRates behavior changes the recovery acceptance criteria

The official `CopyRates` documentation states:
- A request can return the number of elements copied or `-1` on error.
- When history is not ready, an EA/script may receive only the amount ready by timeout while history download continues; subsequent similar requests can return more data.
- Regardless of `ArraySetAsSeries`, copied data is physically placed with the oldest element at the beginning of allocated memory.
- `start_pos=0` is the current, potentially incomplete bar; closed-bar recovery must exclude it.
- Requests outside available server history or beyond `TERMINAL_MAXBARS` can fail.

Official reference: https://www.mql5.com/en/docs/series/copyrates

Consequences:
1. A positive return smaller than the requested count is a partial result, not proof of catch-up.
2. The recovery loop must persist no cursor advancement for an incomplete/ambiguous requested range.
3. Repeat acquisition while history becomes available, with bounded retries and an explicit retryable state.
4. Normalize the physical array order explicitly and test it; do not rely only on `ArraySetAsSeries` assumptions.
5. Keep the current forming bar excluded from the durable closed-bar stream.
6. Enforce a configured bootstrap/history boundary and handle terminal history limits explicitly; never silently jump to the latest bar when older history is unavailable.
7. A request by position (`start_pos`) and a request by raw timestamp have different semantics. Since the raw time and stable source-order contract are not yet approved, the exact resume method remains unresolved.

### 17.5 Revised acceptance tests

39. Request N bars when only K<N are locally ready; confirm the result is marked partial and cursor is unchanged.
40. Repeat the same bounded request after history download progresses; confirm newly available bars are reconciled without skipping or duplicating.
41. Verify physical array ordering with a known synthetic/demo series for both `ArraySetAsSeries(true)` and `false`; confirm chronological persistence order.
42. Confirm shift 0/current bar is never admitted as a closed bar, while the intended latest closed bar is included.
43. Request data beyond available history and beyond `TERMINAL_MAXBARS`; confirm the stream becomes blocked/retryable or bootstrap-limited rather than jumping forward.
44. Test a database transaction where a prepared insert/bind fails midway; verify rollback and unchanged cursor.
45. Test transaction begin failure and commit failure return paths; neither may be treated as success.
46. Verify prepared parameter binding with symbols/metadata containing quotes, punctuation, and broker suffixes; no SQL text concatenation of untrusted values.
47. Verify `DATABASE_OPEN_COMMON` path behavior and single-writer policy on the exact deployed terminal build.
48. Inspect available SQLite PRAGMA behavior only in a disposable Demo database; record which settings are accepted and read back. Do not assume that accepting a command means its durability effect is proven.

### 17.6 Updated technical disposition

- MQL5 SQLite API existence: **CONFIRMED BY OFFICIAL DOCUMENTATION**.
- Database-level transaction mechanism: **CONFIRMED BY OFFICIAL DOCUMENTATION**.
- Exact power-loss durability on target MT5 build: **NOT PROVEN**.
- Prepared parameter binding: **CONFIRMED BY OFFICIAL DOCUMENTATION**.
- CopyRates partial-history behavior and physical array order: **CONFIRMED BY OFFICIAL DOCUMENTATION**.
- Recovery source position/order semantics: **UNRESOLVED**.
- SQLite proof-of-concept: **NEXT TECHNICAL VALIDATION GATE; NOT IMPLEMENTATION AUTHORIZATION**.

No source/runtime code, tests, workflows, or OOS data were changed or executed during this documentation review.

## 18. Source-bar identity and persistent resume-position decision — 2026-11-26

This section separates three concepts that must not be conflated:
- **Source-bar identity:** which upstream bar observation is being represented.
- **Resume position:** where the capture process should continue reading after restart.
- **Ingest deduplication:** whether a previously received observation has already been stored.

A deduplication key or resume cursor is not automatically a canonical source-bar identity.

### 18.1 Native MqlRates identity review

The official MQL5 `MqlRates` structure exposes exactly these fields: `time`, `open`, `high`, `low`, `close`, `tick_volume`, `spread`, and `real_volume`. Its `time` field is documented as the period start time. The documented structure contains no separate upstream immutable bar ID, revision ID, sequence number, or provider event ID.

Official reference:
- https://www.mql5.com/en/docs/constants/structures/mqlrates

Therefore the reviewed MqlRates/CopyRates interface does not currently provide evidence for Model A's native immutable ID. This is a limitation of the reviewed interface, not proof that no broker/provider-specific identity exists elsewhere. Any such alternative would need its own documented API and source contract.

### 18.2 Resume-position candidates

| Candidate | Persistent across new bars/restart? | Identity quality | Disposition |
| --- | --- | --- | --- |
| CopyRates `start_pos` / bar index | No; relative to the current series and shifts as new bars arrive | Not an identity | **REJECT as durable cursor**; allowed only for bounded relative reads |
| Raw `MqlRates.time` | Not yet proven for this exact broker/API path, restart, history corrections, or duplicate behavior | Period-start label only; UTC remains separately unproven in the EA serialization audit | **CONDITIONAL SAME-STREAM POSITION CANDIDATE ONLY** after controlled tests |
| Composite namespace + canonical symbol + timeframe + verified UTC period-start | Potentially stable if all components and correction semantics are proven | Candidate Model B | **BLOCKED** pending UTC, namespace, symbol alias, uniqueness, and revision evidence |
| OHLCV/spread/payload hash | Changes when history is corrected; identical payloads may recur | Content fingerprint, not source identity | **REJECT as canonical identity**; retain only as payload integrity/evidence hash |
| Broker/provider-native immutable bar ID | Would be preferred if an authoritative API exposes it | Potential Model A | **PREFERRED IF FOUND**, not present in reviewed MqlRates fields |

### 18.3 Why bar index cannot be persisted

`CopyRates` position arguments select bars relative to the current time series. When new bars arrive, the same historical bar moves to a different relative index. A restart does not preserve the old index as a stable source locator. Persisting `start_pos=N` can therefore skip or reread bars after the series advances.

The index may still be used to request a bounded page after the stream has been independently anchored and reconciled. It must never be the only durable cursor or a source-bar ID.

### 18.4 Conditional use of raw period-start time

The raw `MqlRates.time` may be evaluated as a same-stream resume locator only after Demo evidence establishes all of the following for each supported symbol/timeframe/provider stream:
1. strictly ordered period-start values in the exact physical order returned by CopyRates;
2. uniqueness within the stream over the tested history and session boundaries;
3. identical values for the same historical bar after EA restart and terminal restart;
4. stable lookup/replay behavior when the same range is requested repeatedly;
5. behavior when the broker revises a previously returned historical bar;
6. no ambiguous collision across broker symbol aliases, suffixes, or provider namespaces;
7. a safe bounded query strategy that can retrieve the cursor bar and overlap before advancing.

Passing these tests would authorize only a **same-stream resume-position contract**. It would not make the raw value UTC, prove cross-source alignment, or create a globally canonical bar identity.

If a historical correction changes OHLCV while period-start time stays the same, preserve both observations and raise a revision/conflict event. Do not overwrite the earlier capture silently. The system must define whether the broker exposes a revision marker; if not, it can only record that a later observation differed, not prove the provider's internal revision number.

### 18.5 Identity and resume acceptance tests

49. Confirm from the exact MQL5 structure/API used that no additional immutable source ID is exposed; document any broker-specific alternative separately.
50. Capture a known closed-bar range, restart the EA, request the same range, and prove stable same-stream period-start values and deterministic reconciliation.
51. Add new bars between two requests and prove that a persisted CopyRates index points to a different relative bar; confirm index-only recovery is rejected.
52. Re-request overlapping ranges across session/weekend boundaries; prove no silent skip and classify gaps without inventing candles.
53. Simulate or observe a historical OHLCV correction for an existing period-start value; preserve both versions and emit conflict/revision evidence.
54. Test two symbol aliases/suffixes and two provider namespaces; prove they cannot collide in stream identity.
55. Test identical payloads at distinct period starts and changed payloads at the same period start; distinguish payload equality from source identity and revision conflict.

### 18.6 Updated decision

- Native immutable ID in reviewed MqlRates: **NOT EXPOSED BY THE DOCUMENTED STRUCTURE**.
- CopyRates index as persistent cursor: **REJECTED**.
- Raw period-start time as same-stream resume locator: **CONDITIONAL / NOT YET PROVEN**.
- Composite Model B identity: **BLOCKED** until timestamp and namespace contracts pass.
- Payload-derived Model C identity: **REJECTED**.
- Source-bar identity approval: **NOT GRANTED**.
- Persistent cursor implementation: **NOT APPROVED**.
- Demo proof-of-concept: **NEXT EVIDENCE GATE; NOT IMPLEMENTATION AUTHORIZATION**.

No source/runtime code, tests, workflows, OOS data, or trading behavior were changed or executed by this specification update.

## 19. MT5 Demo evidence protocol — operator runbook draft

**Purpose:** define how the unresolved source-position and recovery claims must be tested on a disposable MT5 Demo terminal before any implementation decision. This is a test protocol only. It does not authorize EA changes, database implementation, production capture, or PR creation.

### 19.1 Test environment and isolation

Record the following before the first observation:
- broker/provider display name and a non-secret provider/server identifier;
- MT5 terminal build, operating system, terminal data-path identity, and whether the terminal is portable;
- account mode explicitly marked **DEMO**; do not include account number, credentials, investor password, or other secrets in committed evidence;
- exact Market Watch symbol string, any broker suffix/prefix, contract description, and the timeframe under test;
- terminal history settings including `TERMINAL_MAXBARS`, chart/history availability, and whether the symbol is selected/subscribed;
- local test start/end observations and the clock source used to record them;
- capture source version and file/schema hash, without modifying that source during this protocol.

Use a disposable terminal profile and isolated test storage. Do not point the experiment at an existing production/common capture database. Do not run multiple writers against one test store. Begin with one symbol and one timeframe; expand to all six supported timeframes only after the single-stream protocol is repeatable.

### 19.2 Evidence package for every test

Each test execution must preserve:
1. test ID and exact procedure version;
2. environment record from 19.1;
3. requested CopyRates range/position and requested count;
4. returned count, error/result code, and whether history was still downloading;
5. raw returned values in physical array order before any transformation;
6. the same values after the proposed chronological ordering step;
7. separate raw period-start values and clock observations, without relabelling raw time as UTC;
8. capture/restart/disconnect event log with operator-observed sequence;
9. a machine-readable comparison showing missing, duplicate, reordered, and changed observations;
10. explicit PASS, FAIL, INCONCLUSIVE, or NOT RUN, with the reason.

Screenshots may supplement this package but cannot replace raw data and deterministic comparisons. Redact credentials and personal/account identifiers. Do not commit broker-sensitive data unless repository access and data-sharing permission are confirmed.

### 19.3 Ordered execution sequence

**D0 — Baseline repeatability**
- Select one liquid Demo symbol and one supported timeframe.
- Request a fixed, bounded range of closed bars twice without changing the terminal history.
- Compare count, period-start labels, physical order, OHLCV/spread values, and payload fingerprints.
- Expected result: identical source observations reconcile deterministically. Any unexplained variation is FAIL/INCONCLUSIVE, not silently deduplicated.

**D1 — New-bar index shift**
- Record a known bar's relative CopyRates index and period-start label.
- Allow at least one new bar to become closed.
- Query again and locate the same period-start label.
- Expected result: demonstrate that its relative index changed while its period-start label can be used to locate the same observed bar in this controlled run. This demonstrates why index-only persistence is invalid; it does not yet approve raw-time cursor semantics.

**D2 — EA restart and terminal restart**
- Capture the same bounded closed-bar range.
- Stop/restart the EA, then repeat the same request.
- Separately restart the terminal and repeat.
- Expected result: same period-start labels and deterministic reconciliation. Any missing historical range or changed label requires investigation; no cursor may jump to the newest bar.

**D3 — Disconnect and delayed history**
- In Demo, disconnect the terminal or make the test history unavailable, then reconnect.
- Request a bounded range where the terminal may initially have only part of the requested history ready.
- Repeat the same request after history download progresses.
- Expected result: partial count is explicitly partial; no completion/cursor advancement is inferred until the full requested range is reconciled. Record if the broker/server cannot reproduce delayed history; mark NOT RUN rather than assume PASS.

**D4 — Session boundary and gap classification**
- Select a range crossing a known market closure/weekend or a documented instrument session break.
- Compare returned period-start sequence with an independently recorded session calendar for that instrument.
- Expected result: only calendar-supported closures may be classified as EXPECTED_SESSION_GAP. Without authoritative calendar evidence, use GAP_UNKNOWN; never fabricate a bar to fill the interval.

**D5 — Historical correction / revision observation**
- Save an immutable copy of a bounded historical response.
- At a later time, request exactly the same range and compare all fields.
- If a changed historical value is observed, preserve both versions and record a conflict event with observation times and raw values.
- If no correction occurs during the observation window, record NOT OBSERVED; this is not proof that corrections never occur. Do not manufacture a correction in a live broker history and do not claim provider revision semantics from a changed payload alone.

**D6 — Symbol namespace isolation**
- Compare a broker symbol with any suffix/prefix alias only where the broker confirms the instruments represent the same underlying contract.
- Compare the same display symbol across distinct Demo provider/server namespaces only if available.
- Expected result: stream keys remain isolated unless a reviewed canonical instrument mapping explicitly joins them. Similar display names are not sufficient.

**D7 — Current-bar exclusion and physical ordering**
- Request data including shift 0 and multiple closed bars.
- Verify that shift 0 is excluded from the admitted closed-bar dataset.
- Verify chronological persistence order from the physical array, with tests under both ArraySetAsSeries settings.
- Expected result: current/forming bar is never committed as closed; oldest-to-newest persistence order is explicit and deterministic.

### 19.4 Per-test pass/fail rules

A test may be PASS only when its raw evidence package is complete and all stated assertions hold. Use:
- **FAIL** when evidence contradicts an assertion (e.g. a skipped bar, index-only cursor ambiguity, unstable ordering, current bar admitted as closed, or cursor advanced after a partial read).
- **INCONCLUSIVE** when evidence is contradictory or insufficient to decide (e.g. clock source cannot be trusted, broker history changes without clear provenance, or session calendar is unavailable).
- **NOT RUN** when the Demo environment cannot exercise the condition.
- **PASS** only for the narrow assertion tested. A PASS on restart stability does not prove UTC, global identity, power-loss durability, or historical completeness.

No test result may be generalized from one symbol/timeframe/provider to all streams without repeating the relevant tests for each required stream class.

### 19.5 Evidence review gates after Demo

The review must answer, separately:
1. Is raw period-start time stable enough for same-stream resume in this exact environment?
2. Is its uniqueness demonstrated for the configured stream and tested history?
3. Can the API reliably re-read an overlap around the saved position?
4. Can history corrections be detected and preserved without overwriting evidence?
5. Is source namespace and symbol identity sufficiently stable?
6. Is the clock domain independently proven for any UTC claim?
7. Is the storage transaction/durability behavior proven under the defined failure model?

If questions 1–5 pass, a narrowly scoped same-stream resume proposal may be submitted for approval. Questions 6 and 7 remain independent gates; passing the resume tests does not close them.

### 19.6 Exit criteria and authorization boundary

The Demo evidence package must be reviewed and the source-position contract explicitly approved before a persistent cursor implementation is proposed. A separate explicit user approval is still required before source/runtime code changes or PR creation.

Until then:
- recovery implementation: **NOT AUTHORIZED**;
- MQL5 SQLite proof-of-concept implementation: **NOT AUTHORIZED**;
- raw timestamp as persistent cursor: **NOT APPROVED**;
- UTC/cross-source MTF joins: **BLOCKED**;
- production recovery-complete claim: **BLOCKED**;
- 2025 OOS: **LOCKED / NOT TOUCHED**;
- live orders: **NOT AUTHORIZED**.

No source/runtime code, tests, workflows, OOS data, or trading behavior were changed or executed by this runbook addition.


## 20. Operator Test Sheets — D0 Baseline Repeatability and D1 New-Bar Index Shift

This section converts D0 and D1 from the Section 19 Demo protocol into reproducible operator procedures. It is a documentation-only addition. It does not authorize implementation, alter the capture EA, or claim that any Demo test has been run.

### 20.1 Common test controls

Before either test:

1. Use an isolated disposable MT5 terminal and Demo account. Do not use a live account.
2. Record broker/provider name, Demo server label (redact account identifiers), terminal build, OS/version, EA source version and SHA-256, symbol as displayed by Market Watch, timeframe, and TERMINAL_MAXBARS.
3. Select one symbol and one timeframe only. Do not change symbol aliases, timeframe, broker connection, terminal build, or history settings during a test run.
4. Use a bounded historical interval that is already fully available in the terminal. Exclude the currently forming bar (shift 0). Record the exact requested interval and the expected number of closed bars before comparing results.
5. Save original raw output and screenshots/log excerpts as evidence. Do not manually edit captured rows. Store each run in a separate, clearly named evidence folder.
6. Record all times exactly as observed, including the field name and source clock. Do not relabel raw MT5 time as UTC.
7. Record outcomes as PASS, FAIL, INCONCLUSIVE, or NOT RUN. Missing evidence is not PASS.

Common evidence fields:
- test_id, run_id, operator, observation_start, observation_end;
- broker_provider, demo_server_label, terminal_build, OS_version;
- EA_version, EA_SHA256, symbol_market_watch, timeframe, TERMINAL_MAXBARS;
- CopyRates_start_pos, CopyRates_requested_count, CopyRates_returned_count, CopyRates_return_value_or_error;
- history_download_status, array_series_setting, physical_array_index, raw_bar_time, OHLC, tick_volume, spread, real_volume;
- observed server/terminal/host clock fields exactly as emitted;
- expected_count, observed_unique_count, duplicate_count, missing_count, out_of_order_count;
- evidence_file_names and SHA-256 hashes;
- result, reason, reviewer, review_date.

### 20.2 D0 — Baseline repeatability

**Question:** Given the same already-available closed-bar interval, does repeated CopyRates retrieval return the same ordered bar records in the same terminal environment?

**Procedure:**

1. Choose one symbol/timeframe and a fixed historical interval. Record the interval in the raw time representation returned by MT5; do not infer UTC.
2. Determine the intended closed-bar count N for that interval. Ensure the interval excludes shift 0 and is within locally available history.
3. Request the same bounded interval twice using the same API path and identical parameters. Save each returned array before any transformation.
4. Record CopyRates requested and returned counts, return/error state, history synchronization state, and ArraySetAsSeries setting for each run.
5. Preserve physical array order exactly as returned. Separately produce a comparison view sorted by the documented/observed bar-time field; do not overwrite the raw capture.
6. Compare run A and run B by position and by raw field values. Compare time, OHLC, tick volume, spread, and real volume; do not compare only a derived hash.
7. If any count is partial, history is still downloading, or an API error occurred, repeat only after history is ready and retain the incomplete attempt as evidence.

**PASS criteria (narrow):**
- Both calls return exactly N records for the same bounded closed-bar interval.
- Both calls have successful, fully available history status.
- The same raw bar-time sequence and all captured bar fields match record-for-record.
- No duplicate, missing, or out-of-order record is observed within the tested interval.
- Raw physical order and the comparison order are both documented.

**FAIL criteria:**
- With complete history and successful calls, the same fixed request returns conflicting bar records, missing/extra records, duplicates, or inconsistent ordering.
- A forming bar is included despite the test's closed-bar-only selection.

**INCONCLUSIVE / NOT RUN:**
- Partial CopyRates result, history still downloading, terminal error, uncertain interval boundaries, or insufficient evidence.
- A single successful call is NOT repeatability evidence.
- A PASS does not establish restart stability, broker-wide behavior, UTC, immutable identity, correction policy, or crash durability.

**D0 evidence summary template:**

| Field | Run A | Run B |
|---|---|---|
| Requested interval | | |
| Requested count N | | |
| Returned count | | |
| CopyRates result/error | | |
| History ready? | | |
| ArraySetAsSeries | | |
| First raw time in physical array | | |
| Last raw time in physical array | | |
| Duplicate / missing / out-of-order counts | | |
| Field-by-field identical? | | |
| Evidence package SHA-256 | | |

### 20.3 D1 — New-bar index shift observation

**Question:** Does the positional bar index shift when a new bar is added, demonstrating why a relative CopyRates shift/index is not a durable resume cursor?

**Procedure:**

1. Use the same isolated Demo environment, one symbol, and one timeframe. Confirm the terminal has synchronized history.
2. Before the next bar boundary, select and record one already-closed reference bar. Capture its raw time and full OHLCV/spread fields, plus the CopyRates shift/index used to locate it.
3. Record the current server/terminal/host clock observations without converting them to UTC. Record the timeframe and expected next bar boundary as an observation, not as a guaranteed broker clock rule.
4. Wait until MT5 shows that a new bar has actually opened and the prior current bar has closed. Verify this from a fresh API request; do not rely only on a wall-clock estimate.
5. Request the same reference bar again by the same bounded-history method. Record its new relative shift/index and its raw time and full fields.
6. Compare the before/after observations. The intended demonstration is that the same reference bar is now at a different relative index while its raw period-start label and bar fields remain the same in this controlled observation.
7. Repeat for at least two observed new-bar transitions if practical, keeping all observations in the same stream and session.

**PASS criteria (narrow):**
- A new closed bar is independently observed after the transition.
- The exact same reference bar is found before and after.
- Its relative shift/index changes as newer bars are added.
- Its raw time and captured bar fields remain identical during the observation.

**FAIL criteria:**
- The reference bar cannot be uniquely located in the bounded history, or its fields change without a documented correction/revision event.
- The observed index does not shift despite proof that a newer bar was added and the same indexing convention was used; investigate the test method and repeat before drawing a conclusion.

**INCONCLUSIVE / NOT RUN:**
- No confirmed new bar, terminal/history synchronization issue, changed indexing convention, or incomplete evidence.
- A PASS demonstrates only that the tested relative index is positional and shifts in this environment. It does not prove raw time is a safe cursor or immutable source-bar ID.

**D1 evidence summary template:**

| Field | Before new bar | After new bar |
|---|---|---|
| Observation time/source clock | | |
| Reference raw bar time | | |
| Reference bar relative shift/index | | |
| Reference OHLC | | |
| Reference tick volume / spread / real volume | | |
| Newer closed bar observed? | N/A | |
| ArraySetAsSeries | | |
| Same reference bar uniquely matched? | | |
| Evidence package SHA-256 | | |

### 20.4 Review and stop conditions

- Do not use a D0 or D1 result to authorize a persistent cursor.
- Do not substitute a CopyRates shift/index for a source-bar identity or durable resume position.
- If a test produces conflicting data, preserve both observations and stop cursor-design conclusions until the conflict is explained.
- If any evidence field is unavailable, mark it unavailable; do not synthesize a value.
- D0/D1 evidence must be reviewed alongside D2–D7 and the storage durability tests before any source-position contract can be considered.
- No Demo test is claimed as executed by this specification update. Operator execution and evidence review remain outstanding.

