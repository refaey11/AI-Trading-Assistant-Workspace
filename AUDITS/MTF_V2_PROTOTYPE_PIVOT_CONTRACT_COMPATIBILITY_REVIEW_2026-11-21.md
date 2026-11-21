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

## 10. Event lifecycle policy options — static review (2026-11-21)

**Status: OPTIONS ONLY / NO POLICY SELECTED / NO BEHAVIORAL TESTS AUTHORIZED**

### 10.1 Existing prototype behavior (observed, not approved policy)

The PR #139 implementation:
- emits on a close crossing the currently selected latest available boundary of the relevant pivot kind;
- does not emit again merely because the next close remains beyond that boundary;
- can emit again after a later recross and recross-again sequence because the event does not transition or consume the boundary;
- derives each event ID using the break-bar index, so separate crossings receive different IDs within the same synthetic indexed stream;
- does not expire a boundary by age;
- selects the latest available HIGH/LOW pivot for the relevant event branch, so a newer pivot of that kind changes the selected boundary;
- does not explicitly mark the older boundary as superseded, nor define invalidation/reset semantics.

These are implementation observations only. They do not establish user-approved lifecycle rules.

### 10.2 Recross and repeated-cross options

| Option | Deterministic rule | Benefit | Cost / risk |
| --- | --- | --- | --- |
| A — Every crossing is a new occurrence | Emit each qualifying close-crossing; each occurrence has its own event identity bound to the boundary and break bar | Preserves all observed crossings; simple event log | Repeated noise around one boundary can create many events; consumers must distinguish occurrences from a lasting structure transition |
| B — One event per boundary | After the first event for a boundary, suppress further events for that boundary | Strong deduplication; avoids repeated alerts | Can hide meaningful later breaks/reclaims of the same level; requires an explicit re-arm rule |
| C — Explicit re-arm cycle | Emit once; re-arm only after a specified close returns to the opposite side of the same boundary; then allow another crossing | Distinguishes a true recross cycle from consecutive closes | Requires exact equality/side semantics and state persistence; does not itself define expiry or boundary replacement |

No option is selected. In particular, the current “one event while closes remain beyond” test is not sufficient evidence for A, B, or C.

### 10.3 Expiry options

| Option | Deterministic rule | Benefit | Cost / risk |
| --- | --- | --- | --- |
| A — No age expiry | Boundary remains eligible until explicit supersession/invalidation | Avoids arbitrary bar-count or clock thresholds | Old levels may remain eligible for a long time |
| B — Source-bar age expiry | Expire after an approved number of native-timeframe bars since pivot availability | Bounded stale-boundary lifetime | Requires approved per-timeframe age values; bar count alone does not establish elapsed market time |
| C — Time/session expiry | Expire at an approved elapsed-time or session boundary | Can reflect market-session semantics | Requires authenticated clock, session calendar, timezone/DST and continuity authority, all currently unresolved |

No age or time threshold is inferred or proposed as a selected value.

### 10.4 Invalidation and supersession options

**Supersession (new pivot of same kind):**
- Option S1 — Immediate replacement: the newest confirmed HIGH replaces the active HIGH boundary (and likewise for LOW); prior boundary becomes ineligible for future events.
- Option S2 — Retain historical boundaries: keep older confirmed boundaries eligible, with a separate explicit selection rule.
- Option S3 — No implicit replacement: require a separate structure-state transition/confirmation before changing the active boundary.

The current prototype behaves closest to S1 for boundary selection, but it does not implement a governed supersession record or lifecycle state. This must not be mistaken for approval of S1.

**Invalidation/reset:**
- Option I1 — No independent invalidation; only supersession changes boundary eligibility.
- Option I2 — Invalidate on a separately defined opposite-side close/reclaim sequence.
- Option I3 — Reset the event/boundary state only on an upstream-authenticated discontinuity or explicit session/reset event.

An OHLC wick, an index discontinuity, or an unverified timestamp must not be silently treated as an invalidation/reset trigger.

### 10.5 Recommended decision sequence (recommendation only)

To avoid mixing independent decisions, approve these dimensions separately:
1. Recross model: A, B, or C.
2. Expiry model: A, B, or C.
3. Same-kind pivot supersession: S1, S2, or S3.
4. Invalidation/reset: I1, I2, or I3, with exact trigger semantics if I2/I3 is selected.

For each approved combination, define event occurrence identity and replay behavior, then add positive and negative synthetic fixtures. Do not write behavioral tests against an unapproved combination.

