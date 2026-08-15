# Murphy 0008 — PF-B1 Implementation Dry Run V1

Status: EXPERIMENTAL / NOT FROZEN
Policy under test: TIME_FILTER — two successive completed D1 closes below support.

## Source-of-truth check
The current MASTER_TRADING_RULES_V2 record for MURPHY_0008 is READY_FOR_BACKTEST and defines the source semantics as: support is decisively broken to the downside; price later rallies toward the broken support. It does not contain an explicit decisive-break operator. Therefore this dry run does not modify the master rule.

## Deterministic evaluation contract under test
- Support must be available before the first candidate break bar.
- A completed D1 close below support is a candidate break.
- A second successive completed D1 close below support confirms the decisive break.
- Confirmation timestamp is the close of the second bar.
- Retest evidence is evaluated only on bars strictly after confirmation.
- If the second completed bar is unavailable, return NOT_EVALUABLE rather than guessing.
- No ATR, percentage, pip, tolerance, lookback, or future-bar information is introduced.

## Local unit dry-run
Synthetic cases were executed locally:
- Wick below support with close at/above support -> NOT_CONFIRMED.
- One close below followed by recovery -> NOT_CONFIRMED.
- Two successive closes below -> CONFIRMED at second close.
- Only one eligible completed bar -> NOT_EVALUABLE.
- Support becomes available after the alleged break -> NOT_EVALUABLE / rejected chronology.

## Important limitation
This is a contract/logic dry run, not a production historical result. The repository's MURPHY_0008 record still reports testing status UNTESTED. No 2025 data is used.

## Next gate
Run the deterministic evaluator against the authoritative historical D1 dataset only after the approved PF-B1 policy is frozen. Then independently perform 2016–2024 QA, availability/no-lookahead validation, and role-reversal evidence tests.
