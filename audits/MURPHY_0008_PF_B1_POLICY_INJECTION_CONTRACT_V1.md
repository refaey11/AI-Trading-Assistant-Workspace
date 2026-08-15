# Murphy 0008 — PF-B1 Policy Injection Contract V1

Status: PROPOSED GOVERNANCE CONTRACT / NOT PRODUCTION FROZEN
Date: 2026-08-15
Branch: audit/murphy-0008-pf-b1-v1

## Purpose
Close the PF-B1 interface/governance boundary without inventing a universal decisive-break threshold. The contract separates the reusable breakout interface from the consumer-specific policy that determines when a raw break is decisive.

## Source boundary
Murphy supports support/resistance role reversal after a decisive/significant downside penetration and discusses price/time confirmation policy families. The supplied project evidence does not authorize one universal numeric operator for Rule 0008.

Therefore this contract does not hard-code 1%, 3%, two consecutive closes, ATR, pips, arbitrary percentages, arbitrary lookbacks, or hidden tolerances.

## Inputs
- `boundary_id`
- `boundary_price`
- `direction = DOWN`
- completed-bar OHLC evidence
- `policy_id` and approved `policy_object` (optional)
- source/availability metadata

## Raw break event
A completed-data boundary penetration may be recorded as a raw break event using the already-approved upstream `break_structure_down` candidate when its own availability semantics are satisfied.

Raw break evidence is not equivalent to decisive confirmation.

Required raw event fields:
- `boundary_id`
- `direction = DOWN`
- `raw_break_timestamp`
- `raw_break_status`
- `availability_timestamp`

## Decisive confirmation
PF-B1 may emit `CONFIRMED` only when an explicitly approved policy object is present and all of that policy's deterministic conditions are satisfied.

The policy object must declare:
- `policy_id`
- `policy_family`
- exact deterministic condition
- applicable consumer/rule context
- source/provenance reference
- confirmation timestamp semantics
- availability/no-lookahead semantics

If no approved policy is bound, or required evidence is unavailable/ambiguous, PF-B1 MUST return `NOT_EVALUABLE` for decisive confirmation.

## Output
- `boundary_id`
- `direction`
- `raw_break_timestamp`
- `confirmation_timestamp` (null until decisive confirmation is actually available)
- `availability_timestamp`
- `status = CONFIRMED | NOT_CONFIRMED | NOT_EVALUABLE`

## Temporal invariants
1. `raw_break_timestamp` cannot precede boundary availability.
2. `confirmation_timestamp` cannot precede `raw_break_timestamp`.
3. `availability_timestamp` cannot claim evidence was known before its actual source availability.
4. Future candles/pivots cannot be used before their availability timestamp.
5. A later 0008 retest cannot be used to manufacture an earlier decisive-break confirmation.

## Consumer binding
Rule 0008 must bind an approved policy explicitly. PF-B1 must not silently inherit a policy from another Murphy rule/context.

The same PF-B1 interface may serve 0009/0010 and other breakout consumers, but each consumer must have an explicit policy binding or remain `NOT_EVALUABLE`.

## Prohibited behavior
- no threshold selection from historical replay outcomes;
- no 2025 selection/tuning;
- no universal 1% or 3% default;
- no universal two-day default;
- no ATR/pip/arbitrary tolerance/lookback substitution;
- no duplicate breakout engine;
- no conversion of a raw break into decisive confirmation merely because a later event exists.

## Governance state
This document freezes the interface shape only if/when separately approved. It does NOT freeze a decisive-break policy and does NOT make 0008 production-ready.

Current decision: `PF-B1_INTERFACE = COMPATIBLE`; `DECISIVE_POLICY_FOR_0008 = OPEN`; `0008 = NOT_EVALUABLE / BLOCKED_FOR_PRODUCTION` until policy binding and PF-H1 support identity are approved.
