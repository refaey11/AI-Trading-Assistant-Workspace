# Murphy 0021–0023 — Problems Encountered & How We Solved Them
Date: 2026-08-15

## 1. Raw historical file contained 9 rows from 2025
Problem: The accessible historical CSV contained 122,943 rows instead of the expected 122,934; nine rows were dated 2025-01-01.
Solution: Preserve the raw source. Use the 122,934 rows dated 2020–2024 as the historical QA population and exclude the nine 2025 rows from tuning/selection.

## 2. Confusion between raw and clean row counts
Problem: 122,943 raw rows could be confused with the 122,934 clean historical target.
Solution: Freeze the reconciliation target at 122,934 rows for 2020–2024 and document 122,943 as the raw source count.

## 3. Existing Rule Adapter was incomplete
Problem: The initial/design implementation did not expose all fields required by the canonical contract, notably decision_hint and confidence_delta; current_state was not materially used.
Solution: Do not rebuild the Adapter. Add a source-locked 0021–0023 bridge based on the existing Integration Contract V2.

## 4. FAIL could be misread as the opposite trade direction
Problem: A failed condition could incorrectly create an opposite directional signal.
Solution: Direction comes only from evaluator.directional_confirmation. FAIL maps to gate=fail and decision_hint=neutral; no opposite direction is inferred.

## 5. NOT_EVALUABLE could be converted into a decision
Problem: Missing evidence could accidentally become PASS/FAIL.
Solution: NOT_EVALUABLE remains available=false, gate=needs_review, conflict=insufficient, direction=neutral.

## 6. No source-locked confidence magnitude
Problem: The evaluator does not provide a defensible confidence magnitude.
Solution: confidence_delta=0 for this bridge; no confidence is invented from PASS/FAIL.

## 7. Availability/no-lookahead proof was initially incomplete
Problem: The historical result CSV alone did not contain all source-availability timestamps.
Solution: Use existing VOLUME_CONFIRMATION_V2 and OPEN_INTEREST_V1 evidence with conservative safe_availability_timestamp policy. All 122,934 historical rows were checked.
Result: 31,510/31,510 historical PASS decisions had required evidence available; future-OI violations=0. Missing evidence remained non-PASS/NOT_EVALUABLE.

## 8. Risk of changing evaluator semantics during integration
Problem: Integration could introduce thresholds, fixed timeframes, spot-FX OI, or other new logic.
Solution: Keep the bridge source-locked; no evaluator rebuild, thresholds, hard-coded execution timeframe, or spot-FX OI proxy.

## 9. Canonical clean artifact byte identity could not be independently proven
Problem: The documented CLEAN_V1 identity was known, but its separate payload was unavailable for SHA comparison.
Solution: Do not claim byte-for-byte equality. Reconcile the historical population by row count/period and preserve the raw archive plus SHA-256 as provenance.

## 10. Production freeze could be claimed too early
Problem: Passing technical tests does not automatically equal Production Frozen.
Solution: Create freeze-readiness and final-freeze records, then freeze only the defined scope. Future semantic/evaluator/adapter changes require re-audit and re-freeze.

## Final frozen state
- 0021: FROZEN
- 0022: FROZEN
- 0023: FROZEN
- Deterministic bridge tests: 10/10 PASS
- Historical QA population: 122,934 rows (2020–2024)
- 2025 excluded from tuning/selection: 9 raw rows
- Historical PASS decisions with required availability: 31,510/31,510
- Future OI availability violations: 0

## Governance
This record describes the problems and their resolutions. It does not authorize changing frozen semantics. Any change to evaluator logic, thresholds, timeframe policy, OI source, bridge mapping, or evidence interpretation requires a new compatibility audit and re-freeze.
