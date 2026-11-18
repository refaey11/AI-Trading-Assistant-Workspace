# MT5 Clock Source Evidence Register

**Date:** 2026-11-18  
**Parent:** PR #122 — MTF Producer V1 governed design and compatibility gates  
**Status:** READ-ONLY EVIDENCE REGISTER — authoritative platform semantics NOT YET VERIFIED  
**Purpose:** Separate what the repository's EA code visibly does from what can safely be claimed about each clock domain.

## 1. Scope and search result

Reviewed the repository's existing MT5 capture/source audits and the V1 / Forex-Only V1.2 EA timestamp serialization findings. A GitHub code search of the repository's default-branch index for `MqlRates.time`, `TimeGMT`, `TimeTradeServer`, `TimeCurrent`, `CopyRates`, `TimeGMTOffset`, and `bar_time_mt5_utc` returned no matching source/documentation results.

This is a bounded search result, not proof that no documentation exists in every branch, archive, external source, or local installation. No external documentation was consulted for this register.

## 2. Source-by-source register

| API / source | Use visible in the reviewed EA | Claim currently supported by repository evidence | Claim NOT established by this evidence | Required authoritative evidence |
| --- | --- | --- | --- | --- |
| `MqlRates.time` | `rates[0].time` is serialized as `bar_time_mt5_utc` through `IsoUtc()` | The EA serializes the `MqlRates.time` value associated with the selected rate | The EA code alone does not prove the value's UTC semantics, bar-open/close convention, or cross-source comparability | Official MQL5 API reference for the exact `MqlRates.time` semantics, plus a pinned source URL/version in the project |
| `TimeGMT()` | Serialized as `host_gmt_estimate_utc` through the same formatter | The EA records a value returned by `TimeGMT()` | Host clock synchronization, accuracy, uncertainty, and suitability as a trusted observation clock are not proven | Official API reference plus host clock synchronization/uncertainty evidence and controlled terminal observations |
| `TimeCurrent()` | Recorded as a current terminal/server clock observation | The EA records the API return value separately | It is not established as the historical bar timestamp or as a retrieval/availability timestamp | Official API reference and a field-specific source contract |
| `TimeTradeServer()` | Recorded as a current server-time estimate | The EA records the API return value separately | It is not established as the historical bar timestamp, a historical broker timezone rule, or a trusted UTC clock | Official API reference and controlled observations across server conditions |
| `TimeLocal()` | Recorded as a local machine clock observation | The EA records a local-time observation | Accuracy, synchronization, and conversion to UTC are not proven | Official API reference and host clock synchronization evidence |
| `TimeGMTOffset()` | No verified use as a historical conversion policy in the reviewed capture path | No historical conversion behavior is established by the current EA audit | Must not be used to infer historical broker/server timezone or DST policy without authoritative semantics and time-specific evidence | Official API reference and a separately approved broker/server timezone-history policy |
| `CopyRates(..., 1, 1, rates)` | Requests one rate at shift 1; EA marks the captured record `is_closed=true` | The code's intended selection path is the latest prior bar/rate at shift 1 | This alone does not prove the exact close instant, first-availability instant, synchronization state, or all six timeframe boundary behaviors | Official API reference for indexing/series behavior plus deterministic tests and MT5 Demo observations for M5/M15/M30/H1/H4/D1 |
| `IsoUtc(datetime)` | Decomposes the supplied datetime and appends literal `Z` | The formatter emits an ISO-looking string with a Z suffix | It does not perform a timezone conversion or prove the input's clock domain | Code inspection is sufficient for formatter behavior; input clock semantics must be evidenced independently |

## 3. Cross-cutting evidence gaps

- No source-specific clock-domain contract is pinned in the reviewed repository evidence.
- No trusted retrieval/observation timestamp with synchronization and uncertainty evidence is established.
- No `bar_close_time_utc` or first-availability timestamp is emitted by the reviewed V1/V1.2 capture contract.
- No historical broker timezone/DST policy is established for the 2016–2024 archive; its timestamps remain naive.
- A contemporaneous server-minus-host-GMT difference is diagnostic only; it is not a historical timezone conversion table.
- A trailing `Z` or explicit ISO offset is serialization syntax, not independent proof of clock provenance.
- No close-time value may be synthesized by adding timeframe duration.

## 4. Decision and safe next step

**Decision: KEEP THE V1.3 TIMESTAMP GATE BLOCKED.**

Before freezing a V1.3 timestamp schema or implementing its validator:

1. Attach the official MQL5 documentation/source reference for each API above, with exact URL, retrieval date, and relevant quoted definition or source excerpt.
2. Review whether each API describes UTC, trade-server time, local time, last-known quote time, or a calculated estimate; do not transfer semantics from one API to another.
3. Record the clock domain for every proposed field independently.
4. Define how host synchronization and uncertainty are evidenced if a host observation timestamp is required.
5. Run controlled MT5 Demo observations for all six native timeframes, preserving terminal build, broker server identity, raw capture, and observation notes.
6. Only after review, approve a versioned schema and deterministic fixtures. Keep unknown values unavailable.

No source code, EA, CSV, ingest adapter, existing V1/V1.2 data, feature formula, Decision Brain, risk behavior, or trading behavior is changed by this register.

## 5. Gate status

- Repository code inspection: **RECORDED**
- Authoritative platform documentation attached: **PENDING**
- Clock-domain policy approved: **PENDING**
- Trusted observation clock / uncertainty: **PENDING**
- Six-timeframe MT5 Demo boundary evidence: **PENDING**
- V1.3 schema and validator: **BLOCKED**
- Stage C derived MTF feature production: **BLOCKED**
- Stage D historical parity: **BLOCKED**
- 2025 OOS: **LOCKED / NOT TOUCHED**
- Live orders: **NOT AUTHORIZED**
- Automated repository tests: **NOT RUN — documentation-only change**
