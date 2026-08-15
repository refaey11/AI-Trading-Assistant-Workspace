# Murphy 0008 — Singleton Pivot + PF-B1 Experimental Contract V1

Status: EXPERIMENTAL / NOT PRODUCTION FROZEN

## Purpose
Define the smallest deterministic contract that can be tested for 0008 without inventing horizontal clustering/tolerance.

## PF-H1 boundary
- Candidate source: confirmed PIVOT_SEQUENCE_V2 LOW pivot.
- The pivot price is the Support boundary for this event.
- The boundary is identified by its pivot/event identity; no nearby-price clustering is performed.
- The support candidate must be available before the first break observation.
- If the required pivot/support candidate is unavailable, return NOT_EVALUABLE.

## PF-B1 candidate operator
- First completed D1 close strictly below the Support boundary: BREAK_CANDIDATE.
- Second consecutive completed D1 close strictly below the same Support boundary: DECISIVE_BREAK_CONFIRMED.
- Confirmation timestamp = close timestamp of the second bar.
- Retest observation begins only after confirmation.

## 0008 semantic chain
Confirmed Pivot LOW → Support boundary → decisive downside break → later rally/retest → broken Support functions as Resistance.

## Exclusions
- No horizontal clustering.
- No price tolerance.
- No ATR, pips, percentage, or hidden lookback.
- No 2025 input or tuning.
- No profitability inference from event counts.

## Required tests
1. Pivot availability chronology.
2. First-close candidate state.
3. Second-close confirmation.
4. Same-boundary continuity.
5. No-lookahead.
6. Retest starts strictly after confirmation.
7. Missing support returns NOT_EVALUABLE.
8. 2016–2024 fresh replay only.

## Freeze status
This is an experimental operational contract. Production freeze still requires explicit Governance approval, deterministic test pass, fresh 2016–2024 QA, provenance/evidence backup, and final freeze decision.
