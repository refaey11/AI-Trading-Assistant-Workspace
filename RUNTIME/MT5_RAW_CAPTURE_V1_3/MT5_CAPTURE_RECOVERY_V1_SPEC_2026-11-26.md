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



## 21. Operator Test Sheets — D2 Restart and D3 Disconnect / Delayed-History Recovery

This section expands D2 and D3 from Section 19 into operator procedures. These are evidence-gathering tests, not implementation instructions. The currently inspected V1.3 EA keeps its seen-bar state in memory and captures the latest closed bar; a successful terminal history download after reconnect must not be mistaken for proof that the EA's raw capture file recovered every missed bar.

### 21.1 D2 — EA restart and terminal restart

**Question:** After restarting the EA or the terminal, can the operator establish exactly which closed bars were captured before and after restart, and identify any gap, duplicate, or replay?

**Test variants (run and report separately):**
- D2-A: remove/re-attach or otherwise restart the EA while keeping the terminal session running.
- D2-B: close and relaunch the MT5 terminal, then allow the same EA/configuration to start again.

Do not combine the two variants into one result. They exercise different state-loss boundaries.

**Preparation:**
1. Use an isolated Demo terminal, one symbol and one timeframe, and a period with expected market activity. Record the environment fields required by Section 20.1.
2. Ensure history is synchronized before starting. Record the latest fully closed reference bar and a bounded overlap interval of prior closed bars.
3. Preserve a copy of the raw capture output before restart. Record its file size, last complete row, row count, and SHA-256. Do not edit or truncate the source file.
4. Record the EA inputs and output destination. Ensure no second EA instance or terminal is writing to the same stream/file.
5. Record the last observed closed bar before the restart using the raw timestamp representation and full OHLCV/spread fields. Do not call that timestamp UTC.

**D2-A procedure — EA-only restart:**
1. Start capture and allow at least several closed bars to be observed and written.
2. Record the final complete captured row and restart the EA without changing symbol, timeframe, inputs, terminal, or output destination.
3. Record the restart time and all available log messages.
4. After restart, observe subsequent closed bars and preserve the raw output.
5. Independently query the terminal's bounded closed-bar history covering the pre-restart overlap and post-restart interval. Save the query parameters and returned records separately from the EA output.
6. Compare the independent history with the EA capture sequence. Report missing, duplicate, conflicting, and replayed records; do not silently deduplicate the evidence.

**D2-B procedure — terminal restart:**
1. Repeat the preparation and capture steps from a clean run.
2. Close the terminal normally. Record the last complete raw row and hash before closing.
3. Relaunch the same terminal installation and Demo server. Verify the same symbol/timeframe and EA inputs; record any environment change.
4. Allow history synchronization to complete and capture subsequent closed bars.
5. Save the post-restart raw output and logs. Independently query the bounded overlap history and compare it with the raw capture.
6. If the terminal or EA creates a new output file, preserve both files and document the exact path/name; do not merge them manually.

**PASS criteria (observation only):**
- The restart boundary and environment are fully documented.
- Pre-restart and post-restart raw evidence is preserved and independently comparable.
- Every expected closed bar in the bounded test interval is accounted for as captured, intentionally replayed, or explicitly classified as missing/uncertain.
- No conflicting duplicate is silently overwritten or discarded.
- The result clearly distinguishes EA output completeness from terminal-history availability.

A D2 PASS does **not** mean the current EA has a production recovery mechanism. If the EA output omits intermediate bars while CopyRates later exposes them, report that as a capture gap even though terminal history is available.

**FAIL criteria:**
- The test demonstrates a missing closed bar in the EA capture output with no documented intentional exclusion.
- A restart causes a duplicate/conflicting record to overwrite prior evidence or causes the output sequence to become ambiguous.
- The system resumes from the latest bar while the intervening interval is not reconciled.

**INCONCLUSIVE / NOT RUN:**
- No confirmed bar close occurred during the test window.
- History is incomplete or still downloading.
- Output files/logs are missing, the restart type cannot be established, or another writer was active.
- The observed interval cannot be bounded reliably.

**D2 evidence summary template:**

| Field | D2-A EA restart | D2-B terminal restart |
|---|---|---|
| Environment unchanged? | | |
| Last complete pre-restart row | | |
| Pre-restart row count / SHA-256 | | |
| Restart start/end observation | | |
| First post-restart complete row | | |
| Output file continuity/path | | |
| Independent history ready? | | |
| Expected closed bars in interval | | |
| Captured / replayed / missing / conflicting counts | | |
| Logs and evidence SHA-256 | | |
| Result and reason | | |

### 21.2 D3 — Disconnect and delayed-history recovery

**Question:** During a controlled connection interruption, what bars are absent from the live capture stream, what bars later become available from terminal history, and does the evidence distinguish those two facts?

**Important distinction:** This test first measures the behavior of the existing capture path. It does not assume that reconnecting automatically backfills missed bars. A later CopyRates query returning historical bars proves only that the terminal can supply those bars at that time; it does not prove the EA wrote them to its raw capture output.

**Preparation:**
1. Use a Demo account and an isolated terminal. Choose one symbol/timeframe with expected market activity and a short test window.
2. Record the last complete captured closed bar and preserve the raw output, row count, file size, and SHA-256.
3. Record the broker/server label and observed clock fields. Do not infer UTC or assume fixed broker offset.
4. Define a test interruption window and a safe method to disconnect/reconnect the Demo terminal without changing the account, symbol, timeframe, or EA inputs.
5. Before disconnecting, record the last known fully closed bar and the independent-history query parameters that will later be used for reconciliation.

**Procedure:**
1. Start capture and confirm normal writes before the interruption.
2. Disconnect the Demo terminal/network using the planned safe method. Record the exact observable start and end events; do not assume the EA can log while disconnected.
3. Allow at least two expected bar closes during the interruption where market/session conditions permit. If this cannot be achieved, mark the test INCONCLUSIVE rather than manufacturing a gap.
4. Reconnect. Record connection restoration and wait until terminal history reports ready for the tested symbol/timeframe.
5. Save the EA raw capture output immediately after reconnect and preserve all logs.
6. Independently request the bounded closed-bar history spanning the last pre-disconnect bar through the post-reconnect period. Record requested count, returned count, errors, and synchronization state.
7. Compare three timelines separately:
   - bars present in the raw capture before disconnection;
   - bars written by the EA after reconnection;
   - bars available through the independent CopyRates history query.
8. For each expected closed bar in the interruption window, classify it as CAPTURED_DURING, BACKFILLED_AFTER_RECONNECT, HISTORY_AVAILABLE_BUT_NOT_CAPTURED, MISSING_FROM_HISTORY, or GAP_UNKNOWN. Use these as evidence labels only; do not claim the current EA supports backfill unless the raw output proves it.
9. If CopyRates returns fewer records than requested or history is still downloading, preserve the partial result, do not declare the interval complete, and repeat the same bounded query after synchronization.
10. Preserve all raw attempts, including partial/error responses. Do not replace an earlier response with a later successful one.

**PASS criteria (observation only):**
- The disconnect/reconnect interval is documented and the independent history is demonstrably ready.
- The expected closed-bar interval is bounded and reconciled record-by-record.
- Every bar is assigned an evidence-backed classification; unknowns remain GAP_UNKNOWN.
- The report explicitly states whether the EA output itself contains every expected bar.
- No partial CopyRates response is treated as complete and no missing interval is silently skipped.

