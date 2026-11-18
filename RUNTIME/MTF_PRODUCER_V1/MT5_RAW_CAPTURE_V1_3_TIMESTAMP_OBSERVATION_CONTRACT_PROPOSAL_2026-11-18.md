# MT5 Raw Capture V1.3 — Versioned Timestamp and Observation Contract Proposal

**Date:** 2026-11-18  
**Status:** DESIGN PROPOSAL ONLY — NOT AN IMPLEMENTATION SPECIFICATION  
**Target stage:** MTF Producer V1 / Stage B  
**Compatibility:** Preserve existing MT5 Raw Capture V1 and Forex-Only V1.2 unchanged.

## 1. Purpose and non-goals

This proposal defines the evidence required before a future raw-capture version can claim complete timestamp provenance. It responds to the compatibility gaps recorded in `MT5_CAPTURE_TO_MTF_SOURCE_COMPATIBILITY_AUDIT_2026-11-18.md`.

This document does not:
- change the existing V1 or V1.2 EA, CSV schema, ingest adapter, or runtime;
- define or calculate any of the seven Brain MTF feature fields;
- infer broker timezone, daylight-saving rules, historical UTC offsets, or bar-close times;
- convert, repair, or reinterpret the legacy historical archive;
- create direction, signals, entries, SL/TP, lots, or orders;
- access or tune the locked 2025 OOS period.

No V1.3 implementation is authorized by this proposal alone.

## 2. Timestamp concepts must remain separate

The following concepts are not interchangeable. A field must not be populated from another concept merely because both can be represented as ISO-8601 strings.

| Concept | Proposed field | Meaning | Current status |
| --- | --- | --- | --- |
| MT5 bar label | `bar_time_mt5_utc` | The `MqlRates.time` value for the captured bar, under the documented MT5 UTC source contract | Present in V1.2; source semantics must remain explicit |
| Broker/server wall-clock bar label | `bar_time_server` | A separately sourced server-domain representation of the bar label | Not available as a distinct proven field |
| Actual bar close instant | `bar_close_time_utc` | The actual instant at which the market bar ended | Not available; MUST NOT be computed by adding timeframe duration |
| Closed-bar observation instant | `closed_bar_observed_at_utc` | The instant at which the capture process observed the bar as closed and available through its capture path | Proposed; only emit after its clock source and uncertainty are proven |
| Retrieval instant | `retrieved_at_utc` | The instant a specific retrieval operation completed | Not currently emitted; do not alias to a host clock estimate |
| Clock diagnostics | Existing terminal/host observation fields | Contemporaneous observations from their documented clock domains | Diagnostic only; never use as historical broker timezone rules |

A bar observed through `CopyRates(..., 1, 1, rates)` is the latest closed bar returned at the time of observation. That establishes a closed-bar selection behavior; it does not independently reveal the exact historical close instant or prove when the broker first made the bar available.

## 3. Proposed V1.3 schema policy

V1.3, if later approved, must be a separately versioned schema and capture implementation. It must not silently alter the meaning or required columns of V1/V1.2.

Required policy:

1. Preserve `bar_time_mt5_utc` only under the explicitly documented `MqlRates.time` source contract. The serializer must not pretend that formatting a datetime with a trailing `Z` performs timezone conversion.
2. Do not emit `bar_time_server` unless a distinct API/source and its clock domain are documented and tested.
3. Do not emit `bar_close_time_utc` unless an authoritative source for the actual close instant is identified and verified. Timeframe-duration arithmetic is prohibited as a substitute.
4. Add `closed_bar_observed_at_utc` only when a reliable observation clock is available. Record its clock source, clock domain, synchronization status, and bounded uncertainty alongside the timestamp.
5. Keep `retrieved_at_utc` distinct from observation time. If the implementation cannot identify a separate retrieval event, leave it unavailable rather than duplicating another timestamp.
6. A `timezone_policy_id` must identify a reviewed, versioned source policy. It must not be derived from the current server-minus-host offset.
7. Unknown values remain null/unavailable with an explicit reason. No zero-fill, guessed offset, or fabricated timestamp is permitted.

### 3.1 Clock provenance metadata

