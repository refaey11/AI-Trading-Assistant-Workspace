# CURRENT PF-B1 / PF-H1 Governance Freeze — 2026-08-22

## Scope
0008 Support→Resistance role-reversal runtime dependency.

## Promotion decision
Owner-requested promotion of the minimal source-faithful PF-B1/PF-H1 candidate contracts for runtime integration.

## PF-H1
- Consume confirmed pivot-derived level candidates and existing S/R role identity.
- No invented clustering/tolerance/ATR/percentage/pip threshold.
- If approved horizontal identity is unavailable: NOT_EVALUABLE.

## PF-B1
- Consume an approved boundary.
- Breakout event = first completed-bar close beyond the boundary.
- Emit boundary_id, direction, breakout_timestamp, confirmation_timestamp, availability_timestamp, status.
- Do not add external ATR/percentage/volume thresholds.
- Confirmation timestamp is the completed-bar close time for this minimal operator.

## 0008 role-reversal operator
- Upside case: completed-bar close above support/resistance boundary, later completed-bar close at or below the level (retest), then later completed-bar close above the level (role restored / resistance failed).
- Downside case: completed-bar close below support boundary, later completed-bar close at or above the level (retest), then later completed-bar close below the level (role restored / support failed).
- Event timestamps must be strictly ordered and available only after the corresponding completed bar.
- Missing or ambiguous evidence: NOT_EVALUABLE.

## Evidence
- PF-H1 candidates 2016–2024: 2,392.
- PF-B1 raw breakout candidates 2020–2024: 2,335.
- 0008 role-reversal replay 2020–2024: 39 matched breakout events; 36 ROLE_REVERSAL_CANDIDATE; 3 NO_RETEST.
- Chronology violations: 0.
- 2025 excluded from tuning/evaluation.

## Controls
- No external thresholds imported.
- No ATR filter added.
- No percentage/pip tolerance added.
- No lookahead introduced.
- Historical artifacts preserved.

## Status
GOVERNANCE_PROMOTED_FOR_RUNTIME_INTEGRATION

This record promotes the minimal contracts for project runtime use; it does not claim historical profitability or production performance.
