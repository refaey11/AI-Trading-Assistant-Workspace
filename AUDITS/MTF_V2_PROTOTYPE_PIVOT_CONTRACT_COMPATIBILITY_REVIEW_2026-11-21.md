# MTF Producer V2 — Prototype / Pivot Contract Compatibility Review

Date: 2026-11-21

Status: DOCUMENTATION-ONLY REVIEW / NO DETECTOR IMPLEMENTATION / NO PRODUCTION AUTHORIZATION

Scope:
- PR #139 prototype at commit `ac1168918cbf955ae5b9cfedba60d4c54187e685`
- `RUNTIME/MTF_PRODUCER_V2/mtf_structure_producer_v2.py`
- `RUNTIME/MTF_PRODUCER_V2/test_mtf_structure_producer_v2.py`
- PR #141 reference contract at commit `1e7aa167879e7fa4d44468057b7ed60d7118f259`
- `PROJECT_GOVERNANCE/MTF_V2_PIVOT_DETECTOR_REFERENCE_BEHAVIOR_CONTRACT_V1.md`

No market data was opened. No 2025/2026 market data was used. No runtime file was modified.

## 1. Executive result

The PR #139 structure prototype is a useful isolated downstream consumer of already-confirmed pivots. It is not a pivot detector and is not yet a general streaming/production contract.

The PR #141 document is a semantic specification, not executable detector code. The 288-fixture workflow validates fixture-corpus structure and reference identity vectors; it does not execute a pivot detector or prove detector semantics.

The two PRs are complementary but are not yet end-to-end compatible. The key boundary is the confirmed-pivot event schema and its source identity, availability, timeframe, and provenance.

## 2. Confirmed compatibility findings

### 2.1 Downstream prototype boundary

The PR #139 producer accepts completed OHLC bars and caller-supplied confirmed pivots. It deliberately does not detect pivots, authenticate clocks, or generate trade direction. This separation is appropriate and must be preserved.

### 2.2 Hard-coded two-bar availability assumption

The prototype validator rejects a pivot when:
`available_bar_index < source_bar_index + 2`.

This is consistent with the limited historical H1 audit observation but is not established as a universal six-timeframe detector rule. PR #141 explicitly leaves per-timeframe L/R values unresolved. The prototype must not be treated as a generic adapter for arbitrary approved R values until this assumption is made configurable or the upstream event contract explicitly guarantees the two-bar minimum for every input.

### 2.3 Warm-start incompatibility

The prototype requires every pivot's `available_bar_index` to lie inside the supplied bar window. Therefore, it rejects a causally valid pivot confirmed before the first bar in a replay window. PR #141 allows pre-window context only with original source identity and verified availability/provenance. A separate warm-start acceptance contract and tests are required; do not relax the validator without that contract.

### 2.4 Gap semantics are weaker than market-time continuity

The prototype checks consecutive integer bar indices. It has no bar timestamps, session calendar, or upstream continuity evidence. Contiguous indices do not prove contiguous market time and cannot distinguish an expected session closure from a missing in-session candle. PR #141 correctly leaves continuity authority upstream. Production eligibility remains blocked.

### 2.5 Event lifecycle remains unresolved

The prototype prevents repeated events while closes remain beyond a boundary, but it does not define a governed policy for a later recross and recross-again sequence, boundary expiry, invalidation, or supersession. Its event ID includes the break bar index, so separate crossings produce distinct IDs; that is an implementation behavior, not an approved deduplication policy.

### 2.6 Availability is index-only and unauthenticated

The prototype emits `available_bar_index` and marks rows `PROVENANCE_UNVALIDATED`. It has no verified `available_at` timestamp or authenticated source-clock link. The evidence-envelope gate does not automatically authenticate these event objects. Do not interpret index availability as wall-clock or production availability.

## 3. Additional input-validation gaps observed in static review

The current prototype validates OHLC ordering and completion, but does not explicitly reject non-finite numeric values (NaN or infinity) for bar OHLC or pivot prices. It also does not validate that pivot prices are consistent with their referenced source bar's high/low, nor does it validate canonical symbol/timeframe identifiers or a governed pivot identity schema.

These are review findings for future tests and a separately reviewed patch. No behavior is changed in this document.

## 4. Existing tests versus missing semantic tests

The existing PR #139 unit tests cover basic state classification, availability visibility, close-crossing BOS/CHOCH examples, wick-only rejection, one no-repeat-while-beyond case, future-bar perturbation, and MTF conflict.

The following tests remain necessary before the prototype can be considered semantically reviewable beyond its current synthetic examples:

1. **Pivot event contract:** reject empty IDs, malformed kinds/status, non-finite prices, duplicate IDs, and inconsistent source-bar references.
2. **R configurability:** prove the downstream consumer does not silently impose a universal two-bar delay when an approved upstream detector configuration uses another R.
3. **Warm start:** accept only pre-window pivots whose original identity and verified availability precede the first replay decision; reject missing/forged provenance.
4. **Market-time gaps:** prove index continuity alone cannot mark source continuity as verified; test upstream-proven session continuity versus unproven gaps.
5. **Event lifecycle:** same-boundary recross, recross-again, event identity, expiry, invalidation, and supersession after a new pivot. Expected outputs remain blocked until policy is approved.
6. **Causality:** boundary pivot available on the break bar must not be used for that same bar; future perturbations must not revise prior event output.
7. **Numerical validity:** NaN/infinity, invalid pivot prices, extreme but finite values, and trusted precision/equality behavior.
8. **Timeframe isolation:** run independent fixtures for M5/M15/M30/H1/H4/D1 and prove no cross-timeframe state or missingness leakage.
9. **Deterministic replay:** identical inputs and configuration produce stable ordered outputs; byte identity only after all serialization contracts are frozen.

## 5. Required next implementation sequence

1. Freeze the upstream confirmed-pivot event schema, including source-bar ID, native timeframe, source index, availability index/time, confirmation status, and provenance references.
2. Keep L/R explicitly configured per timeframe; do not select numeric values from W2/W3/W5 synthetic labels or infer them from historical H1 availability.
3. Approve gap/session continuity, warm-start, and event lifecycle policies with positive and negative fixtures.
4. Implement a separate test-only semantic oracle for the pivot detector before any production detector code. The oracle must accept explicit L/R inputs and synthetic source identities; it must not claim market-data or source-clock authentication.
5. Add the detector only after the oracle and source/clock contracts are reviewed. Keep it isolated from the Decision Brain until six-timeframe conformance and production provenance gates pass.

## 6. Governance

- Documentation-only change.
- No production detector code or PR #139 runtime code changed.
- No source-bar IDs generated.
- No L/R values selected.
- No formulas inferred from serialized MTF outputs.
- No Decision Brain, Murphy, Nison, Trading in the Zone, Similarity, Risk, or execution behavior changed.
- No 2025 OOS access, tuning, or evaluation.
- No main-branch changes and no merge.
