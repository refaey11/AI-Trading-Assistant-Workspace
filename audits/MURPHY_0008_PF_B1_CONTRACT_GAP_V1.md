# MURPHY 0008 — PF-B1 CONTRACT GAP V1

Status: OPEN GOVERNANCE GAP / NOT PRODUCTION FROZEN
Date: 2026-08-15
Branch: audit/murphy-0008-pf-b1-v1

## Purpose
Record the remaining PF-B1 gap after whole-book Murphy review, Workspace review, and GitHub compatibility search.

## What is established
1. Murphy 0008 semantics are source-supported: support is decisively broken to the downside, price later rallies toward the broken support, and the former support acts as resistance.
2. The canonical project architecture already provides reusable upstream primitives; no new Pivot engine or generic Support/Resistance engine is required for this audit.
3. For 0008, a confirmed reaction-trough candidate from PIVOT_SEQUENCE_V2 can serve as a support-boundary candidate without inventing a horizontal clustering tolerance. This is an operationalization proposal, not a literal quote from Murphy.
4. The PF-B1 interface already distinguishes raw break evidence from decisive confirmation and includes availability timestamps and NOT_EVALUABLE behavior.

## Remaining gap
The project does not currently have an approved, production-frozen deterministic operator that maps a raw downside break of the 0008 support boundary to the source-semantic condition "decisive break."

## Whole-book source reconciliation
The uploaded Murphy material contains price/time confirmation rules in specific contexts, including trendline filters and reversal-pattern confirmation. Those contexts do not, by themselves, authorize a generic 0008 PF-B1 operator. Therefore the following are NOT adopted as 0008 policy merely because they appear elsewhere in the book:
- 1% price filter
- 3% price filter
- two consecutive closes
- ATR-based threshold
- pip-based threshold
- arbitrary percentage/tolerance
- arbitrary lookback

## Governance consequence
PF-B1 must remain policy-injected and must not silently select a confirmation rule from another Murphy context.

Required behavior:
- raw break observable and available -> record raw break event;
- approved 0008 decisive-break policy present -> evaluate decisive confirmation;
- approved policy absent or evidence insufficient -> NOT_EVALUABLE for decisive confirmation.

## No-lookahead requirement
The raw-break timestamp and any future confirmation timestamp must be separated. A later candle cannot be used to retroactively mark an earlier candle as confirmed unless the confirmation timestamp reflects when that evidence actually became available.

## 0008 readiness
0008 may proceed to implementation only after this governance gap is explicitly resolved by an approved project policy and its deterministic tests. Until then, do not claim 0008 production readiness or freeze.

## OOS protection
2025 remains OOS and must not be used to select, tune, or justify the missing PF-B1 policy.

## Decision
OPEN — CONTRACT GAP CONFIRMED.

Next gate: obtain/approve a source-faithful PF-B1 decisive-confirmation policy, then test it before building/finalizing the 0008 evaluator.
