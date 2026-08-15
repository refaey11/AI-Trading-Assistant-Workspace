# Murphy 0008 — Two-Day Execution Plan V1

Status: EXPERIMENTAL EXECUTION PLAN — NOT PRODUCTION FROZEN

## Decision for this run
Use TIME_FILTER / two successive completed D1 closes below the Support boundary as the candidate PF-B1 decisive-break operator for 0008.

This is a project operationalization for this experiment, not a claim that Murphy's text names Rule 0008 specifically.

## Execution order
1. Load authoritative GBPUSD D1 OHLC and PIVOT_SEQUENCE_V2.
2. Use only support candidates whose availability timestamp precedes the first break bar.
3. First completed D1 close below Support = candidate.
4. Second successive completed D1 close below Support = decisive-break confirmation.
5. Begin retest/role-reversal observation only after the confirmation bar closes.
6. Do not use 2025 for selection, tuning, or policy evaluation; scope QA to 2016–2024.
7. Report evidence counts and event timestamps; do not convert diagnostic retest frequency into trading performance.

## Hard exclusions
No ATR, pip tolerance, arbitrary percentage, hidden lookback, clustering tolerance, or backtest-based policy selection.

## Outputs required
- event-level confirmation records
- no-lookahead/availability audit
- edge-case results
- later retest/role-reversal diagnostics
- provenance/evidence artifact
- explicit PASS / FAIL / NOT_EVALUABLE status

## Freeze gate
A successful experimental run does not itself freeze PF-B1 or 0008. Production freeze requires the project governance approval and the remaining PF-H1/0008 validation gates.
