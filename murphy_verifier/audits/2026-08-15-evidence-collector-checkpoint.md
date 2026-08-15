# Murphy Verifier — Evidence Collector Checkpoint — 2026-08-15

## Scope

Built the first repository evidence-collection layer on `feature/murphy-state-verifier` without changing `main` or any protected Rule implementation artifact.

## Implemented

- `tools/murphy_evidence_collector.py`
  - scans Git commit history for Rule-scoped evidence;
  - extracts traceable commit SHA and commit timestamp;
  - scans explicitly supplied artifacts;
  - uses the artifact's last committed SHA/time instead of filesystem mtime;
  - normalizes `COMPLETED` to `FROZEN` only as a status label, without inventing semantics;
  - emits normalized `EvidenceRecord` objects consumed by the reducer.
- `tools/murphy_evidence_chain.py`
  - normalized evidence metadata fields for artifact/OOS/future-data provenance;
  - hard-blocks forbidden 2025 OOS use and future-data contamination;
  - continues to require explicit supersession/closure for stale claims/blockers.
- `tests/test_murphy_evidence_collector.py`
  - deterministic history extraction;
  - four-digit Rule ID boundary handling;
  - tracked-artifact timestamp provenance;
  - rejection of non-Rule numbers.
- `.github/workflows/murphy-state-verifier-tests.yml`
  - CI definition for verifier, reducer, and collector tests.

## Code-level audit findings fixed before checkpoint

1. The first collector draft used an incorrect Rule-ID regex that could miss IDs such as `0025`; corrected to the four-digit `0001`–`0051` range.
2. The first collector draft duplicated an `EvidenceRecord` schema that diverged from the reducer; collector and reducer are now normalized to one record type.
3. Artifact timestamps originally used filesystem mtime; this was replaced with the artifact's last committed Git timestamp to keep provenance deterministic.

## Validation status

GitHub returned no workflow-run records for the latest feature-branch commit at checkpoint time, so CI PASS is **not claimed**. The test workflow is now present and scoped to the verifier/reducer/collector files; it will provide the authoritative CI result when GitHub executes it.

A local execution could not be performed in this environment because direct network cloning of the repository is unavailable. This is recorded as an environment limitation, not a test pass.

## Protected scope

- 0003, 0004, 0006, 0007, 0008, 0021, 0022, 0023, 0025, 0026 remain excluded from implementation changes.
- 0021–0023 retain the explicit `FREEZES/MURPHY_0021_0023_FROZEN_SNAPSHOT_V1_2026-08-15.md` evidence on `main`.
- No 2025 OOS data was used for tuning, threshold selection, calibration, feature selection, rule changes, or optimization.

## Reconciliation status

0006/0007 remain a scope conflict in the verifier until repository evidence explicitly reconciles evaluator/evidence freeze with production freeze. The verifier must not collapse that conflict into unconditional production `FROZEN`.

## Next checkpoint

Use the collector against the complete repository evidence surface (Git history, `FREEZES`, `PROJECT_STATUS_*`, `audits`, `project_state`, and relevant PR-linked artifacts), normalize records for all 51 Rules, then run the reducer per Rule. Do not invent Rule semantics or promote a Rule from evidence-only status to evaluable/frozen without the required contracts and gates.
