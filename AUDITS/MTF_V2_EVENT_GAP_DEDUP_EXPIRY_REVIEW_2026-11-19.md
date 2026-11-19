# MTF Producer V2 — Event Gap, Deduplication, and Expiry Review

Date: 2026-11-19  
Scope: static review of the current synthetic prototype only. No market-data validation, no policy change, and no runtime integration.

## 1. Reviewed implementation

- `RUNTIME/MTF_PRODUCER_V2/mtf_structure_producer_v2.py`
- `RUNTIME/MTF_PRODUCER_V2/test_mtf_structure_producer_v2.py`

The prototype is intentionally limited to completed OHLC bars plus caller-supplied, already-confirmed pivots. It has no timestamp fields on `Bar`, and it does not detect pivots.

## 2. Findings

### A. Index continuity is not a complete market-gap policy

The validator requires consecutive integer `Bar.index` values. This detects missing sequence numbers only if the caller has assigned indices faithfully. Since `Bar` has no open/close timestamps or session/calendar metadata, the producer cannot distinguish:
- a normal adjacent bar;
- a market-session closure/weekend;
- a missing/corrupt bar in the middle of a session;
- a broker feed outage or delayed bar.

The event crossing check compares the previous supplied close with the current supplied close. It therefore cannot apply a time-gap-specific rule. Do not treat contiguous indices as proof of contiguous market time.

### B. Event repeat/re-cross semantics are not fully specified

The implementation emits an event on a qualifying close crossing. The existing test proves that a second close remaining beyond the boundary does not emit another event. It does not test a later recross back through the same boundary and a subsequent recross again.

Because the structure state is recomputed from pivots and is not transitioned by the event itself, a later recross can satisfy the same event condition again. Whether this should be:
- a new event occurrence with a distinct ID;
- suppressed as a duplicate for the same pivot boundary;
- or allowed only after a reset/expiry condition

is a policy decision, not something established by the current approved semantics. No behavior is selected here.

### C. Event expiry / boundary lifecycle is absent

There is no expiry, invalidation, or supersession rule for a confirmed pivot boundary. The current producer continues to consider the latest available high/low pivot of the required kind, regardless of age or intervening structure changes, as long as it remains in the supplied pivot collection.

A maximum bar age, opposite-pivot supersession, structure reset, or session reset would all change event semantics and require explicit approval plus fixtures. None is inferred.

### D. Warm-start / pre-window pivot handling is restrictive

Validation requires every supplied pivot's `available_bar_index` to fall inside the supplied bar-index range. Consequently, a valid pivot confirmed before the current bar window cannot be supplied as warm-start context, even if it is causally available before the first processed bar.

This may be an intentional fixture boundary, but it is not a general streaming/replay contract yet. Decide whether pre-window pivots are allowed with explicit source/availability provenance before broadening it.

### E. The current event output is index-based, not time-authenticated

`StructureEvent.available_bar_index` is set to the break bar index. There is no event `available_at` timestamp, no broker clock evidence on the event itself, and no linkage from event availability to the separate evidence-envelope validator. The envelope gate validates supplied timestamps and hash shapes but does not authenticate the clock or automatically validate these event objects.

## 3. Decisions intentionally not made

This review does NOT choose:
- gap tolerance or maximum elapsed time between bars;
- weekend/session gap handling;
- whether a feed gap blocks, resets, or preserves structure state;
- event de-duplication across recrosses;
- event expiry or boundary invalidation;
- warm-start pivot acceptance;
- event timestamp/clock authentication semantics.

These require explicit deterministic rules and synthetic fixtures before implementation.

## 4. Required next specification

Before changing code, approve a versioned policy covering:
1. source-time continuity and the distinction between expected session closures and missing data;
2. behavior when a gap is detected;
3. same-boundary recross and event identity/deduplication;
4. boundary expiry/supersession;
5. pre-window confirmed-pivot warm start;
6. event `available_at` and provenance linkage.

Each rule must have positive and negative fixtures, plus no-lookahead and replay-determinism tests. Until then, retain current prototype behavior as prototype-only and keep production eligibility false.

## 5. Governance

No detector implementation, no gap/expiry policy was silently added, no 2025 data used, no Decision Brain integration, no order path, and no `main` change.
