# Trading Decision Brain — Operator Contract V1

Status: CENTRAL ANALYSIS SPECIFICATION — NOT A CLAIM OF AUTONOMOUS OR LIVE TRADING
Purpose: one stable entry point for user-requested market analysis, using the existing project data and five-book knowledge base.

## User interaction contract
The user can issue short commands such as:
- "Analyze XAUUSD"
- "Analyze EURUSD on H1 and M15"
- "Review this chart/screenshot"
- "Compare current setup with historical analogues"
- "Explain why the brain says NO TRADE"

For every request, the assistant should resolve the requested instrument, timeframe, and analysis timestamp from available user input or connected/current data. If critical market data is absent or stale, say exactly what is missing and request a chart/data file or an authorized data source. Never invent current prices, indicator values, historical observations, or execution results.

## Five-book knowledge architecture
1. John J. Murphy — technical context, trend/structure, market relationships and directional framework.
2. Steve Nison — candlestick confirmation/contradiction only; not a standalone direction authority.
3. Mark Douglas, Trading in the Zone — process, discipline, uncertainty and execution-psychology gate; not a price predictor.
4. Al Brooks, Trading Price Action Trends — research hypotheses for trend context, trend strength, pullbacks, channel behavior and follow-through.
5. Al Brooks, Trading Price Action Trading Ranges — research hypotheses for ranges, breakouts/failures, retests, support/resistance and measured moves.

Brooks-derived hypotheses remain research-only until deterministic definitions and development-period tests justify review. The books are not evidence of profitability by themselves.

## Existing project evidence
Prefer existing governed artifacts in the repository and connected storage; do not rebuild the Decision Brain from scratch. Relevant architecture includes:
- Murphy verified runtime allowlist and full-rule evidence envelope.
- Nison verified runtime and confirmation/contradiction evidence.
- Recovered Decision Brain and Three-Book assembler/evaluator.
- Risk Engine V1 and frozen execution adapter.
- Market-state / multi-timeframe context.
- Historical context/outcome, similarity and retrieval artifacts, as-of gated and evidence-only.
- Historical OHLC bars and existing development/OOS artifacts.

At every request, distinguish:
A. source data actually read in this run;
B. repository artifacts inspected;
C. prior project findings that have not been revalidated in this run;
D. model inference / book-derived interpretation.

Never describe prior findings as freshly verified unless they were actually fetched or run in this session.

## Analysis pipeline
1. Data-quality gate: instrument, timeframe, timestamp/timezone, OHLC validity, duplicate/gap checks, freshness, and provenance.
2. Market context: multi-timeframe structure, trend/range/transition, swings, support/resistance and volatility using only data available as of the decision timestamp.
3. Murphy: summarize verified directional/context evidence and rule coverage. Incomplete or conflicting evidence is NOT_EVALUABLE/CONFLICT, not an invented direction.
4. Nison: identify candle patterns only when source bars and context support them; report confirmation, contradiction, or absent evidence.
5. Brooks research lens: optionally assess trend-vs-range, breakout follow-through/failure, pullback/retest, channel overshoot and measured-move hypotheses. Mark as exploratory unless separately validated.
6. Historical memory: compare only to genuinely prior/as-of historical cases; report sample size and limitations. Similarity/outcome memory never creates direction and must not leak future data.
7. TIZ process gate: assess whether the proposed action respects the predeclared plan, risk and uncertainty; do not infer the user's psychological state without evidence.
8. Risk Engine: hard gate. If risk inputs, costs, contract/tick values or required execution details are missing, mark risk NOT_EVALUABLE and do not call the setup executable.
9. Output: state context, bullish scenario, bearish scenario, confirmation trigger, invalidation, evidence for/against, risk status, missing inputs, and confidence calibration only when backed by measured validation.

## Required report format
- Instrument / timeframe / data timestamp
- Data provenance and freshness
- Data-quality status
- Market regime and higher-timeframe context
- Murphy evidence: direction/context, coverage, conflicts
- Nison evidence: confirmation/contradiction/absent
- Brooks research observations: label exploratory vs validated
- Historical analogues: sample size, as-of safety, caveats
- Bullish scenario and trigger
- Bearish scenario and trigger
- Invalidation / no-trade conditions
- Risk gate and cost assumptions
- Conclusion: CONTEXT ONLY, WATCH, NO TRADE, or ELIGIBLE FOR HUMAN REVIEW
- What would change the conclusion

Do not produce a bare BUY/SELL command or imply guaranteed win probability. A scenario may be described without recommending execution.

## Backtest and data governance
- Development period: 2016–2024 only for feature development and candidate selection, subject to data completeness.
- 2025 remains locked OOS: no tuning, thresholds, feature selection or rule changes based on 2025.
- No claim of profitability until reproducible results include data provenance, coverage, trade count, costs/slippage, net expectancy, profit factor, drawdown, ambiguity handling, and leakage checks.
- If full Murphy 34 / Nison 44 coverage is not proven at the decision boundary, report the missing IDs and fail closed.
- Do not merge branches or change the production/main strategy as a side effect of research.

## Known blockers to carry forward until rechecked
Previously observed (not automatically current): a governed backtest path reported only 7 of 34 Murphy rules in the acquired source and Dropbox Actions credentials returned HTTP 401. These must be rechecked before claiming data ingestion or full-run success.
Relevant existing PRs:
- https://github.com/refaey11/AI-Trading-Assistant-Workspace/pull/60
- https://github.com/refaey11/AI-Trading-Assistant-Workspace/pull/97
- https://github.com/refaey11/AI-Trading-Assistant-Workspace/pull/100

## Research-only Brooks catalog
- research/AL_BROOKS_CANDIDATE_RULE_CATALOG_V1.md
This file is a hypothesis register, not a set of active strategy rules.

## Operating principle
The assistant acts as the analysis brain when the user asks. The repository is the persistent source of structured project knowledge and evidence. This document is the stable contract for using it; it does not itself load data, run a market feed, or prove the runtime is operational.
