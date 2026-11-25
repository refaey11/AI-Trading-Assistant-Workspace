# Decision Brain V1 — Market Data Vertical Slice Audit
Date: 2026-11-25
Branch: `audit/v1-market-data-vertical-slice-2026-11-25`
Base: `3338ff907cd636cef6f9b51bcee3e784ac0988b2`
Scope: GitHub-only inspection of existing MT5 capture, clock admission, and MTF V2 artifacts. Report-only. No runtime, capture, MTF, tests, workflows, or `main` changes. No market-data payloads or 2025/2026 payloads accessed.

## Objective

Select the shortest safe existing path for the first Decision Brain V1 vertical slice, without rebuilding capture/aggregation and without allowing unverified market data into the Brain.

## Findings

### 1. MT5 Raw Capture V1.3 exists and is reusable — capture only

PR #131, branch `feature/mt5-raw-capture-v1-3-clock-safe`:
- Existing EA: `RUNTIME/MT5_RAW_CAPTURE_V1_3/MT5_Raw_Capture_Only_V1_3.mq5`.
- Captures closed bars from Market Watch for six native timeframes: M5/M15/M30/H1/H4/D1.
- Preserves `MqlRates.time` as `bar_time_epoch_seconds_raw`; marks clock as `MT5_MQLRATES_DATETIME_RAW` and UTC status `UNVERIFIED`.
- Python contract explicitly rejects UTC fields and any status other than `UNVERIFIED`; CSV adapter preserves the raw epoch without conversion.
- Capture dedupe key is symbol + timeframe + raw bar time. The producer does not expose an upstream-native immutable per-bar ID.
- `source_id` is terminal name/path metadata, not a per-bar identity or authenticated producer attestation.
- Documentation requires MetaEditor compilation and MT5 Demo-terminal capture; GitHub CI cannot prove those.

**Disposition:** Reuse V1.3 as the raw capture/diagnostic source. It is not eligible for UTC MTF joins or Decision Brain input while its clock status is UNVERIFIED. Do not modify V1/V1.1/V1.2 or fabricate UTC.

### 2. Clock Provenance Gate V1 is a structural consistency check, not clock authentication

PR #130, branch `fix/mt5-clock-provenance-gate-v1`:
- Requires broker-server wall time, explicit per-bar offset, timezone policy ID, evidence reference, UTC timestamp, and observation timestamp.
- Checks timestamp awareness and arithmetic consistency.
- Does not independently authenticate the broker's timezone/DST policy or prove the evidence reference is authoritative.
- Current runtime's source envelope still trusts caller-supplied `authoritative=true`, source and producer strings; those are not bound to a registry/signature/digest or trusted clock.
- Gate tests cannot turn a caller assertion into source truth.

**Disposition:** Reuse as one validation layer only. A separate approved, authoritative broker timezone/clock evidence source and producer attestation are still required before the result can be called verified.

### 3. MTF V2 structure consumer exists, but pivot producer does not

PR #139, branch `design/mtf-producer-v2-alternative-contract-v1`:
- `mtf_structure_producer_v2.py` consumes completed bars and already-confirmed pivots.
- It emits descriptive structure states and BOS/CHOCH events only; no trading direction, score, or legacy-field mapping.
- README explicitly says the pivot detector is external/not implemented, event gap/dedup/expiry policy is open, and every row has `availability_status=PROVENANCE_UNVALIDATED`.
- The current code hardcodes a minimum two-bar confirmation delay. That is a prototype assumption, not a universal approved detector configuration for all six timeframes.
- The alternative design requires a separate versioned evidence contract and forbids silently mapping V2 output into legacy MTF fields.

**Disposition:** Keep as an isolated prototype. Do not connect it to Brain or present its output as production MTF.

### 4. Pivot Detector V2 is still a behavior contract, not an implementation

