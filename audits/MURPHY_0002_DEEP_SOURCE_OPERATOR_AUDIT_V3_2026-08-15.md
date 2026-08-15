# Murphy 0002 — Deep Source / Operator Audit V3

Date: 2026-08-15
Status: SOURCE VERIFIED / SEMANTICS VERIFIED / OPERATOR CONTRACT NOT FROZEN

## Scope searched
- Current File Library / uploaded project artifacts
- Murphy source copies and Chapter 1 timing material
- Existing project handoffs and rule registry
- Dynamic MTF / Rule Adapter / evaluator architecture
- GitHub repository and Git history
- External Murphy text references for Trading Tactics / timing

## Source conclusion
MURPHY_0002 is the rule "Direction is not enough" under Chapter 1 / Trading Rules and Timing. The project source record states that a correct directional forecast still requires appropriate entry and exit timing, and a directional view without an executable timing condition is not a trade setup. The source record is UNTESTED.

## Murphy source evidence
Murphy separates analysis/forecasting from timing. Timing determines specific entry and exit points and is predominantly technical. In the Trading Tactics discussion, Murphy describes timing as very-short-term action and identifies technical timing tools including trendline breaks, support/resistance, percentage retracements, price gaps, and combinations of these. He also states that intraday charts are useful for timing once the basic decision to enter/exit has been made.

## What the project can safely infer
The operational meaning can be represented as a GATE:
1. A directional view exists.
2. A source-compatible technical timing condition must also be present.
3. Direction without timing evidence is not a trade setup.
4. Missing timing evidence remains NOT_EVALUABLE, not PASS.

## What cannot yet be frozen
The source does NOT select one universal timing primitive, one fixed lower timeframe, one universal lookback, or one numeric threshold for all markets/rules. The project workspace also does not contain a previously frozen 0002-specific timing operator contract. Therefore selecting M5/M15/H1, RSI/MACD, a custom threshold, or a hidden lookback would be an invented rule.

## Existing infrastructure
The project has Dynamic MTF, Trendline Geometry, support/resistance/market-structure infrastructure, Rule Adapter infrastructure, and evaluator/test infrastructure. Availability of these components does not prove that any one is the authoritative 0002 timing operator.

## Decision
Do NOT freeze 0002 and do NOT claim historical QA is complete.
The correct current state is:
SOURCE VERIFIED / SEMANTICS VERIFIED / OPERATIONAL TIMING GATE CONCEPT VERIFIED / EXACT OPERATOR NOT FROZEN.

## Minimal next closure path
Create a project-level timing evidence interface only if governance explicitly approves it. The interface should accept already-authoritative timing evidence from existing producers (rather than inventing new indicators), with states AVAILABLE / NOT_EVALUABLE and a source/provenance reference. Then:
- implement the smallest 0002 evaluator around that interface;
- deterministic unit tests;
- 2016–2024 historical QA;
- availability/no-lookahead audit;
- provenance/freeze manifest;
- 2025 remains OOS.

## Prohibited shortcuts
- No arbitrary timeframe selection.
- No RSI/MACD substitution unless an authoritative 0002 source contract names it.
- No backtest optimization to choose a timing primitive.
- No 2025 tuning/selection.
- No proxy substitution for missing timing evidence.

## Historical status note
The prior V1 workspace verification report said SOURCE RECORD NOT RECOVERED. That statement is superseded by this audit because the source record was subsequently recovered. However, the older report remains preserved as historical provenance.
