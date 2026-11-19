# MTF Pivot Detector V2 — Reference Behavior Contract V1

**Status:** REVIEW CONTRACT — NO EXECUTABLE DETECTOR — NO PRODUCTION PARAMETERS SELECTED  
**Parent:** PR #141  
**Applies to:** M5, M15, M30, H1, H4, D1 independently

## 1. Purpose

This document translates the user-approved conservative policy baseline into an implementation-independent behavioral contract. It is a test oracle design, not a detector implementation. It does not choose numeric L/R settings, identity serialization, lifecycle rules, or production eligibility.

The 180-fixture corpus currently checks fixture structure and scenario coverage. Its CI success must not be described as proof that a pivot detector is correct. A future implementation must be tested against semantic assertions in this document, not merely against fixture counts.

## 2. Input contract

One detector invocation covers one symbol and one native timeframe. Inputs must already be completed source bars with:
- stable source-bar identity and strictly ordered source sequence;
- verified OHLC validity and completion status;
- trusted instrument precision metadata for equality-sensitive comparisons;
- verified source-time / availability provenance;
- explicit gap and missingness evidence;
- producer/schema identity and source payload hash.

The detector must not repair malformed bars, infer a missing candle, infer broker timezone/DST, infer session closure, round prices, or treat absent provenance as valid. Invalid or untrusted input makes affected candidate decisions NOT_EVALUABLE or UNAVAILABLE according to the upstream evidence status. Exact status vocabulary remains a schema decision.

## 3. Candidate evaluation — parameterized, not selected

For a candidate source bar at index i and an approved configuration (L,R):
- the left comparison set is exactly the L source bars immediately preceding i in the verified contiguous source sequence;
- the right comparison set is exactly the R source bars immediately following i in the verified contiguous source sequence;
- a HIGH candidate requires candidate.high to be strictly greater than every comparison high;
- a LOW candidate requires candidate.low to be strictly lower than every comparison low;
- equality with any relevant comparison value makes that candidate NOT_EVALUABLE under the approved plateau policy;
- no rounding, tolerance, minimum price separation, minimum bar separation, forced alternation, clustering, or replacement is applied.

This defines the semantics of a configured window. It does not approve any numeric L/R value for any timeframe. W2/W3/W5 remain synthetic test labels only.

## 4. Confirmation and causality

A candidate at i cannot be confirmed until all R right-side bars are completed and their verified availability is established.

For an uninterrupted, valid window:
- the final required right-side bar index is i + R;
- confirmation must not be visible at any decision snapshot earlier than that bar's verified availability;
- output availability is the verified availability of the final required confirming bar, not a guessed timestamp or the candidate bar timestamp;
- later data must not change any output that was already available at an earlier decision snapshot.

If the required right-side window is truncated, the candidate remains PENDING / insufficient-context; it is not a confirmed pivot.

The exact timestamp representation, evidence references, and final status enum are schema decisions and must be frozen before implementation.

## 5. Equal prices and dual candidates

### 5.1 Equal extrema
A candidate whose high equals any comparison high cannot be selected as a unique HIGH pivot. A candidate whose low equals any comparison low cannot be selected as a unique LOW pivot. Do not choose first, last, center, or arbitrary representative of a plateau.

### 5.2 Same-bar HIGH and LOW
If a bar independently qualifies as both HIGH and LOW, retain both candidate records with distinct kinds and the same source-bar identity. Their intrabar ordering is unknown from OHLC and must remain unresolved. Do not fabricate HIGH-before-LOW or LOW-before-HIGH.

## 6. Gaps and warm-up

A gap inside either required comparison window or the confirmation window blocks confirmation unless upstream source/session evidence explicitly proves that the source sequence is continuous under the governed source calendar. The detector itself does not decide that a weekend or market closure is expected.

Pre-window context may be used only when every supplied context bar has its original source identity, verified availability, and full provenance. No synthetic seed pivot may be created. A pre-window pivot must not be consumed before its original verified availability.

The exact session-calendar authority, gap status vocabulary, and warm-start payload contract remain open and require approval.

## 7. Determinism and identity

