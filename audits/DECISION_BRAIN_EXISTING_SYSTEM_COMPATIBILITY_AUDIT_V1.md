# Decision Brain Existing System Compatibility Audit V1

Date: 2026-08-12

## Executive result

The project is not to be rebuilt. The permanent handoff confirms Decision Brain V1/V1.1 already exists and includes evidence aggregation, risk integration, Similarity integration, book-rule integration, Dynamic MTF/timeframe concepts, market evidence, and process gating.

## Existing architecture / preserved components

- Murphy = primary technical context / market structure.
- Nison = candlestick confirmation only.
- Trading in the Zone = process/psychology gate only.
- Similarity = historical evidence / memory only.
- Risk = hard gate.
- Rule Adapter = normalization layer only.
- Decision Brain = synthesis layer.

The existing project also preserves Historical Memory, Historical Outcomes, Similarity V2/indexes, Market Structure, MTF Alignment, Feature Engineering V2, Feature Weighting V1, Master Evidence, and Evidence Layer. These must not be deleted or rebuilt.

## Rule Adapter compatibility

The existing Rule Adapter contract accepts current market state, registry rule metadata, and historical-memory fields. It normalizes outputs into evidence with module, statement, direction, strength, availability, gate status, and conflict status. Its precedence rules match the project architecture: process and risk hard gates; Murphy directional context; Nison confirm/contradict only; Similarity supportive only; Brain synthesizes.

Current status of the adapter contract is DESIGN_ONLY. Therefore the integration task is validation/wiring against existing evaluators, not rebuilding the adapter or copying the 102 rules into the Brain.

## Baseline status

Official Baseline is NOT YET FROZEN.

Candidate: Similarity Engine V2 + 4H.

Stored result families use different protocols/risk models/sample handling and cannot be combined into one official result. The required baseline gate is one frozen end-to-end protocol across all five assets:
- calibration 2016–2023 -> OOS 2024
- calibration 2016–2024 -> OOS 2025
- same signal, k, SL/TP, ambiguity policy, costs
- no tuning on OOS

## Current blockers ranked

1. Official uniform walk-forward + leakage audit.
2. Adapter/Brain integration verification against the existing evaluator outputs.
3. Murphys evaluator gaps: exact operators not frozen for all 51.
4. 0003–0004 provenance reconciliation.
5. 0006–0007 operational evidence/source lock.

## What is ready to preserve

- Existing Decision Brain V1/V1.1.
- Existing Rule Adapter implementation and contract.
- Existing Market Reader / Market State / MTF / Historical / Similarity components.
- Existing evaluator artifacts for 0003–0004, 0021–0023, 0027–0029, and 0050, subject to their documented freeze/QA limitations.

## Execution plan from this audit

A. Validate existing interfaces and precedence using the preserved contracts/tests.
B. Validate evaluator outputs can be normalized by the existing Rule Adapter without altering source rules.
C. Resolve only missing compatibility fields or adapters.
D. Execute the frozen uniform baseline protocol and leakage audit.
E. Integrate the verified baseline and evidence into Decision Brain V1/V1.1.
F. Run full-system QA, then freeze only after all gates pass.

## Non-negotiable controls

- 2025 is OOS; never use it for tuning, threshold selection, model selection, or implementation selection.
- No rebuilding of Decision Brain V1/V1.1.
- No copying or rewriting the 102 registry rules into the Brain.
- Similarity cannot be sole decision maker.
- Nison cannot create direction alone.
- Trading in the Zone cannot generate direction.
- Risk remains a hard gate.
- Do not promote evaluator file existence into semantic freeze.
