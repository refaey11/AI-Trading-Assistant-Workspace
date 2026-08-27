# Development Backtest Execution Status — 2026-08-27

## What is completed
- Dropbox access through `DROPBOX_ACCESS_TOKEN` is configured and verified in CI.
- Recovered Decision Brain V1 exists and is protected by a governed handoff adapter.
- The current deny-by-default rule allowlist contains 78 verified runtime rules: 34 Murphy + 44 Nison. Murphy 0008 is explicitly blocked.
- Nison development evidence recovery for 2016-2024 is implemented and the Nison runtime path is producing governed evidence.
- Three-Book decision integration exists: Murphy supplies directional context; Nison supplies confirmation/contradiction; TIZ remains process/psychology context; Risk is a hard gate; Similarity/Memory remain evidence only.
- A governed bar-level development backtest runner exists in GitHub and is wired for H1 + Murphy evidence + Nison evidence + Market State context + Decision Brain + Risk/Execution.

## Historical Murphy recovery discovery
A recovered project workspace archive was inspected. The recovered historical Murphy artifacts contain source-backed evidence for 2016-2024, but only 7 Murphy rule IDs are currently represented in the recovered historical evidence files:
- MURPHY_0003
- MURPHY_0004
- MURPHY_0021
- MURPHY_0022
- MURPHY_0023
- MURPHY_0028
- MURPHY_0029

A source-preserving normalization artifact was generated from those files and filtered strictly to 2016-2024. It contains 402,710 rows. No missing rules or directions were invented.

## What is still missing
The current 34-rule Murphy development evidence stream is not yet complete. The missing 27 rule histories must be recovered/generated from existing authoritative project source material, rule mappings, MTF mappings, market-state context, and the existing Murphy evaluator contracts.

## Required execution path
1. Recover/generate source-backed historical evidence for the remaining Murphy development rules.
2. Preserve PASS/FAIL/NOT_EVALUABLE semantics and never synthesize evidence just to increase trade count.
3. Build the governed Murphy 2016-2024 stream.
4. Join Murphy 34 + Nison 44 into the Unified 78 event stream.
5. Run the recovered Decision Brain V1 assessment unchanged.
6. Apply Three-Book decision and frozen Risk/Execution.
7. Execute bar-by-bar trade outcomes with the frozen cost/slippage contract.
8. Produce executed trades, execution funnel, metrics, and validation manifest.

## Required final artifacts
- `unified_78_events_2016_2024.csv`
- `decision_events_2016_2024.csv`
- `executed_trades_2016_2024.csv`
- `execution_funnel_2016_2024.json`
- `backtest_metrics_2016_2024.json`
- `validation_manifest_2016_2024.json`

## Governance locks
- Development window: 2016-2024 only.
- 2025 is OOS/evaluation-only and must not be used for tuning/calibration.
- Murphy remains the directional source.
- Nison remains confirmation/contradiction only.
- Similarity/Historical Memory remain evidence only and cannot create direction.
- TIZ remains process/psychology context only.
- Risk remains a hard execution gate.
- Do not modify rule semantics to force more trades.
- Do not use legacy 2016-2018 profitability artifacts as the current 78-rule result.

## Current status
EXECUTION_IN_PROGRESS — active workstream is Murphy historical evidence fan-in; the end-to-end official 2016-2024 profitability result is not yet claimed.