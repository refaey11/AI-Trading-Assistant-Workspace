# GBPUSD 2025 Rule Runtime Smoke — 2026-08-23

Status: PARTIAL SMOKE ONLY — NOT PROFITABILITY

Scope:
- Fresh 2025 GBPUSD H1 source derived from the frozen OOS master.
- No tuning, calibration, threshold selection, or rule changes.
- This is an executable smoke of the rule evaluators actually recovered in the workspace, not a final Decision Brain run.

Recovered executable evaluators:
- MURPHY_0003 / 0004
- MURPHY_0021 / 0022 / 0023
- MURPHY_0027 / 0028 / 0029
- MURPHY_0050

Important limitation:
- 0003/0004 were not counted as directional evidence in this smoke because their evaluator requires upstream reaction-trough inputs that are not present in the fresh H1 source.
- 0022/0023 require futures open-interest evidence, unavailable in the 2025 source package.
- 0027 requires an approved trend-vs-ranging regime operator; none was invented.
- 0028/0029 require confirmed RSI/price divergence evidence; none was invented.
- 0050 requires its eight upstream checklist evidence fields; none were invented.

Meaningful executable result:
- MURPHY_0021 on 2025 H1 using close-vs-previous-close plus existing volume_direction:
  - PASS: 2,772 bars
  - FAIL: 3,408 bars
  - NOT_EVALUABLE: 36 bars

This smoke does NOT create BUY/SELL signals and does NOT constitute a 2025 profitability result.
The frozen Decision Brain OOS run remains pending the complete upstream evidence/event path required by the project contracts.
