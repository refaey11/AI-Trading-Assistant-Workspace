# Nison 0041 Solution Bridge V1

Status: IMPLEMENTATION-READY / NOT FROZEN

## Problem
Nison 0041 requires trend-line context plus a candlestick confirmation. The canonical Trendline Geometry V1 produces line identity, anchors, direction, and availability, but intentionally does not classify third touch/reaction/no-break. Building a second trendline engine would duplicate canonical infrastructure.

## Solution
Reuse the already validated Murphy 0006/0007 confirmation operator as the structural upstream for Nison 0041, then attach the existing Nison candlestick confirmation layer as a separate confirmation stage.

Pipeline:
PIVOT_SEQUENCE_V2 + TRENDLINE_GEOMETRY_V1
-> validated third-touch/reaction/line-hold evidence
-> Nison 0041 context gate
-> existing Nison candlestick confirmation evidence
-> causal availability gate
-> Nison evidence output

## Structural upstream evidence
The existing Murphy 0006/0007 reconciled operator has a 2016–2024 fresh replay with:
- 0006: 8 confirmations
- 0007: 7 confirmations
- total: 15
- exact reconciliation to the existing 15-confirmation artifact: 15/15
- availability violations: 0
- 2025 confirmations: 0

This is reused as structural evidence, not copied as a Nison rule.

## Nison-specific boundary
Nison does not inherit Murphy direction. The Nison adapter consumes the structural trendline evidence and waits for a qualifying candlestick confirmation. Nison remains confirmation-only and cannot create direction.

## Causal ordering
Required order:
1. line available;
2. third-touch evidence available;
3. reaction/line-hold evidence available;
4. Nison candlestick confirmation occurs later and is available only when its own candle is complete.

No sorting is allowed before causal validation. Out-of-order upstream evidence fails closed.

## No invented operators
Do not add ATR, pip, percentage, hidden lookback, or arbitrary touch tolerance. Reuse the existing Murphy structural operator and existing Nison candle pattern contracts. If a specific Nison candle comparator is unresolved, return NOT_EVALUABLE.

## Expected effect
0041 can move from the previous PARTIAL state to an integration-ready bridge without modifying Pivot Sequence, Trendline Geometry, or inventing a new trendline engine.

## QA gate
Before freeze:
- run the bridge on the canonical 2016–2024 D1 data;
- verify every Nison confirmation availability timestamp is causal;
- verify 2025 is excluded from tuning/selection;
- record PASS/FAIL/NOT_EVALUABLE per event;
- freeze only after governance approval.
