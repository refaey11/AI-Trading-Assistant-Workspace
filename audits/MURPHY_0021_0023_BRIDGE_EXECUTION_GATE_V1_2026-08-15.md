# Murphy 0021–0023 — Bridge Execution Gate V1

Date: 2026-08-15
Status: BRIDGE TEST PASS / DIAGNOSTIC HISTORICAL RECONCILIATION PASS / AVAILABILITY AUDIT OPEN

## Uploaded evaluator artifact inspected
Source ZIP: `MURPHY_EVALUATORS_V1(3).zip`
Historical file: `MURPHY_0021_0023_HISTORICAL_EVALUATION_2020_2024.csv`

Observed:
- 122,943 raw rows
- 122,934 rows dated 2020–2024
- 9 rows dated 2025-01-01

The 9 rows are treated as the previously identified raw/non-clean spill and are excluded only from the diagnostic 2020–2024 reconciliation. They are not promoted into the canonical artifact.

## Bridge execution
The source-locked bridge was executed diagnostically across all 122,943 uploaded rows.

- Bridge transformation errors: 0
- 2020–2024 diagnostic rows: 122,934
- 2025 spill excluded diagnostically: 9
- Rule distribution in 2020–2024 set: 40,978 each for 0021/0022/0023
- Status totals in 2020–2024 set: FAIL 89,161; PASS 31,510; NOT_EVALUABLE 2,263
- FAIL rows with an inferred opposite direction: 0
- NOT_EVALUABLE directional inference: none
- confidence_delta: 0 throughout

## Deterministic contract tests
10/10 PASS, covering PASS/BULLISH, PASS/BEARISH, FAIL without opposite-direction inference, NOT_EVALUABLE, unknown status, missing direction, raw-result preservation, and confidence_delta=0.

## Availability / no-lookahead audit
The evaluator source code requires completed-bar price/volume/OI inputs, and the contract states Runtime/Dynamic MTF without hard-coding an execution timeframe. However, the historical evaluation CSV contains only:
- timeframe
- timestamp
- rule_id
- status
- directional_confirmation

It does NOT contain explicit `availability_timestamp`, source-input timestamps, or per-row provenance for the completed-bar/volume/OI inputs.

Therefore a formal row-level availability/no-lookahead proof cannot be claimed from this artifact alone. The timestamp can be checked for date coverage, but it cannot prove that every input was available at that timestamp.

## Freeze status
- Bridge deterministic tests: PASS
- 122,934-row diagnostic reconciliation: PASS / 0 bridge errors
- Canonical clean artifact provenance: OPEN
- Formal availability/no-lookahead proof: OPEN / requires source-input availability evidence
- Production Freeze: NOT GRANTED

## Governance
No evaluator semantics, thresholds, timeframe, OI proxy, or 2025 tuning/selection was changed.
No trade decision is produced by this bridge.
