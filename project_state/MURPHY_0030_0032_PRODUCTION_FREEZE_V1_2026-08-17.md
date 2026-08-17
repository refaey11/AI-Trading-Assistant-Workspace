# Murphy 0030–0032 — Production Freeze V1

Date: 2026-08-17
Status: PRODUCTION FROZEN

## Scope
Freeze the shared Murphy Point & Figure feature path for:
- MURPHY_0030 — P&F bullish support
- MURPHY_0031 — P&F long stop reference
- MURPHY_0032 — P&F short stop reference

The existing 12 frozen Murphy rules were not reopened or modified.

## Source boundary
Source semantics are locked to the existing Chapter 11 mapping:
- 0030: bullish 45-degree P&F support reference from the lowest O-column base.
- 0031: long stop reference below the previous O column.
- 0032: short stop reference above the previous X column.

These are structural/evidence operators and do not create autonomous BUY/SELL decisions.

## Shared construction policy — FROZEN PROJECT OPERATIONALIZATION
1. Input: canonical completed GBPUSD D1 OHLC.
2. Construction: High/Low 3-box reversal P&F.
3. X column: evaluate High continuation first; only if High cannot continue is Low evaluated for reversal.
4. O column: evaluate Low continuation first; only if Low cannot continue is High evaluated for reversal.
5. Reversal size: exactly 3 boxes.
6. Bootstrap: first completed bar seeds X when Close >= Open using floor(High / box_size) as the initial level; otherwise seeds O using ceil(Low / box_size). This bootstrap is explicitly PROJECT_OPERATIONALIZATION, not Murphy source text.
7. Box size: PROJECT_OPERATIONALIZATION, not Murphy/Tower source truth.
8. Box percentage formula: 100 * sample_std(log(C_t / C_{t-1})) using the prior three calendar years available inside the calibration set for each walk-forward fold.
9. The resulting fold box percentage is frozen for that fold and is never selected or altered using profitability.
10. 2025 is excluded from tuning, selection, calibration and optimization.

## Evidence gates completed
- Source semantics: RESOLVED.
- Shared P&F construction core: IMPLEMENTED and reused.
- Compatibility entrypoint: restored and merged in PR #20.
- Deterministic local QA: 7/7 PASS.
- Canonical D1 historical construction QA: 2,544 rows, 2016-01-03 through 2024-12-31.
- Calibration-only folds: 2019–2024 PASS for deterministic construction and prefix/no-lookahead replay.
- No 2025 data used.
- No profitability-based parameter selection.
- 0030/0031/0032 semantic outputs remain source-bounded.

## Freeze decision
The GBPUSD box-size and bootstrap choices above are approved as explicit project operationalization. They must not be described as Murphy or Kenneth Tower numeric source truth.

The shared P&F feature layer is now frozen for production evaluation of 0030–0032.

## Prohibitions after freeze
- No performance-based retuning of box size.
- No use of 2025 for tuning or selection.
- No invention of pip/ATR stop offsets.
- No future-bar access or retrospective mutation of emitted historical states.
- No reopening of the 12 already-frozen rules as routine cleanup.

## Provenance
Technical batch evidence: commit `b3176a71df73f1389901e4c8125d65c87721e201`.
Compatibility entrypoint fix: merged PR #20, merge commit `f099a877ef71bdc065a5bda114f8b5371d257b9c`.
