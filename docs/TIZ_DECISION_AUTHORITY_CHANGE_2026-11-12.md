# TIZ Decision Authority Change — 2026-11-12

## Decision

The project owner has explicitly removed Trading in the Zone (TIZ) from the Decision Brain decision path because an authoritative, reliable TIZ runtime producer was not established.

Effective immediately, TIZ is optional metadata only.

## Prohibited effects

TIZ must not:
- generate, select, confirm, contradict, or override BUY/SELL direction;
- increase or decrease signal confidence, strength, or eligibility;
- block or allow a trade;
- alter risk acceptance, risk percentage, position size, stop loss, or take profit;
- make the runtime fail because TIZ evidence is missing, unavailable, failed, or not evaluable.

## Permitted use

Existing TIZ books, integrated knowledge, source files, evidence, and provenance are preserved. If a TIZ state is already available, it may be recorded as optional audit metadata. Missing evidence remains explicitly NOT_EVALUABLE metadata; it must not be replaced with a fabricated PASS.

TIZ metadata must remain outside all decision, execution-eligibility, and risk calculations.

## Decision authority

- Murphy: market context and structure.
- Nison: confirmation/contradiction only; never direction generation.
- Historical Similarity/Memory: evidence only; never sole decision maker or direction generator.
- Risk Engine: hard gate.
- TIZ: optional metadata only; no decision authority.

## Data governance

2025 remains locked out-of-sample. No tuning, calibration, threshold selection, optimization, or rule selection may use 2025. This decision changes no 2025 data and does not authorize any OOS retuning.

## Compatibility audit findings

The audit identified legacy TIZ influence in:
- the full Decision Brain assembler's explicit TIZ FAIL / NOT_EVALUABLE returns;
- the governance handoff's TIZ hard-block and review lists;
- the OOS execution adapter's TIZ READY/PASS/AVAILABLE requirement;
- the runtime bridge's production-mode TIZ-authority requirement;
- the legacy frozen execution bridge's process_state == READY requirement;
- the legacy single-event input contract's mandatory TIZ group;
- the legacy fail-closed and optional-evaluation helpers.

These paths are being changed to metadata-only behavior. Risk, Murphy/Nison evidence contracts, allowlists, temporal guards, and frozen execution-level formulas remain independently enforced.

## Verification required

The implementation is not declared complete until:
1. tests prove TIZ absent, NOT_EVALUABLE, FAIL, and arbitrary metadata states do not change decision or execution eligibility;
2. Risk failure still blocks;
3. Nison contradiction still follows its existing review/no-trade contract;
4. 2025 OOS integrity checks remain unchanged;
5. the complete project test suite passes locally and in CI.

No production-trading readiness or profitability claim is implied by this change.
