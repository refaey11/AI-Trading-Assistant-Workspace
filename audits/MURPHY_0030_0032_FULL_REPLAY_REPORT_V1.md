# Murphy 0030–0032 — Full Historical Replay Report V1

Date: 2026-08-16
Branch: proposal/murphy-0030-box-policy-v1
Decision: **BLOCKED — NOT PRODUCTION FROZEN**

## Dataset
- GBPUSD D1 canonical dataset: 2,544 rows
- Range: 2016-01-03 through 2024-12-31
- Calibration/warm-up: 2016–2018 (935 rows)
- Evaluation: 2019–2024 (1,609 rows)
- 2025: excluded

## Policy used
- P&F state carries forward from 2016 into the 2019 evaluation period; no reset at 2019.
- Box percentage: 0.6257356643%.
- Reversal: 3 boxes.
- High/Low bootstrap with same-bar dual qualification treated as AMBIGUOUS / NOT_EVALUABLE.
- These bootstrap/box policies are project operationalizations, not claims of verbatim Murphy/Tower methodology.

## Calibration verification
Using 2016–2018 completed closes, sample daily log-return standard deviation is 0.006257356643053345, giving 0.6257356643053346% when expressed as a percentage. This reproduces the declared proposal value to rounding.

## Full stateful replay result
Building one deterministic P&F state across the complete 2016–2024 dataset produced:
- 150 total columns
- 75 X columns
- 75 O columns
- first column: X on 2016-01-04
- last column: O on 2024-12-19

A fresh P&F build restricted to 2019–2024 would produce a different state (89 columns in the prior diagnostic). That reset is therefore rejected by Policy Decision V1.

## Rule availability in 2019–2024
Evaluating evidence after each completed D1 bar:
- MURPHY_0030 available on 1,609 / 1,609 evaluation bars; first availability 2019-01-01.
- MURPHY_0031 available on 810 / 1,609 evaluation bars; first availability 2019-01-01.
- MURPHY_0032 available on 799 / 1,609 evaluation bars; first availability 2019-01-02.

Availability here means the structural/risk reference is computable from the P&F state available at that completed bar. It does not mean a trade signal.

## No-lookahead checks
Prefix replay at checkpoints passed with exact state equality between the historical prefix and the corresponding state extracted from the full replay:
- 2019-01-01: 61 columns — PASS
- 2020-01-02: 81 columns — PASS
- 2021-06-30: 106 columns — PASS
- 2022-12-30: 130 columns — PASS
- 2024-06-28: 145 columns — PASS
- 2024-12-31: 150 columns — PASS

A stronger future-suffix mutation test was also run at 2022-12-30: the entire future suffix was altered materially, while the state at the checkpoint remained byte/signature equivalent — PASS.

## Structural sensitivity
The declared alternative box percentages were executed without selecting an alternative based on evaluation profitability:
- 0.6257356643%: 150 columns — executable.
- 0.75%: 116 columns — executable.
- 1.00%: 73 columns — executable.
- 0.50%: BLOCKED by the declared same-bar bootstrap ambiguity at 2016-01-04.

The historical diagnostic counts previously recorded in project backups (137 / 89 / 71 / 45) are therefore not reproducible under the now-declared bootstrap and full-state policy. They must not be reused as final sensitivity evidence.

## Interpretation
The final evaluator is deterministic and prefix-safe under the declared policy. However, sensitivity acceptance is not yet granted because the project has not defined a numerical/structural acceptance threshold for how much P&F state may change across pre-declared box alternatives. The 0.50% alternative is additionally non-evaluable under the ambiguity-block policy.

## CI
The dedicated Murphy 0030–0032 workflow exists, but no GitHub Actions workflow run is currently observable for the proposal commits. CI therefore remains UNPROVEN.

## Final decision
**BLOCKED**.

The historical replay and no-lookahead implementation gates are now evidenced. Remaining release gates are:
1. explicit governance acceptance/definition of the structural sensitivity acceptance criterion;
2. decision on whether 0.50% remains a valid sensitivity candidate or is documented as non-evaluable under the fixed bootstrap policy;
3. CI execution evidence (or equivalent reproducible CI record);
4. explicit governance acceptance of the operational box/bootstrap policies without attributing them to Murphy/Tower verbatim.

No merge and no production freeze until these gates are closed.
