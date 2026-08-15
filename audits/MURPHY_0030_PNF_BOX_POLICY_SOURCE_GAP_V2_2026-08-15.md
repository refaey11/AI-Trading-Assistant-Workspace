# MURPHY 0030 — P&F Box Policy Source Gap V2
Date: 2026-08-15
Status: BLOCKED AT BOX-POLICY CONTRACT — NO TUNING

## Evidence reviewed
1. Project Master KB `MURPHY_0030` record: P&F bullish support; X/O structure; bullish support trendline; confirmation and entry fields are empty; testing status is UNTESTED.
2. Project Chapter 11 notes: P&F is time-independent; X/O columns; 3-box or 5-box reversal examples; larger boxes filter noise and smaller boxes are more sensitive; Bullish Support Line is 45 degrees from the lowest O column.
3. John Murphy Chapter 11 source text: computerized P&F can use intraday or end-of-day data; box and reversal sizes can be varied. Kenneth Tower is described as using a logarithmic P&F method where a screening process measures stock volatility over the prior 3 years to determine a percentage box size; examples are AOL 3.6% and Intel 3.2%. The audited text does not publish the exact screening formula.
4. External P&F candidate `gregorian-09/pnf-chart-system`: source tree exposes configurable box-size methods, High/Low construction, reversal, X/O chart construction, trendline logic, and bindings. Candidate capability is not equivalence proof.

## Determination
The project does NOT currently have enough source-backed information to compute a unique GBPUSD box size while claiming that value is Murphy/Tower semantics.

## Prohibited shortcuts
- Do not use 1 pip, 1 point, 5 points, 10 points, ATR, or any other arbitrary value as if it came from Murphy.
- Do not select a box size by maximizing 2016-2024 performance.
- Do not use 2025 for selection or tuning.
- Do not map MURPHY_0030 to S-7 without explicit provenance.

## What can be frozen now
- P&F is time-independent at the chart-semantic level.
- X/O representation.
- High/Low construction where the chosen construction contract explicitly says so.
- 3-box reversal as a supported Murphy construction mode, but not as proof that 0030 itself mandates 3 boxes unless the rule record/source mapping says so.
- Bullish Support Line geometry as source semantics.

## What cannot be frozen yet
- A unique GBPUSD box-size value.
- A unique Tower volatility-screening formula.
- A 0030 entry/confirmation signal beyond the evidence explicitly present in the Master KB.

## Next gate
Find an authoritative, reproducible source for the Tower box-size selection procedure or approve a provenance-labeled project operationalization BEFORE evaluator construction. If neither is possible, keep 0030 `NOT_EVALUABLE` and do not advance to 0031.
