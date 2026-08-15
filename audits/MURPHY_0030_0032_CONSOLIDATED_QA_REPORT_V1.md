# Murphy 0030–0032 — Consolidated QA Report V1

Date: 2026-08-16
Status: BLOCKED / NOT PRODUCTION FROZEN

## Scope
Murphy 0030–0032 Point & Figure evidence layer.

## Source / provenance boundary
- Murphy Chapter 11 remains the source for the qualitative P&F semantics.
- The project logarithmic/percentage implementation is an operationalization.
- The bootstrap is an external deterministic operational policy.
- The project does not claim to reproduce Kenneth Tower's exact volatility-to-box conversion formula.
- 2025 is excluded from policy selection and tuning.

## External verification performed
Independent technical references were checked for the High/Low construction and 3-box reversal. StockCharts documents the High/Low priority rule: X checks High first for continuation, then Low for reversal; O checks Low first, then High for reversal. It also documents the 3-box reversal method. MQL5 references independently describe box size, reversal amount, and deterministic construction mechanics.

These references corroborate the operational construction boundary; they do not establish a verbatim Murphy/Tower bootstrap formula.

## Existing proposal artifacts inspected
- `src/murphy_0030_0032/pnf_3box_log_reference.py`
- `src/murphy_0030_0032/pnf_3box_reference.py`
- `src/murphy_0030_0032/project_box_policy.py`
- existing Murphy 0030–0032 proposal/contract artifacts
- draft PR #15: proposal only, not merged

## Compatibility finding
The existing deterministic 3-box core is reusable. The new evaluator consumes that shared primitive rather than creating separate P&F engines for 0030, 0031, and 0032.

## Implemented in this batch
1. Added `src/murphy_0030_0032/evaluator_v1.py`.
2. Added evaluator tests covering:
   - 0030 availability only after an O column exists;
   - 0031 long-stop relation below previous O in an uptrend;
   - 0032 short-stop relation above previous X in a downtrend;
   - malformed OHLC handling;
   - prefix replay / future-suffix invariance.
3. Corrected the directional test expectation so 0031 is evaluated only on an X column with a previous O column, while 0032 is evaluated only on an O column with a previous X column.

## Local execution
The evaluator and its six focused tests were reconstructed from the committed source in an isolated runtime and executed:

`6 passed`

This local result is not a GitHub Actions result and is not a production QA pass.

## GitHub CI status
The proposal branch contains CI workflows, but GitHub reports no workflow run for the current proposal commits. Therefore CI execution remains UNPROVEN.

## Historical QA status
The project backup records an earlier diagnostic construction on 2,544 GBPUSD D1 bars for 2016–2024, with 1,609 bars in the proposed 2019–2024 evaluation block and 89 P&F columns at the proposed 0.6257356643% policy.

Those are prior diagnostic results. A fresh final 0030–0032 evaluator replay was not executed in this runtime because the canonical D1 bytes are available through File Library search but are not mounted as a runtime file for direct execution here.

Therefore the required 2019–2024 final evaluator QA is still blocked.

## No-lookahead / availability
The evaluator is designed around prefix replay: each rule result is computed only from completed bars through the current timestamp. A focused prefix-vs-suffix invariance test passed in the reconstructed local run.

This is an implementation-level test, not the final historical no-lookahead audit on the canonical 2016–2024 dataset.

## Box Policy decision
The proposed `0.6257356643%` value remains acceptable as a reproducible PROJECT OPERATIONALIZATION PROPOSAL because it is pre-declared from the 2016–2018 calibration block using daily log-return standard deviation and does not use profitability or 2025.

It is NOT approved as a Murphy/Tower exact value and is NOT production-frozen.

## Final decision
**BLOCKED**

Reason: required production gates are not all executable/proven yet:
1. GitHub CI execution is unproven.
2. Fresh 2019–2024 final evaluator QA has not been executed on the canonical runtime dataset.
3. Final dataset-level availability/no-lookahead audit is therefore not proven.
4. Final robustness/sensitivity acceptance has not been completed against the final evaluator.

## Next action
Make the canonical GBPUSD D1 dataset available to the evaluator runtime, execute the final 2019–2024 replay, run dataset-level availability/no-lookahead and pre-declared structural sensitivity checks, then repeat the governance decision. Do not merge or freeze while any gate remains unproven.
