# Fresh Murphy 0021 Progress — 2026-08-23

## Milestone completed
- PR #44 (current 78-rule coverage report) was merged into main with merge commit `2d3f58bbc9eb7c57de36591a5f9dab8b34092ab5` after its CircleCI coverage job passed.
- Fresh Murphy compatibility audit was completed before any fresh producer work.
- Existing Murphy 0021 evaluator semantics were identified as the first clean fresh-production candidate.
- Existing volume semantics are reused: `volume_direction` compares the current completed bar volume with the previous completed bar. No new threshold is introduced.
- MURPHY_0022/0023 remain blocked on approved futures open-interest evidence and are not proxied.

## Current PR
- PR #45: `OOS: fresh Murphy 0021 2025 producer integration`
- Branch: `oos-2025-murphy-0021-fresh-v1`
- Head commit: `b663dd76f42cf313df488354841d9b6380ec6b25`
- Fresh producer job: `murphy_0021_2025_fresh_v1`
- Current CI state: baseline checks are green; `murphy_0021_2025_fresh_v1` and the dependent full-production/coverage jobs are pending.

## Governance
- 2025 remains OOS.
- No tuning, calibration, threshold selection, or source-semantic changes.
- Fresh 0021 run is evidence/producer validation only, not profitability.
- Missing upstream evidence remains NOT_EVALUABLE.

## Next checkpoint
After PR #45 CI completes, record the actual fresh 2025 0021 manifest (row count, PASS/FAIL/NOT_EVALUABLE) in both GitHub and Dropbox before starting the next Murphy rule group.
