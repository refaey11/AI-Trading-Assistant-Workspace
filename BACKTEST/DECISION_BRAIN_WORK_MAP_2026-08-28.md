# Decision Brain — Fixed Execution Map

## Where we are
**CURRENT PHASE: Governed Integration / Runner Completion**

## Completed
- Core knowledge/components recovered and present.
- Murphy 34 and Nison 44 historical evidence sources present.
- Market State source + compatibility boundary present.
- Dynamic MTF binding/runtime boundary present.
- Historical Context Memory boundary present.
- Historical Outcome Memory boundary present.
- Similarity Memory V2 present.
- Context-Aware Retrieval V2 present.
- TIZ process gate present.
- Risk/Execution integration present.
- Recovered Decision Brain V1 present.
- Knowledge/Decision handoff present.
- Backtest-only branch and Integration Gate created.

## Current blocker
The existing `DEV_BACKTEST_RUNNER_V1.py` is simplified and still uses hardcoded/default governance inputs in places. It must be replaced/updated to use the real source-backed adapters and boundaries for every timestamp.

## Fixed runtime architecture
1. GBPUSD H1 authoritative bars.
2. Market State contract normalization.
3. Dynamic MTF role binding.
4. Murphy evidence aggregation.
5. Nison confirmation/contradiction aggregation.
6. Historical Context Memory as-of lookup.
7. Historical Outcome Memory as-of lookup.
8. Similarity Memory as evidence metadata only.
9. Context-Aware Retrieval as evidence/context only.
10. TIZ process gate.
11. Risk/Execution gate using actual upstream SL/TP/ATR inputs.
12. Knowledge/Decision handoff.
13. Recovered Decision Brain V1 assessment unchanged.
14. Execution eligibility gate.
15. Bar-by-bar Backtest 2016–2024.
16. Validation manifest and metrics.

## Governance rules
- Murphy can provide directional context.
- Nison confirms/contradicts, not independent direction.
- Memory and Similarity never generate direction.
- Retrieval never generates direction.
- TIZ never generates direction.
- Risk is a hard gate.
- 2025 is locked OOS and cannot be used for tuning.
- No legacy backtest is substituted for the current 78-rule evaluation.

## Required preflight gate
The full Backtest MUST NOT run unless the Integration Gate can demonstrate, on real source-backed samples:
- timestamp/as-of alignment for all available layers;
- no future data leakage;
- Market State reaches the Decision Brain row;
- MTF evidence reaches the Decision Brain row;
- Murphy and Nison evidence reach the handoff;
- Context/Outcome Memory records reach the evidence package when available;
- Similarity/Retrieval reach the evidence package without creating direction;
- TIZ and Risk are evaluated by their real adapters, not hardcoded PASS values;
- recovered Decision Brain V1 remains unchanged.

## Final validation gate
Only after Integration Gate = PASS and runner compatibility tests = PASS:
- run the 2016–2024 development Backtest;
- inspect execution funnel;
- inspect executed trades;
- inspect metrics;
- require frozen cost/slippage validation before any official profitability claim.

## 2025
2025 remains OOS-locked. No tuning, threshold changes, or rule changes may be based on 2025.

## Next chat instruction
Do not start over. Resume at: **Complete governed runner integration, prove the full evidence flow, then run 2016–2024 Backtest once.**