### 10.6 Cross-cutting blockers that remain independent

Even after lifecycle policy approval, production eligibility remains blocked by:
- unverified source-bar identity and source namespace;
- unauthenticated source clock and event `available_at`;
- unproven market-time/session continuity;
- unresolved canonical symbol/timeframe and configuration binding;
- lack of six-timeframe production conformance.

Lifecycle approval alone does not authenticate an event or authorize Decision Brain integration.

### 10.7 Governance

- Static review/options only; no lifecycle policy selected.
- No behavioral tests added for recross, expiry, invalidation, or supersession.
- No production or prototype runtime code changed.
- No source IDs, timestamps, L/R settings, or market-data-derived thresholds generated.
- No 2025/2026 market data accessed or used.
- No tuning, calibration, feature selection, or performance evaluation.
- No Decision Brain integration, BUY/SELL, order path, main-branch change, or merge.

## 11. User-approved event lifecycle policy and synthetic tests (2026-11-21)

The user approved the four proposed lifecycle choices as the basis for isolated synthetic behavioral tests:

1. **Recross:** explicit re-arm cycle. An upward HIGH-boundary event re-arms only after a later completed close at or below the same boundary; a downward LOW-boundary event re-arms only after a later completed close at or above it. A later crossing can then emit a new occurrence.
2. **Expiry:** no age-based expiry. A boundary remains eligible regardless of elapsed synthetic bars/time until same-kind supersession.
3. **Supersession:** the latest newly eligible confirmed pivot of the same kind replaces the prior active boundary; superseded pivots remain historical evidence but cannot trigger new events.
4. **Invalidation:** no independent invalidation/reset. A return close re-arms only; it does not delete or invalidate the boundary. Wicks, unverified timestamps, local index gaps, and inferred sessions are not invalidation triggers.

### Added artifacts

- `PROJECT_GOVERNANCE/MTF_V2_EVENT_LIFECYCLE_POLICY_V1.md`
- `RUNTIME/MTF_PRODUCER_V2/event_lifecycle_v1_synthetic_oracle.py`
- `RUNTIME/MTF_PRODUCER_V2/test_event_lifecycle_v1_policy.py`

The oracle is synthetic-only, isolated, and not imported by the PR #139 producer or Decision Brain. It consumes closes and synthetic confirmed pivots, uses strict-before availability, and does not classify BOS/CHOCH or generate direction. Synthetic event identity uses pivot ID + direction + break-bar index only; no production event ID is approved.

### Test coverage

The new suite contains 15 tests covering first crossing, suppression while beyond, re-arm and re-cross, equality-side semantics, symmetric downward events, no age expiry across 500 synthetic bars, same-kind supersession, suppression of superseded boundaries, independent HIGH/LOW lifecycle, strict availability causality, re-arm without invalidation, close-only behavior, deterministic replay, duplicate IDs, and boolean numeric rejection.

The existing workflow already includes the `RUNTIME/MTF_PRODUCER_V2/**` path filters and runs unittest discovery, so these tests are included without expanding workflow permissions or touching the archive-forensics scope.

### Governance and limits

- Policy approved for synthetic tests only; no production runtime lifecycle implementation.
- No changes to PR #139 producer code or Decision Brain.
- No L/R values selected; legacy PIVOT_SEQUENCE_V2 untouched.
- No source identity, clock, session continuity, or provider provenance authenticated.
- No 2025/2026 data, tuning, calibration, feature selection, or performance evaluation.
- No live trading, BUY/SELL, order path, main-branch change, or merge.
- PR #141 remains Draft/open/unmerged.



## 12. Warm-start source-context completeness audit and synthetic tests (2026-11-21)

A focused review of the test-only confirmed-pivot consumer oracle found that its initial warm-start fixture verified the pivot source-bar ID and final confirming-bar ID, but did not require every declared left/right context bar to be present in the supplied source history. A pivot could therefore pass the synthetic structural oracle even if an intermediate or outer L/R context bar had been omitted.

### Test-only hardening

Updated the test-only consumer oracle to require the full declared index interval from source_index - left_window through final_confirming_index in the supplied source history. All history bars continue to require unique IDs/indices, same symbol/native timeframe/source namespace, completed status, finite valid OHLC, and source-bar identity consistency.

Added six synthetic tests:
- missing outer-left context rejected;
- missing intermediate left context rejected;
- missing intermediate right context rejected;
- incomplete source-history bar rejected;
- context bar from another source namespace rejected;
- structurally complete indexed context still reports continuity_authenticated=false and production_eligible=false.

