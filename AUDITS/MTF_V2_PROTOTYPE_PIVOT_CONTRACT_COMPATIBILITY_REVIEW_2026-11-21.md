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


## 7. Deeper consumer-contract audit (2026-11-21 continuation)

The exact PR #139 consumer implementation was re-read against the current PR #141 reference contract. The following are additional static findings; they do not change the approved detector policy.

### 7.1 Pivot payload is not yet a governed cross-PR contract

The PR #139 `ConfirmedPivot` object contains only:
- caller-supplied `pivot_id`;
- HIGH/LOW kind and numeric price;
- integer source and availability bar indices;
- a confirmation-status string.

It does not carry a canonical symbol, native timeframe, original source-bar identity, verified `available_at`, producer/schema identity, or provenance references. The surrounding producer call supplies symbol/timeframe at batch level, while each pivot is not independently bound to those values. This is insufficient to demonstrate that a pivot belongs to the exact source stream being consumed.

The prototype's `pivot_id` is only checked for uniqueness within the supplied list. It is not validated against the PR #141 approved conceptual identity ingredients or the still-blocked production source-bar identity contract. Do not treat the current field as an authenticated pivot identity.

### 7.2 Source-bar consistency and runtime type validation are incomplete

Static inspection confirms that the consumer does not establish:
- that `source_bar_index` identifies a bar in the supplied stream or an approved pre-window context;
- that a HIGH pivot price equals the referenced source bar's high, or a LOW pivot price equals its low;
- that pivot source and availability indices are actual non-boolean integers;
- that pivot prices and bar OHLC values are finite numeric values;
- that a pivot source index is unique for a given kind under the approved detector output contract.

The current OHLC envelope comparison is not a sufficient non-finite-value guard: NaN can evade ordinary ordering comparisons. A separate strict input-validation patch and negative tests are required before consuming untrusted producer payloads. No validation behavior is inferred or changed here.

### 7.3 The two-bar check is both hard-coded and not equivalent to the V2 confirmation contract

The validator's `source_bar_index + 2` condition is a fixed minimum delay, while PR #141 defines confirmation from the configured right window R and the verified availability of the final required right-side bar. The historical H1 observation does not authorize this rule for every timeframe. The consumer must eventually validate the upstream event's actual confirmation/availability relationship against an approved per-timeframe configuration, not assume a universal two-bar delay.

### 7.4 Consumer event identity is not source-authenticated

The current event ID is assembled from symbol, timeframe, event type, break-bar integer index, and boundary pivot ID. The `Bar` object has no immutable source-bar ID, and the event has no verified wall-clock `available_at`. Therefore the ID is deterministic within the current synthetic index stream but cannot serve as a governed cross-replay/source event identity. Re-indexing an otherwise identical source stream can change the ID; replays with reused indices can collide across distinct source streams if external namespace is not bound.

The `source_payload_hash` and `clock_policy_id` arguments are copied into output metadata but are not authenticated or bound to individual bars/pivots. The output correctly remains `PROVENANCE_UNVALIDATED`; these strings must not be interpreted as provenance proof.

### 7.5 Event transition and boundary selection need policy-level acceptance tests

The implementation uses the previous row's recomputed pivot structure state to classify a close crossing and selects the latest available pivot of the relevant kind as its boundary. The state itself is not transitioned by the emitted BOS/CHOCH event. Consequently:
- a later cross back through the same boundary and another qualifying cross can emit another event;
- the same pivot boundary can remain eligible indefinitely;
- a newly confirmed pivot can become the selected boundary without any separately specified invalidation/supersession lifecycle;
- no expiry or reset policy exists.

These are not necessarily defects relative to the current prototype's narrow semantics. They are unresolved lifecycle behavior and must remain blocked from production until explicitly specified and tested. Do not silently add deduplication, expiry, or supersession.

### 7.6 Required consumer acceptance matrix before any integration

| Area | Required positive case | Required negative case | Current status |
| --- | --- | --- | --- |
| Pivot stream binding | Pivot matches symbol/native timeframe/source stream | Cross-symbol or cross-timeframe pivot rejected | BLOCKED: fields/provenance absent |
| Source-bar reference | HIGH/LOW price matches original source bar and identity | Missing, mismatched, or forged source reference rejected | NOT TESTED |
| Confirmation timing | Configured R and verified final-bar availability accepted | Early or universal hard-coded delay rejected | BLOCKED: R contract not wired |
| Warm start | Provenanced pre-window pivot available before first decision accepted | Missing identity, late availability, or forged provenance rejected | BLOCKED: current consumer rejects all pre-window availability |
| Event identity | Same source inputs produce stable source-bound event identity | Reindexed/different source stream cannot alias | BLOCKED: index-based only |
| Recross lifecycle | Approved same-boundary transition behavior | Repeated event outside approved lifecycle rejected/handled | POLICY UNRESOLVED |
| Boundary lifecycle | Approved expiry/invalidation/supersession transition | Stale/superseded boundary not silently reused | POLICY UNRESOLVED |
| Event availability | Break event tied to verified availability of completed break bar | Caller index/string alone cannot assert wall-clock availability | BLOCKED: index-only |
| Gap/session continuity | Upstream source/session evidence proves continuity | Integer index continuity alone cannot prove it | BLOCKED: no authenticated evidence |

