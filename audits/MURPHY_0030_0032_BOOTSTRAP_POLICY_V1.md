# Murphy 0030–0032 — P&F Bootstrap Policy V1

Status: PROPOSAL / SOURCE-BOUNDED / NOT PRODUCTION FROZEN

## Purpose
Define the smallest deterministic bootstrap needed to construct a 3-box High/Low Point & Figure series before the first completed column exists.

## Source boundary
Murphy Chapter 11 establishes Point & Figure construction, 3-box reversal, and High/Low usage, but does not provide a complete software bootstrap algorithm for the first column in the project source.

External corroboration used only for operationalization:
- Jeremy du Plessis, *The Definitive Guide to Point and Figure*: the first box is X when the initial price trend is up and O when it is down; the example compares subsequent High/Low observations against the initial range until a move large enough to establish the first direction occurs.
- StockCharts ChartSchool: the High/Low method uses High first for X continuation and Low first for O continuation, with the opposite price used only when continuation fails and a 3-box reversal is triggered.

## Operational bootstrap
1. Start with the first completed D1 High/Low as the initial reference range.
2. Do not create a P&F column merely because the first bar exists.
3. Scan subsequent completed D1 bars in chronological order.
4. Establish the first direction when a subsequent High reaches the first upward box threshold from the initial reference, or a subsequent Low reaches the first downward box threshold.
5. If neither condition is met, ignore the bar for P&F construction and continue scanning.
6. If the upward condition is the first qualifying condition, initialize X; if the downward condition is the first qualifying condition, initialize O.
7. Once the first column exists, use the standard High/Low 3-box rules: X checks High for continuation first and only then Low for reversal; O checks Low first and only then High for reversal.
8. A same-bar dual qualification at bootstrap is a governed ambiguity and must not be resolved using profitability. Until an explicit tie-break is approved, return NOT_EVALUABLE for that bootstrap event.

## Availability / leakage
- Only completed D1 bars may establish or extend the P&F state.
- The bootstrap availability timestamp is the completed timestamp of the bar that first establishes the direction.
- No later bar may alter the bootstrap decision retroactively.
- 2025 is excluded from all policy selection and tuning.

## Boundary
This document is a project operationalization. It is NOT claimed to be verbatim Murphy wording and does not claim to reproduce Kenneth Tower's box-size formula.

## Production gate
Before freeze, compare this bootstrap against at least one independent implementation/reference and run deterministic prefix replay on the project's 2016–2024 data. Any unresolved discrepancy remains NOT_EVALUABLE rather than being tuned away.