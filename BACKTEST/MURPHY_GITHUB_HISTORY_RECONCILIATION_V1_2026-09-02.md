# Murphy 34 — GitHub History Reconciliation V1

Date: 2026-09-02
Branch: diagnostic/murphy-34-recovery-2026-09-02
Scope: governed Murphy 34 only
Locked year: 2025

## Purpose

Reconcile the current 34-rule producer map against authoritative project history already committed to GitHub. This document does NOT promote any rule to current fan-in decision eligibility and does NOT create synthetic historical evidence.

## Verified GitHub history

### MURPHY_0006 / MURPHY_0007
GitHub history contains:
- source-safe candidate evidence work;
- deterministic compatibility/audit work;
- executable evaluator source;
- runtime entry-point integration;
- explicit promotion to Runtime Implemented.

Evidence references:
- `2e1100f9ed398493f1004e3a3f485ada622c5717` — Record 2016-2024 candidate evidence run.
- `a2e25578a582693c83fee62cf6b95587808f5dd4` — V4 evidence audit for runtime gate.
- `d485ebc4de64a97206deba422ae47235037a8d21` — Promote 0006/0007 to Runtime Implemented.

Current decision-eligibility conclusion: NOT promoted here. The current governed fan-in does not contain a production-frozen 0006/0007 PASS stream.

### MURPHY_0018 / MURPHY_0019
GitHub history contains:
- exact evaluators;
- exact no-threshold trendline convergence adapter;
- approved geometry-to-convergence runtime adapter;
- canonical runtime entry point;
- explicit Runtime Implemented promotion and production-freeze records.

Evidence references:
- `61a3ac8ed26fbc2dab603a10a3bf5d6d933d84d8` — exact evaluators.
- `53e8a366297b3ea0a5e9e5de21e14de4bc69b92b` — exact no-threshold convergence adapter.
- `19574e6f8a6b65069ba0c4104f5ac34e6e1cc1b2` — approved geometry-to-convergence runtime adapter.
- `33316a927b28efd6924a49e92da83dac8ca412f3` — canonical runtime entry point.
- `05da42997104bcc9970a501150895ade5b45a85e` — promotion to Runtime Implemented.

Current decision-eligibility conclusion: Runtime/freeze history is verified, but current 2016-2024 source-backed producer rows are still absent from the present fan-in. Do not fabricate rows or silently promote.

### MURPHY_0030 / MURPHY_0031 / MURPHY_0032
GitHub history explicitly records these as PRODUCTION FROZEN.

Evidence reference:
- `0b6bb1f1636dc2265317634948d80fd7ec58460e` — freeze 0030-0032; frozen P&F production path, deterministic 7/7 local QA, 2,544 canonical D1 rows for 2016-2024, and no 2025 use.

Current decision-eligibility conclusion: frozen project history exists. Current governed fan-in still does not contain rows for 0030-0032. Historical producer data must be recovered/bound before current fan-in promotion.

### MURPHY_0033
GitHub history explicitly records a canonical freeze and later runtime wiring/verification.

Evidence references:
- `cc7e4e4a851568fe3d6e6d152ddab6d469b6b889` — canonicalize 0033 after QA gates.
- `0d66be46c37c39904bf4a42fd309c59eaaee6a12` — canonical freeze candidate.
- `b20a2a5723dbdc9d26d0c61a61362ef343e90d49` — verify 0030-0033 runtime wiring.

Current decision-eligibility conclusion: project history is stronger than the current producer map's `producer_not_bound` label, but the current fan-in has no 0033 rows. Keep decision eligibility blocked until the historical producer/evidence payload is recovered and strict-as-of bound.

### MURPHY_0034–MURPHY_0045
GitHub history explicitly contains a reconciled/local production-freeze package for this batch.

Evidence references:
- `109e1611395f44a5c4fd970d0eb96112ca1d81c3` — recovery of source-backed evaluator implementation from production freeze.
- `3cf864579677f36bd3f7c9e0d3afe46a40c3d649` — restore frozen 0034-0045 evaluators.
- `597368c4c8a06c6601761082da70f1a71bda2096` — uploaded local freeze/closure evidence reconciliation for 0033-0045 and 0047-0051.

The reconciliation record explicitly describes `MURPHY_BATCH_0034_0045_PRODUCTION_FREEZE_V1` as `LOCAL_PRODUCTION_FROZEN`, fail-closed when upstream evidence is absent, and excludes 2025 tuning. The same record includes a process/context treatment for 0042-0045.

Current decision-eligibility conclusion: historical freeze provenance exists in GitHub history, but it is not equivalent to current fan-in source rows. Preserve blocked/non-market semantics where applicable; do not synthesize market rows.

### MURPHY_0047–MURPHY_0049
GitHub history contains a closed batch record for 0047-0049.

Evidence references:
- `efbbd43970487b6205c671ba94a98afd949ca508` — promote 0047 runtime and block 0048-0049 on missing operators.
- `d2a035b33c620190bd0a287644960f1b6a13b476` — verify 0047 runtime and block 0048-0049.
- `597368c4c8a06c6601761082da70f1a71bda2096` — `MURPHY_0047_0049_CLOSED_FINAL_V1`, coverage 2016-01-04 to 2020-02-10, no synthetic rows, no proxy substitution, no new thresholds/timeframes; occurrence-count discrepancy is documented.

Current decision-eligibility conclusion: 0047 has stronger historical closure evidence than the current `producer_family_discovered_pending_binding` label, but the exact historical producer payload is not present in current fan-in. 0048/0049 remain blocked because the operator/source contract is not current-frozen for integration.

### MURPHY_0050 / MURPHY_0051
GitHub history contains the final process-gate closure package.

Evidence reference:
- `597368c4c8a06c6601761082da70f1a71bda2096` — 0050/0051 `PROCESS_GATE_FROZEN`, with deterministic QA and explicit non-directional controls.

Current decision-eligibility conclusion: these are non-directional process gates and should not be treated as missing market directional producers.

## Result

The current producer map is conservative relative to older GitHub project history in several places. The important distinction is:

`GitHub history / freeze record != current governed 2016-2024 fan-in row availability`.

Therefore this reconciliation changes the investigation priority only. It does not change current fan-in eligibility, rule semantics, risk logic, or 2025 OOS isolation.

## Next binding priority

1. Recover exact historical producer payloads for 0018-0019, 0030-0033, 0034-0041, and 0047 where GitHub history proves prior freeze/closure records exist.
2. For every recovered payload, verify exact field semantics, provenance, availability timestamp, strict-as-of binding, and 2025 exclusion.
3. Only after those gates pass, rebuild the governed fan-in and rerun the 2016-2024 diagnostic/backtest.
