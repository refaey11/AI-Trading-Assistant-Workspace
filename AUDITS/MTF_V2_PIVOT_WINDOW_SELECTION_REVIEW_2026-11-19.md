# MTF Pivot Detector V2 — Per-Timeframe Window Selection Review V1

**Status:** methodology proposal only — no numeric L/R configuration approved.
**Date:** 2026-11-19
**Parent:** PR #141
**Scope:** M5, M15, M30, H1, H4, D1 only.

## 1. Finding

The accessible repository evidence does not establish canonical numeric left/right lookbacks for the six target timeframes. The historical Murphy 0008 report establishes a two-bar pivot availability delay for its audited H1 output only. It does not prove that the historical detector used L=2, R=2, nor that the same setting applies to other timeframes.

No source-backed basis was found to assign different numeric windows to M5, M15, M30, H1, H4, and D1. A timeframe-specific table filled with numbers now would therefore be an undocumented heuristic, not a recovered project rule.

## 2. Recommended evaluation design (not production settings)

Use a controlled symmetric candidate grid for sensitivity testing only:

| Candidate | L | R | Status |
| --- | ---: | ---: | --- |
| W2 | 2 | 2 | exploratory test candidate |
| W3 | 3 | 3 | exploratory test candidate |
| W5 | 5 | 5 | exploratory test candidate |

Apply the same candidate grid independently to each timeframe's synthetic fixtures. This isolates the effect of window size without claiming that bar-count settings are economically equivalent across timeframes.

These values are test points, not a recommendation that any one should be selected. They must not be used to rank profitability, optimize trading outcomes, or tune against 2025.

## 3. Required per-timeframe sensitivity matrix

| Timeframe | W2 (2/2) | W3 (3/3) | W5 (5/5) | Production L/R |
| --- | --- | --- | --- | --- |
| M5 | synthetic sensitivity only | synthetic sensitivity only | synthetic sensitivity only | NOT APPROVED |
| M15 | synthetic sensitivity only | synthetic sensitivity only | synthetic sensitivity only | NOT APPROVED |
| M30 | synthetic sensitivity only | synthetic sensitivity only | synthetic sensitivity only | NOT APPROVED |
| H1 | synthetic sensitivity only | synthetic sensitivity only | synthetic sensitivity only | NOT APPROVED |
| H4 | synthetic sensitivity only | synthetic sensitivity only | synthetic sensitivity only | NOT APPROVED |
| D1 | synthetic sensitivity only | synthetic sensitivity only | synthetic sensitivity only | NOT APPROVED |

No market-data performance metric is part of this selection exercise. The comparison is structural: when does a candidate become confirmed, how many bars are required, what happens at the truncated boundaries, and do future perturbations leave past outputs unchanged?

## 4. Synthetic fixture requirements for each window candidate

For every timeframe and each W2/W3/W5 candidate, construct deterministic bars that prove:

1. An isolated high/low is not confirmed until all R right-side bars are completed.
2. The candidate's available_at equals the verified availability of the final confirming bar.
3. An equal-high/equal-low plateau is NOT_EVALUABLE under the approved strict/tie policy.
4. A missing source bar inside the right window blocks confirmation unless upstream continuity evidence explicitly proves the sequence.
5. Same-bar high/low candidates retain unresolved ordering.
6. A candidate near the beginning/end of the supplied range is represented as pending/unavailable, never prematurely confirmed.
7. Perturbing bars after a decision timestamp cannot alter any output already available at that timestamp.
8. Replaying identical inputs/configuration yields byte-identical pivot identities and output.
9. The number of required warm-up bars is exactly sufficient for L and no pre-window seed is accepted without identity and provenance.

These fixtures validate implementation semantics only; they do not establish which numeric window is best for a live market.

## 5. Selection principles

Numeric L/R may be frozen only when:
- a canonical source contract is recovered and passes compatibility review; or
- the user explicitly selects a documented configuration after reviewing the synthetic behavior and accepts that it is a new V2 policy, not historical parity.

Do not infer L from the historical H1 availability delay. Right-side confirmation R and left-side comparison L are different concepts; an availability delay alone does not establish the complete candidate definition.

Do not infer settings from candle duration, ATR, volatility, market session, trade frequency, win rate, or profitability without an independently approved methodology. Do not use 2025 under any circumstances for selection or tuning.

## 6. Next approval gate

Review the W2/W3/W5 test grid as a sensitivity set, not as chosen production parameters. After synthetic fixtures are produced, choose exact L/R per timeframe explicitly. Until then:
- no detector code;
- no production configuration;
- no backtest or 2025 tuning;
- no Brain integration or live order path;
- PR #141 remains Draft and unmerged.
