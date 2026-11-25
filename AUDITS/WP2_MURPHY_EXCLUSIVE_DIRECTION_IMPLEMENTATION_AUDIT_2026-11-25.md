# WP2 Murphy-Exclusive Direction Implementation Audit
Date: 2026-11-25
Branch: `fix/wp2-murphy-exclusive-direction-2026-11-25`
Base: WP1 TIZ metadata-only head `baf1f88652390f3b1535760c0fb3bc30fe153171`

## Approved policy
The project owner approved the following implementation rule:
- Murphy PASS is the only source of final BUY/SELL direction.
- Nison can confirm or contradict; contradiction blocks, confirmation affects only the evaluator's qualitative logic label.
- MTF and Volume remain context only and cannot generate, reverse, veto, or score final direction.
- Similarity/history remains audit evidence only.
- Risk remains a hard gate; canonical Live Runtime risk validation retains the 3R minimum.
- Directional confidence is `NOT_EVALUABLE` until a canonical Murphy confidence source/calculation is established. Do not substitute Brain confidence or invent a numeric mapping.
- TIZ remains optional audit metadata only.

## Changes implemented
1. `evaluation/three_book_decision_evaluator_v1.py`
   - Maps Murphy `BUY/BULLISH/BULL` to BUY and `SELL/BEARISH/BEAR` to SELL.
   - Requires Murphy status PASS and a valid Murphy direction.
   - Uses Murphy direction as the final direction.
   - No longer uses Brain bias or Brain confidence to select or veto direction.
   - Emits `confidence: null`, `confidence_status: NOT_EVALUABLE`, and `direction_source: MURPHY`.
   - Records audit flags that Brain and MTF/Volume did not supply direction.

2. `RUNTIME/DECISION_RUNTIME_V1/live_decision_runtime_v1.py`
   - Keeps recovered Brain output only as `brain_context`.
   - Labels Brain bias as `NOT_USED_FOR_DIRECTION`, confidence as `NOT_EVALUABLE`, and evidence as MTF/Volume context.
   - Exposes `direction_authority: MURPHY_ONLY` and `directional_confidence: NOT_EVALUABLE`.
   - Retains the existing Murphy/Risk direction match, canonical Risk evaluation, Nison contradiction block, SIGNAL_ONLY output, and orders-disabled boundary.

3. Tests:
   - Replaced evaluator tests that required Brain directional agreement with tests that prove Brain bias can be opposing, neutral, missing, or extreme without changing Murphy direction.
   - Added Live Runtime adversarial tests for BUY with extreme bearish MTF/Volume, SELL with extreme bullish MTF/Volume, and opposing Similarity memory.
   - Added explicit assertions that directional confidence is not evaluable.

4. `.github/workflows/live-decision-runtime-v1.yml`
   - Adds the Three-Book evaluator contract test to the Live Runtime pull-request test command and path filters.
   - The workflow runs only Python contract tests; no market-data acquisition or Dropbox/CircleCI jobs are invoked by this workflow.

## Static verification
- Branch diff against WP1 base contains only:
  - `RUNTIME/DECISION_RUNTIME_V1/live_decision_runtime_v1.py`
  - `RUNTIME/DECISION_RUNTIME_V1/test_live_decision_runtime_v1.py`
  - `evaluation/three_book_decision_evaluator_v1.py`
  - `tests/evaluation/test_three_book_decision_evaluator_v1.py`
  - `.github/workflows/live-decision-runtime-v1.yml`
- Confirmed the live runtime no longer emits Brain's computed directional bias/confidence as decision fields.
- Confirmed evaluator final direction is selected from normalized Murphy direction.
- Confirmed test workflow now includes both live runtime and Three-Book evaluator tests.

## Remaining validation / blockers
- GitHub Actions must run on this exact branch head before this implementation can be called test-validated.
- This does not authenticate the upstream Murphy source envelope. Existing envelope checks still establish claimed authority/source/producer fields, not cryptographic or registry-backed producer authenticity.
- Brain context no-trade reasons are still retained as metadata and are not independently enforced as a hard gate; this remains a separate governance decision.
- The broader PR #119/#120 integration topology and source-lineage issues remain unresolved.
- No production eligibility, MT5 connection, or automatic order execution is authorized by this work.

## Safety
- No main branch changes, merge, rebase, cherry-pick, Dropbox, CircleCI, market-data payload, or 2025/2026 dataset access.
- No test result is claimed in this report; status is implementation plus static verification pending Actions.
