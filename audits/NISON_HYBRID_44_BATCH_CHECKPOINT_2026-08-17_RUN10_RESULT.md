# Nison Hybrid 44-Rule Batch — Run 10 Result

Date: 2026-08-17
Branch: `feature/nison-hybrid-44-batch-v1`
Base checkpoint: `c0e97080fe6394c06e463b9188debb16c009f0ee`
Run 10 audit commit: `0ed7c4c6ab6553e03d1bf5cc4b3309843b053baa`

## Rerun outcomes
- Nison 44 Rule Batch Run #9 inventory rerun: **FAIL**. New rerun job: `95367216350`. GitHub logs remain unavailable (`BlobNotFound`), so the underlying failure cause is not inferred.
- Nison 0001–0002 Adapter Gate rerun: **FAIL**. New rerun job: `95367257186`.

## Governance outcome
- No gate is promoted to PASS from these reruns.
- No rule is frozen.
- 44/44 rules remain in inventory; unsupported/blocked rules remain fail-closed.
- Nison remains confirmation-only.
- 2025 remains OOS and is not used for tuning, calibration, selection, optimization, or operator choice.
- `main` is untouched.
- No new Nison semantics, thresholds, tolerances, lookbacks, scoring, or direction were introduced.

## Next action
Do not blindly repeat the same reruns. The next execution should inspect the workflow implementation and the 0001–0002 gate for a deterministic, source-backed failure cause that can be repaired without changing Nison semantics, then rerun the affected gate only. Continue independent rules whose own evidence/compatibility chain is already sufficient.
