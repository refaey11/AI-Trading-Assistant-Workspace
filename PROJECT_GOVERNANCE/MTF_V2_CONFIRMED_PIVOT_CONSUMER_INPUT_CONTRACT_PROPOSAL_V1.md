# MTF V2 Confirmed-Pivot Consumer Input Contract — Proposal V1

**Status:** PROPOSAL ONLY — NOT APPROVED — NOT IMPLEMENTED — NOT PRODUCTION-ELIGIBLE  
**Related work:** PR #139 structure consumer; PR #141 Pivot Detector V2 contract; PR #140 structural evidence envelope.

## 1. Purpose and boundary

Define the minimum evidence envelope required before the PR #139 MTF structure consumer may accept confirmed pivots from an independently versioned Pivot Detector V2.

This proposal is a compatibility boundary only. It does not implement a detector, source identity, clock authentication, warm-start, event lifecycle, or Decision Brain integration. It does not claim parity with historical `PIVOT_SEQUENCE_V2`, `trend_regime`, or `mtf_trend_score`.

## 2. Non-negotiable constraints

1. One consumer invocation is bound to exactly one canonical symbol and one native source timeframe.
2. Every pivot must be bound to the same source namespace, symbol, timeframe, producer/schema version, and source stream as the bars being consumed.
3. The source bar's immutable identity is authoritative. Model A (upstream-native immutable per-bar ID) remains preferred. Model B is permitted only after the already-approved absence and evidence gates, with separate review and approval. Model C (payload/OHLC-derived identity) remains rejected.
4. A local integer index may support ordering within one validated sequence; it is not a source identity and cannot authenticate continuity.
5. A pivot cannot be consumed before the verified availability of its final confirming right-side bar.
6. Caller-supplied strings, booleans, hashes, or timestamps are not authentication merely because they are present.
7. Missing, conflicting, or unauthenticated evidence fails closed. No neutral, zero, or inferred fallback is permitted.
8. No numeric L/R values are selected by this proposal. No inference from historical H1 two-bar observations or synthetic W2/W3/W5 labels is allowed.

## 3. Proposed envelope shape

The following is a conceptual field inventory, not a frozen JSON schema. Required/optional status, exact names, types, serialization, and status vocabulary remain open for review.

### 3.1 Source-stream envelope

| Field concept | Purpose | Current decision |
| --- | --- | --- |
| contract/schema version | Identifies the exact envelope contract | Required concept; version string not frozen |
| producer name and version | Identifies the producer that emitted the pivots | Required concept |
| canonical symbol | Binds the stream to the approved instrument identity | Required; canonical mapping contract unresolved |
| native timeframe | Binds the stream to exactly one of M5/M15/M30/H1/H4/D1 | Required; canonical encoding unresolved |
| source namespace | Identifies the upstream source/provider boundary | Required; actual selected source remains unresolved |
| source-bar identity model | Declares Model A or an explicitly approved Model B | Required; Model B not currently authorized |
| clock/provenance evidence reference | Points to independently verifiable source-time evidence | Required for production; evidence contract unresolved |
| source sequence / continuity evidence | Supports ordering and gap/session interpretation | Required for production; authority and schema unresolved |
| instrument precision evidence | Supplies trusted tick/precision metadata | Required for equality-sensitive evaluation; provider contract unresolved |
| detector configuration identity | Binds output to exact L/R and detector settings | Required concept; config schema/fingerprint lifecycle unresolved |

The envelope must not use the terminal environment `source_id`, an unverified MT5 raw epoch, row number, file position, OHLC, or payload hash as a substitute for an immutable source-bar identity.

### 3.2 Confirmed-pivot record

| Field concept | Purpose | Current decision |
| --- | --- | --- |
| pivot identity | Stable identity of this HIGH/LOW event | Conceptually required; production generation blocked until source-bar ID and config fingerprint are governed |
| pivot kind | HIGH or LOW | Required; same-bar dual candidates remain separate |
| pivot price | Exact source precision value | Required; no rounding/tolerance |
| source-bar identity | Original immutable bar that formed the candidate | Required; Model A preferred, Model B conditional |
| source sequence locator | Locates the source bar in its native sequence | Optional helper only; never identity |
| confirmation-window configuration | Exact L/R used for this timeframe | Required; numeric values not selected |
| final confirming-bar identity | Original identity of the final required right-side bar | Required concept |
| verified availability | Availability of the final confirming bar | Required; timestamp representation/evidence unresolved |
| confirmation status | Distinguishes confirmed, pending, invalid/unavailable | Required concept; exact enum unresolved |
| provenance references | Links to source, clock, precision, and producer evidence | Required for production; schema unresolved |

