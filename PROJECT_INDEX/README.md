# AI Trading Assistant — Project Navigation Index

Date: 2026-08-13

This directory is a non-destructive navigation/governance layer. It does not replace Source-of-Truth artifacts.

## Source hierarchy
1. Workspace / File Library = Source of Truth.
2. GitHub = development/provenance mirror.
3. Existing components are reused after compatibility audit; do not rebuild them.

## Global controls
- 2025 is OOS: never use it for tuning, threshold selection, implementation selection, fitting, or historical matching.
- Feature availability != rule evaluability.
- Never invent thresholds, operators, fixed timeframes, proxies, or lookbacks.
- Similarity / Historical Memory = evidence only; not semantic authority or a standalone decision maker.
- Murphy = technical context/market structure.
- Nison = confirmation only.
- Trading in the Zone = psychology/process gate only; cannot generate direction.
- Decision Brain already exists; inspect and integrate rather than rebuild.

## Murphy 51 navigation
See `MURPHY_51_MASTER_AUDIT.csv` for the rule-by-rule problem map.

Current high-level state:
- 0003–0004: NOT FROZEN; provenance reconciliation unresolved.
- 0006–0007: QA PASS / FREEZE CANDIDATE; active work is in another chat and must not be touched here.
- 0021–0023: QA PASS / FREEZE CANDIDATE; not Production Frozen.
- 0025–0026: Source/Feature Compatible; validation pending.
- 0028–0029: QA PASS / FREEZE CANDIDATE; not Production Frozen.

## Project pipeline
SOURCE → RULE REGISTRY → COMPATIBILITY → FEATURE/EVIDENCE → OPERATOR → EVALUATOR → TESTS → HISTORICAL QA (2016–2024) → OOS/LEAKAGE → FREEZE → Decision Brain integration → baseline/robustness → paper/demo → live.

## Protected areas
See `DO_NOT_TOUCH.md` before changing any existing component, evaluator, historical artifact, or freeze state.
