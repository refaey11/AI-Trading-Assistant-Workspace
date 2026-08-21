# Outcome Memory → Scenario Evidence — Official Gap & Next Gate

**Date:** 2026-08-21
**Status:** ACTIVE CHECKPOINT

## Confirmed existing components

- Historical Outcome Memory V1 exists.
- Historical Context Memory V1 exists.
- Historical outcomes are stored as descriptive evidence across existing horizons.
- Existing outcome statistics include context occurrence information and return/positive-rate statistics.
- Historical/Similarity evidence is not permitted to act as a standalone direction generator.
- Decision Brain V1 is recovered; historical evidence integration exists as a prior workstream.

## Confirmed gap

The reviewed project artifacts do not provide a previously frozen, source-backed definition for:

1. Numeric classification boundaries for **BULL / BASE / BEAR** outcomes.
2. The exact **Outcome → Scenario Evidence** classification policy.
3. The scenario calibration method.
4. The uncertainty formula for scenario evidence.

Therefore these items must not be invented silently or inferred from `positive_rate` alone.

## Official next gate

Create the **smallest possible policy/contract layer** required to bridge existing historical outcomes into scenario evidence, subject to compatibility review.

Target flow:

`Historical Outcomes → BULL/BASE/BEAR Classification → bull/base/bear counts → coverage + uncertainty → calibrated scenario evidence → Decision Brain`

## Required safeguards

- Use existing historical outcome records; do not rebuild Historical Outcome Memory.
- Do not use `positive_rate` alone as a directional decision.
- Similarity/Outcome Memory remains evidence only.
- Decision Brain remains responsible for aggregation; this layer must not emit BUY/SELL.
- Preserve AS-OF / no-future-leakage controls.
- Use 2016–2024 for development, calibration, and historical QA only.
- Reserve 2025 for final OOS evaluation only; never use it for tuning.
- Run compatibility review against the recovered Decision Brain and validated Risk Boundary before freeze.

## Exact next work sequence

1. Recover any existing project evidence for scenario boundary conventions before defining new policy.
2. If no prior convention exists, draft the minimum explicit Scenario Classification Policy as a policy artifact, clearly marked as project policy rather than book-derived knowledge.
3. Define the Outcome → Scenario Evidence Contract.
4. Validate on 2016–2024 with AS-OF/no-lookahead tests.
5. Test compatibility with Decision Brain and Risk Boundary.
6. Freeze only after passing QA and compatibility gates.

## Resume rule

Resume from this checkpoint. Do not reopen closed Murphy/Nison work or parked TIZ work, and do not rebuild existing memory modules unless a concrete compatibility test proves a required change.
