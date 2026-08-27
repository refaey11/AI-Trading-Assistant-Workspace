# AI Trading Assistant — Decision Brain
## Project Execution Checkpoint
Date: 2026-08-27

### Current operational truth
- GitHub = source/control plane for project code.
- CircleCI = current execution environment.
- Dropbox = authoritative data/project-source storage.
- Do not rebuild the project from scratch.
- 2025 is OOS and must not be used for tuning/calibration.

### Confirmed runtime scope
- Murphy: 34 active/dispatched runtime rules.
- Nison: 44 runtime rules.
- Total Decision Brain runtime scope: 78 rules.
- MTF: 6 timeframes.
- Decision Brain V1, Three-Book evaluator, Risk/Execution, TIZ process gate, Similarity/Historical Memory are present.

### Nison historical development
- Development window: 2016–2024.
- Existing Nison historical development runner is used unchanged in semantics.
- Dropbox H1 source and Market State are consumed.
- Last blocker was CircleCI inactivity timeout after 10 minutes with no stdout, not a trading-rule failure.
- Heartbeat/progress handling was added to keep the long calculation alive in CircleCI.
- Latest CircleCI status: nison_development_2016_2024_v1 = SUCCESS.
- Required output: NISON_2016_2024_FULL_EVIDENCE.csv plus manifest/artifacts.
- 2025_used_for_tuning = false.

### Murphy historical evidence
- Historical Murphy evidence currently verified as source-backed for 7 rules in the normalized recovery artifact:
  MURPHY_0003, MURPHY_0004, MURPHY_0021, MURPHY_0022, MURPHY_0023, MURPHY_0028, MURPHY_0029.
- Current Murphy runtime scope is still 34 rules; do not confuse runtime availability with historical evaluability.
- The remaining Murphy historical rules must be generated only from legitimate source-backed data/mappings; otherwise mark NOT_EVALUABLE.
- No synthetic evidence or invented thresholds/rule IDs.

### Recent technical fixes
1. Fixed Nison runtime import/path issue causing ModuleNotFoundError: No module named 'OOS_2025'.
2. Fixed/relaxed Market State loader boundary to require timestamp while preserving source-backed fields accepted by the Nison adapter.
3. Added governed Nison CircleCI development job for 2016–2024.
4. Added progress heartbeat to prevent CircleCI 10-minute no-output timeout.
5. Nison development now reaches SUCCESS in CircleCI.

### Exact next execution path
1. Retrieve and validate NISON_2016_2024_FULL_EVIDENCE.csv artifact.
2. Build Murphy historical 34-rule fan-in for 2016–2024 from existing source-backed project data.
3. Preserve NOT_EVALUABLE wherever evidence cannot be legitimately generated.
4. Join Murphy 34 + Nison 44 into Unified 78 by governed timestamp/as-of semantics.
5. Run current Decision Brain V1 unchanged.
6. Apply Three-Book evaluation and Risk/Execution contract.
7. Run governed 2016–2024 backtest using frozen cost/slippage rules.
8. Produce metrics/funnel/validation manifest.
9. Freeze the development result.
10. Only after development freeze, evaluate 2025 as true OOS; never tune on 2025.

### Governance rules
- No legacy 2016–2018 profitability artifacts as official current-system results.
- No substitution with 2025 evidence for development.
- No invented evidence, rule IDs, thresholds, or missing historical data.
- Do not modify Decision Brain semantics unless a compatibility audit proves an adapter is required.
