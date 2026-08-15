# Murphy 0030 — Kenneth Tower P&F Box-Size Source Research Result V1
Date: 2026-08-15
Status: RESEARCH COMPLETE / BOX FORMULA STILL UNRESOLVED

## Sources reviewed
1. John J. Murphy, Technical Analysis of the Financial Markets, Chapter 11 (Point & Figure Charting).
2. Kenneth G. Tower, chapter "Applying Moving Averages to Point and Figure Charts" in New Thinking in Technical Analysis (Bloomberg Press, 2000), available in searchable secondary-hosted text.
3. CMT/MTA archived material containing a 2002 Kenneth Tower interview.

## Findings
### Murphy
Murphy states that Kenneth Tower uses a logarithmic P&F method. A screening process measuring a stock's volatility over the previous three years determines the appropriate percentage box size for each stock. Murphy gives examples of 3.6% for AOL and 3.2% for Intel. Murphy also explains that percentage reversal values are based on the box size and reversal count.

### Tower chapter
Tower's later chapter confirms:
- P&F is price-change based rather than time based.
- UST Securities brought individualized box sizes and log scales into computerized P&F.
- UST analysts determine box sizes to reflect each stock's trading characteristics.
- More volatile stocks require larger reversal values to accurately display their trading patterns.
- The chapter provides concrete examples of individualized percentage box sizes, but the audited text does not publish a reproducible mathematical formula that converts a three-year volatility statistic into a specific percentage box size.

### CMT/MTA interview
Tower describes P&F as not time-based and discusses use of intraday data and a database of 5-cent moves for accurate short-term charts. This supports the principle that data granularity affects P&F construction, but it does not supply the missing three-year screening formula or a GBPUSD-specific box-size value.

## Decision
The research strengthens source provenance but does NOT close the exact GBPUSD box-size contract.

Therefore:
- Do not claim a specific GBPUSD box size is Murphy/Tower source-defined.
- Do not infer 1 pip, 5 pips, 1%, 2%, ATR, or another value as Murphy semantics.
- Do not tune the box size on 2016–2024 outcomes.
- Do not use 2025 for selection/tuning.
- Keep MURPHY_0030 blocked at the box-size contract boundary until either (a) an authoritative reproducible Tower selection formula is recovered, or (b) the project explicitly approves and freezes a provenance-labeled operationalization before evaluation.

## Compatibility implication
The external `pnf-chart-system` candidate remains technically useful because it exposes High/Low, 3-box reversal, X/O, and multiple box-size methods. Capability is not source equivalence. It may be used only after the construction policy is frozen.

## Next gate
Create a formal operationalization decision record if no authoritative Tower formula can be recovered. The decision must specify the exact construction policy, provenance, freeze date, and rule that the parameter cannot be selected from evaluation outcomes.
