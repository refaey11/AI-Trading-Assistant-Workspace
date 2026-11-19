# MTF V2 Source-Bar Identity Contract Proposal V1

**Status:** PROPOSAL ONLY — USER DECISION REQUIRED — NO SOURCE-ID IMPLEMENTATION  
**Parent:** PR #141  
**Date:** 2026-11-19

## 1. Decision to solve

Pivot identity V1 has an approved encoding method, but its `source_bar_id` input is not yet supplied by a verified upstream contract. This proposal separates the identity of an original source candle from:
- capture environment identity;
- raw/unverified clock values;
- row or file position;
- OHLC content and payload integrity hashes;
- a derived MTF feature identity.

No production pivot IDs may be generated until this source identity contract is approved and its evidence requirements pass.

## 2. Existing facts from repository review

1. MT5 Raw Capture V1.3 accepts `symbol`, `timeframe`, and `bar_time_epoch_seconds_raw`, with `bar_time_utc_status=UNVERIFIED`.
2. Its `source_id` identifies the terminal/capture environment, not an individual candle.
3. Its CSV ingest duplicate key is currently `(symbol, timeframe, bar_time_epoch_seconds_raw)`; conflicting payload hashes for the same key are rejected. This is a current ingest deduplication rule, not a formally approved immutable source identity.
4. Its `payload_hash` is an integrity digest over the row payload and may include capture observations; it is not an immutable candle identifier.
5. The six-timeframe source adapter requires explicitly offset timestamps and normalizes them to UTC, but does not issue per-bar IDs.
6. Producer-to-feature lineage V1 binds `symbol`, `timeframe`, `bar_time_utc`, `source`, and `producer`, and verifies payload hashes/input references. It does not define `source_bar_id`.
7. The V2 evidence-envelope gate validates structure and causality, not per-row source identity or the truth of clock evidence.

## 3. Candidate source identity models

### Model A — upstream-native immutable bar identifier

The upstream data provider or capture source supplies a stable per-candle identifier, with documented uniqueness scope and revision semantics.

Required evidence:
- authoritative source documentation or implementation;
- identifier stability across repeated downloads/replay and file reordering;
- uniqueness across symbol, native timeframe, source namespace, and history;
- explicit behavior for corrected/revised candles;
- conformance fixtures across all six timeframes.

Advantages:
- avoids constructing identity from timestamp assumptions;
- source owns the identity semantics.

Limitations:
- no such field has been recovered in the currently inspected repository contracts;
- MT5 `MqlRates` raw capture as currently implemented does not emit a documented native unique bar ID.

### Model B — deterministic composite identity from verified source coordinates

If and only if the upstream source has no native identifier, a separate reviewed contract could define a canonical source-bar key from:
- immutable source namespace and source contract version;
- canonical symbol;
- canonical native timeframe;
- verified UTC bar-open timestamp with explicit clock-policy evidence.

The canonical tuple would be serialized and hashed under a dedicated source-bar identity version. This is only a candidate design, not an approved rule.

Hard prerequisites:
- verified UTC mapping for the bar-open timestamp, not merely an explicit offset supplied by an untrusted caller;
- approved source namespace semantics;
- canonical symbol/timeframe contracts;
- documented uniqueness and duplicate handling;
- correction/revision policy;
- exact canonical serialization and hash test vectors.

Advantages:
- can be stable across file reordering and replay when source coordinates are stable;
- can be independently reproduced.

Limitations:
- identity depends on trustworthy clock mapping;
- if the source can revise a candle at the same coordinates, a separate immutable revision policy is required;
- no composite key may be built from the current V1.3 UNVERIFIED raw epoch.

### Model C — payload-derived identity

A digest over OHLC or the complete capture row is not proposed as the source-bar identity.

Reasons:
- changing OHLC due to a correction changes the ID and obscures whether it is the same source bar or a new revision;
- including capture-time observations makes identity vary across repeated captures;
- omitting those observations creates an incomplete content key that may collide for distinct bars;
- content integrity and source identity are different concepts.

**Decision:** Model C is rejected as a source identity model. Its hashes may remain integrity evidence only.

## 4. Proposed contract requirements common to Model A and Model B

Regardless of selected model, the source identity contract must define:

1. **Namespace:** authoritative source/provider/capture producer and contract version.
2. **Symbol:** canonical symbol value and alias policy; no silent case folding or guessed mapping.
3. **Timeframe:** canonical native timeframe; no inference from filename alone in a production path.
4. **Identity stability:** same source candle retains the same identity across deterministic replay, file reorder, and repeated capture.
5. **Uniqueness:** no two distinct bars in the defined namespace/symbol/timeframe scope share one identity.
6. **Revision semantics:** explicitly distinguish an unchanged bar, a corrected bar, and a conflicting duplicate. Never silently overwrite.
7. **Clock lineage:** where time participates in identity, include verified clock-policy ID and evidence digest; an unverified timestamp blocks identity generation.
8. **Payload integrity:** keep raw payload hashes separate from source-bar identity.
9. **Availability:** identity creation cannot make a bar available before its verified source availability/close.
10. **Six-timeframe coverage:** independent conformance for M5, M15, M30, H1, H4, D1; no extrapolation from one timeframe.

## 5. Required conformance test matrix

Before implementation, the selected model must pass synthetic and source-backed tests for:
- same bar recaptured/replayed => same ID;
- row reorder/file reorder => same ID;
- distinct adjacent bars => distinct IDs;
- same timestamp across different symbols/timeframes/source namespaces => distinct IDs;
- conflicting payload at same identity => explicit conflict/revision outcome, never silent dedup;
- revised candle => documented stable identity plus revision, or documented new identity;
- missing/naive/unverified clock => reject if timestamp is an identity ingredient;
- caller-forged VERIFIED flag without trusted evidence => reject;
- all six timeframes independently;
- deterministic serialization/hash across implementations.

Synthetic tests prove only implementation behavior; they do not authenticate provider or broker clock facts.

## 6. Relationship to approved Pivot Identity V1

Once source identity is approved and verified, its canonical value may be passed as `source_bar_id` to the approved Pivot V1 identity encoder.

The pivot ID continues to include:
- configuration fingerprint;
- detector version;
- pivot kind;
- source-bar identity;
- canonical symbol;
- canonical timeframe.

The source-bar ID must not be replaced with the MT5 terminal `source_id`, raw UNVERIFIED epoch, row number, dataframe index, file position, OHLC, or payload hash.

## 7. User decision required

Please choose the intended source identity basis:

- **A — upstream-native ID only:** block until an authoritative source-native per-bar identifier is available.
- **B — conditional composite ID:** allow a separately versioned composite based on source namespace + canonical symbol + native timeframe + verified UTC bar-open time, but only after the clock/source/revision contracts are approved and tested.

Recommendation for safety: prefer A whenever an authoritative native ID exists; consider B only if source evidence proves no native ID exists and all prerequisites are met.

This proposal does not select L/R values and does not implement either model. No choice is inferred from the current MT5 dedup key.

## 8. Safety and scope

- No changes to legacy PIVOT_SEQUENCE_V2.
- No detector implementation or L/R selection.
- No 2025 data/tuning.
- No Decision Brain integration, signal generation, or order execution.
- No PR merge and no main-branch change.
