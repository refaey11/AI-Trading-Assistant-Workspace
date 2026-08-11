# Project Revisit Queue V1

Date: 2026-08-12

Purpose: ensure unresolved gates are explicitly recorded and revisited after the forward-pass work, without losing provenance or repeatedly blocking the project.

## Deferred / revisit items

### Murphy 0006–0007
Status: WORKING MAPPING RESOLVED / EVALUATOR NOT CLOSED
- 0006 → LOW + UP → BULLISH
- 0007 → HIGH + DOWN → BEARISH
- Existing Trendline Geometry V1 must be checked for explicit third-touch, successful-reaction, no-break, and availability evidence.
- Do not invent numeric tolerance.
- Revisit after forward-pass rule groups.

### Murphy 0008–0009
Status: SOURCE SEMANTICS PARTIAL / OPERATOR NOT CLOSED
- 0008 → support decisively broken downside
- 0009 → resistance decisively broken upside
- Exact decisive-break operator must come from authoritative source/contract.
- Do not invent ATR, percentage, candle-count, wick/close, or lookback thresholds.

### Murphy 0010
Status: SOURCE/OPERATOR REVIEW REQUIRED
- Time/price filter before accepting a break as meaningful.
- Keep separate from the 0008/0009 break event until source contract is verified.

### Murphy 0003–0004
Status: SEPARATE PROVENANCE ISSUE / NOT FROZEN
- 0003 requires higher peaks AND higher troughs.
- 0004 requires lower peaks AND lower troughs.
- Historical provenance mismatch remains separate and must not be altered to solve later rules.

### Official Uniform Walk-Forward
Status: NOT FINAL
- Requires fresh uniform five-asset end-to-end rerun and leakage audit.
- 2025 remains OOS and cannot be used for tuning or implementation selection.

## Revisit policy

1. Continue forward through rules/components that can be closed from existing source and artifacts.
2. Never silently downgrade or delete a blocker.
3. Return to this queue after the forward-pass milestone and resolve each item using source → compatibility → evaluator → tests → QA → freeze.
4. No Decision Brain production freeze until required gates are closed.
