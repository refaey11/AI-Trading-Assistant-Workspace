# Murphy Runtime — CURRENT STATUS V2 (2026-08-22)

## Runtime count
**24 Runtime Implemented / 35 frozen Murphy rules**

## Newly verified in this update
- 0006 — runtime evaluator + tests + repository runtime entry-point integration
- 0007 — runtime evaluator + tests + repository runtime entry-point integration

## Runtime-verified set
0003, 0004, 0006, 0007, 0018, 0019, 0021, 0022, 0023, 0028, 0029, 0034, 0035, 0036, 0037, 0038, 0039, 0040, 0041, 0042, 0043, 0044, 0045, 0050

## Evidence for 0006/0007
- Operational contract: `MURPHY_0006_0007_FINAL_OPERATIONAL_CONTRACT.md`
- Historical QA: 15/15 reconciliation matches; 8 confirmations for 0006 and 7 for 0007; 7/7 unit tests; no availability/leakage violations; 2025 excluded.
- Runtime evaluator: `MURPHY_EVALUATORS_V1/murphy_0006_0007_runtime_v1.py`
- Tests: `MURPHY_EVALUATORS_V1/test_murphy_0006_0007_runtime_v1.py`
- Repository runtime entry point updated: `MURPHY_EVALUATORS_V1/murphy_runtime_entrypoint_v1.py`
- Local runtime tests for the new evaluator: 5/5 PASS.

## Important boundary
Runtime implementation is distinct from Production Frozen governance status. 0006/0007 are now Runtime Implemented, but their production-freeze checklist still has governance/freeze-manifest items open. Do not label them Production Frozen until those gates are explicitly approved.

## Remaining frozen-only / runtime-unproven rules
0008, 0025, 0026, 0030, 0031, 0032, 0033, 0047, 0048, 0049, 0051.
