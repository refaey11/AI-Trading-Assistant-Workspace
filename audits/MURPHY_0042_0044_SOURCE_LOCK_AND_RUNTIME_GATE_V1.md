# Murphy 0042–0044 Source Lock + Runtime Gate V1

Status: SOURCE/SEMANTICS RESOLVED — RUNTIME FREEZE PENDING
Date: 2026-08-17

## Authoritative source reconciliation
The current Master KB and the independent MT5 Pro AI archive impact audit agree on Chapter 16 semantics:

- 0042 — Capital reserve: total investment must not exceed 50% of available capital. Source note: guideline, not universal law.
- 0043 — Single-market exposure: total entry into a single market is limited to 10%–15% of total capital.
- 0044 — Maximum risk per market: risk exposure in a single market is limited to 5% of total capital.

The same Chapter 16 statements are independently present in the uploaded MT5 archives. Provenance is therefore resolved.

## Rule-specific operational boundary
No lower-bound violation is inferred for 0043. The source gives a range, not a single project threshold. The safe source-faithful interpretation is:
- exposure above 15%: hard FAIL;
- exposure within 10%–15%: compatible with source guideline;
- exposure below 10%: not automatically a violation; requires explicit project policy if the project wants to treat it specially.

0042:
- total investment above 50%: hard FAIL;
- at or below 50%: compatible with the source ceiling.

0044:
- single-market risk above 5%: hard FAIL;
- at or below 5%: compatible with the source ceiling.

These are source-boundary translations, not claims that Murphy supplied a software PASS/FAIL implementation.

## Runtime gate
Existing Risk Engine remains authoritative. Rule Adapter only normalizes the rule result.

Input contract:
- rule_id
- authoritative risk evidence
- risk_available
- risk_status = PASS | FAIL | NOT_EVALUABLE
- source metadata
- availability timestamp

Output:
- module = murphy_risk
- source_rule_id = 0042/0043/0044
- available
- gate = pass | fail | needs_review
- conflict = neutral | insufficient
- source-backed statement

Missing evidence => NOT_EVALUABLE / needs_review. Never infer PASS from missing fields.
Risk FAIL is a hard execution blocker and cannot be overridden by Murphy/Nison/Similarity support.

## Current verified state
- Source/provenance: PASS
- Semantics: PASS
- Existing Risk Gate Adapter contract: PASS as shared interface
- Rule-specific runtime field mapping: NOT YET PROVEN from the accessible Risk Engine implementation
- Deterministic rule evaluator: NOT FROZEN
- Historical QA: NOT RUN
- Availability/leakage audit: NOT RUN
- Production freeze: NOT READY

## Do not do
- Do not rebuild Risk Engine.
- Do not invent a position-size formula.
- Do not convert the 10–15% source range into a single arbitrary number.
- Do not use 2025 for tuning or operator selection.
- Do not mark the rules frozen merely because adapter unit tests pass.

## Next smallest action
Locate the actual Risk Engine runtime output fields for capital, single-market exposure, market risk, and margin. Map those fields to 0042–0044, then run deterministic PASS/FAIL/NOT_EVALUABLE tests and the applicable historical QA. If the runtime fields are absent, the correct result is NOT_EVALUABLE and a minimal integration contract—not an invented engine.