### 7.7 Safe sequencing

1. Freeze the versioned pivot-event payload and source-stream binding contract, reusing the approved Model A / conditional Model B source identity policy without authorizing either identity implementation prematurely.
2. Resolve per-timeframe R/configuration linkage and exact confirmation availability.
3. Approve the warm-start acceptance payload and source/clock evidence boundary.
4. Specify event lifecycle (recross, deduplication, expiry, invalidation, supersession) as a separate explicit policy.
5. Add test-only consumer contract tests for the full positive/negative matrix.
6. Only then consider a separately reviewed implementation patch. Keep all production eligibility false until source identity, clock, continuity, and six-timeframe conformance are independently established.

## 8. Final compatibility disposition

PR #139 and PR #141 remain complementary design work, but the consumer boundary is **NOT CONTRACT-COMPATIBLE FOR PRODUCTION**. The immediate blockers are the ungoverned pivot payload, hard-coded two-bar assumption, rejected warm-start context, index-only event identity/availability, and unresolved event lifecycle. This is a review conclusion only; no policy is selected by this report.


## 9. Test-only consumer contract matrix added (2026-11-21)

Added two isolated files under `RUNTIME/MTF_PRODUCER_V2/`:
- `confirmed_pivot_consumer_contract_oracle.py`
- `test_confirmed_pivot_consumer_contract.py`

The oracle is explicitly synthetic-only and refuses non-fixture mode. It returns `production_eligible=false` and all source-identity, clock, and continuity authentication flags false. It is not imported by the production structure consumer and is not a production validator.

The 22 test cases cover:
1. Pre-window warm-start shape with original synthetic source and confirming-bar identities.
2. Rejection of the current minimal PR #139 ConfirmedPivot payload as insufficient for the proposed envelope.
3. Symbol, native timeframe, and source namespace binding.
4. Producer version, schema version, and detector configuration binding.
5. Source-bar identity/index correspondence and HIGH/LOW price consistency.
6. Final confirming-bar identity/index correspondence.
7. Explicit synthetic L/R configuration linkage without a universal two-bar assumption.
8. No use before final confirming-bar availability or after the decision snapshot.
9. Strict integer typing (booleans rejected), finite pivot prices, and finite source OHLC.
10. Duplicate pivot and source-bar identities rejected in the synthetic fixture scope.
11. Evidence-reference consistency checks as structural labels only, not authentication.
12. Separate HIGH and LOW candidates retained for the same source bar.
13. Six timeframe labels (M5/M15/M30/H1/H4/D1) accepted as independent schema fixtures.
14. Explicit non-production and non-authentication output flags.

**GitHub Actions:** latest run **44874316106** completed SUCCESS. The synthetic test job reports **54 total tests**, including all 22 consumer-contract cases. The bounded annual HistData archive-forensics job also completed SUCCESS for its previously defined 2016-2019 and 2021-2024 scope. Pivot fixture/identity workflow **44874316181** completed SUCCESS.

### Test interpretation limits

- The warm-start test proves only that the synthetic oracle can represent a pre-window pivot when source and confirming-bar references are supplied. It does not authorize production warm-start.
- Six timeframe labels are schema-level fixtures only; they do not prove live six-timeframe state isolation or conformance.
- Evidence references are opaque matching strings. The tests do not authenticate source, clock, precision, or continuity evidence.
- Synthetic Model A-shaped IDs do not prove that an upstream-native immutable ID exists in MT5 or HistData.
- The configured R tests verify the synthetic relationship between source index, final confirming index, and declared R; they do not select production L/R values.
- Event lifecycle (recross, deduplication, expiry, invalidation, supersession) remains deliberately untested until its policy is explicitly approved.
- No market data, 2025/2026 data, tuning, calibration, production detector, production consumer integration, Decision Brain integration, main-branch change, or merge.


### L/R coverage clarification

The synthetic confirmed-pivot envelope now requires both explicit `left_window` and `right_window` values and rejects non-positive values. The fixture uses L=2/R=3 solely as a synthetic test point; it is not a selected production configuration for any timeframe.
