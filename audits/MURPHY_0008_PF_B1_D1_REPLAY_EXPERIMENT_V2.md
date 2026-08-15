# Murphy 0008 — PF-B1 D1 Replay Experiment V2

Status: EXPERIMENTAL / NOT PRODUCTION FROZEN
Date: 2026-08-15
Scope: GBPUSD D1, 2016-2024 only. 2025 excluded.

## Source data actually used
- Canonical workspace reconstruction: workspace_full_reconstructed.zip
- D1 OHLC source path used for replay: DMI_ADX_V1_OUTPUT/GBPUSD_D1_DMI_ADX_2016_2024.csv (contains timestamp/open/high/low/close)
- Canonical Pivot Sequence V2: PIVOT_SEQUENCE_V2_OUTPUT/GBPUSD_D1_STRUCTURE_PIVOT_SEQUENCE_V2.csv
- Pivot contract: confirmed after 2 bars; availability used as no-lookahead gate.

## Experimental policy
TIME_FILTER candidate only: two successive completed D1 closes below a pivot-derived support boundary.
- first close below = candidate break
- second successive close below = decisive confirmation
- confirmation timestamp = second close timestamp
- no data from after confirmation is used to define the break

## Support population
Each confirmed LOW pivot is treated as an individual support candidate at its pivot price, with the pivot availability timestamp as the earliest eligibility time. This is an experiment and is NOT a frozen PF-H1 level-clustering contract.

## Replay result
- confirmed LOW support candidates: 404
- candidates with a two-successive-close downside break: 324
- candidates without such a break before the end of 2024: 80
- confirmation events are counted per support candidate; they are not deduplicated into unique market events.

## Later retest diagnostic
A later retest was defined only for diagnostic purposes as a subsequent D1 bar whose HIGH reached or exceeded the broken support price.
- confirmed breaks with later retest: 314 / 324

A stricter role-reversal diagnostic required the later bar HIGH to reach/exceed support while that bar CLOSED below support:
- strict role-reversal diagnostics: 308 / 324

These are evidence diagnostics only. No retest window, tolerance, or outcome threshold was tuned or promoted to production.

## Important interpretation
The replay demonstrates that the candidate two-close policy can be executed against the real workspace D1 + Pivot V2 lineage and that chronology/availability can be enforced. It does NOT prove that two D1 closes is the final approved PF-B1 policy, nor does it authorize a production evaluator.

No 2025 data was used. No threshold was selected from performance. No ATR, pip, percentage, hidden lookback, or tolerance was introduced.

## Current gate
PF-B1 remains GOVERNANCE / NOT FROZEN. 0008 production evaluation remains blocked until the policy is explicitly approved and PF-H1 compatibility is closed.
