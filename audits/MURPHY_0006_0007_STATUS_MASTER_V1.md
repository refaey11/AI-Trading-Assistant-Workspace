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

## Verified discovery — D1 lineage CLOSED
A machine-readable fresh replay artifact exists and an independent local recomputation confirms the following:
- Source M1: `GBPUSD_M1_MASTER_2016_2026_V1.zip`
- D1 reconstruction: calendar-date OHLC aggregation (first Open, max High, min Low, last Close)
- Common 2016–2024 dates: 2,544
- Max absolute OHLC difference against `d1_ref.csv`: 0 for Open/High/Low/Close
- Nonzero OHLC differences: 0
- 2016-01-21 D1 Low is 1.40792 in both sources
- Existing replay JSON records `FRESH_REPLAY_PASS`, 0006=8, 0007=7, total=15, 2025=false, and reference artifact not read

Important correction: the prior blocker that compared Pivot V2 first LOW price `1.43519` with D1 low `1.40792` was invalid because `1.43519` is a Pivot event price, not the D1 bar low. That blocker is superseded by `MURPHY_0006_0007_D1_LINEAGE_RECONCILIATION_V1.md`.

## Verified discovery — Geometry V1 schema CLOSED
Direct inspection of the reconstructed canonical workspace proved:
- Geometry input is `PIVOT_SEQUENCE_V2`.
- Geometry connects consecutive pivots of the same type only.
- Slope is exact price change divided by elapsed seconds.
- Line availability is the later confirmation timestamp of the two defining pivots.
- Pattern classification and breakout detection are explicitly excluded.
- No thresholds are added; 2025 is not used; a line cannot be available before both defining pivots are confirmed.
- D1 Geometry output contains `line_id`, `line_type`, two anchor timestamps/prices, slope, direction, availability timestamps, and source file.
- Canonical D1 Geometry output has 806 lines.
- Geometry QA reports slope, availability, chronology, type, and no-2025 checks as true for the D1 output.

Interpretation: Geometry V1 is an upstream geometry primitive, not the Murphy confirmation detector. It intentionally does NOT emit third-touch/reaction/no-break fields. Those belong to the separate Murphy Confirmation Layer/operator. Therefore the earlier Geometry-schema blocker is CLOSED/SUPERSEDED.

## Gate ledger
| Gate | Status | Evidence / action |
|---|---|---|
| Murphy qualitative semantics | PASS | Source captures / Chapter 4 evidence |
| Pivot V2 | PASS / CANONICAL | Existing canonical output |
| Geometry V1 | PASS / CANONICAL | Direct artifact/schema audit |
| D1/M1 lineage | PASS / VERIFIED | D1 lineage reconciliation artifact |
| Deterministic candidate operator | AVAILABLE | Existing operator + local tests |
| 2016–2024 QA evidence | PASS AS QA ONLY | 8 + 7 = 15; not freeze |
| Lookahead / availability | PASS AS QA | Existing QA + fresh replay evidence |
| Numeric no-break governance | OPEN | Requires explicit project approval |
| Formal evaluator integration | OPEN | Production-path integration still required |
| Independent canonical E2E | PASS AS ARTIFACT | Fresh replay artifact records PASS; preserve hashes and provenance |
| Production freeze | BLOCKED | Cannot close until remaining open gates pass |

## Fresh replay acceptance rule
A replay is accepted as evidence only when a committed artifact records:
1. exact input hashes/paths,
2. aggregation/session contract,
3. operator version/commit,
4. reproducible execution provenance,
5. output counts and case IDs,
6. comparison result,
7. no-lookahead result.

The verified replay JSON plus the D1 lineage reconciliation satisfy the evidence requirements for the D1 lineage and replay result. Do not replace them with conversational claims.

## Prohibited shortcuts
- No tuning on 2025. 2025 is OOS and must remain untouched for tuning/operator selection.
- No 3%, 2-consecutive-close, ATR, pip, arbitrary percentage, hidden lookback, or tolerance threshold unless explicitly source-approved for this rule.
- No rebuilding existing Pivot V2 or Geometry V1.
- No promotion from 15/15 reconciliation alone.

## Exact next sequence
1. Complete numeric no-break governance review against Murphy source semantics.
2. Confirm/formalize evaluator integration into the production path without changing rule behavior.
3. Run/record final production-path validation against the frozen evidence.
4. Create explicit final Freeze Manifest and decision.
5. Once frozen, mark 0006/0007 CLOSED and move to the next unresolved Murphy module; do not reopen without a documented change request.

## Required artifact set before freeze
- `MURPHY_0006_0007_STATUS_MASTER_V1.md` (this file)
- Governance gate document
- `MURPHY_0006_0007_D1_LINEAGE_RECONCILIATION_V1.md`
- Canonical input manifest + hashes
- Geometry V1 build contract/manifest/QA artifacts
- Operator source/contract + version
- Fresh replay report
- No-lookahead report
- Final freeze manifest
- Decision/change log

## What can unblock the remaining gates
The most useful user-supplied artifact now is NOT another D1 or Geometry file. If available, provide the exact production-path evaluator integration file or the final governance approval artifact for the no-break contract. Otherwise no user action is required; the remaining work is audit/integration/governance work.