**FAIL criteria:**
- A bar known to have closed during the interruption is absent from EA output and the system nevertheless reports uninterrupted/complete capture.
- A partial history result is accepted as complete or the capture resumes at the latest bar without classifying the intervening interval.
- Duplicate/conflicting rows are overwritten or discarded without retaining evidence.

**INCONCLUSIVE / NOT RUN:**
- No bar close occurred during disconnection, session was closed, or market data was unavailable.
- Reconnect did not complete, history remained partial, or the independent expected interval cannot be established.
- The operator cannot preserve both pre- and post-interruption outputs.

**D3 evidence summary template:**

| Field | Value |
|---|---|
| Last complete pre-disconnect raw bar | |
| Disconnect observed at / source clock | |
| Reconnect observed at / source clock | |
| Number of expected closed bars during interruption | |
| CopyRates requested / returned count | |
| History ready after reconnect? | |
| Captured during interruption | |
| Backfilled after reconnect in EA output | |
| History available but not captured | |
| Missing from history / GAP_UNKNOWN | |
| Duplicate / conflicting rows | |
| Raw output file hashes before/after | |
| Logs and query evidence hashes | |
| Result and reason | |

### 21.3 Stop conditions and interpretation

- Stop and preserve evidence if the EA output unexpectedly truncates, rotates, changes schema, or is written by another process.
- Do not infer missing bars from elapsed wall-clock time alone. Use the tested market session and independent history evidence; otherwise classify the interval GAP_UNKNOWN.
- Do not infer that all missing bars are recoverable merely because CopyRates can return some older bars.
- Do not advance or approve any persistent cursor based on D2/D3 alone. Cursor semantics, source identity, storage atomicity, history corrections, and clock provenance remain separate gates.
- D2/D3 execution has not been performed by this documentation update. The operator must run the tests in the isolated Demo environment and submit the evidence for review.



## 22. Operator Test Sheets — D4 Session-Gap Classification and D5 Historical-Bar Revision

These tests examine two different sources of apparent history discontinuity: legitimate market-session closures and later changes to historical bar data. They must be run separately and must not be used to approve a source-bar ID or durable cursor by themselves.

### 22.1 D4 — Session-gap classification

**Question:** Can each interval between consecutive observed bars be classified using independent, broker/symbol-appropriate session evidence, without assuming that every elapsed timeframe interval must contain a bar?

**Prerequisites:**
1. Use one Demo symbol and timeframe in an isolated terminal.
2. Obtain an independent session calendar applicable to the exact broker, instrument, and date range. Record its source, version/publication date, timezone semantics, holidays, early closes, and any known special sessions.
3. If a reliable calendar cannot be obtained, the test may still record raw intervals, but it cannot classify them as expected session gaps.
4. Preserve the raw EA output and a separate bounded CopyRates history query. Record query parameters, requested/returned counts, errors, and history synchronization state.
5. Do not convert raw MT5 bar timestamps to UTC or infer broker offset/DST from the observed data.

**Procedure:**
1. Select a bounded interval that includes at least one expected active period and, if available, one known market closure (for example, a weekend or published holiday).
2. Capture the bars available through the EA and independently query closed-bar history for the same bounded interval.
3. Order observations only within the tested stream using a timestamp/order interpretation that is explicitly marked UNVERIFIED unless its semantics have been independently established.
4. For each interval where a bar is absent, consult the independent session calendar for the exact instrument and date.
5. Record whether the calendar predicts the market was open, closed, on an early close, or indeterminate. Preserve the calendar evidence used for each classification.
6. Repeat the bounded history query after synchronization if CopyRates is partial. Preserve both the partial and later responses.
7. Assign one of the following evidence labels to each interval:
   - EXPECTED_SESSION_GAP — an authoritative applicable calendar explains the interval;
   - MISSING_DATA_SUSPECTED — the calendar indicates the instrument should have been trading and the expected bar is absent from the verified comparison source;
   - GAP_UNKNOWN — calendar, timestamp semantics, history readiness, or expected-bar evidence is insufficient;
   - CONTIGUOUS_CONFIRMED — the relevant expected sequence is present under the tested, documented ordering contract.
8. Do not create synthetic candles to fill any interval.

**PASS criteria (classification only):**
- Calendar provenance and applicability are documented.
- Every assessed interval has evidence attached and is classified without using elapsed wall-clock time alone.
- Expected closures are not counted as missing bars.
- Suspected missing data is distinguished from unknown intervals.
- Any timestamp or ordering limitation is explicitly retained in the result.

**FAIL criteria:**
- The process labels every missing timeframe slot as a data-loss event without session evidence.
- A known active-session interval is silently skipped or marked complete despite absent expected data.
- A session closure is filled with fabricated bars or hidden by normalization.
- Calendar timezone or instrument applicability is guessed rather than evidenced.

**INCONCLUSIVE / NOT RUN:**
- No authoritative applicable session calendar is available.
- The tested broker/instrument session schedule cannot be established.
- History is partial, timestamp ordering is not adequate for the comparison, or the test interval is not bounded.
- No relevant gap occurs during the observation window.

**D4 evidence summary template:**

| Field | Value |
|---|---|
| Broker/server and instrument | |
| Symbol as shown by terminal | |
| Timeframe and bounded interval | |
| Session calendar source/version | |
| Calendar timezone/semantics | |
| Holidays / early closes covered | |
| Raw bars expected by calendar | |
| Raw bars present in EA output | |
| Raw bars present in independent history | |
| EXPECTED_SESSION_GAP intervals | |
| MISSING_DATA_SUSPECTED intervals | |
| GAP_UNKNOWN intervals | |
| Partial CopyRates attempts and results | |
| Evidence file hashes | |
| Result and reason | |

### 22.2 D5 — Historical-bar revision observation

**Question:** Does the same historical bar, when queried again later from the same documented source stream, return changed values or become unavailable, and can the observation be preserved without overwriting the original capture?

**Important limitation:** A test that observes no change only establishes that no change was observed for the selected bars, source, and observation period. It does not prove that the broker never revises history or that other symbols/timeframes/providers behave identically.

**Preparation:**
1. Use an isolated Demo terminal, one symbol, one timeframe, and a bounded set of fully closed bars.
2. Record broker/server identity, terminal build, EA/capture version, symbol spelling/alias, timeframe, query parameters, and observed clock fields.
3. Save the first raw response exactly as received, including OHLC, tick volume, spread, real volume, raw time representation, returned count, error/status, and query metadata.
4. Compute and record a SHA-256 fingerprint of the preserved evidence package. This is an integrity fingerprint for the package, not a source-bar identity.
5. Do not edit the original capture or merge subsequent observations into it.

**Procedure:**
1. Query a bounded range of fully closed historical bars and preserve the complete first response as OBSERVATION_A.
2. Record the exact query range, CopyRates requested and returned counts, synchronization status, and array ordering configuration.
3. Repeat the identical query after a documented delay and after any relevant history synchronization event. Preserve the response as OBSERVATION_B.
4. Where practical, repeat at a later observation point as OBSERVATION_C. Keep each response immutable and separately hashed.
5. Match candidate bars only using a documented, tested within-stream matching method. Until raw timestamp uniqueness and stability are established, treat timestamp matching as provisional and report ambiguity.
6. Compare every available field independently: raw time, OHLC, tick volume, spread, and real volume. Do not compare only a row hash and infer which field changed.
7. Classify each candidate bar:
   - UNCHANGED_OBSERVED — all compared fields match across the observations;
   - REVISION_OBSERVED — one or more compared fields differ for a provisionally or authoritatively matched bar;
   - BAR_DISAPPEARED — a previously returned bar is absent in a later complete, synchronized response;
   - BAR_APPEARED_LATER — a bar absent in an earlier response appears in a later complete response;
   - MATCH_AMBIGUOUS — the source-bar matching key is not sufficiently unique/stable;
   - QUERY_INCOMPLETE — one or more responses are partial, unsynchronized, or otherwise not comparable.
