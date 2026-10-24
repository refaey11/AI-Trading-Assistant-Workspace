# Al Brooks Candidate Rule Catalog V1 (Research Only)

Status: RESEARCH_CANDIDATES — NOT GOVERNED STRATEGY RULES
Sources: user-provided EPUB, *Trading Price Action Trends* (Al Brooks, 2012); user-provided PDF, *Trading Price Action Trading Ranges* (Al Brooks, 2012).

## Governance boundary
- Murphy remains technical-context / directional-structure authority.
- Nison remains confirmation-or-contradiction only; it does not generate direction.
- Trading in the Zone remains a process/psychology gate only.
- Brooks concepts are research-only candidate features. They cannot override Murphy, Nison, TIZ, or the Risk Engine.
- Do not tune or select candidates on 2025. Use 2016–2024 development data only, then require a separately governed untouched OOS evaluation.
- No BUY/SELL automation is authorized by this document. Missing/ambiguous evidence remains NOT_EVALUABLE / NO_TRADE.
- This catalog paraphrases research concepts; it does not claim that the books establish profitable expectancy.

## Candidate hypotheses

| ID | Source concept | Candidate observable definition | Hypothesis | Failure / no-signal condition |
|---|---|---|---|---|
| AB-TREND-01 | Trend vs. trading-range spectrum (*Trends*, Ch. 1) | Causal directional swing progression, bar overlap, pullback size | Regime classification separates continuation from two-sided behavior | Insufficient lookback, conflicting features, unstable label |
| AB-TREND-02 | Trend strength (*Trends*, Ch. 19) | Fixed-lookback directional bars, overlap, swing progression | Trend strength changes conditional outcomes of with-trend/countertrend setups | No predeclared minimum evidence |
| AB-TREND-03 | Breakout and follow-through (*Trends*, Ch. 3; *Ranges*, Ch. 2) | Cross a level defined before breakout; measure next-bar/multi-bar follow-through | Follow-through separates continuation from failure | Future bars used to define level or signal |
| AB-TREND-04 | Trend pullback (*Trends*, Ch. 4; *Ranges*, Ch. 11) | Counter-move depth/duration relative to prior impulse | Pullback context distinguishes continuation from deterioration | Trend or boundaries not mechanically defined |
| AB-TREND-05 | Channel overshoot / wedge (*Trends*, Ch. 14; *Ranges*, Ch. 18) | Past-bars-only channel fit; overshoot and close back inside | Re-entry may predict correction vs matched baseline | Channel uses future bars or subjective geometry |
| AB-RANGE-01 | Failed breakout (*Ranges*, Ch. 5) | Cross a predefined boundary, then close back inside within a fixed window | Failed and successful breakouts have different forward-return distributions | Retrospective boundary/window selection |
| AB-RANGE-02 | Trading-range context (*Ranges*, Ch. 21–23; *Trends*, Ch. 1) | Fixed lookback, bounded high/low, overlap/volatility criteria | Range setups differ from trend setups | Criteria not frozen or regime unclassifiable |
| AB-RANGE-03 | Breakout pullback/retest (*Ranges*, Ch. 5) | Retest confirmed breakout level without invalidation within fixed horizon | Retest differs from initial breakout in adverse excursion/follow-through | Retest late or breakout invalidated |
| AB-RANGE-04 | Support/resistance magnets; measured move (*Ranges*, Ch. 7–10) | Prior swing levels and fixed projections from completed impulse/range | Levels may explain stalls/reversals; test as features before entries | Retrospective anchors/projection formula |
| AB-RISK-01 | Trader's equation (*Ranges*, Ch. 25) | Record probability estimate, reward, risk, costs and realized outcome consistently | Candidate survives only with acceptable net expectancy/drawdown out of sample | Uncalibrated probabilities or omitted costs |
| AB-RISK-02 | Two reasons to take a trade (*Ranges*, Ch. 26) | Require two independently defined evidence features for research eligibility | Multi-evidence filter may improve over single-feature baseline | Correlated duplicate reasons or post-hoc selection |

## Frozen evaluation protocol
1. Validate timestamps, duplicates, gaps, timezone, OHLC consistency, symbol/timeframe metadata.
2. Compute features using closed bars only; record decision timestamp and source-bar range.
3. Compare each candidate against a simple baseline and matched setup baseline; report all tested candidates.
4. Include spread, commission, slippage, contract/tick values, and realistic intrabar stop/target ordering. If required cost fields are missing, mark NOT_EVALUABLE.
5. Report trade count, coverage, win rate, average win/loss in R, net expectancy in R, profit factor, max drawdown in R, adverse/favorable excursion, and symbol/timeframe/regime breakdowns.
6. 2025 is locked: no feature design, thresholds, selection, or calibration on it.
7. Register candidate IDs/parameters before testing; preserve negative results and disclose variants tested.
8. Brooks evidence cannot create direction or bypass Murphy, Nison, TIZ, or Risk Engine.

## Required report per candidate
Candidate ID/source chapter; formula/code version/parameters; data slice; eligible observations/exclusions; gross/net metrics and cost model; baseline comparison and uncertainty; failure cases; artifact hash and reproducible command; status UNTESTED, NOT_EVALUABLE, REJECTED, or PROMOTE_FOR_REVIEW.

## Priority order
1. AB-TREND-01 and AB-RANGE-02: deterministic regime classification.
2. AB-TREND-03 and AB-RANGE-01: breakout follow-through vs failure.
3. AB-TREND-04 and AB-RANGE-03: pullback/retest.
4. AB-TREND-05 and AB-RANGE-04 only after deterministic definitions exist.
5. AB-RISK-01 and AB-RISK-02 are evaluation/selection protocols, not directional signals.

No candidate is promoted by this catalog. Implement deterministic feature extraction and audit the event table before any development experiment with costs.