The pivot record must be independently verifiable against the referenced source bar. A HIGH record must match the source bar's high; a LOW record must match its low. This is a proposed acceptance invariant, not an implemented check.

### 3.3 Consumer decision snapshot

The consumer must receive an explicit decision snapshot boundary. A pivot is eligible only when its verified availability is no later than that snapshot. A pre-window pivot may be used only if its original source-bar identity, final confirming-bar identity, availability, and full provenance are preserved and verified. No synthetic warm-up pivot or re-created identity is allowed.

The current PR #139 behavior that requires every pivot's availability index to fall inside the current bar array is not compatible with this proposed warm-start contract. Do not relax it until the payload and acceptance policy are approved.

## 4. Consumer-side validation invariants

Before any production consumer can use a pivot, a separately tested validator must establish:

1. Envelope symbol/timeframe/source namespace match the exact consumer bar stream.
2. Producer/schema and detector configuration versions are recognized and immutable for the invocation.
3. Source-bar identity is present, unique in its governed scope, and valid under Model A or an explicitly approved Model B contract.
4. Pivot kind is exactly HIGH or LOW; dual candidates remain separate.
5. Pivot price is finite, numeric (not boolean), and equals the referenced source bar's corresponding high/low at trusted precision.
6. Source and availability references are well-typed and causally ordered.
7. The configured R and final confirming bar match the PR #141 rule; no universal two-bar assumption.
8. Verified availability is no later than the consumer decision snapshot.
9. Gaps and session closures are interpreted only by the approved upstream continuity authority.
10. Duplicate/revised source records follow an explicit upstream revision policy; the consumer does not silently deduplicate by OHLC or payload hash.
11. Identical source inputs, evidence, producer version, and configuration yield deterministic ordered consumer inputs.

A failure must produce an explicit unavailable/not-evaluable outcome under a separately frozen status vocabulary; it must not silently discard provenance or substitute another timeframe.

## 5. Event output boundary

This proposal distinguishes pivot identity from structure-event identity.

A future structure event should reference:
- the exact boundary pivot identity;
- the immutable source-bar identity of the completed break bar;
- the canonical symbol and native timeframe;
- event type and event-contract version;
- verified availability of the completed break bar;
- producer and provenance references.

The existing PR #139 event ID assembled from a local integer break-bar index and caller-supplied pivot ID is prototype-only. This proposal does not define a final event hash/serialization or event lifecycle.

## 6. Explicitly unresolved policy decisions

The following remain separate approvals and are not decided here:

- selected upstream source/provider and source namespace;
- Model A evidence or the full conditional Model B absence/clock/uniqueness/revision/serialization proof;
- canonical symbol and timeframe registries;
- trusted UTC clock and availability evidence;
- source sequence and session-calendar authority;
- exact status vocabulary and schema serialization;
- per-timeframe numeric L/R values and configuration fingerprint schema;
- warm-start provenance payload and acceptance procedure;
- event recross/deduplication, expiry, invalidation, supersession, and reset behavior;
- event identity encoding and replay compatibility.

## 7. Compatibility disposition

Until this proposal is reviewed and the open decisions are resolved, the PR #139 `ConfirmedPivot` dataclass is a synthetic prototype input only. It must not be treated as a production pivot-event contract. PR #140 structural validation does not authenticate source identity or clock truth and does not fill these fields automatically.

## 8. Governance

- Proposal only; no schema or policy is approved by this document.
- No detector or consumer runtime code changed.
- No production source-bar ID or event ID generated.
- No L/R values selected.
- No 2025/2026 market data accessed or used.
- No tuning, calibration, feature selection, or performance evaluation.
- No Decision Brain integration, live trading, BUY/SELL, or order path.
- No `main` changes and no PR merge.
