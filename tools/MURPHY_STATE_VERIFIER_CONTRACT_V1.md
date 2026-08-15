# Murphy State Verifier Contract V1

## Purpose

Provide a deterministic, evidence-first way to classify Murphy Rules without relying on chat memory, a single handoff, or an unverified status claim.

## Source-of-truth order

1. Git history and traceable repository artifacts.
2. Explicit freeze/QA/evidence records in the repository.
3. Canonical project state, reconciled against the evidence chain.
4. Chat claims are signals for investigation only, never proof.

## States

- `FROZEN`: explicit production-freeze evidence, freeze manifest, and canonical frozen state are all proven.
- `QA_COMPLETE`: tests, historical QA, and no-lookahead evidence pass, but production freeze is not proven.
- `TECHNICALLY_COMPLETE`: implementation and compatibility evidence exist, but required QA/freeze evidence is incomplete.
- `INTEGRATION_PENDING`: freeze evidence exists but the complete production-freeze proof is incomplete.
- `BLOCKED`: a current, evidence-backed blocker is present.
- `UNVERIFIED`: evidence is insufficient to classify the rule.
- `CONFLICT`: independently traceable evidence asserts incompatible states and no later reconciliation resolves the conflict.

## Mandatory guardrails

- Never downgrade a frozen rule because of an older handoff or chat memory.
- Never upgrade a rule because of a chat claim alone.
- A later closure commit supersedes an older blocker only when the closure is traceable and satisfies the relevant gate.
- 2025 remains OOS and must not be used for tuning, calibration, threshold selection, feature selection, or optimization.
- Reject evidence with future-data/lookahead contamination.
- Before any new integration, require a compatibility audit against existing contracts and reuse existing artifacts.
- Murphy remains technical context/market-structure evidence; this verifier does not make trading decisions.

## Freeze protection

The verifier must treat a rule recorded as frozen as protected. A proposed regression requires an explicit governed change/revalidation path and must never silently rewrite the frozen state.

## Required evidence record per rule

`rule_id`, `state_assertions`, `implementation`, `tests_pass`, `historical_qa`, `no_lookahead`, `compatibility_audit`, `blocker_open`, `blocker_closed`, `freeze_manifest`, `frozen_snapshot`, `production_freeze`, `merged_main`, `canonical_frozen`, `oos_2025_clean`, and the commit/file references supporting each field.

## Conservative rule

If evidence is missing, ambiguous, stale, or contradictory: do not guess. Return `UNVERIFIED` or `CONFLICT` and identify the exact evidence required to resolve it.
