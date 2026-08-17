# Murphy 39 Canonical Queue V1

Source of truth used to build this queue: `AI_Trading_Assistant_MASTER_KB_V1` / `02_Trading_Rules/MASTER_CANDIDATE_RULES_V1.json` and `AI_Trading_Assistant_TRADING_RULES_V2` / `MASTER_TRADING_RULES_V2.json`.

## Rule boundary

The project has 51 Murphy candidate rules in the Master KB. Rules **MURPHY_0001–MURPHY_0012 are the frozen/previously handled set**. The active 39-rule queue is therefore exactly **MURPHY_0013–MURPHY_0051**.

## Canonical 39-rule order

13. Symmetrical triangle
14. Ascending triangle
15. Descending triangle
16. Flag continuation
17. Pennant continuation
18. Falling wedge
19. Rising wedge
20. Rectangle breakout
21. Volume confirms price action
22. Price up + volume up + OI up
23. Price down + volume up + OI up
24. Moving-average trend filter
25. Four-week breakout
26. Four-week breakdown
27. Oscillator regime filter
28. Bearish divergence warning
29. Bullish divergence warning
30. P&F bullish support
31. P&F long stop placement
32. P&F short stop placement
33. Candlestick context filter
34. Wave 2 rule
35. Wave 3 shortest rule
36. Wave 4 overlap rule
37. Common retracement zones
38. Cycle period
39. System discipline
40. Parabolic SAR regime limitation
41. ADX regime filter
42. Capital reserve
43. Single-market exposure
44. Maximum risk per market
45. Total margin limit
46. Top-down breadth analysis
47. Bearish A/D divergence
48. High TRIN oversold warning
49. Low TRIN overbought warning
50. Multi-factor checklist before trade
51. Pre-trade plan completeness

## Current source-readiness split from Trading Rules V2

`READY_FOR_BACKTEST.json` contains: 13–20, 25–26, 28–29, 47.

`INCOMPLETE_NEEDS_DEFINITION.json` contains: 21–24, 27, 30–46, 48–51.

This split is a workflow/readiness classification, **not a PASS/FAIL or production-freeze decision**.

## Execution rule

Work in canonical numeric order unless a compatibility dependency requires an earlier shared primitive first. For each rule: compatibility audit -> reuse existing primitive -> define evaluator -> tests -> availability/no-lookahead -> historical QA -> explicit freeze decision.

No rule is promoted merely because it exists in `READY_FOR_BACKTEST.json`. No invented semantics, no silent threshold selection, and no 2025 tuning.

## Immediate batch

The next four canonical rules are **MURPHY_0013–MURPHY_0016**. They are already classified as READY_FOR_BACKTEST, so this is the next execution batch after the current P&F work. The batch must use their existing source definitions and must not import Nison confirmation semantics into Murphy.
