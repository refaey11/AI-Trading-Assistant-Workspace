# CME 6B Open Interest Acquisition V1

## Objective
Supply Murphy rules that explicitly require futures Open Interest with authoritative CME 6B/BP OI evidence for 2024-2025.

## Source decision
CME Group Daily Bulletin / Volume & Open Interest is the primary source. CME states the Daily VOI report is preliminary and official data appears in the Daily Bulletin the following morning. Historical Daily Bulletin access is exposed through CME DataMine.

## Important constraint
This repository currently contains the adapter and governance logic, but no authoritative 2024-2025 CME 6B OI raw dataset. Do not manufacture OI, infer it from spot volume, or use CFTC COT as an OI substitute.

## Acquisition modes
1. Entitled CME DataMine API/download: preferred production path.
2. Historical Daily Bulletin files supplied/retrieved from CME: acceptable authoritative input after release-time validation.

## Required evidence lineage
Each OI row must retain:
- trade_date
- contract
- open_interest
- event_time
- available_time
- source
- revision_status
- raw_file_id

## Point-in-time rule
For each GBPUSD decision event, select the latest OI record with `available_time <= decision_time`. Future or unverified evidence is rejected.

## Next action
Load the 2024 and 2025 CME 6B OI raw files, validate completeness/release timing, then run Murphy 0022/0023 and the full 34-rule coverage audit.