PR #141, branch `spec/mtf-v2-pivot-detector-proposal-v1`:
- The 288 fixtures validate structure/coverage only; they do not execute a detector.
- Numeric L/R per timeframe, exact identity serialization/fingerprint, gap/session authority, and lifecycle status remain unapproved/open.
- Approved behavioral baseline requires strict highs/lows, no plateau tie-break, completed right-side bars, availability at final confirming bar, unresolved same-bar dual candidates, and provenance-backed warm-up.
- W2/W3/W5 fixture labels are not production parameter choices.

**Disposition:** No production pivot detector can be responsibly implemented until the remaining contract values are explicitly approved. Do not choose L/R by backtest performance or tune on 2025.

### 5. MTF V2 envelope gate remains non-authenticating

PR #140, branch `feature/mtf-v2-evidence-envelope-gate-v1`:
- Validates explicit-offset timestamps, bar-close/availability/decision ordering, contiguous indices, SHA-256 formatting, exact six-timeframe coverage and same-symbol consistency.
- It explicitly returns `STRUCTURALLY_VALID_NOT_AUTHENTICATED`, `production_eligible=false`, and `authentication_required=true`.
- Hash format/consistency does not authenticate the underlying source or clock.

**Disposition:** Reuse for structural checks only. Do not treat it as production admission.

## First vertical slice — selected architecture

Use the existing components in this order, without rebuilding them:

1. MT5 Raw Capture V1.3 emits raw closed bars for one FX symbol and the six native timeframes.
2. CSV ingest validates row structure, OHLC geometry, payload hash, duplicate conflicts, and preserves raw time.
3. A separate source-attestation/clock adapter must bind each bar to an approved source identity, immutable bar identity, authoritative per-bar timezone evidence, and verified availability. Until this exists, rows remain capture-only and fail closed.
4. Only after admission is verified may the existing MTF join/producer path build point-in-time context.
5. The existing Murphy source provider must independently pass WP3 source authority/eligibility checks.
6. Only then may the existing Decision Runtime / Three-Book / Risk path evaluate the event.

This is a staged vertical slice. It deliberately does not force MTF V2 into the current Brain's legacy fields or change any frozen knowledge semantics.

## Exact blockers to close next

P0:
- **Authoritative clock evidence:** identify a broker/server timezone + DST policy source that can justify the per-bar offset, with traceable evidence. Current capture diagnostics are insufficient.
- **Native source-bar identity:** recover an authoritative immutable per-bar identifier upstream, or submit a separately governed fallback proposal. Do not promote raw epoch to an authenticated bar ID.
- **Producer trust:** define how source, producer version, config/code digest, and clock attestation are bound to the captured event and verified at runtime.
- **MTF admission contract:** reconcile source bar identity, bar-open/bar-close/available-at semantics, session gaps, and freshness without inventing a maximum-age threshold.
- **Pivot detector contract:** close per-timeframe L/R choices, identity encoding/fingerprint, session/gap authority, and lifecycle policy before implementation.
- **Murphy provider:** independently close WP3's canonical provider/row-level authority gap; market data alone cannot authorize a direction.

P1:
- Confirm MetaEditor compilation and MT5 Demo capture for V1.3. No such terminal validation is claimed here.
- Establish one-symbol replay/shadow evidence with duplicate, outage, restart, stale-event and audit-trace tests.
- Expand to the full approved FX symbol universe only after the first symbol's complete vertical slice passes.

## Explicit non-actions

- No source or test code changes.
- No new workflow runs or claims of test success.
- No changes to PR #130/#131/#139/#140/#141; all remain separate review tracks.
- No PR merge, no `main` changes, no live orders.
- No Dropbox/CircleCI.
- No 2025/2026 market-data payload access, tuning, calibration, or threshold selection.

## Decision

**The first data-capture component is already present. The missing piece is not another capture EA: it is authoritative source/clock/bar-identity admission.** The safest next implementation is a narrowly scoped adapter only after the authoritative evidence source and identity contract are recovered/approved. Until then, the product must not generate a supposedly trusted live signal from these raw bars.
