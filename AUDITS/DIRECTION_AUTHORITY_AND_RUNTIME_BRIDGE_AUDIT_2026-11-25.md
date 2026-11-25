# Direction Authority and Runtime Bridge Audit — 2026-11-25

## Scope
GitHub-only review on branch `fix/similarity-direction-isolation-2026-11-25`. No market-data payloads were opened. No 2025/2026 market data was accessed. No runtime source or frozen Decision Brain semantics were changed.

## Confirmed findings

### 1. Decision Brain direction is not currently Murphy-exclusive
File: `RECOVERED_SOURCES/DECISION_BRAIN_V1/decision_brain.py`

The recovered `assess(row, similarity=None)` creates directional evidence from:
- `mtf_trend_score` (MTF bullish/bearish evidence);
- `M5/M15/M30/H1/H4/D1_trend_regime` (Structure bullish/bearish evidence);
- volume-regime fields when `volume_available` is true (currently bullish or neutral evidence).

Similarity can also create directional evidence if a non-null object is passed, but the aligned caller and governed adapter reviewed on this branch pass `similarity=None`.

The evaluator later compares Brain bias with Murphy direction and rejects an opposing direction. This is a conflict check, not proof that the Brain's directional row fields were produced by Murphy.

**Disposition:** Murphy-only directional authority is NOT PROVEN. Do not authorize production direction from these fields until field-level lineage is demonstrated or an explicit architecture decision changes the boundary.

### 2. Runtime bridge authority checks are asymmetric
File: `RUNTIME/DECISION_RUNTIME_V1/full_brain_runtime_bridge_v1.py`

The bridge requires non-empty Murphy, Nison, and Risk evidence mappings, but checks `authoritative=True` only for Risk. It does not itself require Murphy authority/provenance or a Nison confirmation/authority state. The evaluator requires Murphy `status == PASS` and rejects an explicit Nison contradiction, but these checks do not establish source authority or require positive Nison confirmation.

**Disposition:** Bridge-level fail-closed behavior for Murphy and Nison is not established. Do not add guessed field names or semantics. First recover the authoritative evidence schemas and all direct callers.

### 3. Assembler/evaluator boundary
Files:
- `OOS_2025/full_decision_brain_assembler_v1.py`
- `evaluation/three_book_decision_evaluator_v1.py`
- `compatibility/decision_brain_v1_handoff_adapter.py`

The assembler passes the row into the governed adapter and separately passes Murphy/Nison evidence into the evaluator. The adapter calls the recovered Brain with `similarity=None`. The evaluator uses Brain bias as the final BUY/SELL direction after Murphy status and conflict checks, risk pass, and no Nison contradiction. Thus the present contract is still Brain-direction-led with a Murphy consistency check, not proven Murphy-direction-led.

### 4. Branch-aware caller/source enumeration limitation
GitHub code search returned no results for the targeted symbols (`mtf_trend_score`, `M5_trend_regime`, `M5_volume_regime`, `run_full_brain_cycle`, `full_brain_runtime_bridge_v1`). The connector's code search is documented as default-branch-only, so those empty results cannot be treated as proof of absence on this review branch. Several guessed test paths returned 404 and are not evidence that tests do not exist.

**Disposition:** Direct bridge callers and upstream field producers remain unenumerated. No exhaustive caller audit is claimed.

## Required next evidence
1. Obtain a branch-aware repository tree/source enumeration for this exact branch.
2. Trace each directional row field from its producer through adapters to `run_full_brain_cycle`.
3. Identify every direct caller of `run_full_brain_cycle` and the concrete Murphy/Nison evidence schema each supplies.
4. Decide explicitly whether (A) every directional MTF field is Murphy-derived with verifiable provenance, or (B) Murphy becomes the sole directional authority and Brain remains non-directional context/evidence. This is an architecture decision, not a silent code refactor.
5. Only after schema and callers are known, specify and test fail-closed bridge requirements for non-authoritative Murphy and absent/malformed Nison evidence.

## Guardrails preserved
- No edits to frozen recovered Decision Brain semantics.
- No changes to runtime bridge, assembler, evaluator, or production eligibility.
- No merges, no main-branch changes, no PR creation.
- No CI/workflow dispatch; no Dropbox or external project storage.
- 2025 OOS remains locked; no tuning/calibration or market-data access.
- No live trading or automatic orders enabled.

## Result
This is an evidence audit only. Direction authority remains unresolved; bridge authority hardening is blocked pending caller and schema recovery. Tests were not run.
