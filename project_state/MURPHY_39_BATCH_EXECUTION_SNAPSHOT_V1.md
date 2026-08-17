# Murphy 39-Rule Batch Execution Snapshot V1

Basis: MURPHY_39_BATCH_AUDIT_QUEUE_V1.csv + MURPHY_39_ACCELERATOR_REGISTRY_V1.csv + Master KB candidate rules.
Scope: 39 open Murphy rules (0013-0051 by canonical numbering), excluding the 12 protected/closed rules.

## Batch result

| Rule | Current status | Work lane | Accelerator | Next gate |
|---|---|---|---|---|
| 0001 | REVIEW | SEMANTIC_AUDIT | SHARED_EVIDENCE | source_operator_audit |
| 0002 | NOT_EVALUABLE | TIMING_AUDIT | SHARED_EVIDENCE | timing_producer_compatibility |
| 0005 | UNBLOCKED | FEATURE_AUDIT | PIVOT_SEQUENCE_V2 | source_contract_and_evaluator |
| 0009 | REVIEW | BREAKOUT_AUDIT | SHARED_PF_B1 | decisive_break_contract |
| 0010 | NOT_EVALUABLE | FILTER_AUDIT | SHARED_EVIDENCE | source_filter_contract |
| 0011 | REVIEW | STRUCTURE_AUDIT | PIVOT_SEQUENCE_V2 | established_trend_contract |
| 0012 | REVIEW | STRUCTURE_AUDIT | PIVOT_SEQUENCE_V2 | reversal_consolidation_contract |
| 0013 | REVIEW | GEOMETRY_AUDIT | SHARED_PF_B1 | convergence_and_breakout_binding |
| 0014 | UNBLOCKED | PIVOT_AUDIT | PIVOT_SEQUENCE_V2 | point_qualification_contract |
| 0015 | UNBLOCKED | PIVOT_AUDIT | PIVOT_SEQUENCE_V2 | point_qualification_contract |
| 0016 | UNBLOCKED | FLAGPOLE_AUDIT | SHARED_EVIDENCE | flagpole_detector_contract |
| 0017 | UNBLOCKED | FLAGPOLE_AUDIT | SHARED_EVIDENCE | flagpole_detector_contract |
| 0018 | UNBLOCKED | GEOMETRY_AUDIT | SHARED_EVIDENCE | converging_two_line_contract |
| 0019 | UNBLOCKED | GEOMETRY_AUDIT | SHARED_EVIDENCE | converging_two_line_contract |
| 0020 | REVIEW | S_R_AUDIT | SHARED_EVIDENCE | horizontal_parallel_tolerance_contract |
| 0024 | REVIEW | INDICATOR_BINDING_AUDIT | EXISTING_MA_MODULE | exact_ma_spec_binding |
| 0027 | PARTIAL | EVIDENCE_AUDIT | EXISTING_OSCILLATOR_MODULE | strong_trend_range_gate |
| 0030 | NOT_EVALUABLE | PNF_AUDIT | EXISTING_PNF_WORK | verified_pnf_feature_and_source |
| 0031 | NOT_EVALUABLE | PNF_AUDIT | EXISTING_PNF_WORK | verified_pnf_trend_feature |
| 0032 | NOT_EVALUABLE | PNF_AUDIT | EXISTING_PNF_WORK | verified_pnf_trend_feature |
| 0033 | REVIEW | NISON_INTEGRATION_AUDIT | EXISTING_NISON_INTEGRATION | candlestick_context_contract |
| 0034 | NOT_EVALUABLE | ELLIOTT_AUDIT | SHARED_EVIDENCE | verified_wave_structure |
| 0035 | NOT_EVALUABLE | ELLIOTT_AUDIT | SHARED_EVIDENCE | verified_wave_length |
| 0036 | NOT_EVALUABLE | ELLIOTT_AUDIT | SHARED_EVIDENCE | verified_wave_structure |
| 0037 | REVIEW | FIBONACCI_AUDIT | EXISTING_FIBONACCI_MODULE | source_level_binding |
| 0038 | NOT_EVALUABLE | CYCLE_AUDIT | SHARED_EVIDENCE | verified_cycle_trough |
| 0039 | REVIEW | DECISION_BRAIN_GATE | DECISION_BRAIN_PROCESS | process_gate_contract |
| 0040 | UNBLOCKED | INDICATOR_AUDIT | EXISTING_SAR_MODULE | exact_sar_operator |
| 0041 | UNBLOCKED | INDICATOR_AUDIT | EXISTING_DMI_ADX_MODULE | exact_dmi_adx_operator |
| 0042 | REVIEW | RISK_AUDIT | EXISTING_RISK_ENGINE | risk_rule_binding |
| 0043 | REVIEW | RISK_AUDIT | EXISTING_RISK_ENGINE | exposure_scope_binding |
| 0044 | REVIEW | RISK_AUDIT | EXISTING_RISK_ENGINE | risk_per_market_binding |
| 0045 | REVIEW | RISK_AUDIT | EXISTING_RISK_ENGINE | margin_scope_binding |
| 0046 | REVIEW | BREADTH_AUDIT | EXISTING_BREADTH_DATA | broad_market_dataset_verification |
| 0047 | NOT_EVALUABLE | BREADTH_AUDIT | EXISTING_BREADTH_DATA | ad_line_and_new_highs_verification |
| 0048 | NOT_EVALUABLE | BREADTH_AUDIT | EXISTING_TRIN_DATA | trin_ma_verification |
| 0049 | NOT_EVALUABLE | BREADTH_AUDIT | EXISTING_TRIN_DATA | trin_verification |
| 0050 | PARTIAL | COMBINED_EVIDENCE_AUDIT | SHARED_EVIDENCE | subcontract_closure |
| 0051 | REVIEW | DECISION_BRAIN_GATE | DECISION_BRAIN_PROCESS | checklist_contract |

## Counts

- REVIEW: 16
- NOT_EVALUABLE: 12
- UNBLOCKED: 9
- PARTIAL: 2
- Total: 39

## Execution policy

1. Process all UNBLOCKED rules first using their named existing accelerator.
2. Process REVIEW/PARTIAL rules only through their named next gate; do not infer missing operators.
3. NOT_EVALUABLE rules remain blocked until the required evidence/primitive exists.
4. No new semantics, thresholds, lookbacks, tolerances, or proxies may be invented.
5. Nison integration remains a separate workstream; 2025 remains OOS and cannot be used for tuning.
6. Production freeze requires implementation, tests, availability/no-lookahead, and QA evidence; this snapshot is not a freeze.
