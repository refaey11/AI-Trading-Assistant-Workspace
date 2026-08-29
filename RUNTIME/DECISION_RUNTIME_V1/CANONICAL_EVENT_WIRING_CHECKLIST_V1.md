# Canonical Event Wiring Checklist V1
Date: 2026-08-29

Purpose: prove wiring of existing producers without introducing strategy semantics or consuming CI credits.

## Required inputs
- [ ] One market snapshot with authoritative as_of.
- [ ] Market State + MTF output for the same as_of.
- [ ] Murphy evidence mapped by MURPHY_34_ROLE_MAP_V1.
- [ ] Nison confirmation/contradiction evidence for the same snapshot.
- [ ] Similarity/Outcome memory evidence using the existing shared builder and AS-OF guard.
- [ ] TIZ authoritative state when available; otherwise explicit NOT_EVALUABLE.
- [ ] Risk result from the existing risk boundary.

## Required invariants
- [ ] No module receives future data relative to event as_of.
- [ ] Missing evidence is explicit; no bullish/bearish default.
- [ ] Nison cannot originate direction.
- [ ] Memory cannot be sole decision maker.
- [ ] TIZ cannot originate direction and cannot be synthetically inferred.
- [ ] Risk remains a hard execution gate.
- [ ] 2025 is excluded from tuning.

## Required output
One canonical event containing all evidence groups, provenance, Brain decision, Risk result, and Trade Plan when approved.

## Gate 3C exit
PASS only when one pre-2025 event is assembled and consumed end-to-end by the existing runtime with all invariants satisfied. No CI/Workflow run is required for this wiring check.
