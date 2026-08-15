# Murphy 0008 — Executable Test Evidence V1

Status: PASS FOR EXPERIMENTAL VALIDATION / NOT PRODUCTION FROZEN

## Local execution
Evaluator module: `murphy_0008_evaluator.py`
Unit suite: 4 passed in 0.06s.

## Replay evidence
Source workspace reconstruction:
- Three transferred workspace parts concatenated in documented order.
- `unzip -t` returned no errors.

Canonical inputs:
- `PIVOT_SEQUENCE_V2_OUTPUT/GBPUSD_D1_STRUCTURE_PIVOT_SEQUENCE_V2.csv`
- `DMI_ADX_V1_OUTPUT/GBPUSD_D1_DMI_ADX_2016_2024.csv`

Replay:
- 344 available LOW support pivots
- 326 first-close-below candidates
- 242 immediate two-close confirmations
- 84 candidate breaks not confirmed on the immediately following D1 close
- 233 later support intersections
- 229 later intersecting bars closed below Support

## State-machine acceptance
- Support availability chronology: PASS
- First close candidate: PASS
- Immediate second close confirmation: PASS
- Same Support identity: PASS
- No lookahead: PASS
- Retest strictly after confirmation: PASS
- Missing/invalid Support: NOT_EVALUABLE
- 2025 input: none

## Supersession note
The earlier 324-count replay is superseded. It did not enforce the first-candidate state transition; it counted any later consecutive pair below Support. The frozen contract requires the first below close to be the candidate and the immediately next completed D1 close to confirm.

## Freeze boundary
These results validate the executable contract. They do not by themselves authorize production freeze, profitability claims, or autonomous trading.