Any newly introduced observation/retrieval timestamp must be accompanied by enough metadata to identify:
- clock source and API;
- clock domain (MT5 UTC contract, broker/server, host, or another explicitly named domain);
- synchronization state and evidence;
- declared maximum clock uncertainty, or an explicit unknown state;
- capture software/schema version;
- source and broker-server identity.

A host-derived `TimeGMT()` estimate remains diagnostic unless independent synchronization and uncertainty bounds are demonstrated. `TimeTradeServer()` and current quote/server-time observations remain current-time diagnostics, not historical bar timestamps.

## 4. Closed-bar availability contract

The capture contract may state that a row represents a bar selected as closed by the MT5 capture path only when:
- the selected API call and shift semantics are documented;
- the emitted closed flag is tied to that exact selection;
- the observation timestamp is generated at the actual observation event from an approved clock;
- stale or unavailable feeds fail closed;
- no later/future bar is attached to an earlier observation event.

The contract must distinguish:
- **bar identity time** — the source timestamp identifying the bar;
- **actual close time** — unknown unless independently sourced;
- **observation/availability time** — when this capture process observed the closed bar;
- **retrieval completion time** — when a retrieval operation completed, if separately measurable.

Do not infer that these four times are equal.

## 5. Validation and deterministic test requirements

Before any V1.3 implementation can be considered, tests must cover all six native periods: M5, M15, M30, H1, H4, and D1.

Required test groups:

1. **Schema compatibility:** V1 and V1.2 fixtures remain readable with unchanged semantics; V1.3 has an explicit schema/version discriminator.
2. **Clock provenance:** missing source, unknown synchronization, unknown uncertainty, invalid offsets, naive timestamps, and contradictory clock-domain metadata fail closed.
3. **Closed-bar selection:** verify shift-1 selection and `is_closed` behavior for all six periods against controlled MT5 observations.
4. **Boundary behavior:** period boundaries, weekend/session gaps, market closures, stale quotes, delayed ticks, and reconnect/restart behavior.
5. **Replay and duplicates:** repeated observations, out-of-order rows, conflicting duplicates, deterministic payload hashes, and idempotent ingestion.
6. **No-future availability:** a row must never be treated as available before its recorded observation instant; future-dated or causally impossible evidence is rejected.
7. **Clock disagreement:** preserve separate clock observations and reject any attempt to turn a contemporaneous offset into a historical timezone/DST conversion.
8. **Missing evidence:** unavailable close/retrieval timestamps remain unavailable; tests prove no timeframe-duration synthesis or imputation occurs.

Tests must use controlled clocks/fixtures where deterministic behavior is required. Live MT5 observations can supplement but cannot replace deterministic contract tests.

## 6. Historical archive remains a separate blocked problem

The legacy 2016–2024 archive has naive timestamps and unresolved broker-clock/DST provenance. Nothing in this proposal authorizes assigning UTC, applying a current broker offset, or deriving historical timezone transitions.

Historical archive normalization remains blocked until its original source lineage and timestamp policy are recovered independently. A new live capture contract cannot retroactively validate old timestamps.

## 7. Acceptance gates

V1.3 must not move from proposal to implementation until all of the following are reviewed and approved:

- [ ] MT5 API/source evidence for every proposed timestamp field.
- [ ] A reviewed clock-domain and synchronization policy.
- [ ] Explicit uncertainty bounds for any timestamp claimed as UTC.
- [ ] A reviewed `timezone_policy_id` and immutable policy documentation.
- [ ] Deterministic six-timeframe closed-bar and boundary tests.
- [ ] V1/V1.2 backward-compatibility tests.
- [ ] CSV/ingest schema review, including null/unavailable semantics.
- [ ] Independent compatibility audit against Stage A/B requirements.

Until then: Stage B remains PARTIAL; Stage C feature production and Stage D historical parity remain BLOCKED.

## 8. Decision

Treat this file as a design proposal only. Keep V1/V1.2 unchanged. The next safe work is evidence recovery and test design—not timestamp fabrication, feature formulas, or live-runtime integration. The 2025 OOS lock and no-live-orders restriction remain in force.
