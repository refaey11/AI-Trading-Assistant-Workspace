# Murphy 0013-0020 — Pivot Availability Evidence Audit V1

Status: EVIDENCE AUDIT — NOT PRODUCTION FROZEN
Date: 2026-08-16

## Source artifact inspected
GBPUSD_RULE_EVALUATOR_V2_WORKSPACE_PART_03_OF_03 (split workspace artifact, parts 1-4).

The pivot/structure rows explicitly contain:
- pivot timestamp;
- pivot type (HIGH/LOW);
- pivot confirmation timestamp;
- confirmation label `CONFIRMED_AFTER_2_BARS`;
- source structure file and row index.

## Direct evidence samples
### M5
2019-03-11 23:45:00 -> 2019-03-11 23:55:00 = 10 minutes = 2 M5 bars.
2016-10-26 15:35:00 -> 2016-10-26 15:45:00 = 10 minutes = 2 M5 bars.

### H1
2019-11-10 21:00:00 -> 2019-11-10 23:00:00 = 120 minutes = 2 H1 bars.

These samples are taken directly from the split workspace chunks and are labelled `CONFIRMED_AFTER_2_BARS`.

## Decision
The inspected artifact provides explicit availability/confirmation timestamps for pivots and demonstrates a causal two-bar confirmation convention in the sampled M5 and H1 records.

This is materially stronger than an assumption that pivot availability equals pivot timestamp.

## Remaining gate
This audit does NOT prove that every boundary used by the Murphy structural evaluator is constructed exclusively from pivots whose confirmation timestamp is <= the decision timestamp. The boundary-construction provenance must still be wired and checked explicitly.

Therefore:
- Pivot availability evidence: PASS (sampled evidence)
- Boundary provenance: OPEN
- Structural historical validity: NOT YET FROZEN

## Prohibited inference
Do not backdate a pivot to its visual turning-point timestamp for rule evaluation. Use its confirmed/available timestamp.

## OOS
2025 remains OOS and is not used for tuning.
