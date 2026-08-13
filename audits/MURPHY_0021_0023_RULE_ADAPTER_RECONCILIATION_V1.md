# Murphy 0021–0023 — Rule Adapter Reconciliation V1

Date: 2026-08-13
Status: RECONCILIATION COMPLETE / ADAPTER INTEGRATION CONTRACT GAP RECORDED

## Scope

Reconcile the existing Murphy 0021–0023 evaluator outputs with the existing project Rule Adapter contract and implementation. No existing evaluator, evidence module, or Decision Brain component is rebuilt.

## Existing evaluator contract

MURPHY_0021–0023 evaluator is implemented and unit-tested.

Operationalization:
- price direction = current completed close vs previous completed close
- volume confirmation = existing `volume_direction == UP`
- OI confirmation = existing CFTC futures `oi_direction == UP`
- CFTC scope = CME British Pound futures 096742; not spot-FX OI
- no added thresholds
- no OI proxy
- Dynamic MTF
- 2025 excluded

Evaluator outputs include:
- `rule_id`
- `status` = PASS / FAIL / NOT_EVALUABLE
- `directional_confirmation`
- reason

## Existing Rule Adapter contract

The existing Rule Adapter normalizes registry rules into Decision Brain evidence and is explicitly a normalization layer, not a trade decision maker.

Declared normalized evidence fields:
- module
- statement
- direction
- strength
- available
- source_rule_id
- gate
- conflict

The current contract declares status `DESIGN_ONLY`.

## Compatibility finding

The evaluator output and adapter output are semantically compatible at the conceptual boundary:

`MURPHY evaluator result -> normalized Decision Brain evidence`

However, the current Rule Adapter implementation accepts a registry-rule object and optional current-state/similarity inputs. It does NOT define or implement a source-locked input contract for an evaluator result (`status`, `directional_confirmation`, evidence availability).

Therefore a direct evaluator-to-adapter integration cannot be claimed complete without adding an explicit adapter contract for evaluator outputs.

## Safety decision

Do NOT modify the existing adapter by inventing a mapping for:
- PASS -> gate value
- FAIL -> gate value
- NOT_EVALUABLE -> gate value
- evaluator strength
- conflict semantics

Those mappings are not currently frozen by the existing adapter contract.

In particular, `NOT_EVALUABLE` must not be converted into FAIL or PASS.

## Historical evidence

The clean historical artifact for 0021–0023 is a validated 2020–2024 artifact with 2025 absent, but its validation workflow checks the artifact rather than independently recomputing every decision from raw inputs. The project therefore requires reconciliation against the actual evaluator/data lineage before Production Freeze.

## Result

- Evaluator contract: VERIFIED
- Evaluator unit tests: VERIFIED
- Existing Rule Adapter: VERIFIED AS EXISTING / DESIGN-ONLY
- Direct evaluator-output adapter contract: MISSING
- No existing component modified by this audit
- Production Freeze: NOT GRANTED by this reconciliation alone

## Next smallest safe gate

Define/approve an evaluator-result-to-Decision-Brain evidence contract using only fields already produced by the evaluator. Then add deterministic adapter tests and perform the final 0021–0023 freeze reconciliation. No thresholds, proxies, new rule semantics, or 2025 tuning are permitted.
