# AI Trading Assistant — Murphy 0008 Project State Freeze

Date: 2026-08-15
Status: PRODUCTION FROZEN

## Frozen 0008 path
- PF-H1: confirmed LOW pivot from PIVOT_SEQUENCE_V2 is the singleton Support boundary for the 0008 validation/production path.
- PF-B1: first completed D1 close strictly below Support = candidate; immediately following completed D1 close strictly below the same Support = decisive-break confirmation.
- Retest observation begins strictly after confirmation.
- Role-reversal evidence requires a later Support-intersecting D1 bar that closes strictly below Support.

## Validation record
- 2016–2024 only.
- Confirmed LOW Support candidates: 344.
- First-close break candidates: 326.
- Immediate second-close confirmations: 242.
- Candidate failures at immediate next close: 84.
- Later range-intersection retests: 233/242 (96.28%).
- Later role-reversal evidence: 229/242 (94.63%).
- Availability violations: 0.
- Confirmation chronology violations: 0.
- Retest-before-confirmation violations: 0.
- 2025 confirmations: 0.

## Governance exclusions
No clustering, equality tolerance, ATR, pips, arbitrary percentage, hidden lookback, future-pivot rewriting, or 2025 tuning/selection.
Event-frequency diagnostics are not profitability or win-rate metrics.

## Important correction
The earlier 324-confirmation replay is superseded. The frozen operator requires the immediate next completed D1 close to confirm the first candidate; the corrected executable replay yields 242 confirmations.

## GitHub promotion
Production promotion was merged into main through PR #10.
Merge commit: 515aac5785ed36529763cbf1b4e0f8324b2aeee3.

## Continuity rule
0008 is frozen and must not be silently retuned. Future work should build on the frozen artifacts and preserve 2025 as OOS. Any change to the 0008 contract requires a new version, compatibility audit, validation, and explicit freeze decision.