8. Preserve all conflicting versions. Do not replace OBSERVATION_A with OBSERVATION_B or treat the latest value as proof that the earlier capture was invalid.
9. If a change is observed, repeat the query and retain the repeated result. Do not automatically label the cause as broker correction; first exclude query-range differences, partial history, symbol alias changes, timeframe/configuration changes, and ordering mistakes.

**PASS criteria (observation protocol only):**
- Multiple immutable observations of the same bounded query are preserved with query metadata and hashes.
- Comparisons are field-by-field and ambiguous matches remain explicitly ambiguous.
- Any observed revision or disappearance is retained as a conflict/evidence event rather than overwriting the first observation.
- If no changes are observed, the conclusion is narrowly worded as NOT OBSERVED for this sample and observation window.

**FAIL criteria:**
- A later historical response silently overwrites the earlier captured values.
- Different query ranges, symbol aliases, or synchronization states are treated as identical observations without qualification.
- A partial response is used to conclude that a bar disappeared.
- An ambiguous timestamp match is presented as a confirmed revision.

**INCONCLUSIVE / NOT RUN:**
- History is not fully synchronized or responses are partial.
- The tested source cannot be held constant across observations.
- Bar matching is ambiguous or the query range cannot be reproduced.
- The observation window is too short to support any conclusion beyond NOT OBSERVED.

**D5 evidence summary template:**

| Field | Observation A | Observation B | Observation C |
|---|---|---|---|
| Observation date/time and clock source | | | |
| Broker/server / terminal build | | | |
| Symbol / timeframe | | | |
| Exact query range and parameters | | | |
| CopyRates requested / returned count | | | |
| History synchronized? | | | |
| Raw response file SHA-256 | | | |
| Matched bars / ambiguous matches | | | |
| OHLC changes | | | |
| Tick volume changes | | | |
| Spread changes | | | |
| Real volume changes | | | |
| Bars appeared / disappeared | | | |
| Result and reason | | | |

### 22.3 D4/D5 interpretation and authorization boundary

- D4 can classify only the tested instrument/session/date range. It does not define a universal market calendar or authorize UTC conversion.
- D5 can report observed revisions only for the tested source and sample. No observed revision is not proof of immutable history.
- A revision observation means the capture design must preserve conflicting versions and define a reviewed revision policy before production recovery is considered.
- Neither test authorizes Model A source identity, Model B composite identity, raw timestamp cursor use, SQLite implementation, or production recovery claims.
- D4/D5 execution has not been performed by this documentation update. Operator evidence collection and independent review remain outstanding.
- Development remains restricted to 2016–2024. The 2025 OOS dataset remains locked and untouched.
- No trading logic, source/runtime code, workflows, or live-order behavior is changed or authorized by this section.


## 23. Operator Test Sheets — D6 Symbol-Namespace Isolation and D7 Closed-Bar / Array-Order Semantics

D6 and D7 test whether observations from different symbol namespaces remain isolated and whether CopyRates array behavior is understood correctly. Neither test establishes a universal source-bar identity or approves a persistent cursor.

### 23.1 D6 — Symbol namespace isolation

**Question:** When two terminal-visible symbols may represent the same underlying instrument but have different broker names, suffixes, prefixes, contract specifications, or data feeds, can the capture evidence keep their streams distinct without silently merging them?

**Preparation:**
1. Use an isolated Demo terminal and identify two symbols that are available from the same broker but have different terminal symbol names or namespaces. Do not assume they are equivalent merely because their labels look similar.
2. Record the exact symbol names as returned by the terminal, broker/server identity, contract description, digits, point size, tick size/value where available, and any suffix/prefix.
3. Record the EA version/hash, terminal build, timeframe, output path, and single-writer arrangement.
4. Choose a bounded interval where both symbols have history. Preserve the initial Market Watch / symbol selection evidence and the exact CopyRates query parameters for each stream.
5. Do not normalize case, strip suffixes, or map aliases during collection. Preserve the source spelling exactly.

**Procedure:**
1. Capture symbol A and symbol B independently, recording the exact terminal symbol argument used for each request.
2. Save each stream's raw rows and logs separately where possible. If the EA writes to a shared file, retain the original file and verify that each row contains enough source information to identify the exact requested symbol.
3. Independently query the same bounded closed-bar interval for each exact symbol name and preserve both responses.
4. Compare the symbol field, raw timestamp, OHLC, tick volume, spread, real volume, and query metadata across the two streams.
5. Repeat the queries with the same exact symbol names after a terminal restart or history synchronization event, if the test environment allows.
6. Check whether two aliases have identical bars, different bars, overlapping timestamps, or different trading sessions. Identical OHLC values do not prove that the symbols are the same source stream.
7. Verify that a row from symbol A is never assigned to symbol B solely because the timestamp and OHLC match.
8. Record any mapping proposed by the broker or terminal documentation as external evidence; do not create a canonical-symbol mapping from visual similarity alone.

**PASS criteria (isolation observation only):**
- Every captured/query row can be traced to the exact requested terminal symbol name and broker/server namespace.
- A and B remain separate streams even when their bar timestamps or OHLC values happen to match.
- Any alias relationship is documented with independent evidence and is not silently applied by the capture process.
- Missing symbol provenance, ambiguous aliases, or conflicting source labels are reported as unresolved.

**FAIL criteria:**
- The capture or comparison process merges A and B based only on matching timestamp/OHLC or a guessed alias.
- Suffixes/prefixes or case are silently removed and the original source spelling is lost.
- A row cannot be traced to the exact symbol request that produced it.
- Data from one symbol is attributed to another without authoritative mapping evidence.

**INCONCLUSIVE / NOT RUN:**
- Only one symbol is available.
- The broker's symbol namespace or instrument mapping cannot be established.
- History for one symbol is incomplete or the test interval cannot be compared.
- The EA output does not preserve enough symbol provenance to identify the source stream.

**D6 evidence summary template:**

| Field | Symbol A | Symbol B |
|---|---|---|
| Exact terminal symbol name | | |
| Broker/server namespace | | |
| Contract / instrument description | | |
| Suffix / prefix / case | | |
| Digits / point / tick details | | |
| Timeframe and bounded interval | | |
| CopyRates requested / returned count | | |
| Raw output file and SHA-256 | | |
| Rows with exact symbol provenance | | |
| Timestamp overlap | | |
| Identical / different OHLC observations | | |
| Session differences | | |
| Alias evidence source | | |
| Result and reason | | |

### 23.2 D7 — Current-bar exclusion and physical array ordering

**Question:** Does the operator correctly identify the currently forming bar versus fully closed bars, and correctly interpret the physical array order returned by CopyRates under both ArraySetAsSeries settings?

