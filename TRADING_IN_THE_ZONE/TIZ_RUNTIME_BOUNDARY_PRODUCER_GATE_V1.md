# Trading in the Zone — Runtime Boundary Producer Gate V1

Date: 2026-08-18
Status: BLOCKED / NOT AUTHORITATIVE

## Source authority
The integrated Three-Book contract defines Trading in the Zone as **Execution psychology and process discipline**. Its declared outputs are:

- `pre_trade_state_gate`
- `risk_acceptance`
- `rule_adherence`
- `loss_sequence_control`
- `post_trade_review`
- `no_impulsive_override`

## Boundary rules
- TIZ is process/evidence only.
- TIZ is direction-neutral.
- TIZ cannot generate BUY/SELL direction.
- TIZ cannot override Murphy technical context or Nison confirmation.
- Missing evidence must resolve to `NOT_EVALUABLE`.
- No psychological numeric threshold may be invented.
- Stop-loss and take-profit mechanics remain owned by the Risk/Execution layer; TIZ may evaluate adherence only when authoritative plan-vs-actual evidence exists.
- 2025 remains locked OOS and cannot be used for tuning/selection/calibration.

## Producer gate
An authoritative producer is required to expose each TIZ output with:

1. value/state
2. availability
3. timestamp
4. provenance
5. deterministic state semantics

Current status: **no authoritative producer implementation has been established for these outputs in the current workspace evidence**.

Therefore this document deliberately does **not** implement a new producer and does **not** freeze any TIZ rule.

## Rule disposition
- PSY_0001 PREDEFINE_RISK — blocked: no authoritative proof that risk was predefined before entry.
- PSY_0002 ACCEPT_RISK — candidate only: `risk_accepted` mapping exists, but producer provenance is not authoritative.
- PSY_0003 INDEPENDENT_OUTCOMES — process-only; no runtime market operator.
- PSY_0004 NO_CERTAINTY — blocked: no authoritative certainty-state producer.
- PSY_0005 CUT_LOSS_RULE — blocked: stop-loss mechanics do not prove adherence; producer semantics for adherence are not authoritative.
- PSY_0006 SYSTEMATIC_PROFIT — blocked: take-profit mechanics/post-trade review do not prove profit-taking adherence.
- PSY_0007 RULE_DISCIPLINE — candidate only: rule-adherence/impulse flags exist, but producer semantics and precedence are not authoritative.

## Next gate
Close the authoritative producer/provenance contract first. Then implement only the smallest missing evidence fields, deterministic evaluators, adapter integration, historical QA, and final freeze gates.
