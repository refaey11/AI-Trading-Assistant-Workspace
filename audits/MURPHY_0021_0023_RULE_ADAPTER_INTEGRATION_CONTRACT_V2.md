# Murphy 0021–0023 — Rule Adapter Integration Contract V2

Date: 2026-08-15
Status: INTEGRATION CONTRACT PROPOSAL — NOT PRODUCTION FROZEN

## Purpose
Close the smallest remaining integration gap between the existing, unit-tested Murphy 0021–0023 evaluator and the existing Rule Adapter without changing rule semantics, adding thresholds, inventing timeframes, or making the adapter a trade decision maker.

## Source evaluator
The existing evaluator is authoritative for these fields:
- rule_id
- status = PASS | FAIL | NOT_EVALUABLE
- directional_confirmation = BULLISH | BEARISH | NONE | UNKNOWN
- reason

Operationalization already frozen at evaluator level:
- 0021: price UP/DOWN + existing volume_direction UP
- 0022: price UP + volume UP + available CFTC futures OI UP
- 0023: price DOWN + volume UP + available CFTC futures OI UP
- Dynamic MTF; no hard-coded execution timeframe
- no added thresholds
- no spot-FX OI proxy
- 2025 excluded

## Adapter mapping
Input: evaluator result only; no new market-state inference.

### source_rule_id
`source_rule_id = evaluator.rule_id`

### availability
- PASS -> `available = true`
- FAIL -> `available = true`
- NOT_EVALUABLE -> `available = false`

This preserves the distinction between a known negative result and missing evidence.

### gate
- PASS -> `gate = pass`
- FAIL -> `gate = fail`
- NOT_EVALUABLE -> `gate = needs_review`

No missing evidence is converted to PASS or FAIL.

### direction
Use only the evaluator's `directional_confirmation`:
- BULLISH -> `direction = bullish`
- BEARISH -> `direction = bearish`
- NONE/UNKNOWN -> `direction = neutral`

No direction is inferred from rule names or free text.

### statement
Use the evaluator's source-backed `reason` together with the canonical rule statement. Do not synthesize a new trading rule.

### strength
No strength is inferred from PASS/FAIL. Until a source-locked strength field exists, `strength = null` is permitted and must not be converted into confidence.

### conflict
- PASS -> `conflict = neutral`
- FAIL -> `conflict = contradicts`
- NOT_EVALUABLE -> `conflict = insufficient`

The FAIL mapping means the evaluated Murphy condition contradicts the expected rule condition; it does not authorize the adapter to create an opposite trade.

### decision_hint
- PASS + BULLISH -> `bullish`
- PASS + BEARISH -> `bearish`
- FAIL or NOT_EVALUABLE -> `neutral`

This is an evidence hint only; it is not a trade decision.

### confidence_delta
`confidence_delta = 0` for this bridge. The 0021–0023 evaluator does not produce a source-locked confidence magnitude, so the adapter must not invent one.

## Hard safety rules
- Do not rebuild the evaluator.
- Do not alter 0021–0023 source semantics.
- Do not add thresholds.
- Do not substitute spot-FX OI for CFTC futures OI.
- Do not hard-code an execution timeframe.
- Do not use 2025 for tuning or operator selection.
- Do not convert NOT_EVALUABLE into PASS or FAIL.
- Adapter remains normalization only; Decision Brain remains the synthesis layer.

## Required deterministic tests
T1: 0021 PASS BULLISH -> available=true, gate=pass, direction=bullish, conflict=neutral, decision_hint=bullish, confidence_delta=0.
T2: 0021 PASS BEARISH -> available=true, gate=pass, direction=bearish, conflict=neutral, decision_hint=bearish, confidence_delta=0.
T3: 0021 FAIL NONE -> available=true, gate=fail, direction=neutral, conflict=contradicts, decision_hint=neutral.
T4: 0022 PASS BULLISH -> same pass mapping.
T5: 0022 FAIL NONE -> fail mapping; no opposite direction inferred.
T6: 0022 NOT_EVALUABLE UNKNOWN -> available=false, gate=needs_review, direction=neutral, conflict=insufficient.
T7: 0023 PASS BEARISH -> same pass mapping.
T8: unknown status -> needs_review/available=false; no inferred direction.
T9: missing evaluator directional confirmation -> no inferred direction.
T10: 2025 metadata -> no tuning/selection behavior.

## Freeze gate
This contract is a bridge proposal, not a production freeze.
After deterministic adapter implementation/tests, perform:
1. 2016–2024 historical reconciliation;
2. availability/leakage audit;
3. provenance/freeze manifest;
4. explicit Production Freeze decision for 0021–0023.
