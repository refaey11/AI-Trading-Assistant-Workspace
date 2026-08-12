# Murphy MTF Alignment Evidence Reconciliation V1

Date: 2026-08-12

## Context

Continue from the Murphy freeze sprint. Do not change the project path.

## Newly verified evidence availability

The File Library / Workspace audit lists existing Murphy and MTF artifacts including:
- `GBPUSD_RULE_EVALUATOR_V2/MURPHY_51_RULE_TO_MTF_FUNCTION_MAP_V1.csv`
- `GBPUSD_RULE_EVALUATOR_V2/MURPHY_51_TIMEFRAME_MAPPING_AUDIT_V1.csv`
- `GBPUSD_RULE_EVALUATOR_V2/DYNAMIC_TIMEFRAME_SELECTION_EXAMPLES_V1.csv`
- `GBPUSD_RULE_EVALUATOR_V2/MURPHY_51_EXACT_CONDITION_PREP_V1.csv`
- exact mapping slices for multiple Murphy rule ranges.

The Workspace audit also records MTF Alignment archives with M5 alignment datasets and manifests across multiple assets/years, including EURUSD, GBPUSD, USDJPY, XAUUSD, and USDCAD. Annual files exist for 2016–2025 and later years in the preserved workspace audit inventory.

## Compatibility conclusion

These artifacts materially strengthen the existing **Dynamic MTF / timeframe evidence layer** for Murphy. They should be reused for:
- rule-to-timeframe binding verification;
- availability/no-lookahead checks;
- cross-asset MTF evidence consistency;
- evaluator input compatibility.

They do **not** by themselves resolve missing semantic operators such as:
- Murphy 0002 entry/exit timing;
- Murphy 0006–0007 successful touch/reaction confirmation;
- Murphy 0027 exact trend-vs-range regime operator;
- Murphy 0003–0004 historical provenance.

## Important OOS control

MTF archives contain 2025 files, but 2025 remains OOS. Those rows must not be used for tuning, implementation selection, or operator/threshold selection. They may only be used later for the official OOS evaluation gate.

## Freeze impact

For Murphy rules that already have a source-backed operator/evaluator, the MTF archives can now be treated as an existing compatibility/evidence source rather than a blocker.

For blocked rules, MTF evidence should only be used to close the MTF/availability gate; it cannot manufacture the missing semantic operator.

## Next action

Use the existing MTF mapping/audit artifacts to perform the remaining Murphy freeze checks, prioritizing:
1. exact timeframe binding and availability for evaluator-backed rules;
2. 0006–0007 compatibility with existing Trendline Geometry and MTF;
3. remaining rules whose current blocker is feature/MTF rather than source semantics.

Do not rebuild Dynamic MTF or create a new MTF selector.
