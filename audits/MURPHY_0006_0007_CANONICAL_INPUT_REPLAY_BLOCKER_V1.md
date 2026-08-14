# Murphy 0006/0007 — Canonical Input Replay Blocker V1

Date: 2026-08-14
Status: SUPERSEDED — D1 LINEAGE MISMATCH CLAIM INVALIDATED

## Why this artifact is superseded
The original blocker compared the canonical Pivot V2 first LOW price `1.43519` with the D1 bar low `1.40792` for 2016-01-21 and treated the difference as evidence that the M1-derived D1 was not canonical.

That comparison was invalid: `1.43519` is a Pivot V2 event price, not the D1 bar's low.

## Correct verification
Using the uploaded `GBPUSD_M1_MASTER_2016_2026_V1.zip` and the project D1 reference `d1_ref.csv`:
- aggregate M1 by calendar date,
- Open = first M1 Open,
- High = max M1 High,
- Low = min M1 Low,
- Close = last M1 Close.

For 2,544 common 2016–2024 dates:
- max absolute Open difference = 0
- max absolute High difference = 0
- max absolute Low difference = 0
- max absolute Close difference = 0
- nonzero OHLC differences = 0

For 2016-01-21 specifically, both D1 sources have Low = 1.40792.

## Superseding evidence
See `MURPHY_0006_0007_D1_LINEAGE_RECONCILIATION_V1.md` for the full verification, input hashes, and governance impact.

## Consequence
The D1/M1 lineage mismatch is no longer an open blocker. The existing fresh replay artifact records 0006=8, 0007=7, total=15, with 2025 excluded and lookahead/availability checks enforced.

## Remaining blockers
- formal evaluator integration into the production path,
- governance approval of the operational no-break contract,
- explicit final freeze manifest/decision.

## Guardrails remain
- Do not rebuild Pivot V2.
- Do not rebuild Geometry V1.
- Do not tune 2025.
- Do not introduce 3%, 2-day, ATR, pip, percentage, or hidden lookback thresholds.
- Do not declare production freeze until remaining gates are explicitly evidenced and approved.
