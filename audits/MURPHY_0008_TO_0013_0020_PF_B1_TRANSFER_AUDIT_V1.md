# Murphy PF-B1 Transfer Audit — 0008 → 0013-0020

Status: TRANSFER AUDIT / NOT PRODUCTION FROZEN
Date: 2026-08-16

## Objective
Determine whether the breakout architecture used/planned for Murphy 0008 can be reused for Murphy 0013-0020 without creating a duplicate breakout engine or silently transferring an unapproved threshold.

## Source findings
The 0008 handoff and PF-B1 Governance Proposal define PF-B1 as a shared Breakout Confirmation primitive intended for 0008/0009/0010 and additional breakout rules. The proposed interface consumes a canonical boundary, completed OHLC, an explicitly approved breakout policy, and availability metadata; it returns boundary_id, direction, raw break timestamp, decisive confirmation timestamp, availability timestamp, and status.

The source materials explicitly prohibit silently choosing 3%, 2-day, ATR, pips, arbitrary percentages, lookbacks, or tolerances. If no approved breakout policy exists, decisive-break confirmation must be NOT_EVALUABLE.

## Transfer decision
### Architecture: REUSE
The 0008 PF-B1 architecture is compatible as the shared primitive for 0013-0020. A new breakout engine must NOT be created.

### Policy: DO NOT AUTO-TRANSFER
The preserved PF-B1 proposal is PROPOSAL / NOT PRODUCTION FROZEN. The latest continuity record lists 0008 as PRODUCTION FROZEN but explicitly records a source-snapshot conflict and says no already-approved decisive-break contract was found. Therefore the 0008 status cannot, by itself, prove a transferable production policy.

### Interface: REUSE
0013-0020 can consume the same PF-B1 evidence shape: boundary, direction, raw break event, confirmation event, availability, and fail-closed status.

### Governance: REUSE
The following rules transfer unchanged:
- no-lookahead;
- availability timestamp gate;
- provenance requirement;
- NOT_EVALUABLE when required policy/evidence is missing;
- no 2025 tuning;
- no arbitrary thresholds.

## Rule compatibility
0013, 0014, 0015, 0016, 0017, 0018, 0019, and 0020 all specify breakout confirmation as part of complete rule evidence. Therefore the shared PF-B1 interface is applicable to all eight, but none should inherit an unapproved threshold merely because 0008 is later recorded as frozen.

## Result
ARCHITECTURE TRANSFER: PASS
INTERFACE TRANSFER: PASS
GOVERNANCE TRANSFER: PASS
PRODUCTION POLICY TRANSFER: BLOCKED pending explicit reconciliation/approval of the actual 0008 decisive-break policy.

## Required next step
Recover the exact operational artifact that produced the latest 0008 frozen status. If that artifact contains an explicitly approved breakout policy, perform a rule-by-rule compatibility audit for 0013-0020. If it does not, retain PF-B1 as fail-closed NOT_EVALUABLE and approve a shared policy separately.

2025 remains OOS and must not be used for policy selection or tuning.
