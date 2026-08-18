# Nison Hybrid 44 Batch — Run 28 Checkpoint

Date: 2026-08-18
Branch: `feature/nison-hybrid-44-batch-v1`
Parent checkpoint: `3ed89e474fbb17612850e5ee9cd5a3548a89334c`

## Pre-change audit
- Re-read the source-bounded Nison 44-rule workflow and the latest Run 27 checkpoint before any implementation.
- Verified the feature branch still contains the Nison source archive, source inventory/source-map artifacts, Nison contracts, workflows, and audit history.
- Verified the source map remains 44/44 with `count_check=true`; all 44 entries are source-referenced and `NOT_FROZEN` in the source-map layer.
- Verified the inventory keeps all 44 rules as Steve Nison confirmation rules with no assigned evaluator and `NOT_EVALUABLE` at inventory level.

## CI verification
Two workflow runs attached to the Run 27 checkpoint were checked again:
- `Nison 0001-0002 Adapter Gate` run #92: job `tests` (job `95704881989`) completed `failure` with `steps=null`.
- `Nison Hybrid 44 Source Verify` run #107: job `verify-source` (job `95704882055`) completed `failure` with `steps=null`.

Because neither job reports executed steps, these results are not valid evidence of adapter-test failure or source-verification failure. They remain GitHub Actions runner/infrastructure blockers. No blind rerun was issued in Run 28 because repeated zero-step attempts do not create new rule evidence.

## Canonical/main comparison
Compared feature checkpoint `3ed89e474fbb17612850e5ee9cd5a3548a89334c` against canonical Nison freeze commit `84257ada950ccd1ca5fca0357e0aa6f25d4eb8b3`.
- Refs remain diverged; merge base is `2cccec2838d82f806aa1cabe0bdb0ebc66dbb6f3`.
- The canonical-side delta includes the Nison canonical freeze record and the off-branch `bridges/nison_evaluator_to_evidence_bridge.py` plus its tests, but does not prove those artifacts are integrated on the feature branch.
- No merge/cherry-pick was performed.
- `tools/setup-codespace-runner.sh` is also main-side and is not treated as evidence that a runner is registered or targeted by the Nison workflows.

## Current verified counts
- Source inventory / source map: 44/44.
- Source-referenced: 44/44.
- Semantic assessed in source-map layer: 0/44.
- Evaluator assessed in source-map layer: 0/44.
- QA assessed in source-map layer: 0/44.
- Freeze status in source-map layer: 44/44 `NOT_FROZEN`.
- Production Frozen: 0.

## Carried-forward rule statuses
- 0038: structural compatibility PASS; deterministic tests 6/6; historical QA PASS for 2016–2024 calendar-D1 scope; availability/no-lookahead PASS within its stated session-level scope; production freeze remains blocked by governance/upstream sessionization scope.
- 0035–0037: blocked on source-locked qualitative comparator/trend-context requirements.
- 0001/0002/0008/0009/0013: partial existing infrastructure; exact source mapping and compatibility QA remain required.
- 0003–0034: source/contract decomposition and compatible operator mapping remain required where no narrower rule-level proof exists.
- 0039–0041: authoritative methodology/source decomposition remains required for rule-level evaluation.
- 0042–0044: contract-level compatibility exists, but no authoritative producer exists on-branch, so they remain NOT_EVALUABLE.

## Governance
- Nison remains confirmation-only.
- No invented semantics, thresholds, tolerances, lookbacks, scoring, or direction.
- 2025 remains OOS and untouched for tuning, calibration, selection, optimization, or operator choice.
- No auto-freeze.
- No modification to `main`.

## Decision
Do not implement a new S/R/breakout/retest engine and do not promote the off-branch evaluator bridge. Do not treat the main-side canonical freeze or Codespace runner setup as integrated feature-branch evidence. Continue independent rules only where an existing compatible primitive/adapter and authoritative evidence path are proven. The immediate blocker remains a valid GitHub Actions runner execution path; until jobs actually execute, no deterministic QA or source-verification PASS may be claimed.
