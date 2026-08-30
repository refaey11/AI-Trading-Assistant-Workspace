# MTF regime normalization preflight

This checkpoint records the only known code-level blocker in the source-acquisition path at this point: `_normalize_regime()` uses pandas before the local function import. The governed compatibility normalization itself is unchanged; this is an import-scope repair only.

Required next verification: execute the existing source-acquisition normalization path on source-backed MTF data, with no backtest and no 2025 tuning.

Guardrails: do not change Murphy, Nison, Decision Brain V1, TIZ policy, Risk policy, or the six-TF contract.
