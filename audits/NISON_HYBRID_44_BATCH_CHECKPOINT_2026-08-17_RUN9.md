# Nison Hybrid 44 Batch Checkpoint — Run 9

Date: 2026-08-17
Branch: `feature/nison-hybrid-44-batch-v1`
Parent checkpoint: `63c43dd0760e9592bf7bcd531c7c08a6650b6cb1`

## Inspection
- Re-inspected the Nison 44 workflow, source-map implementation, inventory runner, current-gate audit, and Run 8 failure before changing implementation.
- Run 8 attempt 2 failed in the `inventory` job before any rule processing; the source verification repair had not fixed the inventory runner's own fixed registry path.

## Repair
- Updated `nison_batch/run_nison_44_inventory.py` to discover `INTEGRATED_RULE_REGISTRY_V1.json` under the extracted source tree instead of assuming one archive-internal path.
- No Nison semantics, thresholds, tolerances, lookbacks, scoring, direction, evaluator behavior, or rule definitions were changed.
- No new upstream primitive was created and no Murphy logic was substituted for Nison evidence.

## Validation state
- Repair commit: `3d09e2e06b8d60f358a064f663275e2f4f5a300b`
- Nison 44 Rule Batch Run #9 is queued on the repaired commit; no PASS is claimed until the workflow completes.
- Previous Run 8 failure remains recorded and is not overwritten.

## Current rule state carried forward
- Inventory target: 44/44 Nison confirmation rules.
- 0038 remains a structural freeze candidate, not production-frozen.
- 0035–0037 remain blocked on source-locked qualitative comparators.
- 0039, 0040, 0043, and 0044 remain NOT_EVALUABLE for missing authoritative upstream evidence.
- 0041 remains partial/NOT_EVALUABLE as a full rule because qualitative candle clauses are not deterministically locked.
- 0042 remains candidate-ready but not PASS because canonical S/R provenance and Nison evaluator binding remain unproven.
- 0001–0002 remain gated until deterministic CI closure is actually observed.

## Governance
- Nison remains confirmation/evidence only.
- 2025 remains OOS and is excluded from tuning, calibration, selection, optimization, and operator choice.
- No auto-freeze.
- No merge to `main`.
- Missing authoritative evidence remains fail-closed.

## Next action
- Complete Run 9 from inventory through source mapping and governance. If those gates pass, continue independently into compatibility/evaluator/availability/no-lookahead/deterministic QA/historical QA for rules with evidenced compatible assets. Keep unsupported rules NOT_EVALUABLE rather than inventing semantics.
