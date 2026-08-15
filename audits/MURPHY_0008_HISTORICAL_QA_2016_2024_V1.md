# MURPHY 0008 Historical QA — 2016-2024 V1

Status: EXPERIMENTAL / NOT FROZEN
Policy under test: TIME_FILTER — two successive completed D1 closes below the confirmed pivot-low support.
2025: EXCLUDED.

## Data basis
- D1 GBPUSD OHLC: project DMI/ADX D1 dataset, 2016-2024.
- Support candidates: 402 D1 LOW pivots from PIVOT_SEQUENCE_V2.
- Pivot availability is respected: only bars strictly after availability are eligible to confirm a break.

## Results
- Support candidates evaluated: 402
- Candidates with two successive D1 closes below support: 242
- Unique confirmation timestamps: 164
- Candidates with later retest evidence: 229 / 242
- Later retest definition used for this diagnostic: a later bar (strictly after confirmation) whose high reaches/exceeds the former support while its close is at/below the former support.

## Timing diagnostics
- Median confirmation delay from pivot availability: 12.5 days.
- Median later-retest delay from confirmation: 9 days among events with a retest.
- 25th/50th/75th percentile retest delay: 3 / 9 / 44 days.

## Important interpretation
This is a historical QA diagnostic, not a performance/tuning exercise. The retest definition is explicitly labeled diagnostic and is NOT being proposed as a new production threshold. No 2025 data was used. No parameter was optimized on the historical results.

## Caveats
- Multiple pivot candidates can map to the same confirmation timestamp; unique confirmation timestamps are therefore lower than candidate-level confirmations.
- The result validates that the proposed event sequence is operationally testable on the available project data; it does not establish that the two-close policy is source-mandated by Murphy.
- Production freeze remains blocked pending governance approval, implementation/unit tests, provenance review, and freeze manifest review.
