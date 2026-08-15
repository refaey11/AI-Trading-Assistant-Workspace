# Hybrid Evidence Murphy Pilot — Results V1

Date: 2026-08-16
Status: PILOT / NOT PRODUCTION

## Important scope boundary
This run tests the **engineering evidence architecture**, not a production Murphy pattern evaluator. The source-reconciled Murphy rules 0013–0020 still require approved shared canonical primitives for horizontal levels, convergence/parallelism, and breakout confirmation. Those primitives were not replaced by this pilot.

## Dataset
- GBPUSD D1
- 2,544 rows
- 2016–2024
- Calibration: 2016–2018
- Evaluation: 2019–2024 (1,609 rows)
- 2025: excluded

## Pilot measurements
A fixed 20-completed-bar observation window was used solely as an engineering pilot parameter. It was declared before evaluation and was not optimized on evaluation outcomes.

Three engineering measurements were generated:
1. Horizontalness proxy — normalized average boundary slope magnitude.
2. Convergence-strength proxy — normalized shrinkage of the recent high/low range.
3. Breakout-magnitude proxy — close penetration beyond the prior window high/low normalized by ATR(14) already present in the dataset.

The 2016–2018 calibration block defined fuzzy membership bounds using the 10th and 90th percentiles only. No 2019–2024 performance metric was used to select these bounds, and 2025 was not accessed.

Calibration bounds:
- horizontalness: 0.9598842151 to 0.9970281710
- convergence_strength: 0.0000000000 to 0.4383250825
- breakout_magnitude: 0.0000000000 to 0.0432365622

## Evaluation output
All 1,609 evaluation rows received engineering evidence for all three pilot measurements.

Hybrid evidence grade distribution:
- LOW: 786
- MEDIUM: 699
- HIGH: 124

These grades are **engineering evidence only**. They are not Murphy pass/fail conditions and do not generate direction.

## Hard-gate invariant
A canonical failure with engineering measurements at 0.99/0.99 remains `NOT_EVALUABLE`.
This confirms that the engineering layer cannot rescue a failed canonical gate.

## No-lookahead test
At cutoff 2022-12-30, all future OHLC values were heavily modified after the cutoff and the pre-cutoff hybrid evidence was recomputed.
Maximum pre-cutoff score difference: **0.0**.

Result: PASS for this pilot's feature implementation.

## Interpretation
### What passed
- The architecture can represent qualitative concepts as separate engineering evidence without changing the canonical gate.
- Parameters can be declared from the calibration block rather than selected from evaluation performance.
- The pilot feature calculations are prefix-stable under a future-suffix mutation test.
- Evidence remains evidence-only.

### What did NOT pass / is not claimed
- This does **not** prove Murphy 0013–0020 are now production evaluators.
- The raw OHLC pilot proxies are not substitutes for the required PIVOT_SEQUENCE_V2 / TRENDLINE_GEOMETRY_V1 / approved BREAKOUT_CONFIRMATION contracts.
- No trading profitability conclusion is permitted.
- No production freeze or merge is authorized.

## Pilot decision
**ARCHITECTURE: PASS AS AN ENGINEERING-EVIDENCE PILOT.**

**MURPHY RULE INTEGRATION: NOT YET PROVEN.**

Next required step: attach the engineering evidence layer to the existing canonical shared primitives for one or two actual Murphy rules (starting with 0014/0018 or 0013/0016), then rerun historical QA and provenance checks. If that integration preserves the same invariants, the architecture can be promoted for broader qualitative-rule use.
