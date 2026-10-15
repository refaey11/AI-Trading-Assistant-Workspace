# MURPHY_0013 — Breakout Window Source-Lock V1

Status: GOVERNANCE PROPOSAL / NOT PRODUCTION FROZEN
Date: 2026-08-16

## Source-grounded finding

Murphy Chapter 6 describes a time limit for triangle resolution at the apex and gives a general rule that breakout normally occurs between roughly two-thirds and three-quarters of the horizontal triangle width. Murphy also states that the actual trend signal is a closing penetration of one of the trendlines and describes a minimum penetration criterion as a closing price outside the trendline rather than an intraday penetration.

The two-thirds to three-quarters statement is explicitly presented as a **general rule**, not as a deterministic hard cutoff. Therefore this contract does not convert that descriptive guidance into a numerical eligibility threshold.

## Deterministic breakout-window operator

For an already-valid canonical triangle:

1. The triangle base/start timestamp and canonical apex timestamp must be available from the approved geometry contract.
2. A breakout event is evaluated only on completed bars.
3. An UP breakout event exists when the completed bar closes strictly above the canonical upper boundary.
4. A DOWN breakout event exists when the completed bar closes strictly below the canonical lower boundary.
5. The breakout close must be strictly before the canonical apex timestamp.
6. A close at or after the apex is not a valid in-pattern breakout event and must be classified `NOT_CONFIRMED` or `NOT_EVALUABLE` according to provenance completeness.
7. Intraday-only penetration without a closing penetration is not a breakout event.
8. The two-thirds to three-quarters position is retained as source-derived descriptive metadata (`TIMING_CONTEXT`) and is not used as a hard pass/fail threshold.

## Separation from confirmation

`BREAKOUT_OBSERVED` is the source-bounded event: a completed close beyond a canonical boundary before the apex.

A separate confirmation policy may add a second completed close (the shared 0008-derived two-close candidate), but that policy is an engineering compatibility layer and is **not claimed to be verbatim Murphy**. It must never erase or redefine the underlying source-bounded breakout event.

## No-lookahead / provenance

- The boundary and apex must be available at the evaluation timestamp.
- The breakout bar's close must be available at its own completion timestamp.
- No later pivot or refitted line may rewrite the historical boundary/apex used for the event.
- Missing provenance is fail-closed as `NOT_EVALUABLE`.
- Future bars cannot establish an earlier breakout.

## Forbidden operationalizations

- Do not use 2/3 or 3/4 as an exact numerical gate.
- Do not invent ATR, pip, percentage, or distance tolerances.
- Do not use 2025 to choose between breakout policies.
- Do not use historical outcome counts to select a breakout window.

## 0013 assembly

`PIVOT_SEQUENCE_V2`
→ `TRENDLINE_GEOMETRY_V1`
→ `PF-G1 CONVERGING`
→ `BREAKOUT_OBSERVED` before apex
→ optional candidate confirmation layer
→ `MURPHY_0013 evaluator`

## Governance gate

This document closes the **representation question** by separating Murphy's deterministic event (closing penetration before apex) from descriptive timing guidance (roughly 2/3–3/4). It does not by itself approve the shared two-close confirmation layer or production-freeze 0013.
