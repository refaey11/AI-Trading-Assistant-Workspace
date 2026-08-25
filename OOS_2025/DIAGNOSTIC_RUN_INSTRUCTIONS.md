# 2025 No-Trade Diagnostic

The read-only diagnostic is `run_final_2025_no_trade_diagnostic_v1.py`.

It accepts an already-produced `FINAL_2025_GOVERNED_78_RULE_MANIFEST.json` and emits `FINAL_2025_NO_TRADE_DIAGNOSTIC.json`.

It does not modify rules, thresholds, evidence, or the Decision Brain, and it records `oos_tuning` / `new_rule_semantics` guards in the output.

Use it after a governed Final 2025 run:

```bash
python OOS_2025/run_final_2025_no_trade_diagnostic_v1.py \
  <path-to>/FINAL_2025_GOVERNED_78_RULE_MANIFEST.json \
  --output FINAL_2025_NO_TRADE_DIAGNOSTIC.json
```

The report contains the event count, executable/no-trade/not-evaluable counts, primary blocker reasons, event/execution status counts, risk/TIZ status counts, trades, P&L, total R, expectancy, and profit factor.
