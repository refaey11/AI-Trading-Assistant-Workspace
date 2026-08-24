# Murphy 0022/0023 — Evidence V1 Bridge Milestone

Date: 2026-08-24
Branch: `evidence-architecture-v1`

## Completed
- Corrected adapter registry provenance: historical OI is `CFTC_FUTURES_ONLY`, contract `GBP_FUTURES_096742`, while CME 6B is a separate future/external source candidate.
- Added `EVIDENCE_ARCHITECTURE_V1/existing_oi_bridge_v1.py` to adapt the existing source-locked 096742 OI alignment into the canonical Evidence Record V1 shape.
- Added `EVIDENCE_ARCHITECTURE_V1/test_existing_oi_bridge_v1.py`.
- Bridge behavior is fail-closed for missing OI and rejects future availability timestamps.
- Bridge does not alter Murphy 0022/0023 semantics, does not add thresholds, and does not use proxies.

## Validation
Local isolated unit test run: 3/3 PASS.

Cases:
1. Existing available OI row -> AUTHORITATIVE / AVAILABLE.
2. Missing OI -> MISSING / NOT_EVALUABLE.
3. Future availability -> INVALID / NOT_AVAILABLE.

## Provenance
The source project records Murphy 0022 and 0023 as production-frozen with CME British Pound futures 096742 OI context, availability-safe handling, and historical QA through 2024. The current 2025 gap is an evidence coverage gap, not a missing evaluator/rule implementation.

## Next step
Run the bridge against the existing aligned 2020–2024 OI datasets as an integration QA, then attach an authoritative 2025 futures-OI stream without changing 2025 OOS governance.
