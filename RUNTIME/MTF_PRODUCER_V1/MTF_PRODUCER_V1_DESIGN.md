# MTF Producer V1 — Design and Compatibility Gate

**Status:** DESIGN ONLY — no producer formula or live signal generation is authorized by this document.

**Parent runtime:** `feature/live-decision-runtime-v1` (PR #120 head `d1df29b0d3526378402e47959a55a73b13bd1889`)

## 1. Purpose

Build an independently versioned, source-backed MTF data producer for the Decision Brain's existing six-timeframe contract:

- M5
- M15
- M30
- H1
- H4
- D1

The producer supplies evidence and provenance. It does not create a trade direction, override Murphy, replace Nison confirmation, alter TIZ, calculate broker lots, or execute orders.

## 2. Non-negotiable compatibility rules

1. Do not modify the frozen Decision Brain, Murphy, Nison, TIZ, Similarity Engine, or canonical Risk Engine semantics.
2. Reuse and validate the existing strict `RUNTIME/DECISION_RUNTIME_V1/mtf_brain_input_join_v1.py` adapter. Do not create a parallel join or scoring layer.
3. Do not substitute the Similarity Engine's standardized 57D matrix for the Brain's semantic MTF inputs.
4. Do not infer a timezone for historical naive timestamps. A timezone/DST/broker-server-clock contract must be evidenced before timestamp normalization.
5. Preserve missing values as unavailable evidence. Never impute missing MTF inputs to zero or another neutral-looking value.
6. Enforce closed-candle availability and backward as-of joins only. No current unfinished higher-timeframe candle and no future evidence.
7. 2025 remains locked OOS: do not read, train, tune, calibrate, select features, or validate against 2025.
8. No live orders; no merge to main without explicit approval.

## 3. Evidence currently established

The read-only audit `AUDITS/MTF_SOURCE_COMPATIBILITY_AUDIT_2026-11-16.md` establishes:

- Canonical archive: `MTF_ALIGNMENT_GBPUSD_V1.zip`, pinned revision `01659665ff5a6d300000003796dcfe3`.
- 671,601 rows across 2016–2024; six declared timeframes; 106 columns.
- Serialized `trend_regime` values observed as -1/0/1 and `mtf_trend_score` observed in -6..+6. These are observations, not recovered formula semantics.
- All archive timestamps are naive; timezone, broker clock, DST, and epoch interpretation are unresolved.
- 2,512 missing cells occur across the seven Brain MTF input fields. Their warm-up interpretation is plausible but not proven.
- No six-timeframe producer source code was found in the inspected archive or top-level full-project source/documentation search.
- Existing H1/H4 reader is research-only and is not a replacement for the six-timeframe producer.

## 4. Required source contract before implementation

The following must be recovered from authoritative source documentation/code or explicitly defined and approved as a new versioned contract. No formula may be guessed.

### 4.1 Historical source lineage

- Exact source artifact and immutable revision/hash.
- Timestamp meaning and timezone, including broker/server clock and DST policy.
- Bar-open versus bar-close timestamp convention.
- Missing-bar and warm-up behavior.
- Symbol/instrument mapping and price precision.

If historical timezone provenance cannot be recovered, the historical MTF archive remains non-evaluable for time-sensitive joins. Do not silently relabel naive timestamps as UTC.

### 4.2 Feature semantics

For each of the seven existing Brain inputs, document:

- exact formula or authoritative producer mapping;
- input columns and lookback/warm-up requirements;
- allowed output domain and meaning;
- missing-value behavior;
- version and deterministic test vectors.

The existing observed ranges (-1/0/1 and -6..+6) are not sufficient to reconstruct the formulas. Murphy material may be used to identify governed market-structure concepts, but no new formula is attributed to Murphy without explicit source support and compatibility review.

### 4.3 Live MT5 source

The live capture interface must record:

- broker/server identity and configured timezone policy;
- symbol, timeframe, OHLCV, spread where available, bar timestamp, and bar-close/availability timestamp;
- retrieval time, producer version, source identifier, and raw payload hash;
- explicit volume availability and volume type (tick/real) without silently mixing them;
- closed-bar status and duplicate/gap diagnostics.

All six timeframes must be sourced from the same declared broker feed and joined by closed-bar availability. A missing or stale timeframe must cause abstention/NOT_EVALUABLE, not a fabricated neutral value.

## 5. Proposed implementation stages

### Stage A — Contract recovery (current)

- Inventory existing MTF architecture documents, the strict join adapter, and relevant Murphy source mappings.
- Recover or formally declare timestamp, feature, and missing-value semantics.
- Produce a field-level compatibility matrix and unresolved-items report.
- No production feature values are emitted in this stage.

### Stage B — Raw MT5 capture

- Implement a standalone, versioned OHLCV capture component for M5/M15/M30/H1/H4/D1.
- Capture raw bars and provenance only; do not infer directional features.
- Add deterministic tests for closed-bar boundaries, timezone conversion, DST transitions, duplicates, gaps, stale feeds, and restart/replay idempotency.

### Stage C — Feature producer

- Implement only feature definitions whose semantics have passed Stage A.
- Keep the producer separate from Decision Brain and from the strict join adapter.
- Preserve unavailable fields as null/explicit unavailable states; never fill with zero.
- Attach field-level lineage and `available_at` to every produced value.

### Stage D — Historical compatibility validation

- Use only 2016–2024 development data, and only after timestamp provenance is established.
- Compare produced values against the pinned canonical archive using exact row/time alignment.
- Report per-field agreement, missingness, warm-up behavior, and discrepancies.
- No 2025 access and no parameter tuning against the locked OOS year.

### Stage E — Runtime integration

- Integrate through the existing strict MTF join adapter and PR #120 runtime boundary.
- Require source/producer/version/availability envelopes.
- Preserve fail-closed behavior and signal-only execution.
- MT5 Demo execution is a later, separately gated phase and is not part of this design approval.

## 6. Acceptance gates

A stage cannot be marked PASS without evidence:

- **G1 Source lineage:** pinned raw data and authoritative timestamp contract.
- **G2 Feature semantics:** all seven field definitions, domains, warm-up and missing-value policy.
- **G3 Live capture:** six timeframe capture with provenance and closed-bar guarantees.
- **G4 Historical parity:** deterministic 2016–2024 comparison with documented tolerances and no 2025 access.
- **G5 Runtime compatibility:** strict adapter tests, no lookahead, fail-closed missing/stale behavior.
- **G6 Governance:** no frozen component changes, no live orders, no merge to main absent explicit approval.

## 7. Immediate next engineering action

Complete Stage A as a read-only compatibility matrix by inspecting the existing MTF architecture specifications, Murphy source mappings, and strict join adapter. Do not begin feature formula implementation until every required field has an authoritative definition or a separately approved new contract.

## 8. Explicit non-goals

- No EMA/RSI/MACD or other guessed replacement formula.
- No use of the old research-only H1/H4 reader as a six-timeframe source.
- No Similarity 57D substitution.
- No generated BUY/SELL direction from this producer.
- No 2025 data access.
- No MT5 order submission.
