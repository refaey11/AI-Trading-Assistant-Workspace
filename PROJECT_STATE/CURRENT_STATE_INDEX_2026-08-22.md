# CURRENT STATE INDEX — 2026-08-22

## Purpose
Single entry point for the live project state. When multiple versions exist, read this index first.

## Current operational source of truth
1. This index
2. `AUDITS/MURPHY_FINAL_COMPATIBILITY_AUDIT_2026-08-22.md`
3. Rule-specific newest final/approval record
4. `AUDITS/MURPHY_35_RUNTIME_MATRIX_V2_2026-08-22.md` (older conservative snapshot; not newer than the final compatibility audit)
5. `AUDITS/MURPHY_35_RUNTIME_INVENTORY_2026-08-22.md` (older conservative snapshot)
6. Canonical/frozen source artifacts
7. Historical audits and recovery files

## Murphy active scope
**35 Frozen/Closed rules**

## Verified Runtime count
**34 / 35**

## Verified Runtime rules
0003, 0004, 0006, 0007, 0018, 0019, 0021, 0022, 0023, 0025, 0026, 0028, 0029, 0030, 0031, 0032, 0033, 0034, 0035, 0036, 0037, 0038, 0039, 0040, 0041, 0042, 0043, 0044, 0045, 0047, 0048, 0049, 0050, 0051.

## Frozen / Runtime NOT PROVEN / BLOCKED
**0008 only**.

## Important corrections
- An earlier checkpoint recorded **35/35 Runtime Implemented**. That was too broad.
- The older conservative matrix recorded **22/35** because it pre-dated the latest current GitHub adapters/tests.
- The final compatibility audit reconciles those two states to **34/35 verified Runtime**, with **0008 blocked**.
- Frozen/Closed does not imply Runtime Implemented.

## Rule 0008 — LIVE BLOCKER
The canonical 0006–0008 freeze artifact does not approve an operational definition for `decisively broken`. The runtime has been corrected to fail closed with `NOT_EVALUABLE` until an approved PF-B1 binding exists. No generic threshold or role-reversal mapping is being invented.

## Recent runtime fixes verified
- 0030–0032 had a real status-overwrite bug where the P&F reference payload's `status=AVAILABLE` overwrote the adapter's intended `PASS`. Fixed in commit `b84134f360047de7a78adf18b36dd4e4dd472582`.
- 0008 had a semantic overreach: a generic role-reversal adapter was incorrectly promoted despite the canonical freeze blocker. Corrected to fail-closed in commit `8f2bfce2399cc28f80a2b94bc07cbe227042c92d` and its tests were corrected in `ed001560cc8b36e044351f63bf3302ad5a58c85f`.

## Existing historical evidence retained
- 0047 authoritative occurrence count = **25**; the `24` in `CLOSURE.md` is stale metadata.
- 0048 historical reconciliation = **186/186 exact** for `trin_ma10 > 1.20`.
- 0049 historical reconciliation = **122/122 exact** for `trin < 0.70`.
- 0051 remains a process/completeness gate and does not generate BUY/SELL direction.

## Verification boundary
This baseline uses current GitHub Runtime source, current routing, deterministic test inspection, direct local execution for the audited adapters, and the canonical frozen artifacts. It does **not** claim a GitHub Actions CI run because manual workflow dispatch is not available through the current connector.

2025 remains OOS and must not be used for tuning or selection.

## Immediate next work
Freeze the corrected **34/35 Murphy Runtime baseline**. Keep 0008 blocked until its approved decisive-break contract is source-locked. Then move to broader Decision Brain integration without reopening the 34 verified rule contracts.
