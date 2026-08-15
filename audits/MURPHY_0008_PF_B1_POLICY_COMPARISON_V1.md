# Murphy 0008 — PF-B1 Policy Comparison V1

Date: 2026-08-15
Status: EXPERIMENT ONLY / NOT A FREEZE
Universe: GBPUSD D1, 2016-01-01 through 2024-12-31
OOS exclusion: 2025 not used

## Purpose
Compare two source-supported PF-B1 candidate policies on the same confirmed pivot-low candidates, without tuning from performance:

- TIME_FILTER: two successive completed D1 closes below the support candidate.
- PRICE_FILTER: first completed D1 close at or below 97% of the support candidate (3% penetration).

## Upstream data
- Confirmed pivot-low candidates: 402
- Pivot confirmation/availability is respected; bars before the candidate's availability timestamp are not eligible.
- D1 OHLC: GBPUSD D1 2016-2024 project dataset.

## Results
| Metric | TIME_FILTER: 2 D1 closes | PRICE_FILTER: 3% close penetration |
|---|---:|---:|
| Confirmed pivot-low candidates | 402 | 402 |
| Candidate breaks confirmed | 324 | 280 |
| Confirmation rate | 80.60% | 69.65% |
| Unique break timestamps | 196 | 90 |
| Median days from availability to confirmation | 18 | 137 |
| Retest within 5 subsequent D1 bars | 189 (58.33%) | 2 (0.71%) |
| Retest within 10 subsequent D1 bars | 225 (69.44%) | 38 (13.57%) |
| Retest within 20 subsequent D1 bars | 241 (74.38%) | 44 (15.71%) |
| Retest within 40 subsequent D1 bars | 259 (79.94%) | 95 (33.93%) |
| Retest within 60 subsequent D1 bars | 269 (83.02%) | 109 (38.93%) |

Retest diagnostic definition: after confirmation, any of the next N D1 bars has High >= the original support candidate. This is diagnostic only; it is NOT being proposed as a 0008 rule or new threshold.

## Interpretation
1. The two policies are materially different operationally even though both are source-supported filter families.
2. The 3% policy is substantially slower and produces fewer distinct break timestamps in this experiment.
3. The 2-close policy confirms earlier and produces substantially more near-term retest opportunities.
4. These results do NOT prove that the 2-close policy is the correct Murphy 0008 policy. They show only the behavioral consequences of the two candidate operators on the existing project data.
5. No threshold was selected by optimizing these results. 2025 was not used.

## Important methodological note
This experiment uses the project's confirmed pivot-low candidate as the support boundary and completed D1 closes for confirmation. It does not claim that `break_structure_down` is already equivalent to PF-B1 decisive confirmation. The existing governance reconciliation states that `break_structure_down` is an upstream candidate and that the decisive definition remains a governance decision.

## Decision status
- TIME_FILTER / 2 D1 closes: viable candidate; NOT FROZEN.
- PRICE_FILTER / 3% close penetration: viable candidate; NOT FROZEN.
- 0008 evaluator: remains un-frozen until Governance selects and approves the PF-B1 operator.
