# Provenance + Uniform Walk-Forward Gate Audit V1

Date: 2026-08-12
Status: GATE AUDIT — NOT YET CLEARED

## Source-of-truth policy
Workspace / File Library artifacts remain the project source of truth. GitHub is a development/provenance mirror and must not silently replace missing project provenance.

## 1. Murphy 0003–0004 provenance

The available reconciliation report states that the old artifact `MURPHY_0003_0004_HISTORICAL_COMPARISON_2016_2024.csv` and its generator/metadata are not present in the currently available Workspace/project ZIP archives. The old reported populations therefore cannot be reproduced or attributed to a known generator.

The current V2 lineage is verified as:
`MARKET_STRUCTURE_GBPUSD_ALL_TF_V1 -> PIVOT_SEQUENCE_V2 -> current evaluator`.

PIVOT_SEQUENCE_V2 uses confirmed pivots after 2 bars and no-lookahead availability; 2025 is excluded.

The current V2 evaluator semantics are the corrected joint conditions:
- 0003: higher successive reaction peaks AND higher successive reaction troughs.
- 0004: lower successive reaction peaks AND lower successive reaction troughs.

No tuning or forcing of the old counts is permitted.

## 2. Uniform official walk-forward protocol

The frozen protocol artifact specifies five assets:
EURUSD, GBPUSD, USDJPY, USDCAD, XAUUSD.

Calibration/OOS folds:
- 2016–2023 train -> 2024 OOS
- 2016–2024 train -> 2025 OOS

The protocol freezes k=20 and defines calibration-only parameter selection. OOS parameters are locked; future outcomes cannot enter retrieval or calibration for the OOS year.

The existence of protocol and prior OOS artifacts does NOT by itself prove that the current project has passed the required fresh uniform end-to-end rerun.

## 3. Current gate finding

The project state and roadmap identify the required gate as:
`uniform official walk-forward + leakage audit`.

The stored baseline/OOS artifacts explicitly state that a fresh uniform end-to-end rerun across all five assets is still required before official baseline status.

Therefore this audit does not mark the baseline as frozen and does not mark the final Decision Brain as complete.

## 4. 2025 rule

2025 remains OOS and must not be used for tuning, implementation selection, or forcing historical agreement.

## 5. Required execution order

1. Recover old 0003–0004 artifact OR generator/metadata if available; otherwise preserve the provenance blocker.
2. Verify the frozen uniform walk-forward protocol and leakage controls against actual runnable artifacts.
3. Run the fresh five-asset uniform protocol without changing locked rules/parameters.
4. Perform leakage audit.
5. Only if the gate passes, freeze the official baseline.
6. Then proceed to Decision Brain V1 integration.

## Gate decision

**NOT CLEARED YET.**

No claim of official baseline freeze or final Decision Brain completion is made by this audit.
