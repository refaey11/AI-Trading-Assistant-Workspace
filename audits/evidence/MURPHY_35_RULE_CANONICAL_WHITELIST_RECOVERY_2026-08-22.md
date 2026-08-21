# Murphy 35-Rule Canonical Whitelist Recovery — 2026-08-22

## Purpose
Recover the exact canonical set of 35 Murphy rules that are confirmed frozen/closed, without treating all 51 historical registry rules as active and without reopening already closed rules.

## Authoritative evidence chain
1. `MURPHY_CANONICAL_RECONCILIATION_REGISTRY_V1` at commit `4be77bbb46dd6b2b97bc9b198416620af79e779d` records:
   - 19 `ALIGNED_FROZEN`
   - 2 `EXPLICITLY_APPROVED_FROZEN`
   - 14 `EVIDENCE_RECONCILED_FROZEN`
   - total confirmed frozen = 35
   - master-audit-only/open-deferred = 16
   - total rules = 51
2. `MURPHY_33_MASTER_FREEZE_MANIFEST_V1` provides the exact 33-rule historical freeze set.
3. The same reconciliation registry adds `MURPHY_0018` and `MURPHY_0019` as explicitly approved production-frozen rules.

## Canonical closed/frozen whitelist (35)
`MURPHY_0003, MURPHY_0004, MURPHY_0006, MURPHY_0007, MURPHY_0008, MURPHY_0018, MURPHY_0019, MURPHY_0021, MURPHY_0022, MURPHY_0023, MURPHY_0025, MURPHY_0026, MURPHY_0028, MURPHY_0029, MURPHY_0030, MURPHY_0031, MURPHY_0032, MURPHY_0033, MURPHY_0034, MURPHY_0035, MURPHY_0036, MURPHY_0037, MURPHY_0038, MURPHY_0039, MURPHY_0040, MURPHY_0041, MURPHY_0042, MURPHY_0043, MURPHY_0044, MURPHY_0045, MURPHY_0047, MURPHY_0048, MURPHY_0049, MURPHY_0050, MURPHY_0051`

## Excluded open/deferred set (16)
`MURPHY_0001, MURPHY_0002, MURPHY_0005, MURPHY_0009, MURPHY_0010, MURPHY_0011, MURPHY_0012, MURPHY_0013, MURPHY_0014, MURPHY_0015, MURPHY_0016, MURPHY_0017, MURPHY_0020, MURPHY_0024, MURPHY_0027, MURPHY_0046`

## Contract consequence
Any future Murphy evidence provider integration must treat the 35-rule list above as the current canonical governed whitelist and must not silently admit the 16 excluded rules.

This whitelist recovery does not create a new evaluator, change rule logic, tune thresholds, or alter historical artifacts. It is governance/provenance recovery only.

## 2025 control
2025 remains locked Out-of-Sample and is not used for tuning, calibration, threshold selection, or implementation selection.

## Next action
Use this exact whitelist to inspect the existing Rule Adapter / Murphy runtime path and determine whether the active evidence provider can filter to these governed rules without changing rule logic.