# Murphy 0002 — Operator / Provenance Audit V2

Date: 2026-08-15
Status: SOURCE VERIFIED / OPERATOR CONTRACT PENDING

## Scope
Deep review of available Workspace/File Library records, Murphy source material, existing project contracts, and GitHub audit infrastructure. No implementation or tuning performed.

## Source recovery
The authoritative Master KB record for MURPHY_0002 is now recovered.
- Rule ID: MURPHY_0002
- Chapter: 1 — Trading Rules and Timing
- Rule name: Direction is not enough
- Core condition: a correct directional forecast still requires appropriate entry and exit timing.
- Decision logic: a directional view without an executable timing condition is not a trade setup.
- Source registry status: UNTESTED.

Independent Murphy Chapter 1 source material confirms the same semantic separation between analysis/forecasting and timing. Murphy describes timing as determining specific entry and exit points and identifies timing as a technical part of the trading decision.

## What the source does NOT provide for this project
The recovered rule record does not freeze a deterministic project operator for:
- exact entry trigger;
- exact exit trigger;
- exact timeframe role for the rule;
- numeric threshold/tolerance;
- exact PASS/FAIL evidence predicate.

The source describes the concept of timing, not a unique software predicate that can safely be treated as the 0002 evaluator contract.

## Existing project architecture checked
- Dynamic MTF infrastructure exists.
- Rule Adapter exists, but it is a normalization layer and must not invent or decide source rules.
- Existing evaluator architecture exists.
- Decision Brain already exists and must not be rebuilt.

Feature/infrastructure availability does not itself make 0002 evaluatable.

## Decision
MURPHY_0002 remains NOT_EVALUABLE for production evaluation, but for a corrected reason:

SOURCE RECORD: RESOLVED
SOURCE SEMANTICS: RESOLVED
OPERATOR CONTRACT: NOT FROZEN
EVALUATOR: NOT IMPLEMENTED
HISTORICAL QA: NOT STARTED
FREEZE: NOT AUTHORIZED

## Prohibited actions
- Do not invent RSI/MACD/MA/price-action thresholds as the 0002 operator.
- Do not assign M5/M15/H1/etc. as the 0002 timing timeframe without authoritative project evidence.
- Do not optimize an operator against historical results.
- Do not use 2025 for selection or tuning.
- Do not create a new timing engine when existing infrastructure can be reused.

## Next gate
Search the remaining source-linked Chapter 1 / Trading Tactics material and existing project timing primitives for an authoritative operational mapping. If none exists, record 0002 as source-verified but operationally under-specified and leave it NOT_EVALUABLE.

Only after an operator is source-locked:
1. compatibility audit;
2. smallest missing evaluator;
3. deterministic unit tests;
4. 2016–2024 historical QA;
5. availability/no-lookahead audit;
6. provenance/freeze manifest.

2025 remains OOS throughout.

## Historical note
MURPHY_0002_WORKSPACE_VERIFICATION_REPORT_V1 dated 2026-08-14 said SOURCE RECORD NOT RECOVERED. That statement is superseded by this V2 audit because the Master KB / MT5 archive impact audit subsequently recovered the source record. The older report remains preserved as historical evidence and is not deleted.
