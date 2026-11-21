# MTF V2 Structure Event Lifecycle Policy V1

**Status:** USER-APPROVED POLICY BASELINE FOR SYNTHETIC TESTS ONLY — NOT PRODUCTION-ELIGIBLE  
**Approval recorded:** 2026-11-21

## 1. Approved decisions

1. **Recross — explicit re-arm cycle.** A boundary emits at most one event per armed cycle. After an upward crossing of a HIGH boundary, a later completed close at or below that same boundary re-arms it. After a downward crossing of a LOW boundary, a later completed close at or above that same boundary re-arms it. A subsequent qualifying crossing may emit a new occurrence.
2. **Expiry — no age-based expiry.** A boundary does not expire merely because bars or time have passed. It remains eligible until superseded by a newer confirmed pivot of the same kind in the same validated stream.
3. **Supersession — latest confirmed same-kind pivot replaces the active boundary.** A newly eligible confirmed HIGH supersedes the previously active HIGH; likewise for LOW. The superseded pivot remains historical evidence but is no longer eligible to trigger new events.
4. **Invalidation — no independent invalidation.** There is no separate invalidation/reset trigger. A return close to the pre-break side only re-arms the event cycle; it does not invalidate, delete, or expire the boundary. A wick, unverified timestamp, local index gap, or inferred session event does not invalidate/reset it.

## 2. Exact synthetic crossing semantics

- HIGH / upward crossing: previous completed close <= boundary price and current completed close > boundary price.
- LOW / downward crossing: previous completed close >= boundary price and current completed close < boundary price.
- Equality is on the pre-break/re-arm side: close <= HIGH price re-arms upward; close >= LOW price re-arms downward.
- The first supplied close is not a crossing because no previous close is available.
- The re-arm close cannot also be a new crossing on the same bar.
- BOS versus CHOCH classification, structure-state transitions, pivot detection, and trade direction are outside this lifecycle policy.

## 3. Ordering and supersession in synthetic tests

The test oracle receives explicit synthetic pivot availability indices. A pivot becomes eligible only on a bar whose index is strictly greater than its availability index. When multiple synthetic same-kind pivots are supplied, deterministic fixture ordering is by availability index, source index, and pivot ID. This ordering is a fixture convention, not an authenticated production source ordering rule.

## 4. Event occurrence identity in tests

Each synthetic occurrence is represented by boundary pivot ID, crossing direction, and break-bar index. Repeated occurrences after a valid re-arm have distinct break-bar indices. This does not approve a production event hash, serialization, or stable cross-replay identity contract.

## 5. Required behavioral coverage

Tests cover first crossing, suppression while beyond, re-arm including equality, subsequent crossing, symmetric LOW behavior, no age expiry, same-kind supersession, rejection of superseded boundaries, independent HIGH/LOW lifecycle, deterministic replay, and causality.

## 6. Explicit limitations and production blockers

This policy and test oracle do not authenticate source-bar identity, provider namespace, source clock, UTC timestamps, event availability, market-time continuity, session calendars, canonical symbol/timeframe, or production pivot configuration. Production ordering, event identity, persistence, and replay compatibility remain unresolved.

This does not implement or authorize a production detector, modify PR #139 runtime, connect to the Decision Brain, generate BUY/SELL, place orders, or establish MT5 readiness. No 2025/2026 market data, tuning, calibration, feature selection, or performance evaluation is part of this work.

## 7. Governance

- The four lifecycle choices are user-approved as the basis for isolated synthetic behavioral tests.
- Numeric L/R values remain unresolved.
- Legacy PIVOT_SEQUENCE_V2 remains untouched.
- PR #141 and PR #142 remain Draft/open/unmerged.
- No changes to main.
