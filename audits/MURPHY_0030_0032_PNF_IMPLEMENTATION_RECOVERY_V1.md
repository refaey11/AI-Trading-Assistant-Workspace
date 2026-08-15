# Murphy 0030–0032 — P&F Implementation Recovery V1

Date: 2026-08-16
Status: IMPLEMENTATION RECOVERED / NOT PRODUCTION FROZEN

## Decision
The project does not have to search for Murphy Chapter 11 again. Source provenance is already established. The missing gate is a deterministic Point & Figure implementation.

A single shared reference P&F core is therefore added for 0030–0032. This is the smallest shared implementation, not three independent evaluators.

## Source-backed construction
Murphy Chapter 11 describes the 3-box reversal construction using daily High/Low data. In an X column, High is checked first for continuation; only if X cannot continue is Low checked for reversal. In an O column, Low is checked first; only if O cannot continue is High checked for reversal.

Murphy also describes 1-, 3-, and 5-box reversal charts and explains that the 3-box method is a compressed form suitable for intermediate-trend analysis. Percentage/logarithmic P&F is described separately through Kenneth Tower's volatility-based percentage-box approach.

## Project operationalization boundary
The reference engine makes the following items explicit inputs rather than silently inventing them:
- percentage box size (`box_pct`)
- logarithmic grid anchor (`anchor_price`)
- reversal size (default 3 boxes)
- initial seed column/direction

The current implementation does NOT claim that a specific GBPUSD box percentage or Tower formula has been recovered from Murphy. Therefore no production box percentage is frozen by this artifact.

## Implementation
`src/murphy_0030_0032/pnf_reference.py`

The implementation:
- consumes completed OHLC bars;
- enforces High-before-Low continuation priority for X columns;
- enforces Low-before-High continuation priority for O columns;
- creates reversals only after continuation fails;
- uses an explicit 3-box reversal configuration;
- has no future-bar access;
- requires an explicit initial seed instead of guessing one.

## Tests
`tests/murphy_0030_0032/test_pnf_reference.py`

Required tests cover:
- X continuation priority;
- X reversal;
- O continuation priority;
- O reversal;
- deterministic replay;
- invalid OHLC rejection.

## Remaining gates before 0030–0032 evaluation
1. Recover/approve the exact rule-to-P&F mapping for each of 0030, 0031, 0032 from the existing Master Rule Database/Chapter 11 artifacts.
2. Approve the GBPUSD box-size operationalization without using OOS performance.
3. Integrate the shared P&F core with the existing rule/evidence adapter.
4. Run deterministic, prefix, availability/no-lookahead tests on the integrated path.
5. Run fresh 2016–2024 historical QA.
6. Keep 2025 locked OOS.
7. Create the final provenance/freeze manifest and governance approval.

## Explicit prohibitions
- Do not tune box size from profitability.
- Do not use 2025 for box-size or operator selection.
- Do not treat the implementation as verbatim Murphy numeric wording where the source leaves operational choices open.
- Do not create separate bespoke engines for 0030, 0031, and 0032.
- Do not declare PASS/FROZEN until the integrated evaluator gates pass.

## Current status
0030–0032 remain NOT_EVALUABLE for production evaluation until the remaining gates above are completed. The implementation blocker itself is no longer an empty folder: a deterministic shared reference core now exists.
