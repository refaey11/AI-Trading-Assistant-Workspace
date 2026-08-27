# Final 78 Wiring Decision

The 2025 profitability result of zero trades is not accepted as final while the downstream compatibility layer can mask a valid Murphy PASS with a legacy candidate FAIL/NOT_EVALUABLE row.

The full 34-rule Murphy evidence remains authoritative for provenance. The compatibility view is derived from that evidence only for the governed full-evidence path. This preserves the project roles and avoids adding strategy logic.

Acceptance criteria for the next run:
- 34 Murphy + 44 Nison provenance remains intact.
- 2025 OOS tuning remains false.
- No new rule semantics.
- Regression tests pass.
- Reason-count changes are explainable from the wiring correction.
- Only then is the frozen P&L result evaluated as a strategy outcome.
