# MURPHY 0006/0007 — D1 LINEAGE RECONCILIATION V1

Date: 2026-08-14
Status: VERIFIED FOR THE AVAILABLE ARTIFACTS

## Discovery
The previously stated claim that calendar-date M1 aggregation reproduced the project D1 is supported by an existing machine-readable replay artifact and by an independent local recomputation from the uploaded files.

## Inputs
- M1 source: `GBPUSD_M1_MASTER_2016_2026_V1.zip`
- Canonical/reference D1: `/mnt/data/d1_ref.csv`
- Existing replay report: `murphy_0006_0007_FRESH_REPLAY_2016_2024_V1.json`
- Existing replay case list: `murphy_0006_0007_FRESH_REPLAY_2016_2024_V1.csv`

SHA-256:
- M1 ZIP: `edb39db9c91dcfd2f3b5b11fa25734810d50cf501be37555d5ec9951715d8202`
- D1 reference: `c3d415c65887d1133e8b645c8d5c7473f4d2e2f6426361216b6908b75aad34c8`
- Fresh replay JSON: `6606b597fe5272d6c8833d2392b06ca74409289cc028419d2e57d4b76c942fdd`
- Fresh replay CSV: `3afb1edacf2ef0683096f869ce393732772fad415e5b1511537a0ab13c235c20`

## Exact reconstruction tested
For each calendar date in the common 2016–2024 range:
- Open = first M1 open of the date
- High = maximum M1 high of the date
- Low = minimum M1 low of the date
- Close = last M1 close of the date

Result:
- Common dates: 2,544
- Open max absolute difference: 0
- High max absolute difference: 0
- Low max absolute difference: 0
- Close max absolute difference: 0
- Nonzero OHLC differences: 0

Spot check:
- 2016-01-21 D1 low = 1.40792 in both the M1-derived D1 and `d1_ref.csv`.

## Important correction
The earlier blocker statement that compared the canonical Pivot V2 first LOW price `1.43519` against the D1 low `1.40792` was a category error: `1.43519` is a Pivot V2 event price, not the D1 bar's low. It cannot be used to disprove D1 lineage.

Therefore the documented `MURPHY_0006_0007_CANONICAL_INPUT_REPLAY_BLOCKER_V1.md` conclusion about a D1 lineage mismatch is superseded by this verified reconciliation.

## Existing fresh replay evidence
`murphy_0006_0007_FRESH_REPLAY_2016_2024_V1.json` records:
- status: `FRESH_REPLAY_PASS`
- D1 reconstruction: calendar-date M1 OHLC aggregation
- 2,544 common dates, max absolute OHLC difference 0
- canonical Pivot V2 reused
- canonical Geometry V1 reused
- period 2016–2024
- 2025 not used
- result: 0006 = 8, 0007 = 7, total = 15
- availability ordering enforced
- reaction strictly after touch
- confirmation available at reaction availability
- reference artifact not read by the fresh run

## Governance impact
D1/M1 lineage is no longer an open blocker for 0006/0007 based on the available artifacts.
Remaining freeze gates are:
1. formal evaluator integration into the production path,
2. governance approval of the operational no-break contract,
3. explicit final freeze manifest/decision.

No production freeze is declared by this artifact alone.
