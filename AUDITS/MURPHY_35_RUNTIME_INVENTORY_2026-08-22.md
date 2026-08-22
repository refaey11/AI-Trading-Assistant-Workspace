# Murphy 35 Runtime Inventory — 2026-08-22

## Scope
The 35 Murphy rules currently recorded as CLOSED/FROZEN. This audit separates frozen governance state from executable Runtime state. No rule semantics or thresholds are changed here.

## Status legend
- **RUNTIME_CONFIRMED**: current Runtime status records the rule in the executable runtime set/integrated runtime batch, with routing + integration-test coverage recorded.
- **RUNTIME_CONFIRMED_LATEST**: later current-state record promotes the rule beyond the older 20-rule snapshot; runtime files/tests are present.
- **FROZEN_NOT_RUNTIME_PROVEN**: frozen/closed rule, but current evidence does not establish executable runtime routing + integration-test coverage.

## Matrix
| Rule | Frozen | Runtime status | Evidence basis |
|---|---|---|---|
| 0003 | YES | RUNTIME_CONFIRMED | Current runtime status; evaluator inventory |
| 0004 | YES | RUNTIME_CONFIRMED | Current runtime status; evaluator inventory |
| 0006 | YES | FROZEN_NOT_RUNTIME_PROVEN | Frozen continuity evidence; no current runtime routing record |
| 0007 | YES | FROZEN_NOT_RUNTIME_PROVEN | Frozen continuity evidence; no current runtime routing record |
| 0008 | YES | FROZEN_NOT_RUNTIME_PROVEN | Frozen status, but runtime batch audit explicitly says do not mark runtime PASS; blocker remains |
| 0018 | YES | RUNTIME_CONFIRMED_LATEST | Current State records IMPLEMENTED; runtime evaluator + runtime entry + integration tests |
| 0019 | YES | RUNTIME_CONFIRMED_LATEST | Current State records IMPLEMENTED; runtime evaluator + runtime entry + integration tests |
| 0021 | YES | RUNTIME_CONFIRMED | Current runtime status; evaluator inventory |
| 0022 | YES | RUNTIME_CONFIRMED | Current runtime status; evaluator inventory |
| 0023 | YES | RUNTIME_CONFIRMED | Current runtime status; evaluator inventory |
| 0025 | YES | FROZEN_NOT_RUNTIME_PROVEN | Frozen continuity evidence; no current runtime routing record |
| 0026 | YES | FROZEN_NOT_RUNTIME_PROVEN | Frozen continuity evidence; no current runtime routing record |
| 0028 | YES | RUNTIME_CONFIRMED | Current runtime status; shared 0027-0029 evaluator inventory |
| 0029 | YES | RUNTIME_CONFIRMED | Current runtime status; 0029 runtime adapter + tests |
| 0030 | YES | FROZEN_NOT_RUNTIME_PROVEN | Frozen/master-freeze evidence; no runtime routing entry in current Runtime status |
| 0031 | YES | FROZEN_NOT_RUNTIME_PROVEN | Frozen/master-freeze evidence; no runtime routing entry in current Runtime status |
| 0032 | YES | FROZEN_NOT_RUNTIME_PROVEN | Frozen/master-freeze evidence; no runtime routing entry in current Runtime status |
| 0033 | YES | FROZEN_NOT_RUNTIME_PROVEN | Frozen/master-freeze evidence; no runtime routing entry in current Runtime status |
| 0034 | YES | RUNTIME_CONFIRMED | Integrated runtime batch |
| 0035 | YES | RUNTIME_CONFIRMED | Integrated runtime batch |
| 0036 | YES | RUNTIME_CONFIRMED | Integrated runtime batch |
| 0037 | YES | RUNTIME_CONFIRMED | Integrated runtime batch |
| 0038 | YES | RUNTIME_CONFIRMED | Integrated runtime batch |
| 0039 | YES | RUNTIME_CONFIRMED | Integrated runtime batch |
| 0040 | YES | RUNTIME_CONFIRMED | Integrated runtime batch |
| 0041 | YES | RUNTIME_CONFIRMED | Integrated runtime batch |
| 0042 | YES | RUNTIME_CONFIRMED | Integrated runtime batch |
| 0043 | YES | RUNTIME_CONFIRMED | Integrated runtime batch |
| 0044 | YES | RUNTIME_CONFIRMED | Integrated runtime batch |
| 0045 | YES | RUNTIME_CONFIRMED | Integrated runtime batch |
| 0047 | YES | FROZEN_NOT_RUNTIME_PROVEN | Evidence-reconciled frozen; not in current 20-rule Runtime set |
| 0048 | YES | FROZEN_NOT_RUNTIME_PROVEN | Evidence-reconciled frozen; not in current 20-rule Runtime set |
| 0049 | YES | FROZEN_NOT_RUNTIME_PROVEN | Evidence-reconciled frozen; not in current 20-rule Runtime set |
| 0050 | YES | RUNTIME_CONFIRMED | Current runtime status; evaluator inventory |
| 0051 | YES | FROZEN_NOT_RUNTIME_PROVEN | Evidence-reconciled frozen; not in current 20-rule Runtime set |

## Totals
- Frozen/CLOSED Murphy rules: **35**
- Runtime confirmed in the current operational status plus latest 0018/0019 promotion: **22**
- Frozen but runtime not proven by current routing/integration evidence: **13**

### Runtime confirmed (22)
0003, 0004, 0018, 0019, 0021, 0022, 0023, 0028, 0029, 0034, 0035, 0036, 0037, 0038, 0039, 0040, 0041, 0042, 0043, 0044, 0045, 0050

### Frozen but not runtime-proven (13)
0006, 0007, 0008, 0025, 0026, 0030, 0031, 0032, 0033, 0047, 0048, 0049, 0051

## Important source limitation
The 2026-08-22 runtime batch audit states that the reconstructed evaluator workspace exposes only a subset of evaluator source entries and that underlying ZIP payload reads failed with corruption errors. Therefore the 22-rule Runtime classification is based on the current operational Runtime status plus the explicit latest 0018/0019 runtime promotion, while the 13-rule NOT-PROVEN classification intentionally avoids inferring runtime from frozen status alone.

## Next work
Do not reopen the 35-rule freeze scope. Park the 13 frozen-but-not-runtime-proven rules as Runtime TODOs and continue the project from the 22 confirmed Runtime rules.
