# Murphy 0008 — Executable Replay V2

Status: EXECUTED / EXPERIMENTAL VALIDATION — NOT PRODUCTION FROZEN

## What was actually executed
The uploaded three-part `GBPUSD_RULE_EVALUATOR_V2` workspace was reconstructed locally from the transferred parts and passed `unzip -t` with no archive errors. The canonical `PIVOT_SEQUENCE_V2_OUTPUT/GBPUSD_D1_STRUCTURE_PIVOT_SEQUENCE_V2.csv` and `DMI_ADX_V1_OUTPUT/GBPUSD_D1_DMI_ADX_2016_2024.csv` were then read directly.

## Inputs
- GBPUSD D1 OHLC: 2,544 rows, 2016-01-03 through 2024-12-31.
- Confirmed LOW pivots available through 2024-12-31: 344.
- PIVOT_SEQUENCE_V2 availability: pivot timestamp + two confirming bars; break observation begins after availability.
- 2025 excluded completely.

## Executable operator
For each confirmed LOW pivot:
1. Treat pivot price as the singleton Support boundary.
2. Search after support availability for the first completed D1 close strictly below Support.
3. The immediately following completed D1 close must also be strictly below the same Support boundary.
4. Only after that second close search for later range intersection with Support.
5. Role-reversal diagnostic requires a later intersecting D1 bar whose close is strictly below Support.

## Executed results
- Support candidates: 344
- First-below-support candidates: 326
- Decisive two-successive-close confirmations: 242
- First-break candidates without immediate second-close confirmation: 84
- Later range-intersection retest: 233 / 242 (96.28%)
- Later intersecting bar closing below Support: 229 / 242 (94.63%)

## Important correction
An earlier conversational replay reported 324 confirmations. That count corresponds to finding any pair of consecutive closes below Support somewhere after availability, not enforcing the contract's state machine of FIRST close = candidate followed immediately by SECOND close = confirmation. Under the frozen validation contract, the executable result is 242 confirmations. The earlier 324 figure is superseded and must not be used as validation evidence.

## Deterministic tests executed
The local evaluator unit suite passed: 4 passed in 0.06s.
Covered explicitly:
- first close candidate + second close confirmation
- intervening close above/equal Support blocks confirmation
- retest cannot occur on confirmation bar
- unavailable/wrong support source returns NOT_EVALUABLE

Replay integrity checks:
- Support availability precedes candidate break: PASS
- Confirmation is immediately next completed D1 close: PASS
- Retest starts strictly after confirmation: PASS
- Role-reversal evidence is strictly after confirmation: PASS
- 2025 contamination: ZERO
- No ATR/pips/percentage/clustering/tolerance/lookback used

## Interpretation
This is a deterministic executable validation result for the current 0008 operational contract. It is not a profitability result and does not constitute production freeze. The 242/344 result is the correct result for the explicitly frozen state machine used here.

## Remaining gate
Independent provenance review and final production-freeze decision remain required. The project must retain the 2025 OOS boundary and must not tune the operator against replay counts.
