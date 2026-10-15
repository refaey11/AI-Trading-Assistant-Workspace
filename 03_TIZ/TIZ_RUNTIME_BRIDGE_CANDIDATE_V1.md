# TIZ Runtime Bridge Candidate V1

## Status
CANDIDATE — NOT AUTHORITATIVE — NOT FROZEN

## Purpose
Provide a narrow compatibility bridge from the existing `trading_zone` runtime object to the seven existing TIZ rules. This is an adapter/normalizer only; it does not create psychological semantics.

## Seven-rule mapping
- PSY_0001 PREDEFINE_RISK -> `pre_trade_state_gate`
- PSY_0002 ACCEPT_RISK -> `risk_acceptance`
- PSY_0003 INDEPENDENT_OUTCOMES -> `post_trade_review` / process-only
- PSY_0004 NO_CERTAINTY -> `pre_trade_state_gate`
- PSY_0005 CUT_LOSS_RULE -> `loss_sequence_control`
- PSY_0006 SYSTEMATIC_PROFIT -> `post_trade_review`
- PSY_0007 RULE_DISCIPLINE -> `rule_adherence` + `no_impulsive_override`

## Non-negotiables
1. TIZ cannot generate BUY/SELL direction.
2. Missing evidence must remain `NOT_EVALUABLE`.
3. No psychological numeric thresholds are introduced.
4. Stop-loss/take-profit mechanics remain owned by Risk/Execution.
5. 2025 remains OOS and cannot be used for tuning, selection, calibration, or optimization.
6. This bridge does not claim that a producer exists; evidence must arrive with value, availability, timestamp, provenance, and state semantics.

## Promotion gate
Do not promote until the authoritative producer/provenance contract, deterministic evaluator, adapter validation, historical QA, OOS checks, and cross-file consistency audit all pass.
