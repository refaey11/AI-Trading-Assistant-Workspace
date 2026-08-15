# MURPHY 0030 — COMPATIBILITY AUDIT V2 FINDINGS
Date: 2026-08-15
Status: IN PROGRESS — FEATURE PATH FOUND; RULE CONTRACT PARTIALLY SOURCE-LOCKED

## 1. Authoritative project rule record recovered
The current Master Knowledge Base `02_Trading_Rules/MASTER_CANDIDATE_RULES_V1.json` contains the authoritative candidate record for `MURPHY_0030`.

Rule identity:
- Rule ID: MURPHY_0030
- Book: Technical Analysis of the Financial Markets
- Chapter: 11
- Section: Point and Figure
- Setup name: P&F bullish support
- Direction: BULLISH
- Conditions: price structure represented through X/O columns; use the bullish support trendline as a structural reference.
- Decision logic: use P&F trendlines as structural guides; confirm with the specific P&F signal rules.
- Testing status in the source record: UNTESTED.

This resolves the earlier claim that the exact 0030 rule identity was unavailable. The rule record is recoverable from the uploaded Master KB archive.

## 2. Murphy source semantics recovered from Chapter 11
The source describes the 3-point/3-box reversal Point & Figure method and its trendlines:
- 3-box reversal is the intermediate-trend method discussed by Murphy.
- The 3-box chart is constructed from high/low prices.
- On 3-point-reversal charts, trendlines are drawn at 45-degree angles.
- The bullish support line is drawn at a 45-degree angle upward to the right from under the lowest column of O's.
- As long as prices remain above that line, the major trend is considered bullish.
- Murphy also states that the line may need adjustment after a correction; a new support line can be drawn from the bottom of the reaction low.

The source therefore gives a source-faithful structural operator for 0030: P&F 3-box-reversal bullish support context, with price remaining above the bullish support line.

## 3. What the source does NOT uniquely fix for this project
Murphy's text states that a value must be assigned to each box and that the Chartcraft service supplied the already-constructed charts/assigned box values. The text demonstrates different box sizes (e.g. 3, 5, 10) and explains that box size changes sensitivity. Therefore the book does NOT provide one universal GBPUSD project box-size value that can be silently hard-coded from the examples.

Do NOT select a box size by optimizing on historical outcomes.
Do NOT import a percentage/ATR/pip box-size rule from another P&F system and call it Murphy.
Do NOT use 2025 to choose the box-size policy.

## 4. External implementation discovery
A current open-source P&F engine was found:
- `pnf-chart-system` / PyPI package `pnf-chart-system` (Python import `pypnf`), MIT licensed.
- It supports HighLow construction, configurable box-size method, reversal, X/O columns, bullish-support/bearish-resistance context, support/resistance, signals, patterns, and data adapters including MetaTrader/CSV.
- Its documented quick-start configuration explicitly supports `ConstructionMethod.HighLow`, `BoxSizeMethod.Traditional`, and `reversal = 3`.
- The package documentation also exposes a direct bullish-support structural check.

This is an implementation candidate only. It is NOT yet integrated into the project.

## 5. Compatibility conclusion
The previous `FEATURE UNAVAILABLE` conclusion is superseded for discovery purposes: a reusable external implementation candidate exists.

However, the rule is NOT yet Production Frozen because the project still needs to prove:
1. the engine's HighLow/3-box construction reproduces Murphy's source semantics exactly enough for 0030;
2. the box-size policy is explicitly approved/source-faithful rather than chosen by tuning;
3. the engine's bullish-support output and availability timestamps are compatible with the project's no-lookahead model;
4. the same implementation can be replayed deterministically over the required historical population;
5. unit tests, 2016–2024 QA, availability/leakage audit, provenance and freeze are completed.

## 6. Important no-rebuild decision
Do NOT build a new P&F engine yet.
First compatibility-test the discovered engine against Murphy 0030. If compatible, integrate the smallest adapter required. If incompatible, identify the smallest missing behavior rather than replacing the whole engine.

## 7. Current exact status
MURPHY_0030 = IN PROGRESS / COMPATIBILITY AUDIT

Resolved:
- rule identity/source record
- Chapter 11 provenance
- bullish-support semantic direction
- 3-box reversal / HighLow source path
- existence of a reusable external P&F implementation candidate

Still open:
- project-approved box-size policy
- engine behavior equivalence
- availability/no-lookahead contract
- deterministic evaluator
- 2016–2024 historical QA
- freeze manifest

## 8. Next exact action
Run a source-faithful compatibility harness using the candidate P&F engine and canonical project GBPUSD OHLC. Do not tune box size. The harness must first test the engine's deterministic construction and bullish-support context against Murphy's Chapter 11 semantics and the project availability model.

This rule remains the active work item. Do not advance to 0031 until 0030 reaches either FROZEN or a formally approved BLOCKED state with the exact blocker recorded.