**Preparation:**
1. Use one Demo symbol and timeframe with synchronized history.
2. Record terminal build, symbol, timeframe, EA/test harness version, CopyRates start position and requested count, ArraySetAsSeries setting, and query observation time/source clock.
3. Select a bounded query that includes the current bar and several earlier bars. Do not infer that array index zero always means the oldest or newest element without considering the series setting and documented physical storage behavior.
4. Preserve the raw returned array values and the exact query parameters for each run.

**Procedure:**
1. Run a controlled CopyRates query with start position 0 and a fixed requested count. Record the returned count and every element's array index, raw bar time, OHLC, and volume fields.
2. Repeat the same query with ArraySetAsSeries enabled, preserving the complete array and configuration.
3. Repeat with ArraySetAsSeries disabled, preserving the complete array and configuration.
4. Compare the physical memory sequence and the logical indexing view. Record the oldest physical element and newest physical element explicitly.
5. Identify the forming bar using an independent observation of the terminal's current bar state, not merely by assuming that a particular array index is closed.
6. Identify the latest fully closed bar separately. Verify that the intended capture selection excludes the forming bar and includes the latest closed bar.
7. Repeat the query after a new bar begins. Record how the current bar and latest closed bar move in the logical array view and in the returned physical sequence.
8. If fewer bars are returned than requested, preserve the partial result and mark the run incomplete; do not infer a complete ordering result from a truncated array.
9. Repeat the bounded query after history synchronization if needed, preserving both attempts.

**PASS criteria (array semantics observation only):**
- Both ArraySetAsSeries configurations are recorded and their logical indexing is distinguished from physical memory order.
- The oldest and newest returned elements are identified from the actual captured sequence and checked against the documented CopyRates behavior.
- The forming bar and latest fully closed bar are independently identified.
- The result demonstrates that the forming bar is excluded from a closed-bar capture selection.
- Partial results are not treated as complete.

**FAIL criteria:**
- The process treats index 0 as a universal oldest/newest indicator regardless of ArraySetAsSeries and physical storage semantics.
- The forming bar is included in a dataset labelled closed bars.
- The latest fully closed bar is omitted while a forming bar is selected in its place.
- The test silently reorders or rewrites raw observations without preserving the original returned sequence.

**INCONCLUSIVE / NOT RUN:**
- The terminal history is not synchronized or CopyRates returns partial data.
- The forming/closed state cannot be independently established.
- The two ArraySetAsSeries runs do not use equivalent query parameters.
- The terminal build or test harness does not expose enough evidence to reconstruct the returned sequence.

**D7 evidence summary template:**

| Field | Series=true | Series=false |
|---|---|---|
| Terminal build / symbol / timeframe | | |
| start_pos / requested count | | |
| Returned count / error | | |
| Observation time/source clock | | |
| Physical first element raw time | | |
| Physical last element raw time | | |
| Logical index 0 raw time | | |
| Logical final index raw time | | |
| Forming bar identified? | | |
| Latest fully closed bar identified? | | |
| Closed-bar selection excludes shift 0? | | |
| Raw array evidence SHA-256 | | |
| Result and reason | | |

### 23.3 D6/D7 interpretation and authorization boundary

- D6 applies only to the tested broker, symbols, terminal build, and timeframe. It does not approve a universal symbol canonicalization policy.
- D7 validates observed CopyRates array semantics for the tested build and call pattern. It does not approve a durable resume cursor or immutable source-bar identity.
- A successful D7 result must not be used to promote CopyRates relative shift/index into a persistent cursor; bar positions move as new bars arrive.
- Any ambiguous symbol mapping or array-order discrepancy blocks the relevant conclusion and must be preserved as evidence.
- D6/D7 execution has not been performed by this documentation update. Operator execution and evidence review remain outstanding.
- Recovery implementation, SQLite PoC, raw timestamp cursor, UTC/cross-source MTF joins, and production recovery-complete claims remain unauthorized or blocked pending their separate evidence and approval gates.
- Development remains restricted to 2016–2024. The 2025 OOS dataset remains locked and untouched.
- No source/runtime code, workflows, trading behavior, or live orders are changed or authorized by this section.


## 24. Storage Proof Plan — SQLite Transaction, Failure, and Durability Tests (Acceptance Tests 29–48)

This section turns acceptance tests 29–48 into a controlled evidence plan. It does not authorize building a SQLite prototype, changing the EA, writing a fault-injection harness, or claiming durability. Any test that requires new executable code remains NOT RUN until separately authorized. Documentation review and environment inventory may be performed without changing runtime behavior.

### 24.1 Storage-test safety and test environment

**Required isolation:**
1. Use a disposable MT5 Demo terminal/profile and a disposable database path. Never point fault-injection tests at a live account, production capture store, or the only copy of any evidence.
2. Record terminal build, OS version/filesystem, storage device/type, broker/server, EA build/hash, MQL5 database API availability, database path mode, and test harness version/hash.
3. Enforce one writer for the test database. Any Python inspection must use a read-only connection and must not mutate the database while the EA/test harness is writing.
4. Preserve a baseline backup and hash before each destructive test. After every test, preserve the database, WAL/journal sidecars if present, logs, and a machine-readable test result.
5. Use synthetic test records clearly marked as synthetic. Do not import historical market datasets, mixed-year artifacts, or any 2025 OOS material.
6. Do not use real credentials, account identifiers, or secrets in the evidence package.
7. Stop immediately if the test path resolves outside the disposable directory, if another writer is detected, or if the baseline cannot be restored.

**Evidence bundle required for every test:**
- Test ID and exact acceptance-test number(s).
- Terminal/build/OS/filesystem/storage environment.
- Database path mode and exact API calls/results.
- Schema version and synthetic batch/bar identifiers.
- Operation sequence with ordered timestamps and clock source (no unsupported UTC relabeling).
- Injected fault point and observed return/error code.
- Database integrity result, row counts, batch state, cursor value/generation, and conflict/event rows before and after restart.
- Hashes for database, sidecars, logs, test inputs, and outputs.
- PASS / FAIL / INCONCLUSIVE / NOT RUN with a narrow assertion and limitations.

### 24.2 Transaction invariants — apply to tests 30–33 and 44–45

The test oracle must evaluate these invariants after reopening the database, not merely from in-memory return values:

1. **Atomic batch:** a capture batch and its bar rows are either committed together or absent together.
2. **Cursor never ahead:** the persistent stream cursor must never refer to a bar/batch that is not durably represented in the database.
3. **Replay safety:** if a batch may have been written but the cursor update did not commit, replay must not create silent duplicate/conflicting records.
4. **No false success:** failed begin, statement preparation, parameter binding, execution, or commit must not be reported as a successful capture.
5. **Conflict preservation:** a repeated logical key with different payload must be retained as a conflict/evidence condition, not silently overwritten.
6. **Restart reconciliation:** after any interruption, the reopened database must be checked for integrity and cursor/data agreement before capture resumes.
7. **Unknown commit outcome:** if the process terminates during commit and the outcome cannot be established, mark recovery state uncertain/blocked and reconcile; do not assume either success or failure.

These are required acceptance properties, not claims that the current V1.3 EA already satisfies them.

### 24.3 Test procedures and pass/fail criteria

