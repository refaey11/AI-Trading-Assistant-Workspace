# Master Testing Order Before Decision Brain Integration

**Date:** 2026-08-21
**Status:** ACTIVE PROJECT GOVERNANCE / OFFICIAL RESUME ORDER

## Core rule

Do NOT integrate all modules into the Decision Brain first.

Each major layer must be recovered/audited/tested independently, using its existing implementation where available, before progressive integration. The full Decision Brain end-to-end test happens only after the required individual layers have passed their relevant standalone gates.

## Required testing path

1. **Timeframe Layer**
   - Start at M5.
   - Supported project chain: M5 → M15 → M30 → H1 → H4 → D1.
   - Validate timeframe availability, alignment, boundaries, and no-future leakage.

2. **Market / Multi-Timeframe Reading**
   - Test the existing market evidence readers and cross-timeframe context independently.

3. **Murphy Knowledge Layer**
   - Use existing closed/runtime-ready work only.
   - Do not reopen already closed Murphy rules.

4. **Nison Knowledge / Confirmation Layer**
   - Test as confirmation/context only.
   - Do not reopen closed Nison work.

5. **Historical Evidence Layer**
   - Similarity Memory, Historical Context Memory, and Historical Outcome Memory.
   - Historical memory remains evidence, never the sole direction generator.

6. **Risk Layer**
   - Test independently as a hard gate/boundary.
   - Existing Knowledge Alignment → Risk validation is recorded as PASS 8/8, but any new integration must preserve the established boundary contract.

7. **Progressive Decision Brain Integration**
   - Integrate only the layers that have passed their required standalone/compatibility gates.
   - Reuse the recovered existing Decision Brain; do not rebuild it from scratch.

8. **Full End-to-End Decision Brain Test**
   - Run only after the preceding required layers and integration boundaries are validated.

9. **Final 2025 OOS Evaluation**
   - 2025 is final out-of-sample evaluation only.
   - Never use 2025 for tuning, calibration, threshold selection, or iterative fitting.

## Current governance exclusions

- Trading in the Zone is PARKED / DEFERRED for the current path.
- Do not restart closed Murphy or Nison work.
- Do not perform broad schema hunting unless a concrete runtime/contract gate identifies a specific missing dependency.
- Do not jump directly from an unresolved historical calibration gap into full Decision Brain integration.

## Resume discipline

This document is the master checkpoint for testing order. Future work must first identify the earliest unverified gate in this order, verify only that gate, record the result, then continue forward. Do not repeatedly restart completed audits or jump ahead to the final Decision Brain test.

## Data discipline

Development, historical QA, and calibration use the approved 2016–2024 development window. Preserve AS-OF/no-lookahead controls and availability rules. Keep 2025 untouched until final OOS evaluation.
