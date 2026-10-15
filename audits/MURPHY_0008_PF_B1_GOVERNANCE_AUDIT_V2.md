# Murphy 0008 — PF-B1 Governance / Compatibility Audit V2

Status: BLOCKED / NOT PRODUCTION-APPROVED

## Source-locked semantics
- Support is broken decisively to the downside.
- A later rally/retest occurs toward the broken support.
- The broken support functions as resistance.
- The resulting rule evidence is bearish support-to-resistance role reversal.

## Existing architecture
- PF-H1: shared horizontal support/resistance primitive proposal.
- PF-B1: shared breakout-confirmation primitive proposal intended for 0008/0009/0010.
- PF-B1 proposed outputs: boundary_id, direction, breakout_timestamp, confirmation_timestamp, availability_timestamp, status.

## Governance result
No production-frozen decisive-break operator was established in the inspected project evidence.
Therefore PF-B1 cannot be bound as a production evaluator contract yet.

## Explicitly prohibited operationalization
- Do not convert Murphy's 3% example into a mandatory 0008 threshold.
- Do not convert the two-day example into a mandatory 0008 threshold.
- Do not select thresholds from historical replay performance.
- Do not add ATR, pip, arbitrary percentage, arbitrary lookback, or hidden tolerance.
- Do not use 2025 for tuning.

## Decision
0008 remains NOT_EVALUABLE for production implementation until PF-B1 decisive-break governance is explicitly approved from authoritative project evidence.

## Next gate
1. Approve PF-B1 without inventing a threshold, or recover an already-approved compatible contract.
2. Audit PF-H1 compatibility.
3. Only then implement 0008 evaluator/adapter.
4. Run deterministic tests, availability/no-lookahead, and fresh 2016-2024 replay.
5. Keep 2025 OOS.