| Test | Controlled action | Required evidence | PASS condition | FAIL condition |
|---|---|---|---|---|
| 29 — API/build capability | Inventory exact deployed MT5 build and verify documented database API availability in that build; record compile/runtime evidence only if an already-authorized disposable harness exists | Build number, API list, compile/run log, DATABASE_OPEN_COMMON result | Required API surface is available and exact build is recorded | Missing API or unverified build is treated as supported |
| 30 — Schema and rollback | In disposable DB, create schema, insert synthetic rows with prepared statements, exercise constraints, explicitly rollback a test transaction | Schema, statements, row counts before/after, rollback log | Constraints behave as specified and rollback leaves no partial transaction rows | Partial rows remain after confirmed rollback or constraints are bypassed |
| 31 — Failure after bar inserts | Within a test transaction, insert batch/bar rows, inject controlled failure before cursor update, rollback/reopen | Fault point, transaction result, DB integrity, batch/bar/cursor state | No partial batch/bar/cursor state is committed | Any bar/batch persists while cursor/batch atomicity contract says it must not |
| 32 — Failure after cursor update | Update cursor inside transaction, inject failure before commit, rollback/reopen | Old/new cursor generation and committed rows | Neither cursor advance nor batch rows are committed | Cursor advances without its corresponding committed data |
| 33 — Process termination stages | Terminate disposable EA/terminal at each documented transaction stage; reopen and reconcile after each run | Stage-by-stage crash matrix, integrity_check, cursor/data comparison | Every outcome is either consistent committed state or consistent rollback/blocked recovery | Corrupt/inconsistent state is accepted as complete or capture resumes without reconciliation |
| 34 — OS crash / power-loss | Controlled crash/power-loss simulation only on disposable test storage under an approved lab procedure | OS/storage details, fault method, DB and sidecar hashes, reopen/integrity results | Evidence supports only the exact durability claim demonstrated under that environment | Any broader power-loss guarantee is inferred from FileFlush/transaction API or one successful run |
| 35 — PRAGMA configuration | In disposable DB, attempt only documented/supported settings; read back effective values where possible | Exact commands, return codes, read-back values, journal/sidecar behavior | Accepted settings and limits are reported precisely | Command acceptance alone is described as proof of durable persistence |
| 36 — Storage fault matrix | Separately test disk full, DB lock/busy, timeout, corruption, backup/restore, and schema migration | One evidence bundle per fault, recovery result, integrity checks | Each fault fails closed; backup/restore and migration preserve validated data/cursor consistency | Silent data loss, cursor advance, unsafe auto-resume, or unverified restore |
| 37 — Writer/access policy | Attempt second writer and read-only Python inspection in isolated test; multi-terminal only if required | Lock behavior, writer identity, access mode, concurrent-operation log | Single-writer rule is enforced; readers cannot mutate active DB | Concurrent writer corrupts/changes stream or read-only observer writes |
| 38 — CSV export | Export committed DB rows repeatedly using same schema/version; compare output and prove export cannot advance cursor | Export parameters, DB snapshot, CSV hashes, cursor before/after | CSV is reproducible from committed rows and is downstream/read-only | CSV becomes independent cursor authority or export changes capture state |
| 39 — Partial CopyRates | Request N bars when only K<N are available; preserve exact result | N, K, return/error, history readiness, cursor before/after | Partial result is marked incomplete and cursor unchanged | Partial result advances cursor or is labelled complete |
| 40 — Retry after history download | Repeat identical bounded query after history progresses | Both raw responses, counts, matching/reconciliation report | Newly available bars reconcile without skip/duplicate; partial attempt retained | Retry overwrites evidence or silently skips newly available bars |
| 41 — Array order | Test both ArraySetAsSeries settings against a known synthetic/demo sequence | Full arrays, physical/logical order, chronological persistence | Stored order is proven and independent of mistaken logical-index assumptions | Incorrect order or current-bar ambiguity is accepted |
| 42 — Closed-bar selection | Query including shift 0 and identify current vs latest closed bar | Raw array, shift mapping, bar state | Shift 0 excluded; latest closed bar included | Forming bar admitted as closed or latest closed omitted |
| 43 — History boundary | Query beyond available history and TERMINAL_MAXBARS | Requested/returned counts, error, terminal setting, retry state | Stream is marked blocked/retryable/bootstrap-limited; no cursor jump | Cursor jumps to newest available bar despite unresolved earlier interval |
| 44 — Prepared insert/bind failure | Cause a prepared insert/bind failure midway through a disposable transaction | Statement status, rollback result, rows/cursor after reopen | Transaction rolls back and cursor remains unchanged | Partial rows or cursor advance survive |
| 45 — Begin/commit failures | Exercise transaction-begin failure and commit failure paths | Return codes, transaction state, reopen result | Neither failure path is treated as success; uncertain commit is reconciled | Failed/uncertain commit is reported as successful |
| 46 — Parameter binding | Bind synthetic symbols/metadata containing quotes, punctuation, Unicode, and suffixes | Bound inputs, stored values, statement logs | Values round-trip exactly; no SQL concatenation/injection | Values are altered, truncated, or interpreted as SQL |
| 47 — COMMON path / writer | Verify DATABASE_OPEN_COMMON path and one-writer behavior on exact target build | Resolved path, permissions, concurrent access tests | Actual path and locking policy are proven for target build | Assumed path/locking behavior differs from observed environment |
| 48 — PRAGMA behavior | Inspect PRAGMA support only in disposable DB; compare accepted commands with effective read-back | Command results, read-back, journal/sidecar observations | Supported behavior and unknowns are documented without overclaim | Acceptance of command is treated as durability guarantee |

**Note on test 29:** A source/API inventory is not equivalent to an EA compile. A compile is not equivalent to a runtime test. A runtime test is not equivalent to crash-durability proof. Record each evidence level separately.

### 24.4 Required fault-injection stage matrix for test 33

The disposable test harness, if later separately authorized, must define and record these interruption points independently:

| Stage | Interruption point | Reopen-time assertion |
|---|---|---|
| T0 | Before transaction begin | No batch/bar/cursor changes |
| T1 | After transaction begin, before inserts | No committed changes |
| T2 | After batch metadata insert | No partial committed batch |
| T3 | After one or more raw-bar inserts | No partial committed bar set |
| T4 | After conflict/event insert | No partial committed evidence set |
| T5 | After cursor update, before batch finalization | No cursor-only advance |
| T6 | After batch finalization, before commit | No uncommitted batch is visible as committed |
| T7 | During commit / commit outcome uncertain | Reconcile after reopen; never assume outcome |
| T8 | Immediately after successful commit return | Verify committed batch and cursor agree after process restart |
| T9 | After reopen/reconciliation but before next capture | Ensure resume starts only from validated committed state |

For every stage, record whether termination was a controlled process exit, terminal kill, OS crash, or power interruption. These are not interchangeable fault models.

### 24.5 Durability claim ladder

The final report must not collapse distinct evidence levels into a single word such as “safe” or “durable”:

- **L0 — API available:** exact build exposes the required database API.
- **L1 — Logical transaction behavior:** begin/insert/update/rollback/commit behavior passes controlled tests.
- **L2 — Process-restart consistency:** state remains consistent after EA/terminal termination and restart.
- **L3 — OS-crash evidence:** controlled OS crash testing on the specified environment supports a narrowly scoped claim.
- **L4 — Power-loss evidence:** controlled power-loss testing on the specified hardware/filesystem/storage configuration supports a narrowly scoped claim.
- **L5 — Operational recovery:** backup, restore, corruption handling, disk-full handling, migration, single-writer policy, and reconciliation are validated together.

