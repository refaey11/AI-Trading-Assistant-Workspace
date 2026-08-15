# Murphy 0002 — Timing Evidence Contract V1
Date: 2026-08-15
Status: GOVERNANCE CONTRACT — NOT YET PRODUCTION FROZEN

## Source semantics
MURPHY_0002 / Chapter 1 / Trading Rules and Timing: a correct directional forecast still requires appropriate entry and exit timing. A directional view without an executable timing condition is not a trade setup.

Murphy's source treats timing as a technical trading-tactics layer for specific entry and exit points. It does not prescribe one universal indicator, threshold, or fixed timeframe for this rule.

## Critical architectural conclusion
0002 is a META-RULE / EXECUTION-TIMING GATE, not a standalone directional signal.
It must not invent an RSI, MACD, fixed MTF, percentage, ATR, or other threshold.

## Operational contract
The 0002 evaluator consumes timing evidence produced by already-authorized technical timing modules/rules.

Inputs:
- directional_view (from an existing authorized directional/context producer)
- entry_timing_evidence
- exit_timing_evidence
- availability timestamps for the evidence

Outputs:
- PASS: directional view exists AND required entry/exit timing evidence is available and chronologically valid.
- NOT_EVALUABLE: required timing evidence is unavailable or its availability timestamp is missing/after the decision point.
- FAIL / NO_TRADE: directional view exists but the required executable timing condition is absent.

The evaluator does not choose which timing indicator/rule to use. It only consumes an approved upstream timing result.

## Source compatibility
Murphy's broader timing material identifies technical timing tools including trendline breaks, support/resistance, retracements, gaps, and shorter-term charts for timing. These are source-level examples, not a command to bind all of them to 0002.

## Historical evaluation boundary
A standalone historical 0002 signal-count backtest is not authorized unless the project defines which upstream timing producer(s) constitute the approved timing evidence set. Historical evidence can validate the selected upstream producer, but cannot be used to choose the producer or threshold.

## Freeze gate
0002 may be promoted only after:
1. the project names the authoritative upstream timing evidence producer(s);
2. the Rule Adapter/evidence schema accepts their outputs without duplicating rules;
3. deterministic unit tests cover PASS / FAIL / NOT_EVALUABLE / chronology;
4. 2016–2024 QA validates availability/no-lookahead;
5. 2025 remains OOS and is not used for selection/tuning;
6. a freeze record is approved.

## Explicit prohibitions
- No invented indicator.
- No invented threshold/tolerance.
- No fixed timeframe invented for 0002.
- No 2025 tuning.
- No duplicate timing engine.
- No standalone trade direction from 0002.

## Current status
SOURCE VERIFIED / SEMANTICS VERIFIED / TIMING GATE CONTRACT DEFINED / UPSTREAM PRODUCER BINDING + QA PENDING.
