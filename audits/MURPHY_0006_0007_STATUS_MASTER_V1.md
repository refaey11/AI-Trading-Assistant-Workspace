# MURPHY 0006/0007 — STATUS MASTER V1

Date: 2026-08-14
Status: OPEN / NOT PRODUCTION FROZEN

## Purpose
This file is the single status ledger for Murphy 0006/0007 during freeze review. Do not restart investigation from conversation memory. Before changing anything, read this file plus the linked evidence artifacts.

## Canonical facts
- Murphy source semantics: up trendline uses successive reaction lows; down trendline uses successive reaction highs; confirmed trendline requires a third successful touch/reaction without breaking.
- Pivot Sequence V2 is canonical. Do not rebuild it.
- Trendline Geometry V1 is canonical. Do not rebuild it.
- Existing 2016–2024 QA evidence contains 8 provisional 0006 confirmations and 7 provisional 0007 confirmations.
- Existing reconciliation is 15/15 against the existing confirmation artifact.
- Existing QA reports no observed availability/lookahead leakage violations.
- The current no-break numeric predicate is an operationalization, not verbatim Murphy numeric source text.

## Gate ledger
| Gate | Status | Evidence / action |
|---|---|---|
| Murphy qualitative semantics | PASS | Source captures / Chapter 4 evidence |
| Pivot V2 | PASS / CANONICAL | Existing canonical output |
| Geometry V1 | PASS / CANONICAL | Existing canonical output |
| Deterministic candidate operator | AVAILABLE | Existing operator + local tests |
| 2016–2024 QA evidence | PASS AS QA ONLY | 8 + 7 = 15; not freeze |
| Lookahead / availability | PASS AS QA | Existing QA reports zero observed violations |
| Numeric no-break governance | OPEN | Requires explicit project approval |
| Formal contract promotion | OPEN | Candidate contract must be promoted only after governance review |
| Independent canonical E2E | OPEN / NOT PROVEN | Must be independently evidenced from canonical inputs |
| Production freeze | BLOCKED | Cannot close until all open gates pass |

## Data-lineage guardrail
The newly supplied GBPUSD M1 dataset must not be silently mixed with canonical Pivot/Geometry outputs. The current audit has a documented calendar-day aggregation mismatch against a canonical pivot value; therefore the exact canonical D1/session boundary or source artifact must be proven before claiming an independent E2E replay.

## Important correction / anti-regression rule
Do NOT treat conversational claims of a "fresh replay" as evidence. A replay is accepted only when a committed artifact records:
1. exact input hashes/paths,
2. aggregation/session contract,
3. operator version/commit,
4. execution command or reproducible runner,
5. output counts and case IDs,
6. comparison result,
7. no-lookahead result.

If those items are not present, the run remains UNPROVEN regardless of what a chat message says.

## Prohibited shortcuts
- No tuning on 2025. 2025 is OOS and must remain untouched for tuning/operator selection.
- No 3%, 2-consecutive-close, ATR, pip, arbitrary percentage, hidden lookback, or tolerance threshold unless explicitly source-approved for this rule.
- No rebuilding existing Pivot V2 or Geometry V1.
- No promotion from 15/15 reconciliation alone.

## Exact next sequence
1. Recover/prove canonical D1/session aggregation lineage.
2. Freeze the input manifest and hashes.
3. Run independent canonical E2E using canonical Pivot V2 + Geometry V1 and the approved operator.
4. Produce machine-readable replay report with case IDs, counts, mismatches, and leakage checks.
5. Complete numeric no-break governance review.
6. Promote the formal contract only if governance approves it.
7. Create final Freeze Manifest only after every gate is PASS.
8. Once frozen, mark 0006/0007 CLOSED and move to the next unresolved Murphy module; do not reopen without a documented change request.

## Required artifact set before freeze
- `MURPHY_0006_0007_STATUS_MASTER_V1.md` (this file)
- Governance gate document
- Canonical input manifest + hashes
- Operator source/contract + version
- Independent replay report
- No-lookahead report
- Final freeze manifest
- Decision/change log

## What can unblock the project
The most useful user-supplied artifact is the original project ZIP/workspace that contains the canonical D1 construction/source lineage, if it exists. Otherwise, the next useful artifact is any saved script/config/manifest that defines M1→D1 session boundary/timezone/aggregation.