Passing a lower level does not imply any higher level. Even L4 evidence is environment-specific and does not prove universal durability across brokers, terminals, operating systems, or storage devices.

### 24.6 Stop conditions and authorization boundary

- Do not execute destructive storage/fault tests against any non-disposable database.
- Do not create a SQLite PoC, fault-injection executable, EA modification, or source/runtime PR without separate user authorization.
- Do not infer atomicity between the existing CSV output and a separate SQLite cursor; they are different storage systems with no demonstrated shared transaction.
- Do not treat FileFlush, a successful DatabaseTransactionCommit return, or a PRAGMA command being accepted as independent proof of power-loss durability.
- If commit outcome is uncertain, if the database is corrupt, or if cursor/data agreement fails, the only acceptable state is blocked recovery pending reconciliation.
- Tests 29–48 have not been executed by this specification update. This section defines evidence requirements and operator review criteria only.
- The 2025 OOS dataset remains locked and untouched; no mixed-year historical payload is to be loaded for these tests.
- No source/runtime code, workflows, trading behavior, live orders, or production recovery status is changed by this documentation section.


## 25. Source Identity and Resume-Position Proof Matrix — Acceptance Tests 49–55

This section converts acceptance tests 49–55 into a proof matrix and makes explicit which conclusions each test can and cannot support. The matrix is documentation only. It does not approve an identity model, cursor, Demo harness, or implementation.

### 25.1 Required separation of concepts

The evidence review must keep these three concepts separate:

- **Source-bar identity:** answers which original source bar this observation represents, including source namespace and revision semantics.
- **Resume position:** answers where the capture process should continue reading after a validated committed batch. It is an operational checkpoint, not necessarily an immutable bar identity.
- **Ingest deduplication key:** prevents the same observation from being inserted twice during replay. It does not prove that two observations are the same original source bar.

A single field must not be promoted to serve all three roles without independent evidence and explicit approval.

### 25.2 Acceptance-test proof matrix

| Test | Procedure and evidence | PASS means only | FAIL / BLOCK consequence |
|---|---|---|---|
| 49 — Native identity inventory | Review exact deployed MQL5 structures and APIs; record fields and any broker/provider extension separately | No native immutable identifier was found in the reviewed API surface, or a specific candidate is documented for separate review | Do not invent an ID from row index, OHLC, or unverified timestamp; source identity remains unresolved |
| 50 — Restart and repeat range | Save a bounded closed-bar response, restart EA, request the exact same range, preserve both raw responses and deterministic comparison | Period-start observations are repeatable in this exact stream/build/test interval | Repeatability alone does not establish global uniqueness, immutable identity, UTC, or revision behavior |
| 51 — Relative index shift | Record a bar's CopyRates relative index, allow new bars to arrive, request again and locate the same observed period-start | Relative index moves as history advances; index-only persistent cursor is invalid | Any design persisting only relative index is rejected |
| 52 — Overlap across session/weekend | Re-request overlapping bounded ranges across a documented session boundary; compare every observation and attach independent calendar evidence | Overlap reconciliation is deterministic for tested range; gaps can be classified only where calendar evidence supports it | Any silent skip, fabricated candle, or unsupported session-gap classification blocks recovery approval |
| 53 — Historical revision | Preserve immutable response A, query same range later as B/C, compare fields, record conflict/revision evidence | If changed, revision was observed for the exact matched source/sample; if unchanged, no revision was observed in this window | Overwriting A, ambiguous matching, or treating no observed change as proof of immutability blocks approval |
| 54 — Symbol/provider namespace | Compare exact symbol strings, broker/provider namespaces, and independently evidenced alias mappings | Tested streams remain isolated; only an explicitly reviewed mapping may establish equivalence | Any collision or guessed alias merge blocks composite identity |
| 55 — Payload equality vs source identity | Compare identical payloads at distinct period starts and changed payloads at the same provisional period start | Payload hash can serve as integrity fingerprint and aid conflict detection, not as source identity | Any use of payload/OHLC hash as immutable source-bar ID is rejected |

### 25.3 Detailed operator procedure for tests 49–55

**T49 — Native identity inventory**
1. Record the exact MQL5 structure/API names and deployed terminal build being reviewed.
2. Enumerate documented fields exactly as exposed; distinguish documented fields from broker-specific metadata or assumptions.
3. Search for an immutable provider event ID, source sequence, revision ID, or equivalent only where the exact API actually exposes it.
4. If a candidate exists, preserve its source documentation, scope, uniqueness guarantee, stability across restart/replay, and revision behavior as a separate evidence item.
5. Result must say either NATIVE_ID_NOT_EXPOSED_IN_REVIEWED_API or CANDIDATE_REQUIRES_SEPARATE_CONTRACT_REVIEW. Do not infer a native ID from timestamp or array position.

**T50 — Restart and repeat range**
1. Select one symbol/timeframe and a bounded range containing fully closed bars.
2. Preserve response A, exact request parameters, returned count, raw physical order, and environment.
3. Restart the EA without changing the terminal profile or source history; request the exact same range as response B.
4. Repeat after a full terminal restart as response C if feasible.
5. Compare exact raw period-start representations and every bar field. Retain all observations and hashes.
6. PASS is limited to repeatability of the observed range. Any changed value, missing bar, ambiguous matching, or partial response is recorded as revision/missing/inconclusive as appropriate.

**T51 — Relative index shift**
1. Record a specific closed bar's current CopyRates relative index and its raw period-start representation.
2. Allow at least one new bar to close in the same stream.
3. Request the range again and locate the same bar by its observed period-start representation.
4. Record the new relative index and compare it with the old one.
5. If the index changes, mark index-only cursor REJECTED. If it does not change during the selected interval, the result is INCONCLUSIVE for demonstrating movement; index-only cursor remains rejected because the index is relative by API design and no durable identity contract follows from a single unchanged observation.

**T52 — Overlap and session boundary**
1. Select two bounded requests with a known overlap, one spanning a documented session/weekend boundary.
2. Preserve both responses and request metadata independently.
3. Compare the overlap without discarding duplicates or conflicting payloads.
4. Attach authoritative calendar evidence for any interval classified as expected closure.
5. Report all unmatched bars and partial queries. Never synthesize missing bars.
6. PASS is limited to tested overlap reconciliation; it does not establish a global resume cursor.

**T53 — Revision observation**
1. Preserve response A as immutable evidence.
2. Repeat the exact request at a later observation point as response B and, if possible, C.
3. Match bars only under an explicitly stated matching confidence. If timestamp uniqueness/stability is not yet proven, matching remains provisional.
4. Compare time, OHLC, tick volume, spread, and real volume separately.
5. If values change for a sufficiently matched period, preserve both versions and mark REVISION_OBSERVED. If no values change, report NOT_OBSERVED_WITHIN_TEST_WINDOW.
6. Never manufacture a correction or claim a broker's revision policy from a single changed observation without excluding query and synchronization differences.

**T54 — Namespace and aliases**
1. Preserve exact symbol spelling and exact broker/provider/server namespace for each source.
2. Compare aliases only with authoritative broker/provider instrument mapping evidence.
3. Keep two providers' identically named symbols separate unless a canonical-source contract explicitly states otherwise.
4. Verify no cross-stream collision occurs when timestamps and OHLC happen to match.
5. A proposed composite identity cannot be approved while namespace, canonical symbol, and provider scope remain unresolved.

