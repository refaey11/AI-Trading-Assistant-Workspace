# Timeframe Architecture Correction

**Recorded:** 2026-08-21
**Status:** CORRECTION / GOVERNANCE CLARIFICATION

## Official project timeframe architecture

The official multi-timeframe architecture is:

M5 -> M15 -> M30 -> H1 -> H4 -> D1

The timeframe hierarchy therefore starts at **M5**.

## Important distinction

A prior Market Pipeline audit reported H4/H1 as the available context in the specific artifacts inspected in RUN 072 and reported M15 unavailable in that artifact path. This is an artifact coverage finding only.

It must NOT be interpreted as:
- replacing the official six-timeframe architecture;
- redefining the project as H1/H4-only;
- removing M5, M15, or M30 from the official architecture;
- fabricating a missing timeframe from another timeframe.

## Interpretation rule

Official architecture and current artifact coverage are separate facts:

- Architecture: M5/M15/M30/H1/H4/D1.
- A particular audit may have incomplete coverage for one or more official timeframes.
- Missing artifact coverage is a coverage gap to be audited, not a reason to silently change the architecture.

## Related Risk Engine files

The uploaded `RISK_ENGINE_SPEC_V1` files are treated as Risk Engine specifications and do not alter the official timeframe architecture.

## Anti-loop governance

Before any future integration or audit changes timeframe assumptions, check this correction record and distinguish:
1. official architecture;
2. artifact availability/coverage;
3. implementation gaps.

Do not collapse these categories into one.
