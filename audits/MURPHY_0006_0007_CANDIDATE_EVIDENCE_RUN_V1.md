# Murphy 0006–0007 Candidate Evidence Run V1

Date: 2026-08-12
Period: 2016-01-01 through 2024-12-31 (2025+ excluded)

## Inputs actually reconstructed/read

- `PIVOT_SEQUENCE_V2_OUTPUT/GBPUSD_D1_STRUCTURE_PIVOT_SEQUENCE_V2.csv`
- `TRENDLINE_GEOMETRY_V1_OUTPUT/GBPUSD_D1_STRUCTURE_TRENDLINES_V1.csv`
- `DMI_ADX_V1_OUTPUT/GBPUSD_D1_DMI_ADX_2016_2024.csv` used only for D1 OHLC evidence (`timestamp/open/high/low/close`), not as a Murphy rule source.

The original Pivot lineage still names `D1/GBPUSD_D1_STRUCTURE.csv` as its source file.

## Method

For each Geometry line:
1. Require the Murphy family mapping: 0006 = LOW + UP; 0007 = HIGH + DOWN.
2. Select the first confirmed same-type pivot after point 2 as a third-touch candidate.
3. Calculate the mathematical line price at that pivot timestamp.
4. Record distance and whether the D1 High/Low range intersects the line.
5. Record the next confirmed opposite-type pivot as a reaction candidate.
6. Record whether that next pivot is directionally consistent and on the expected side of the line.
7. Record raw post-touch daily-range breaches until the next opposite pivot as no-break candidate evidence.
8. Do not apply any touch tolerance, reaction magnitude, ATR, pip, percentage, lookback, or automatic 3%/2-day rule binding.

## Results

| Rule | Candidate lines 2016–2024 | D1 range intersects line | Directional reaction candidate | Reaction on expected side | No-break candidate to next opposite pivot | Exact touch |
|---|---:|---:|---:|---:|---:|---:|
| MURPHY_0006 | 166 | 32 | 163 | 91 | 41 | 0 |
| MURPHY_0007 | 181 | 30 | 178 | 114 | 65 | 0 |

Additional diagnostic:
- 0006: 3 candidates within 0.0005 absolute price distance of the line; 0 exact.
- 0007: 2 candidates within 0.0005; 0 exact.
These distance values are diagnostics only and are not used as a rule threshold.

## Interpretation

The canonical upstream artifacts are sufficient to generate reproducible candidate evidence. They are not sufficient to authorize production PASS/FAIL because the reviewed source does not define a deterministic `successful touch + reaction` operator.

Therefore every row in the candidate output remains `CANDIDATE_ONLY`.

## Safety

- No 2025+ data used.
- No tuning on OOS data.
- No invented threshold.
- No automatic 3% or 2-consecutive-day binding to 0006/0007.
- No modification to PIVOT_SEQUENCE_V2 or TRENDLINE_GEOMETRY_V1.