**T55 — Payload/identity distinction**
1. Preserve two distinct period-start observations with intentionally or naturally identical OHLCV payloads in a synthetic test fixture clearly marked SYNTHETIC, or use observed data without altering it.
2. Preserve two observations for the same provisionally matched period start where one or more fields differ, if such a revision is naturally observed.
3. Demonstrate that equal payload fingerprints do not establish equal source-bar identity.
4. Demonstrate that a changed payload fingerprint signals changed content but does not alone establish whether the source revised a bar, the namespace changed, or the query was inconsistent.
5. Treat SHA-256 payload hash as integrity metadata only.

### 25.4 Decision rules for Model A / B / C

- **Model A — native immutable source ID:** remains preferred only if a genuine source-provided immutable ID is found and its namespace, uniqueness, replay stability, and revision semantics are documented and tested. The current reviewed MqlRates structure does not expose such an ID.
- **Model B — composite identity:** remains conditional. It cannot be approved until the exact source namespace, canonical symbol mapping, period-start semantics, uniqueness within stream, restart/replay stability, and historical revision behavior are evidenced. Raw period-start time is not UTC merely because it is represented as an epoch-like integer.
- **Model C — payload/OHLC-derived identity:** remains rejected as source identity. A payload hash may be retained as an integrity fingerprint and aid conflict detection, but identical payloads can occur at distinct periods and changed payloads can represent revisions.

### 25.5 Evidence review gates and current blockers

The following must all be closed before any source identity or persistent resume-position decision is proposed for approval:

1. Exact Demo broker/provider, terminal build, OS, and symbol namespace are recorded.
2. D0–D7 evidence packages are complete for the selected symbol/timeframe, with limitations explicit.
3. T49–T55 evidence packages are complete, with no ambiguous match presented as proof.
4. Same-stream period-start ordering, uniqueness, restart stability, and overlap behavior are demonstrated within a bounded scope.
5. Historical revision behavior is either observed and handled as versioned conflict evidence, or remains explicitly unknown with a conservative policy that cannot overwrite prior observations.
6. Session gaps are supported by independent calendar evidence; unknown intervals remain unknown.
7. The storage proof gates 29–48 are separately reviewed. Source identity proof does not prove atomic persistence; storage transaction proof does not prove source identity.
8. A separate written decision records the selected identity model, resume locator, dedup key, revision policy, namespace rules, and residual risks.

**Current status:**
- Native immutable MqlRates source ID: NOT EXPOSED BY THE REVIEWED DOCUMENTED STRUCTURE.
- Relative CopyRates index as durable cursor: REJECTED.
- Raw period-start as resume locator: CONDITIONAL / NOT PROVEN.
- Model B composite identity: BLOCKED.
- Payload-derived Model C identity: REJECTED.
- Persistent cursor implementation and SQLite PoC: NOT AUTHORIZED.
- Recovery production-complete claim: BLOCKED.

### 25.6 Safety and scope

- Tests 49–55 have not been executed by this documentation update; no Demo result is implied.
- No source/runtime code, EA, test harness, workflows, PR, or live trading behavior is changed or authorized.
- No MT5 history or mixed-year historical artifact is imported for these procedures.
- Development remains limited to 2016–2024. The 2025 OOS dataset remains locked and untouched.


## 26. Whole-Spec Compatibility Audit — 2026-11-26

**Audit scope:** internal consistency and traceability across Sections 1–25, including the V1.3 baseline, cursor contract, timestamp/gap policy, storage candidates, MQL5 API constraints, operator sheets D0–D7, and acceptance tests 1–55. This is a documentation compatibility audit only; it is not a source-code review rerun, Demo test result, or implementation approval.

### 26.1 Compatibility findings

| Area | Audit result | Required interpretation |
|---|---|---|
| V1.3 raw capture compatibility | PASS — no proposed change redefines existing raw timestamp fields | V1.3 remains raw input only; it is not a recovery-complete source |
| Three identity/state concepts | PASS — cursor, ingest deduplication, and source-bar identity are separately defined | Never reuse one as proof of another |
| Timestamp and UTC semantics | PASS — raw time remains UNVERIFIED; UTC is a separate proof obligation | Raw period-start may only be considered as a narrowly scoped same-stream resume locator after tests; no UTC join follows |
| CopyRates relative index | PASS — rejected as durable cursor | It may be used for bounded relative reads only |
| Partial history and physical ordering | PASS — tests 39–43 and D3/D7 cover partial results, retries, array order, current-bar exclusion, and history limits | No cursor advancement on partial/ambiguous reads |
| Session gaps and missing bars | PASS — GAP_UNKNOWN and MISSING_DATA_SUSPECTED fail closed | No fixed-interval assumption or synthetic candle |
| Revision/conflict handling | PASS — previous observations are preserved; payload hash is not identity | Revision matching remains provisional until position semantics are proven |
| Storage transaction design | PASS as a candidate design; NOT PROVEN operationally | MQL5 SQLite is a proof-of-concept candidate only; no implementation or durability claim |
| CSV and cursor separation | PASS — independent CSV plus cursor is not treated as atomic | Requires a proven journal/two-phase protocol or a different selected store |
| 2025 OOS governance | PASS — excluded throughout the test plan | No OOS import, read, filter, tuning, or evaluation |
| Authorization boundary | PASS — repeated throughout the document | No code, EA change, PoC, PR, workflow, merge, or live trading is authorized |

### 26.2 Acceptance-test traceability and intentional overlap

The detailed operator sheets and numbered acceptance tests overlap by design: the sheets describe what an operator observes, while the numbered tests define the system property and acceptance oracle. They are not separate evidence of a PASS.

| Operator sheet | Related numbered tests | Coverage boundary |
|---|---|---|
| D0 — baseline repeatability | 50 | Same bounded range repeatability only |
| D1 — new-bar index shift | 51 | Demonstrates relative index instability; does not approve raw time |
| D2 — EA/terminal restart | 1, 14, 50, 52 | Observed restart/reconciliation; not crash durability |
| D3 — disconnect/delayed history | 2–4, 26, 39–40, 43, 52 | Partial/retry behavior and bounded overlap; not proof that the existing EA backfills |
| D4 — session-gap classification | 11–12, 52 | Classification only with independent calendar evidence |
| D5 — historical revision | 17, 27, 53 | Preserve changed observations; no revision observed is not proof of immutability |
| D6 — symbol namespace isolation | 18, 25, 54 | Exact provider/symbol isolation; no guessed alias merging |
| D7 — closed-bar/array order | 10, 41–42 | Physical order and shift-0 exclusion |
| Storage proof plan | 5–6, 16, 19–24, 29–38, 44–48 | Logical atomicity and durability levels; requires separately authorized executable tests |
| Identity proof matrix | 49–55 | Source identity, resume position, namespace, revision, and payload distinction |

Test 49 is primarily a documentation/API inventory, not a Demo observation. Test 55 requires a clearly labelled synthetic fixture or naturally observed data; it must not alter broker history. The detailed operator sheets do not replace the machine-readable evidence bundles required by Sections 19 and 24.

### 26.3 Important distinctions confirmed by the audit

