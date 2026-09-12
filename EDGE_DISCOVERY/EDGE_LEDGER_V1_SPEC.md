# Edge Discovery Ledger V1

## Purpose
Measure whether existing governed trading evidence contains a persistent economic edge before adding filters, weights, thresholds, or new rule semantics.

This layer is analytical only. It does not generate direction and does not replace Decision Brain V1.

## Source-of-truth and locks
- Development/calibration window: 2016-2024.
- 2025 remains OOS/evaluation-only and must never be used for tuning.
- Murphy remains the directional source.
- Nison remains confirmation/contradiction only.
- TIZ remains process/psychology context only.
- Similarity/Historical Memory remain evidence-only.
- Risk and execution remain hard gates.
- No synthetic evidence may be created to increase sample size.
- Existing rule semantics must not be changed to improve metrics.

## Core question
For every governed event/rule, measure the conditional distribution of future outcomes rather than counting PASS signals.

## Required event-level fields
- event_id
- event_time
- available_time
- rule_id
- direction
- status
- source
- symbol
- timeframe
- regime/context fields when already available
- entry_time / entry_price when an executable event exists
- exit_time / exit_price when a frozen exit contract exists
- gross_R
- cost_R
- net_R
- MFE_R
- MAE_R
- holding_bars

## Required outputs
1. Per-rule ledger: event count, executable count, trade count, wins, losses, net expectancy/R, PF, max drawdown, turnover, MFE/MAE.
2. Yearly stability: 2016 through 2024 separately.
3. Regime stability using already-governed market-state fields; no new regime thresholds are invented here.
4. Cost sensitivity: frozen baseline plus deterministic higher-cost stress cases.
5. Execution perturbation: only if supported by existing frozen execution contract; never tune to the best result.
6. OOS lock report proving no 2025 rows were used for calibration.
7. Provenance manifest linking every result to source artifacts.

## Edge qualification
No single metric qualifies an edge. A candidate edge must demonstrate:
- positive net expectancy after the frozen cost/slippage contract;
- adequate sample size;
- no dependence on one isolated year;
- acceptable drawdown and tail behavior;
- resilience to the predefined cost/execution stress tests;
- no lookahead/as-of violation;
- no 2025 contamination;
- reproducibility from source-preserved evidence.

## Important interpretation rule
A high win rate is not an edge by itself. A lower win rate with asymmetric winners can be profitable; a high win rate with large losses can be unprofitable.

## Current blocker
The repository checkpoint states that the recovered historical Murphy evidence currently contains only 7 of the 34 development Murphy rule IDs. Therefore this ledger must report coverage honestly and must not treat the current 7-rule historical stream as the official 34-rule profitability result.

## Next execution gate
Complete source-backed Murphy historical fan-in for the remaining governed rules, then run this ledger against the resulting unified event stream and frozen execution outputs.

<!-- trigger replay recovery after V2 workflow fix -->
<!-- trigger replay recovery 2026-09-12-v2 -->
<!-- trigger replay recovery 2026-09-12-v3 -->
