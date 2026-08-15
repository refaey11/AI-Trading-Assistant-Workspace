# Murphy 0008 — Replay Status Correction V1

Status: CORRECTIVE AUDIT RECORD

## Purpose
Preserve a truthful separation between an experimental replay claim and the authoritative production-validation state.

## Authoritative project state
The uploaded 0008 handoff remains controlling: PF-B1 is PROPOSAL / NOT FROZEN; PF-H1 is PROPOSAL / NOT FROZEN; the decisive-break operator is NOT APPROVED; the 0008 evaluator is NOT BUILT / NOT FROZEN; 2016–2024 QA is PENDING; 2025 is OOS; freeze is BLOCKED.

## Replay interpretation
Prior conversational messages reported a two-day replay result. That result must be treated as EXPERIMENTAL / NON-AUTHORITATIVE until it is independently reproducible from the authoritative dataset and an approved PF-B1 contract, with event-level provenance and no-lookahead evidence.

The reported counts must NOT be promoted to production QA, freeze evidence, profitability evidence, or governance approval.

## Why
The project handoff explicitly prohibits automatically binding Murphy's two-day example to 0008 and requires explicit governance approval before PF-B1 can be used by the production evaluator. It also requires a fresh 2016–2024 replay independent of reference-result artifacts.

## Next executable gate
1. Explicitly approve the candidate TIME_FILTER policy as project operationalization, or retain NOT_EVALUABLE.
2. Freeze PF-B1 only after deterministic contract review.
3. Audit/close PF-H1 without inventing a tolerance.
4. Run fresh event-level 2016–2024 QA from authoritative OHLC + PIVOT_SEQUENCE_V2.
5. Run availability/no-lookahead and role-reversal tests.
6. Create provenance/evidence backup.
7. Freeze 0008 only after all gates pass.

## 2025
2025 remains strictly OOS and must not be used for operator selection or tuning.
