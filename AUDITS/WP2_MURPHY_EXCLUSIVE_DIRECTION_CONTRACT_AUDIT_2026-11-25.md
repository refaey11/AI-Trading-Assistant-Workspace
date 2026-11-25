# WP2 Murphy-Exclusive Direction Contract Audit
Date: 2026-11-25
Branch: `audit/wp2-murphy-exclusive-direction-contract-2026-11-25`
Base: `baf1f88652390f3b1535760c0fb3bc30fe153171` (WP1 TIZ metadata-only validation head)

## Scope
Static compatibility audit only. No runtime or evaluator code changed. No market-data payloads, historical datasets, 2025 OOS data, Dropbox, or CircleCI were accessed. No tests or workflows were run on this audit branch.

## Verified current behavior
1. `RUNTIME/DECISION_RUNTIME_V1/live_decision_runtime_v1.py` validates the seven MTF fields, then passes the full normalized row to recovered `decision_brain.assess(normalized_row, similarity=None)`.
2. `RECOVERED_SOURCES/DECISION_BRAIN_V1/decision_brain.py` generates bullish/bearish evidence from:
   - `mtf_trend_score`
   - the six timeframe `*_trend_regime` fields
   - positive volume mean when `volume_available` is true.
   Its `directional_bias` and `confidence` are calculated from the combined evidence. Therefore MTF and Volume currently affect both Brain direction and Brain confidence.
3. Live Runtime passes that Brain `directional_bias` and `confidence` into `evaluate_three_book_decision`. The evaluator selects final BUY/SELL from Brain bias, and copies Brain confidence into `signal.confidence`. Murphy is checked for PASS and directional conflict; agreement does not establish that Murphy generated the direction.
4. The evaluator's current contract rejects neutral/conflicted Brain bias and opposing Brain bias, but does not select direction directly from Murphy.
5. The historical Gate3C path has a stronger directional provenance contract:
   - `OOS_2025/build_single_event_risk_evidence_v1.py::_one_directional_murphy_row` selects exactly one registry-eligible directional PASS row.
   - The selected row supplies `direction`, `pass_rule_id`, and `source_rule_id`.
   - `tools/gate3c_build_single_event_bundle_v1.py` propagates this direction and provenance into Murphy and Risk evidence.
   - `gate3c_single_event_e2e_v1.py` verifies Murphy/Risk direction, pass-rule, and directional-source agreement.
   This is historical evaluation plumbing, not proof that the live runtime uses Murphy as its exclusive direction source.
6. The inspected Murphy directional evidence contract provides direction and rule provenance but no documented `directional_confidence` field or governed confidence-calculation rule. The existing evaluator's `signal.confidence` is Brain confidence, which is contaminated by MTF/Volume and cannot be relabelled as Murphy confidence.

## Hard blockers
- **Direction authority violation:** live BUY/SELL is generated from Brain's MTF/Volume-derived directional bias, not selected directly from authoritative Murphy direction.
- **Confidence authority unresolved:** no verified Murphy directional-confidence field or calculation contract was found in the inspected producer/consumer path. Do not invent a numeric mapping, infer confidence from rule count, use Brain confidence, or silently treat context confidence as directional confidence.
- **MTF context contract:** current live event requires all seven MTF fields and source equality. Whether MTF remains a required context input after direction isolation must be explicitly separated from its directional authority. This audit does not remove MTF requirements.
- **No-trade reasons:** Brain no-trade reasons are included in the payload but are not enforced as an independent gate by the Three-Book evaluator. This is a separate governance question and must not be silently conflated with Murphy direction authority.

## Required WP2 acceptance tests
1. Same authoritative Murphy BUY with MTF/Volume all bearish, bullish, neutral, missing where allowed, or extreme values must never change final direction from BUY.
2. Same authoritative Murphy SELL with MTF/Volume all bullish, bearish, neutral, or extreme values must never change final direction from SELL.
3. MTF/Volume perturbations must not change a field labelled directional confidence.
4. Nison may confirm, contradict, or remain absent according to its approved confirmation contract; it must never generate or reverse direction.
5. Similarity/historical memory remains absent from Brain direction and must not change direction/confidence.
6. Murphy missing, non-authoritative, non-PASS, invalid direction, unknown/unapproved rule, or invalid pass-rule/source linkage must fail closed.
7. Risk direction must equal Murphy direction; canonical Risk hard gate and 3R requirement remain mandatory.
8. TIZ absent/failed/malformed remains non-blocking metadata only (WP1 behavior).
9. Final runtime remains SIGNAL_ONLY, orders disabled, broker volume null.

## Smallest safe next action
Before changing runtime code, obtain or approve a canonical Murphy directional-confidence contract. If no such contract exists, keep directional confidence explicitly NOT_EVALUABLE/absent rather than reusing Brain context confidence. Then implement Murphy direction selection as the sole source of final BUY/SELL, and separate Brain's MTF/Volume assessment into non-directional context metadata. Add the adversarial invariance tests above before changing implementation.

## Safety
- WP1 was validated on commit `baf1f88652390f3b1535760c0fb3bc30fe153171` by GitHub Actions runs `45544173344` and `45544173351`, both successful.
- This branch is a static audit only and is not an integration branch.
- No PR created, no merge/rebase/cherry-pick, no `main` changes.
- No automatic orders or MT5 connection enabled.
- 2025 OOS remains locked.