### Interpretation and remaining blockers

This closes only a structural fixture gap. Consecutive integer indices do not prove elapsed market-time continuity, distinguish a legitimate market closure from a missing in-session candle, authenticate a session calendar, or prove source clock truth. Opaque evidence-reference strings remain labels, not authentication.

The warm-start fixture still does not authorize production warm-start. Production acceptance remains blocked until source identity and clock evidence are independently authenticated, the complete pre-window context payload and availability boundary are governed, continuity/session evidence is authoritative, and six-timeframe conformance is demonstrated. No production consumer or detector code was changed.

No 2025/2026 market data, tuning, calibration, feature selection, performance evaluation, Decision Brain integration, main-branch change, merge, or order path.


## 13. Market-time continuity and session-gap audit (2026-11-21)

A focused static review compared the PR #139 structure consumer, the PR #140 structural evidence-envelope gate, the approved PR #141 pivot contract, and the approved synthetic event-lifecycle policy.

### 13.1 PR #139 consumer: sequence continuity only

The exact PR #139 `Bar` schema contains only integer index, OHLC, and a completed flag. Its validator requires consecutive ordered integer indices and valid completed OHLC. The event loop compares the previous supplied close with the current close without any bar-open/bar-close timestamp, source availability time, timezone, session calendar, or upstream continuity attestation.

Therefore, this consumer cannot distinguish:
- normal adjacent native-timeframe bars;
- expected weekend or market-session closures;
- a missing in-session candle;
- a delayed, duplicated, revised, or out-of-order feed record;
- a broker/provider outage.

A consecutive index sequence is only a caller-provided sequence property. It is not evidence of elapsed market-time continuity.

### 13.2 PR #140 envelope: stronger structure, still not continuity authentication

The separate PR #140 gate checks explicit-offset timestamp structure, timestamp ordering/causality, contiguous source indices, same-symbol binding, and exact six-timeframe envelope coverage. Its documented output remains `STRUCTURALLY_VALID_NOT_AUTHENTICATED`, with `production_eligible=false` and `authentication_required=true`.

Those checks do not establish the truth of the source clock, broker timezone/DST mapping, expected native-bar schedule, session calendar, or whether a time interval represents a legitimate closure versus missing in-session data. A monotonic sequence of timestamps does not by itself prove that no expected bar is missing.

### 13.3 Cross-contract boundary

The Pivot V2 contract permits confirmation across a gap only when upstream source/session evidence proves continuity. The approved event-lifecycle policy also explicitly says that a local index gap or inferred session is not an independent invalidation/reset trigger. These rules are compatible: neither index gaps nor guessed session semantics may be promoted to authenticated continuity or invalidation.

The present synthetic warm-start hardening checks that all declared L/R integer indices exist and are completed, but deliberately leaves `continuity_authenticated=false`. It does not resolve market-time/session continuity.

### 13.4 Evidence required before selecting production gap behavior

A production continuity contract still needs, at minimum:
1. authoritative source namespace and canonical symbol/native-timeframe mapping;
2. source bar-open, bar-close, and verified availability-time semantics;
3. independently verified source clock lineage, timezone, and DST policy;
4. an authoritative expected-bar/session calendar for the selected feed and instrument;
5. deterministic classification of expected closures versus missing in-session bars, delayed bars, duplicates, and revisions;
6. explicit state behavior at a proven discontinuity (block confirmation, preserve prior structure state, reset, or another approved transition);
7. six-timeframe positive/negative fixtures, including session boundaries, weekends, missing bars, provider outages, duplicate/revised bars, and replay determinism.

No gap tolerance, maximum elapsed time, session schedule, reset behavior, or continuity policy is selected in this audit. In particular, no arbitrary duration threshold is inferred from timeframe labels.

### 13.5 Disposition

**Market-time continuity remains BLOCKED / NOT AUTHENTICATED.** PR #139 remains a sequence-indexed synthetic consumer. PR #140 remains a structural envelope gate, not a trusted clock/session authority. The next safe step is to recover or define the selected upstream source/session authority and its evidence contract before proposing gap-state semantics.

Static review/documentation only. No PR #139 or PR #140 runtime changes, no production continuity implementation, no market-data-derived thresholds, no 2025/2026 data, no tuning/calibration, no Decision Brain integration, no main-branch change, and no merge.


## 14. Clock provenance and `available_at` contract audit (2026-11-21)

