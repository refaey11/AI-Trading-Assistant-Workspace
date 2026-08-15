# Murphy 0028 — Continuity / Problems & Solutions / Backup

Date: 2026-08-15
Status: **PRODUCTION FROZEN**

## Purpose
This file is the continuity handoff for Murphy 0028. It is intended to prevent repeated audits, accidental rebuilding, contradictory status reports, or loss of the problem/solution history.

## Final canonical state
- Rule: MURPHY_0028
- Status: PRODUCTION FROZEN
- Frozen: 2026-08-15
- Freeze commit: `79ddf163e91101e168825c086deba47beaf556e9`
- Canonical status commit: `ea950b5e9d1dc24c505bad067bb633d79a1236df`
- Frozen-rule count after this freeze: 11/51
- Next active candidate: 0029

## Problem we found
0028 already had the rule semantics, evaluator, bridge, Pivot Sequence V2, and 2020–2024 RSI divergence evidence. The missing historical piece was authoritative RSI(14) producer/artifact coverage for 2016–2019.

## Why we did NOT rebuild 0028
Project governance requires existing components to be audited and integrated rather than silently rebuilt. Rebuilding the rule/evaluator/divergence detector would have risked semantic drift and would have required repeating already completed work.

## Solution used
1. Preserve the existing 0028 rule semantics and evaluator.
2. Preserve the existing OSCILLATOR_DIVERGENCE_V1 contract and PIVOT_SEQUENCE_V2.
3. Reproduce Wilder RSI(14) from the canonical OHLC already available in the workspace.
4. Reverse-validate the RSI reproduction against the existing 2020–2024 divergence artifact.
5. The reverse validation matched the existing RSI values to numerical precision and preserved the existing divergence pairing/availability behavior.
6. Extend the same proven RSI implementation to 2016–2019.
7. Apply the existing divergence semantics to the recovered historical period.
8. Combine 2016–2019 with the existing 2020–2024 evidence.
9. Execute full 2016–2024 Historical QA.
10. Execute integrated availability/no-lookahead checks.
11. Record final provenance.
12. Freeze 0028 in the canonical project state.

## Final evidence / QA
- Total divergence events: 5,819
- 2016–2019 recovered events: 2,583
- 2020–2024 existing events: 3,236
- 0028 PASS: 2,889
- 0028 FAIL: 2,930
- Duplicate events: 0
- Missing availability: 0
- Availability before Pivot 1: 0
- Availability before Pivot 2: 0
- 2025 rows: 0
- Out-of-scope rows: 0
- Nonconforming 0028 labels: 0

## Artifacts created
- `project_state/MURPHY_0028_PRODUCTION_FREEZE_V1.md`
- `project_state/MURPHY_0028_FINAL_PROVENANCE_V1.json`
- `project_state/MURPHY_0028_CONTINUITY_BACKUP_V1.md`
- Local recovery/evidence files created during the audit:
  - `MURPHY_0028_RSI_DIVERGENCE_CONTROLLED_RECOVERY_V1.json`
  - `MURPHY_0028_RSI_14_REVERSE_VALIDATION_AND_RECOVERY_V1.json`
  - `MURPHY_0028_RSI_DIVERGENCE_2016_2019_RECOVERED_V1.csv`
  - `MURPHY_0028_RSI_DIVERGENCE_2016_2024_COMBINED_RECOVERY_V1.csv`
  - `MURPHY_0028_FULL_HISTORICAL_QA_2016_2024_V1.json`
  - `MURPHY_0028_FREEZE_CANDIDATE_MANIFEST_V1.json`
  - `MURPHY_0028_CONTINUITY_BACKUP_V1.json`

## Do not repeat / do not reopen
- Do not redo the RSI source-recovery search unless new contradictory evidence appears.
- Do not rebuild 0028.
- Do not rebuild the divergence detector.
- Do not modify evaluator semantics.
- Do not tune or select using 2025.
- Do not introduce new thresholds, tolerances, timeframes, lookbacks, or proxies.
- Do not downgrade the frozen state because of an older snapshot/status file.
- Any semantic change to frozen 0028 requires a new compatibility audit and a new freeze.

## Handoff rule
0028 is closed. Future work should continue from this recorded state. The next rule to work on is 0029; 0028 should be treated as an immutable frozen dependency/evidence module unless a formally approved change is initiated.
