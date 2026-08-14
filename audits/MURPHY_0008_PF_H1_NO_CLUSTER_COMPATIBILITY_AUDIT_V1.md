# PF-H1 / Murphy 0008 — No-Cluster Compatibility Audit V1

Status: GOVERNANCE PROPOSAL / NOT PRODUCTION FROZEN
Date: 2026-08-15

## Purpose
Determine whether Murphy Rule 0008 requires a horizontal-level clustering/tolerance operator, or whether its support boundary can be represented directly from an existing confirmed reaction trough without inventing a tolerance.

## Source basis
The uploaded Murphy Chapter 4 source describes support as a price level or area below the market identified by prior reaction troughs, and describes support-to-resistance role reversal after a decisive downside break. It does not specify a project numeric tolerance for merging nearby trough prices into one horizontal level.

## Rule-0008 contract evidence
The existing Trading Rules V2 registry defines MURPHY_0008 as:
- a support level is decisively broken to the downside;
- price later rallies toward the broken support;
- direction bearish.

The registry does not require multiple support tests, a clustered support zone, or a numeric level tolerance.

## Compatibility decision
For 0008 only, PF-H1 does NOT need to perform level clustering as a prerequisite.

Smallest source-faithful operationalization candidate:
1. Consume a confirmed LOW/reaction-trough candidate from canonical PIVOT_SEQUENCE_V2.
2. Use that candidate's price as the support boundary candidate.
3. Represent the boundary as a constant horizontal price level at that candidate price.
4. Preserve the pivot's confirmed availability timestamp.
5. Do not merge nearby troughs and do not invent percentage/ATR/pip/tolerance/lookback values.
6. If the upstream pivot/support evidence is unavailable, return NOT_EVALUABLE.

This is an operationalization candidate, not a claim that Murphy literally specifies a one-pivot software rule.

## Important semantic boundary
A confirmed pivot-derived trough is a support-boundary candidate. It must not be silently labeled an "important" or "major" support level unless the source/project contract separately establishes that fact.

Therefore this proposal removes the clustering blocker for 0008 but does not create a new significance filter.

## PF-B1 interaction
PF-B1 can consume the resulting support boundary without needing PF-H1 clustering. However, decisive-break confirmation remains a separate open gate.

The project may record an observable break event separately from decisive confirmation, but no source-faithful decisive operator is approved yet. No 3%, 2-day, ATR, pip, arbitrary percentage, arbitrary lookback, or hidden tolerance is introduced here.

If no approved decisive-break policy is supplied, PF-B1 must return NOT_EVALUABLE for decisive confirmation.

## 0008 path after this audit
PIVOT_SEQUENCE_V2
-> confirmed LOW reaction-trough candidate
-> PF-H1 0008 boundary candidate (no clustering)
-> PF-B1 decisive downside confirmation (policy still open)
-> later rally/retest
-> former support acts as resistance
-> 0008 evidence output

## Decision
PF-H1 clustering is NOT a blocker for 0008.
PF-B1 decisive confirmation remains the blocker.
Do not build/freeze the 0008 evaluator until PF-B1 governance is approved and tested.
2025 remains OOS and is excluded from operator selection/tuning.