This section reviews the exact PR #131 MT5 Raw Capture V1.3 implementation, PR #140 MTF V2 evidence-envelope gate, and the approved Pivot V2 confirmation contract. It is a static contract audit; it does not authenticate a live terminal, broker, host clock, or historical source.

### 14.1 What PR #131 V1.3 actually observes

The inspected `RUNTIME/MT5_RAW_CAPTURE_V1_3/MT5_Raw_Capture_Only_V1_3.mq5`:
- reads closed `MqlRates` records through `CopyRates(symbol, tf, 1, 1, rates)`;
- preserves `MqlRates.time` as `bar_time_epoch_seconds_raw`;
- labels it `MT5_MQLRATES_DATETIME_RAW` and `bar_time_utc_status=UNVERIFIED`;
- records `TimeTradeServer()`, `TimeCurrent()`, `TimeGMT()`, and `TimeLocal()` as wall-clock observations;
- records `observed_server_minus_host_gmt_seconds` as a diagnostic;
- records `broker_server_id` and terminal-derived `source_id`.

The corresponding Python contract explicitly rejects UTC-alignment fields and requires the raw clock status to remain `UNVERIFIED`. It parses the observed clock strings as wall times but does not authenticate any of the clocks or establish the broker's historical timezone/DST schedule. The server-minus-host-GMT diagnostic is one observation, not a verified mapping for every historical bar. Terminal `source_id` identifies the capture environment, not a clock authority or candle.

**Finding:** V1.3 is correctly conservative, but it cannot supply a verified UTC `bar_open_time`, `bar_close_time`, or `available_at` for Pivot V2. Do not promote the raw epoch, server wall time, or diagnostic offset to UTC.

### 14.2 What PR #140 validates — and what it does not

The exact `mtf_v2_evidence_envelope_gate_v1.py`:
- requires ISO-8601 timestamps with an explicit offset;
- requires `bar_open_time < bar_close_time`;
- requires `available_at >= bar_close_time`;
- rejects `available_at > decision_time`;
- requires increasing contiguous integer indices and strictly increasing bar-open times;
- checks the declared source and clock evidence values are lowercase SHA-256-shaped strings.

It does **not**:
- verify that the explicit offset corresponds to the actual broker/source clock;
- require all timestamp values to be normalized to `+00:00` (different explicit offsets are accepted);
- authenticate the bytes behind `clock_evidence_sha256` or recompute a signed attestation;
- validate a clock-policy document against an approved registry (the `clock_policy_id` is only a non-empty string);
- prove host clock synchronization, broker server timezone, DST transitions, or historical offset changes;
- establish when the source made a completed bar observable to the capture process;
- establish whether `available_at` is source publication time, terminal observation time, ingestion time, or a later processing timestamp.

The returned state remains `STRUCTURALLY_VALID_NOT_AUTHENTICATED`, `production_eligible=false`, and `authentication_required=true`. A well-shaped hash and explicit offset are syntax/integrity placeholders, not proof of clock truth.

### 14.3 Required distinction between event times

Before implementation, the clock contract must distinguish at least:
1. **bar_open_time** — the source-defined opening instant for the native timeframe candle;
2. **bar_close_time** — the source-defined scheduled/actual completion boundary, including explicit treatment of session-shortened bars if applicable;
3. **source_available_at** — when the authoritative upstream provider made the completed bar available;
4. **captured_at** — when the MT5 capture process observed/read the completed bar;
5. **ingested_at** — when the ingestion system accepted the record;
6. **decision_time** — the as-of cutoff for a Decision Brain snapshot.

These are not interchangeable. A local capture timestamp cannot be substituted for source publication time. A candle's scheduled close cannot be substituted for actual source availability without an approved source guarantee. The pivot's `available_at` must be the verified availability of its final confirming bar, as required by the Pivot V2 contract; it must not be copied from the pivot source candle or guessed as close time.

### 14.4 Minimum evidence contract before clock authentication

A future source-clock contract must identify and independently verify:
- the selected provider/broker and authoritative source namespace;
- canonical instrument/symbol mapping and native timeframe;
- source timestamp semantics (bar open vs close, epoch unit, timezone/offset basis);
- broker-server timezone history and DST transition rules, if server-local time is used;
- authoritative UTC reference and synchronization/error bounds for the capture host and terminal;
- source publication/availability semantics and evidence for the actual completed-bar observation boundary;
- immutable evidence payload, digest/signature, issuer identity, version, and verification procedure;
- clock-policy registry/version and fail-closed behavior when evidence is stale, missing, conflicting, or outside tolerance;
- duplicate, delayed, revised, and out-of-order record handling;
- six-timeframe fixtures covering ordinary bars, weekends, DST transitions, session changes, delayed publication, terminal reconnect, host clock drift, and replay.

