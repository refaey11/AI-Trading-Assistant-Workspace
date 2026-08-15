# Murphy 0025–0026 — Four-Week Compatibility Audit V1

Date: 2026-08-15
Status: OPERATOR CONTRACT IDENTIFIED / EVALUATOR IMPLEMENTATION GATE OPEN

## Source-locked Four-Week contract
The reconstructed Workspace contains `FOUR_WEEK_LOOKBACK_V1_OUTPUT/FOUR_WEEK_LOOKBACK_CONTRACT_V1.json` and `FOUR_WEEK_LOOKBACK_BUILD_CONTRACT_FINAL_V1.json`.

The contract defines:
- reference window = four completed calendar weeks immediately preceding the current calendar week;
- current week excluded from the reference window;
- no 20/50/100-bar substitution;
- 0025 uses the preceding four-week high;
- 0026 uses the preceding four-week low;
- Dynamic MTF decides where the feature is consumed; the Four-Week module itself does not select a timeframe;
- 2025 excluded from tuning/selection.

The build contract further specifies price basis:
- four-week high uses HIGH;
- four-week low uses LOW;
- four completed ISO calendar weeks precede the current ISO week.

## Rule mappings
0025: `current high >= preceding-four-completed-weeks high` → bullish context.
0026: `current low <= preceding-four-completed-weeks low` → bearish context.

The mapping artifacts explicitly reject fixed-bar substitutes and mark validation pending until the Four-Week convention is bound.

## Important artifact discrepancy found
The weekly reference artifact is internally consistent: its `new_four_week_high/low` flags agree with the weekly high/low crossing the preceding four-week reference.

The H1 derived artifact propagates the weekly `new_four_week_high/low` flag across H1 rows in a week. Therefore those boolean columns must NOT be treated as the exact row-level evaluator condition for 0025/0026.

A row-level evaluator must instead use the source H1 `high`/`low` against the preceding four completed calendar-week reference values. This is an integration/binding correction, not a new trading rule.

## No invented semantics
This audit does not introduce:
- a fixed H1 bar count;
- a hidden lookback;
- a new threshold;
- a new timeframe;
- a close-only substitute;
- 2025 tuning.

## Gate
0025–0026 now have a source-locked operator contract. The next step is the smallest evaluator implementation using existing Four-Week reference evidence, followed by deterministic tests and 2016–2024 historical QA.
