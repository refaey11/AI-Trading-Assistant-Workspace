# Nison Hybrid 44 Batch Checkpoint — Run 8

Date: 2026-08-17
Branch: `feature/nison-hybrid-44-batch-v1`
Parent checkpoint: `6d1ad3cff37e252c0c1fcf65c15647a7edf475ac`

## Inspection
- Re-inspected the branch head, Nison 44-rule workflow, source-map implementation, 0001–0002 adapter workflow, and the latest failed workflow runs before making changes.
- Latest recorded CI failures were `Nison Hybrid 44 Source Verify` and `Nison 0001-0002 Adapter Gate`.
- The source workflow contained a hard-coded archive-internal registry path while the source-map implementation also assumed the same fixed root. This was a verifiable infrastructure fragility, not a missing Nison semantic.

## Repair
- Updated `nison_batch/source_map_44.py` to locate `INTEGRATED_RULE_REGISTRY_V1.json` under the extracted archive and derive the source root from the discovered registry.
- Updated `.github/workflows/nison-44-batch.yml` to verify the archive by discovering the registry rather than requiring one fixed internal path.
- No Nison rule semantics, thresholds, tolerances, lookbacks, scoring, direction, or evaluator behavior were added or changed.
- No new upstream primitive was created and no Murphy logic was substituted for Nison evidence.

## Current status
- Nison inventory remains 44/44.
- 0038 remains a structural freeze candidate but is not production-frozen because governance/sessionization scope is incomplete.
- 0035–0037 remain blocked on source-locked qualitative comparators.
- 0039, 0040, 0043, and 0044 remain NOT_EVALUABLE for missing authoritative upstream evidence.
- 0041 remains partial/NOT_EVALUABLE as a full rule because qualitative candle clauses are not deterministically locked.
- 0042 remains candidate-ready but not PASS because canonical S/R provenance and Nison evaluator binding remain unproven.
- 0001–0002 implementation exists; the prior CI gate failed, and the repair in this run does not promote it without a successful deterministic test/gate result.
- No production frozen rules were added in this run.

## Governance
- Nison remains confirmation/evidence only.
- 2025 remains OOS and is excluded from tuning, calibration, selection, optimization, and operator choice.
- No auto-freeze.
- No merge to `main`.
- Missing authoritative evidence remains fail-closed.

## Validation
- The repaired commits are on the Nison feature branch.
- The new branch commits trigger the Nison batch workflow; the workflow result was not yet available at checkpoint creation time, so no PASS is claimed.
