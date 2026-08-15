# Murphy 0028 — Source-Locked Bridge Gate V1

Date: 2026-08-15
Status: BRIDGE IMPLEMENTED / DETERMINISTIC TESTS PASS / PRODUCTION FREEZE NOT GRANTED

## Scope

This gate adds only the missing evaluator-to-Decision-Brain evidence bridge for Murphy 0028.
It does not rebuild the divergence detector, alter the existing evaluator, add thresholds, tune historical results, or make a trade decision.

## Source/project basis

The existing workspace evaluator contract records:
- 0028 = PASS only on confirmed BEARISH divergence at a HIGH pivot.
- Existing Pivot Sequence V2 + RSI_14 + confirmed divergence artifacts are consumed.
- The evaluator consumes pre-confirmed divergence evidence; it does not rebuild the detector.
- Divergence `availability_timestamp` is the lookahead-control evidence.
- `2025_used = false`.

The evaluator emits:
- PASS + `BEARISH_WARNING` for confirmed bearish divergence at a HIGH pivot.
- FAIL + `NONE` for the wrong divergence/pivot combination.
- NOT_EVALUABLE when required divergence evidence is missing.

## Adapter contract mapping

The new bridge maps the existing evaluator output into the project's Rule Adapter fields:
- module = `murphy_context`
- statement = canonical 0028 statement
- direction = bearish only when the evaluator status is PASS and the evaluator emits bearish confirmation
- strength = null
- available = true for PASS/FAIL; false for NOT_EVALUABLE/unknown status
- gate = pass / fail / needs_review
- conflict = neutral / contradicts / insufficient
- decision_hint = bearish only for a PASS bearish confirmation; otherwise neutral
- confidence_delta = 0
- raw evaluator result is preserved

FAIL is never converted into bullish evidence. NOT_EVALUABLE is never converted into PASS.

## Deterministic tests

8/8 tests pass locally:
1. PASS + BEARISH_WARNING -> bearish
2. PASS + plain BEARISH -> bearish
3. FAIL does not infer bullish
4. NOT_EVALUABLE -> needs_review / insufficient
5. unknown status -> neutral / needs_review
6. missing status does not create evidence
7. confidence_delta remains 0
8. raw evaluator result is preserved

## Governance

- No evaluator semantics changed.
- No divergence detector rebuilt.
- No numeric threshold introduced.
- No timeframe hard-coded.
- No future price outcome used as evidence.
- 2025 remains OOS and is not used for tuning or selection.
- Adapter remains evidence normalization only.
- Decision Brain remains the synthesis layer.

## Remaining gates

This bridge does not itself grant Murphy 0028 Production Frozen status.
Remaining gates include the final 2016–2024 historical QA/sign-off, availability/leakage verification at the integrated path, provenance/freeze manifest, and explicit governance approval.
