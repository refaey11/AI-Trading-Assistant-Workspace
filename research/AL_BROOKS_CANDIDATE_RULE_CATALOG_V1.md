# Al Brooks Candidate Rule Catalog V1 (Research Only)

Status: RESEARCH_CANDIDATES — NOT GOVERNED STRATEGY RULES
Sources: user-provided EPUB, Trading Price Action Trends (Al Brooks, 2012); user-provided PDF, Trading Price Action Trading Ranges (Al Brooks, 2012).
Purpose: translate source concepts into falsifiable research hypotheses without changing frozen Murphy/Nison governance or generating live trade signals.

## Governance boundary

- Murphy remains technical-context / directional-structure authority.
- Nison remains confirmation-or-contradiction only; it does not generate direction.
- Trading in the Zone remains a process/psychology gate only.
- Brooks concepts below are research-only candidate features. They cannot override Murphy, Nison, TIZ, the Risk Engine, or the 2025 locked OOS policy.
- Do not tune or select candidates on 2025. Use development data before a separately governed, untouched OOS evaluation.
- No BUY/SELL automation is authorized by this document. Missing/ambiguous evidence must remain NOT_EVALUABLE / NO_TRADE.
- This catalog paraphrases research concepts; it does not claim that the books establish profitable expectancy.

## Candidate hypotheses

| ID | Source concept | Candidate observable definition | Hypothesis to test | Failure / no-signal condition |
|---|---|---|---|---|
| AB-TREND-01 | Trend versus trading-range spectrum (Trends, Ch. 1) | Classify local structure using predeclared, causal features: directional swing progression, bar overlap, and pullback size. | Trend-context classification separates continuation behavior from two-sided/range behavior. | Features disagree, lookback insufficient, or regime label changes materially across adjacent reasonable windows. |
| AB-TREND-02 | Strength of trend (Trends, Ch. 19) | Count causal trend-strength features such as directional bars, limited overlap, and trending swing highs/lows over a fixed lookback. | Stronger trend context changes conditional outcomes of with-trend versus countertrend setups. | No predeclared minimum evidence or mixed feature readings. |
| AB-TREND-03 | Breakout followed by follow-through (Trends, Ch. 3; Ranges, Ch. 2) | Breakout beyond a pre-existing, algorithmically defined level; measure next-bar and multi-bar follow-through without look-ahead. | Follow-through features help distinguish continuation breakouts from failures. | Level not known before breakout, or signal uses bars not yet closed at decision time. |
| AB-TREND-04 | Pullback within a trend (Trends, Ch. 4; Ranges, Ch. 11) | After trend classification, identify a counter-move against the trend and measure depth/duration relative to the prior impulse. | Pullback context may distinguish continuation from trend deterioration. | Trend not established or pullback boundaries are subjective/non-reproducible. |
| AB-TREND-05 | Channel overshoot / wedge (Trends, Ch. 14; Ranges, Ch. 18) | Fit channel boundaries using only past bars; mark boundary overshoot and subsequent close back inside. | Overshoot/re-entry may predict mean reversion or a larger correction versus a matched baseline. | Channel fit requires future bars or pattern is not mechanically reproducible. |
| AB-RANGE-01 | Failed breakout and breakout test (Ranges, Ch. 5) | Price crosses a predefined prior swing/range boundary, then closes back inside within a fixed, preregistered number of bars. Track immediate failure separately from later retest. | Failed-breakout patterns have different forward-return distributions from successful breakouts. | Boundary subjective, failure window chosen after seeing results, or costs erase any effect. |
| AB-RANGE-02 | Trading-range context (Ranges, Ch. 21–23; Trends, Ch. 1) | Identify a range using fixed lookback, bounded high/low, and predeclared overlap/volatility criteria. | Range-context setups differ from trend-context setups; range boundaries may act as conditional reference levels. | Range criteria not fixed before evaluation or regime cannot be classified. |
| AB-RANGE-03 | Breakout pullback (Ranges, Ch. 5) | After a confirmed breakout, price retests the breakout level and does not invalidate the breakout under a predeclared rule. | Retest entries may differ in adverse excursion and follow-through from entering on the initial breakout. | Retest outside allowed horizon or breakout invalidated. |
| AB-RANGE-04 | Support/resistance as magnets; measured move (Ranges, Ch. 7–10) | Calculate prior swing levels and projected distances from a completed impulse/range using a fixed formula. | These levels may describe where price stalls/reverses; test as outcome labels or risk-management features before considering entries. | Projection formula or anchor points selected retrospectively. |
| AB-RISK-01 | Trader's equation / trade selection (Ranges, Ch. 25) | For each hypothetical setup, record estimated win probability, target reward, stop risk, costs, and realized outcome using a consistent execution model. | Candidate survives only if net expectancy and drawdown are acceptable out of sample. | Probability estimates uncalibrated, costs omitted, or reward/risk calculated using future knowledge. |
| AB-RISK-02 | Need two reasons to take a trade (Ranges, Ch. 26) | Require two independently defined pieces of evidence before a candidate is marked research-eligible; keep evidence sources explicit. | A multi-evidence filter may improve quality versus a single-feature baseline. | Reasons are correlated duplicates, selected after outcome, or used to override existing governance. |

## Evaluation protocol (freeze before running)

1. Data integrity: timestamp-sort bars; validate duplicates, gaps, timezone, OHLC consistency, symbol/timeframe metadata.
2. Causality: every feature must be computable at decision timestamp using closed bars only. Record exact decision timestamp and source-bar range.
3. Baseline first: compare each candidate with a simple no-feature baseline and matched setup baseline; report all tested candidates, not just winners.
4. Execution realism: apply spread, commission, slippage, contract size, pip/tick value, stop/target fill assumptions, and realistic intrabar ordering. If required cost/contract fields are missing, mark NOT_EVALUABLE.
5. Metrics: trade count, coverage, win rate, average win/loss in R, net expectancy in R, profit factor, max drawdown in R, adverse/favorable excursion, sensitivity by symbol/timeframe/regime.
6. No leakage: do not use 2025 for feature design, thresholds, candidate selection, or calibration. Any eventual 2025 evaluation must be one frozen evaluation with recorded artifact and provenance.
7. Multiple testing: register candidate IDs and parameters before running; preserve negative results and disclose number of variants tested.
8. Governance: candidate output is evidence only. It cannot create direction or bypass Murphy, Nison, TIZ, or Risk Engine gates.

## Required output for every tested candidate

- Candidate ID and source chapter
- Exact formula / code version / parameters
- Data slice and timestamp range
- Eligible observations and exclusions
- Gross and net metrics, cost model, drawdown
- Baseline comparison and uncertainty estimate
- Failure cases and known limitations
- Artifact hash and reproducible run command
- Status: UNTESTED, NOT_EVALUABLE, REJECTED, or PROMOTE_FOR_REVIEW

## Initial priority

1. AB-TREND-01 and AB-RANGE-02: causal regime classification.
2. AB-TREND-03 and AB-RANGE-01: breakout follow-through versus failed breakout.
3. AB-TREND-04 and AB-RANGE-03: pullback / breakout-retest behavior.
4. AB-TREND-05 and AB-RANGE-04: more subjective geometry/projection concepts, only after deterministic definitions exist.
5. AB-RISK-01 and AB-RISK-02: evaluation/selection protocol, not standalone directional signals.

No candidate is promoted by this document. First implement deterministic feature extraction and audit the event table; only then run a development-period experiment with costs.
