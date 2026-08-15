# Murphy Verifier — Repository Surface Collector V2 — 2026-08-15

## Result

The evidence collector was expanded on `feature/murphy-state-verifier` to cover the known repository evidence surface without scanning data payloads as evidence.

## Evidence surface

The collector now deterministically expands these roots/files by default:
- `FREEZES/`
- `PROJECT_INDEX/`
- `audits/`
- `project_state/`
- `PROJECT_STATUS_CURRENT_2026-08-12.md`
- `PROJECT_STATUS_CURRENT_2026-08-13.md`

Only text-like tracked artifacts (`.md`, `.json`, `.yaml`, `.yml`, `.txt`, `.csv`) are read. `data/` is deliberately not part of the default evidence roots, so market datasets cannot silently become status evidence.

Artifact provenance uses the last Git commit SHA/time for the tracked path; filesystem mtime is never used.

## Rule handling

- Rule IDs are constrained to the exact `0001`–`0051` range.
- `COMPLETED` is normalized to `FROZEN` only as a status label; no semantics are inferred.
- Git commit history remains a separate evidence stream from artifact text.
- The collector does not manufacture `supersedes`, blocker closure, freeze, or production scope facts. Those require explicit traceable evidence for the reducer.

## Tests added

`tests/test_murphy_evidence_collector.py` now covers:
- deterministic Git history extraction;
- four-digit Rule-ID handling;
- Git timestamp provenance;
- repository-surface expansion;
- exclusion of unrelated/non-Rule numeric data and the `data/` tree from default surface collection.

## CI status

The verifier workflow exists on the feature branch, but GitHub returned no workflow-run records for the latest collector test commit at checkpoint time. Therefore **CI PASS is not claimed**. This is an execution/status limitation, not a successful test result.

## Reconciliation

`main` still contains `PROJECT_STATUS_CURRENT_2026-08-13.md`, which explicitly keeps 0006/0007 at `NOT_EVALUABLE / OPERATIONAL GATE OPEN`. Repository commit search also found later 0006-related fixture/compatibility commits but no commit search result that establishes an unconditional production freeze. The verifier therefore must not promote 0006/0007 to Production Frozen from chat claims or evaluator-level evidence alone.

The protected rules remain excluded from implementation changes. 0021–0023, 0025–0026, 0003–0004, and the other requested protected set are not modified by this collector work.

2025 remains OOS and is not used for tuning, threshold selection, calibration, feature selection, rule changes, or optimization.

## Next checkpoint

Run the repository-surface collector/reducer against the complete checkout and produce a 51-row machine-readable state report, with each row linked to its evidence commits/artifacts. Do not infer missing evidence. Any contradictory authoritative state must remain `CONFLICT`; any insufficient evidence must remain `UNVERIFIED`/`NOT_EVALUABLE` at the project layer.
