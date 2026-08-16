# Murphy PF-B1 Fail-Closed Compatibility Contract V1

Status: COMPATIBILITY CONTRACT — NOT PRODUCTION FROZEN

## Scope
PF-B1 is the breakout-confirmation primitive required by Murphy 0013, 0014, 0015, 0016, 0017, 0018, 0019, and 0020.

## Source-derived constraint
A complete pattern rule requires breakout confirmation where the applicable Murphy rule contract specifies it. Structural pattern detection alone MUST NOT be promoted to complete rule confirmation.

## Accepted evidence
Only an existing, explicitly approved breakout policy may produce a decisive/confirmed breakout state.

## Fail-closed behavior
If the canonical breakout policy is missing, unapproved, ambiguous, or depends on an unapproved tolerance/threshold, PF-B1 MUST return `NOT_EVALUABLE`.

The evaluator MUST NOT infer decisiveness from:
- a single visual close;
- arbitrary pip/percentage/ATR thresholds;
- backtest-selected parameters;
- future bars;
- a policy copied from another rule without explicit compatibility approval.

## Reuse boundary
Existing breakout governance may be reused as an architectural template, but a rule-specific approval is required before applying its operational policy to Murphy 0013-0020.

## Rule effect
Until a compatible PF-B1 policy is explicitly approved, structural results for Murphy 0013-0020 remain structural-only and cannot be represented as complete Murphy rule confirmation.

## Freeze restriction
This contract does not production-freeze PF-B1. Full freeze requires compatibility, no-lookahead, tests, historical QA, evidence, and provenance gates.

2025 remains OOS and must not be used for tuning.
