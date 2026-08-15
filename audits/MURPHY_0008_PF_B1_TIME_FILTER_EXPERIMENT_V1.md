# Murphy 0008 — PF-B1 TIME_FILTER Experiment V1

Date: 2026-08-15
Status: EXPERIMENT ONLY / NOT FROZEN / NOT USED FOR TUNING

## Objective
Test the proposed PF-B1 policy `two successive completed D1 closes below an available support level` on the existing 2016–2024 GBPUSD D1 project data, without using 2025.

## Existing project inputs
- `PIVOT_SEQUENCE_V2` D1 confirmed LOWs and availability timestamps.
- Existing D1 OHLC from the workspace DMI/ADX dataset (`GBPUSD_D1_DMI_ADX_2016_2024.csv`).
- Existing Rule 0008 mapping: `support level + break_structure_down`.

## Experimental state machine
1. Select the latest confirmed pivot-low support available before a bar and below the current close.
2. Keep that support level active while testing the downside break.
3. For the proposed TIME_FILTER, require two consecutive completed D1 closes below the same support level.
4. On the second close, emit a candidate decisive-break timestamp.
5. For descriptive role-reversal evidence only, inspect whether price later reaches the broken level and closes below it. This retest check is experimental and does NOT define the production 0008 contract.

## Results (2016–2024)
- Confirmed pivot-low candidates: 402.
- Candidate downside breaks with one completed D1 close below support: 164.
- Candidate downside breaks with two consecutive completed D1 closes below support: 109.
- Two-close filter therefore removes 55 of the 164 one-close candidates (~33.5%) and retains ~66.5% of the one-close candidates.

### Descriptive retest check (not a contract)
For the 109 two-close candidates:
- within 5 D1 bars: 78 touched the broken level; 53 had a high >= level and closed below it.
- within 10 D1 bars: 87 touched; 62 rejected below.
- within 20 D1 bars: 91 touched; 79 rejected below.
- within 40 D1 bars: 94 touched; 84 rejected below.
- within 60 D1 bars: 96 touched; 88 rejected below.

The 20-bar window is reported only as a diagnostic sensitivity view. It is NOT being proposed as the 0008 rule because no such window is source-locked or governance-approved.

## Interpretation
The proposed two-close D1 policy is operationally usable with the existing project primitives and materially reduces raw one-close downside-break candidates. It does not, by itself, prove that the policy is the correct Murphy 0008 production definition.

## Governance boundary
This experiment must NOT be used to select/tune the policy. No 2025 data was used. No price percentage, ATR, pip threshold, or hidden tolerance was introduced.

Production status remains `NOT_FROZEN` until PF-B1 policy approval, deterministic tests, availability/no-lookahead validation, provenance, and freeze review are completed.
