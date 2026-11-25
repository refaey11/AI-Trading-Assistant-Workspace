# Murphy 0006/0007 — Knowledge Alignment Provider Compatibility Audit

Date: 2026-11-25
Scope: read-only compatibility audit; no runtime changes.

## Canonical status checked

`project_state/MURPHY_0006_0007_CURRENT_CANONICAL_STATUS_2026-08-15.md` is the current canonical status record. It states that 0006/0007 are COMPLETED / FROZEN at evaluator + Decision-Brain-evidence level, with:
- 2016-2024 replay: 0006 = 8, 0007 = 7, total = 15;
- reconciliation: 15/15;
- availability/no-lookahead: PASS;
- deterministic test evidence: 4 passed in the final completion record;
- 2025 excluded.

This does not mean the entire live Decision Brain is complete, nor that the rules are wired into the active runtime provider.

## Existing evaluator output

`runtime/murphy/murphy_0006_0008_runtime_v1.py` and `MURPHY_EVALUATORS_V1/murphy_0006_0007_runtime_v1.py` expose:
- `rule_id`;
- `status` (`CONFIRMED` or `NOT_EVALUABLE`);
- `direction` (`BULLISH` / `BEARISH` when confirmed);
- `third_touch_timestamp`;
- `confirmed_at`.

The evaluator test file covers 0006/0007 confirmed direction, lookahead rejection, missing evidence, and invalid candidate handling. This is evaluator-level evidence, not the complete Knowledge Alignment provider envelope.

## Existing candidate adapter is a different contract

`src/murphy_0006_0007/evidence_adapter.py` deliberately emits `evidence_status=CANDIDATE_ONLY`. Its contract forbids production PASS/FAIL and preserves touch/reaction/no-break observations without promoting them.

The current `.github/workflows/0006-0007-deterministic-audit.yml` runs `tests/test_murphy_0006_0007_evidence_adapter.py`; it does not invoke `MURPHY_EVALUATORS_V1/test_murphy_0006_0007_runtime_v1.py`. Therefore this workflow's success would validate the candidate adapter only, not the frozen evaluator.

## Knowledge Alignment provider requirement

The recovered Knowledge Alignment Adapter contract expects frozen Murphy evidence with the provider fields:
- `available=true`;
- `frozen=true`;
- `direction=bullish|bearish`;
- `source_rule_id=MURPHY_0006|MURPHY_0007`.

The evaluator output uses `status=CONFIRMED` and `direction`, but does not itself emit the complete provider record or establish the provider's `available` and `frozen` fields.

No explicit, approved mapping from evaluator `CONFIRMED` to provider `available=true, frozen=true` was found in the active repository artifacts inspected here. The candidate adapter cannot supply this mapping because it explicitly remains `CANDIDATE_ONLY`.

## Decision

- Preserve the canonical evaluator freeze; do not downgrade 0006/0007 to generic NOT_EVALUABLE based on older audit snapshots.
- Do not fabricate `available=true` or `frozen=true`.
- Do not convert the candidate adapter's CANDIDATE_ONLY output into provider evidence.
- Do not change Murphy rule semantics, MTF, Nison, Risk, or the live runtime in this audit.

## Required next gate

Recover the exact approved Knowledge Alignment provider mapping/closure record from the original milestone source, or obtain explicit governance approval for a versioned adapter contract that maps the frozen evaluator output to the provider schema.

After that contract is source-locked:
1. implement the smallest provider adapter on a separate branch;
2. test exact rule ID, CONFIRMED status, direction binding, availability timestamp, and frozen provenance;
3. test that missing, conflicting, NOT_EVALUABLE, or candidate-only evidence fails closed;
4. prove the active runtime consumes that provider record without allowing Nison, MTF, Volume, Similarity, or Brain context to create Murphy direction.

No 2025 data may be used for tuning, calibration, or selection.