For identical source inputs, metadata, detector version, and configuration, output ordering and content must be deterministic. Replaying the same input must produce byte-identical canonical output once the serialization contract is frozen.

Pivot identity ingredients are approved conceptually:
- symbol;
- native timeframe;
- original source-bar identity;
- pivot kind (HIGH or LOW);
- detector version;
- configuration fingerprint.

The exact canonical field ordering, encoding, normalization, hash algorithm, and fingerprint derivation are NOT APPROVED. Do not write production identity code until these are specified and approved. A synthetic replay fixture may assert a deterministic-output requirement but cannot prove byte identity while encoding is undefined.

## 8. Semantic acceptance matrix

Every case must run independently for M5, M15, M30, H1, H4, and D1, and independently for every candidate (L,R) configuration under evaluation.

| Case | Expected behavior | Must reject |
| --- | --- | --- |
| Strict isolated high | HIGH candidate only after complete left/right context; confirm at final right bar availability | Earlier confirmation |
| Strict isolated low | LOW candidate only after complete left/right context; confirm at final right bar availability | Earlier confirmation |
| Equal high | HIGH candidate NOT_EVALUABLE | First/last/center tie-break |
| Equal low | LOW candidate NOT_EVALUABLE | First/last/center tie-break |
| Same-bar dual candidate | Retain separate HIGH and LOW candidates; ordering unresolved | Intrabar order inferred from OHLC |
| Incomplete left context | Pending / insufficient context | Treat truncated context as full window |
| Incomplete right context | Pending until all R bars are completed | Early confirmation |
| Unproven gap in comparison/confirmation window | Block affected candidate | Treat gap as ordinary adjacency |
| Verified continuity evidence | Apply only the upstream-approved continuity interpretation | Detector invents session policy |
| Future perturbation | Earlier decision snapshots remain byte-identical | Future values revise prior outputs |
| Identical replay | Canonical output identical after encoding freeze | Nondeterministic IDs/order |
| Invalid or unfinished OHLC | Reject affected input/candidate | Silent repair or use |
| Missing precision metadata | Equality-sensitive case NOT_EVALUABLE | Arbitrary decimal rounding/tolerance |
| Provenanced warm-up | May be consumed only with original identity and availability proof | Synthetic seed pivot |

## 9. Required test layers before detector code is production-reviewable

1. **Fixture integrity:** schema, unique IDs, complete timeframe/window/scenario matrix.
2. **Semantic oracle tests:** exact candidate classification, pending/confirmed transitions, tie handling, dual-candidate handling, gap blocking.
3. **Causality tests:** availability boundary, future perturbation, no early visibility.
4. **Replay tests:** deterministic ordering and, after identity freeze, byte-identical IDs and serialized outputs.
5. **Input rejection tests:** malformed OHLC, unfinished bars, missing precision, missing provenance, unproven gaps.
6. **Warm-start tests:** valid original pre-window source events versus missing/forged identity and availability.
7. **Six-timeframe isolation:** no cross-timeframe leakage; one timeframe's missingness cannot be filled from another.
8. **Property tests:** strict extrema and causality invariants over generated synthetic inputs, with fixed seeds and reproducible fixtures.

A passing fixture-integrity workflow is necessary but insufficient. No detector correctness, market validity, profitability, or production readiness claim may be made from it.

## 10. Open decisions that block implementation

- Numeric L/R values for each of six timeframes.
- Whether one configuration can be shared across some timeframes or each must differ (default expectation: explicit per-timeframe config).
- Exact gap/session continuity evidence contract.
- Exact pre-window warm-start payload and acceptance boundary.
- Exact status vocabulary for pending, insufficient context, invalid input, and unavailability.
- Canonical identity serialization and configuration fingerprint.
- Event expiry, invalidation, supersession, and recross/dedup lifecycle policy (separate review; not decided here).

No default values may be silently chosen. Do not tune any of these using 2025 or profitability outcomes.

## 11. Safety boundary

The pivot detector is evidence production only. It does not create directional bias, a trade recommendation, BUY/SELL, entry, SL/TP, or orders. It does not bypass Murphy/Nison/Trading in the Zone role boundaries or Risk hard gate. No Decision Brain integration, live trading, or MT5 readiness claim is authorized by this document.
