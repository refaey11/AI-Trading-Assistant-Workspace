# Murphy 0030 P&F Box Scaling — Project Operationalization Candidate V2

Status: CANDIDATE / NOT FROZEN
Date: 2026-08-15

## Source boundary
Murphy/Chapter 11 supports logarithmic P&F and states that Kenneth Tower used a screening process measuring volatility over the prior three years to determine a percentage box size. Murphy gives examples for AOL and Intel, but the audited source does not provide Tower's complete reproducible formula for converting three-year volatility into the final percentage box size.

Therefore this document is NOT a claim that the formula below is Tower or Murphy.

## Candidate operationalization
Use a deterministic trailing-three-year realized daily log-return volatility as the project-defined percentage box size:

box_pct = 100 * sample_std(log(C_t / C_{t-1}))

where:
- C is canonical GBPUSD D1 close;
- the calibration window is exactly the prior three calendar years;
- only observations available inside the calibration window are used;
- no future evaluation/OOS observations are used;
- no backtest outcome is used to select or modify the formula.

This is intentionally labeled PROJECT_OPERATIONALIZATION, not MURPHY_BOX_SIZE.

## Walk-forward use
Respect the project's existing frozen walk-forward protocol:
- Calibration 2016–2023 -> OOS 2024.
- Calibration 2016–2024 -> OOS 2025.

For each fold, the operationalization must be computed only from the calibration data. If a three-year trailing window is required, the latest three calendar years inside that calibration set are used. The resulting box percentage is frozen for that OOS fold.

## Observed diagnostic values on canonical GBPUSD D1
Using the current canonical D1 file as a diagnostic only:
- 2021–2023 daily log-return sample standard deviation = 0.5881978895%.
- 2022–2024 daily log-return sample standard deviation = 0.5837480891%.

These values are NOT selected because of performance and are NOT production parameters. They demonstrate that the formula is deterministic and reproducible.

## Why this candidate is auditable
- It directly operationalizes Murphy's stated three-year-volatility concept without pretending to reproduce Tower's unpublished screening formula.
- It contains no performance optimization step.
- It has a fixed mathematical definition.
- It can be independently recomputed from the canonical data.
- It can be applied fold-by-fold without using OOS information.

## Required rejection conditions
Reject this candidate if:
1. an authoritative, reproducible Tower formula is recovered and supersedes it;
2. compatibility testing shows the P&F engine cannot represent the resulting percentage box deterministically without lookahead;
3. the governance review determines that this operationalization is insufficiently source-faithful;
4. the construction requires an unapproved intrabar High/Low ordering assumption.

## Freeze gate
This candidate must NOT be used for final 0030 evaluation until explicitly approved and frozen. No alternative box formula may be selected by comparing historical profitability.