1. **Raw resume locator is not Model B identity.** A raw period-start value might eventually be accepted as a same-stream operational resume locator without being UTC. Model B composite identity remains blocked until its stronger namespace, canonical symbol, verified time, uniqueness, and revision requirements are met.
2. **Database atomicity is not source completeness.** A transaction can atomically store an incomplete or incorrectly ordered batch. Passing storage tests 29–48 cannot substitute for CopyRates/source-position tests.
3. **Source-position repeatability is not storage durability.** Passing tests 49–55 cannot prove that data and cursor survive a crash as one committed unit.
4. **A later historical query is not proof of original capture.** The existing EA's reconnect behavior and a later successful CopyRates query must be reported separately; historical availability does not prove the raw capture file contains the missing bars.
5. **PASS is scoped to its evidence envelope.** No result from one symbol, timeframe, provider, terminal build, OS, or storage medium generalizes automatically to another.

### 26.4 Remaining blockers — no technical approval implied

The audit found no basis to approve a production Recovery Architecture yet. The following evidence remains absent or unexecuted:

- no completed operator evidence bundle for D0–D7;
- no executed acceptance tests 29–55;
- no proven same-stream raw-time uniqueness/order/restart/replay contract for the exact provider/build;
- no approved canonical provider namespace and symbol-alias mapping;
- no demonstrated broker revision contract or fully approved conservative revision policy;
- no approved bootstrap boundary and historical completeness scope;
- no selected storage implementation with validated transaction, restart, OS-crash, power-loss, and operational recovery evidence;
- no end-to-end evidence proving capture, persistence, restart recovery, and gap reconciliation together.

The current document defines how to collect and judge that evidence; it does not contain the evidence itself.

### 26.5 Audit disposition and next permitted action

**Whole-spec internal compatibility:** PASS WITH OPEN EVIDENCE GATES.

**Recovery Architecture approval:** BLOCKED.

**Implementation / SQLite PoC / EA modification / PR:** NOT AUTHORIZED.

**Next permitted action:** prepare a read-only operator evidence checklist and collect the first D0 baseline package on one disposable MT5 Demo symbol/timeframe. Before any executable change or fault-injection harness, obtain separate explicit authorization. Record all outcomes as PASS, FAIL, INCONCLUSIVE, or NOT RUN; do not infer missing results.

No source/runtime code, EA, tests, workflows, trading behavior, or OOS data were changed or executed by this audit.


## 27. D0 Operator Preflight and Execution-Readiness Checklist

**Purpose:** make the first Demo observation operationally unambiguous while avoiding an unauthorized change to the existing EA. This section is a preflight/checklist only. It does not provide executable code or claim D0 has been run.

### 27.1 Critical execution constraint

The inspected V1.3 EA requests only one latest closed bar using `CopyRates(symbol, timeframe, 1, 1, rates)`. D0 requires two identical bounded multi-bar range requests and preservation of both returned arrays in physical order.

Therefore, **the existing V1.3 EA alone cannot produce the full D0 evidence package as specified**. Do not treat repeated latest-bar CSV rows as a substitute for the bounded-range D0 test.

D0 may be marked READY TO RUN only if an already-existing, separately authorized, read-only MT5 test mechanism can:
- issue the same bounded multi-bar CopyRates request twice;
- record requested and returned counts and API error/result information;
- preserve the complete returned MqlRates fields and physical array order for each call;
- record the ArraySetAsSeries setting and history readiness state;
- write evidence only to a disposable test location without modifying the production/common capture output.

If no such authorized mechanism is available, record **NOT RUN — READ-ONLY RANGE CAPTURE MECHANISM NOT AVAILABLE**. Do not create or modify an EA/script/harness under this specification authorization.

### 27.2 Preflight checklist

Before starting D0, the operator/reviewer must confirm every item:

- [ ] Terminal is connected to a broker/provider Demo server; account identifiers and credentials are not recorded.
- [ ] Test uses a disposable terminal profile or otherwise isolated test environment.
- [ ] Exact broker/provider/server label is recorded without account secrets.
- [ ] Exact Market Watch symbol string is recorded, including any suffix/prefix.
- [ ] One timeframe only is selected for this run.
- [ ] Terminal build, OS version, terminal data-path identity, and TERMINAL_MAXBARS are recorded.
- [ ] History for the chosen interval is fully available and synchronized.
- [ ] The chosen interval contains only closed bars; shift 0/current bar is excluded.
- [ ] The bounded request parameters and intended count N are written down before the first request.
- [ ] An authorized read-only range-capture mechanism is already available.
- [ ] Evidence output path is disposable and is not the existing V1.3 Common Files capture output.
- [ ] No second writer or concurrent test is using the same evidence store.
- [ ] Raw output, screenshots/logs, and comparison results can be retained without editing source observations.

If any required item is unchecked, do not start the test. Record NOT RUN or INCONCLUSIVE with the exact missing prerequisite.

### 27.3 D0 run record — duplicate this block for each run

| Field | Value |
|---|---|
| Test ID | D0 |
| Run ID | |
| Date/time observed (clock source named) | |
| Broker/provider + Demo server label | |
| Terminal build / OS | |
| Symbol exactly as shown in Market Watch | |
| Timeframe | |
| EA/read-only mechanism name and version | |
| Mechanism authorization/reference | |
| TERMINAL_MAXBARS | |
| Requested bounded interval (raw source representation) | |
| CopyRates start position / range parameters | |
| Requested count N | |
| Run A returned count / result / error | |
| Run A history ready? | |
| Run A ArraySetAsSeries | |
| Run B returned count / result / error | |
| Run B history ready? | |
| Run B ArraySetAsSeries | |
| Physical array order preserved? | |
| Exact field-by-field comparison completed? | |
| Duplicate / missing / out-of-order counts | |
| Current/forming bar excluded? | |
| Evidence filenames and SHA-256 | |
| Result: PASS / FAIL / INCONCLUSIVE / NOT RUN | |
| Reason and reviewer | |

### 27.4 D0 decision rules

- **PASS:** both requests return exactly N closed bars, history is ready, raw physical-order arrays match record-for-record across time, OHLC, tick volume, spread, and real volume, and no duplicate/missing/out-of-order record is observed.
- **FAIL:** complete successful requests for the same fixed interval produce conflicting values, counts, duplicates, missing records, inconsistent order, or include a forming bar.
- **INCONCLUSIVE:** partial response, history synchronization uncertainty, changed request parameters, missing raw array evidence, or any unexplained environmental change.
- **NOT RUN:** no authorized read-only bounded-range capture mechanism, no isolated Demo environment, or a required prerequisite is unavailable.

Do not rerun a failed/inconclusive request in a way that overwrites the first evidence. Preserve each attempt as a separate run. A later successful retry does not erase an earlier partial or conflicting observation.

### 27.5 What a D0 PASS does not approve

Even a valid D0 PASS is limited to repeatability of one bounded range for one exact provider/server, symbol, timeframe, terminal build, and observation window. It does not approve:
- raw period-start as a persistent resume cursor;
- Model A, Model B, or any canonical source-bar identity;
- UTC conversion or MTF joins;
- broker history immutability or revision semantics;
- SQLite, CSV journaling, atomic cursor commits, or crash/power-loss durability;
- multi-symbol or six-timeframe recovery;
- source/runtime changes, a test harness, a PR, or production recovery.

The next evidence step after D0 review is D1, then D2–D7 and the separately gated storage/identity tests. No result may be generalized beyond its tested scope.

### 27.6 Current execution status

D0: **NOT RUN by this specification work**.

D0 readiness: **BLOCKED until an already-authorized read-only bounded-range mechanism and isolated Demo environment are available**.

No source/runtime code, EA, test harness, workflows, PR, or OOS data were changed or executed by this checklist.
