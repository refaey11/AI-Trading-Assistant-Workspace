# Murphy 0008 — PF-B1 Governance Gate V1

Status: GOVERNANCE GATE / NOT PRODUCTION FROZEN
Date: 2026-08-15

## Purpose
Define the exact current gate for Rule 0008 without inventing a decisive-break threshold.

## Source-backed rule identity
0008 is the support-to-resistance role reversal case:
- support is decisively broken to the downside;
- price later rallies toward the broken support;
- the broken support acts as resistance;
- the resulting role reversal is bearish.

Project source status: SOURCE SEMANTICS RESOLVED / EVALUATOR PENDING.

## Audit result
The current project artifacts contain PF-B1 (Breakout Confirmation) as a shared primitive proposal. PF-B1 requires an approved breakout/filter definition and returns NOT_EVALUABLE when no approved definition exists.

No authoritative project-specific decisive-break contract was found that closes 0008 to a production operator.

## Murphy filter evidence
Murphy Chapter 4 discusses breakout filters including price-filter and time-filter concepts. Project governance explicitly prevents silently binding the general 3% example or two-day example to 0008.

Therefore this gate does NOT choose:
- 3%
- two consecutive closes
- ATR
- pips
- arbitrary percentage
- arbitrary lookback
- hidden tolerance

## Reuse decision
Do not create a separate 0008 breakout engine.
Reuse PF-B1 once its governance contract is approved. Reuse PF-H1 for the support/resistance level representation where applicable.

## Current executable status
Until an approved deterministic decisive-break contract exists:
- PF-B1 status for 0008 = NOT_EVALUABLE
- 0008 evaluator = NOT_EVALUABLE / not yet production-ready
- historical QA = blocked
- freeze = blocked

## Required next gate
Close the smallest shared PF-B1 governance contract using source-compatible evidence. The contract must define the evidence needed for:
1. downside break of the support boundary;
2. breakout timestamp;
3. confirmation timestamp;
4. availability timestamp;
5. explicit NOT_EVALUABLE behavior when required evidence is missing.

The contract must remain separate from Murphy's qualitative wording and must not claim unsupported numeric rules as verbatim Murphy.

## Validation after closure
1. deterministic unit tests;
2. availability/no-lookahead tests;
3. 2016–2024 historical QA;
4. provenance/reconciliation;
5. 2025 remains OOS and cannot be used for tuning or operator selection;
6. final freeze manifest only after all gates pass.

## Evidence references
- MURPHY_READY_BATCH_0008_0014_V1.txt
- MURPHY_PATTERN_PRIMITIVES_IMPLEMENTATION_SPEC_V1.md
- MURPHY_0013_0020_PRIMITIVE_CLOSURE_PROPOSAL_V1.md
- MURPHY_0013_0020_SOURCE_RECONCILIATION_V2.md

## Decision
The correct action now is to close PF-B1 governance before implementing 0008. No historical optimization is authorized to choose the decisive-break operator.