Any tolerance or synchronization bound must come from authoritative source/operations evidence and explicit approval; no numeric tolerance is selected here.

### 14.5 Disposition

**Clock authentication and production `available_at` remain BLOCKED / NOT AUTHENTICATED.** PR #131 V1.3 correctly preserves raw time as UNVERIFIED. PR #140 validates envelope structure and as-of ordering only. The approved Pivot V2 causality requirement remains unchanged: a pivot becomes available only at the verified availability of its final confirming bar.

Next safe step: identify the actual intended source boundary (historical archive vs live broker/MT5 feed) and recover its clock/publication-time authority. These may be different sources and must not be silently combined into one clock policy.

Static review/documentation only. No timestamp promotion, clock-authentication code, source-bar ID, production `available_at`, detector/consumer runtime change, 2025/2026 data, tuning/calibration, Decision Brain integration, main-branch change, merge, or order path.


## 15. Historical-vs-live clock authority boundary inventory (2026-11-21)

The Section 14 recommendation to identify the actual source boundary was checked against the existing bounded repository evidence. The current evidence describes at least two distinct source paths; it does not justify one shared clock policy.

| Candidate source path | What is positively evidenced | Clock/publication-time authority | Current disposition |
|---|---|---|---|
| Annual HistData GBPUSD M1 MT archives, 2016–2019 and 2021–2024 | The eight individually inspected annual release archives identify HistData.com in companion metadata | No explicit UTC/GMT timezone, DST, broker-server, or offset declaration recovered; no provider publication-time SLA/evidence | Historical file provenance known; clock lineage and available_at BLOCKED |
| 2020 GBPUSD M1 | No matching annual HistData M1 asset in the inspected release inventory | Provider and clock authority unresolved | BLOCKED; do not bridge the gap by assumption |
| Combined GBPUSD M1 master 2016–2026 | Prior workflows downloaded and parsed/loaded it; the earlier OOS-scope correction is recorded in Section 11 of the source identity audit | Its internal per-year provider/clock manifest was not recovered in this review; 2025 remains protected and is not to be re-inspected | BLOCKED; do not infer all-year HistData provenance from annual subset |
| TitanFX-labelled derived volume path, GBPUSD 2020–2024 | Existing audit records source_volume as TitanFX M1-derived timeframe volume for OBV | This is volume-path attribution only; no raw OHLC clock/publication-time contract recovered | Not a candidate clock authority for general OHLC/Pivot input |
| Live MT5 Raw Capture V1.3 | EA captures broker-server identifier, raw MqlRates time, terminal/server/host clock observations | Actual broker/server identity and its historical timezone/DST policy are not yet selected or evidenced; raw candle time is explicitly UNVERIFIED | Capture schema only; no authenticated UTC or provider available_at |

### 15.1 Boundary decision

There is currently **no single selected authoritative source boundary** for both historical and live Pivot V2 inputs. Historical HistData files and a live MT5 terminal capture must be treated as separate source namespaces and separate clock policies unless a future, evidence-backed contract explicitly proves equivalence.

Do not:
- use the TitanFX OBV volume label as proof of the OHLC provider;
- assume the annual HistData timezone from observed wall-clock values;
- infer the missing 2020 provider from adjacent years;
- infer the combined master provider from the annual archive subset;
- treat a broker/server name captured at runtime as proof of its timezone/DST history;
- synthesize provider source_available_at from candle close or local capture time.

### 15.2 Required next input / recovery target

To proceed without guessing, the project must recover one of:
1. the authoritative historical source manifest that maps each development-year OHLC file to provider, symbol mapping, timezone/offset and revision policy; or
2. the selected live broker/server's official clock/timezone/DST and bar-publication semantics, plus a controlled terminal observation protocol.

These are separate workstreams. A future implementation may support both, but it must use separately versioned source/clock policies and keep their identities distinct. The historical path must not be promoted into a live clock authority, and the live MT5 observations must not retroactively authenticate historical archive timestamps.

**Disposition:** no source boundary selected, no UTC promotion, no Model B source identity authorization, and no production available_at. The next safe action is source-manifest recovery for historical data or broker-specific clock authority recovery for the live feed; a choice is required before either can become an implementation contract.

Static evidence inventory only. No external lookup, no 2025/2026 data access, no tuning, no source/runtime change, no main change, no merge, and no order path.
