# Memory Integration Compatibility Audit — 2026-08-22

## Existing integration recovered
A prior Run 070 historical-evidence integration already exists in:
- `decision_brain/run_070/decision_brain_historical_evidence_integration.py`
- `decision_brain/run_070/DECISION_BRAIN_FULL_HISTORICAL_EVIDENCE_INTEGRATION_RUN_070.json`

The wrapper explicitly keeps Similarity as retrieval/evidence only, passes `similarity=None` into the legacy Decision Brain assessment, attaches historical evidence as metadata, and records governance checks. The existing Run 070 report states PASS for a smoke test using real project historical memory artifacts, with all retrieved candidates pre-2025 and no 2025 calibration leakage.

## Current verified memory boundaries
- Historical Context Memory: Runtime/CI Verified
- Historical Outcome Memory: Runtime/CI Verified
- Similarity Memory V2: Runtime/CI Verified
- 2025: locked OOS; not allowed for development retrieval/tuning/calibration

## Compatibility decision
Do not rebuild or replace the existing Run 070 integration. Add only the smallest contract-bound integration packaging boundary needed to:
1. accept the three verified evidence packages;
2. enforce that memory remains evidence only;
3. preserve provenance/source status;
4. reject 2025/future development evidence fail-closed;
5. expose no BUY/SELL/final trade decision from memory integration.

## Important existing gap
Run 070 was a historical integration smoke test using a synthetic Decision Brain input row. Its own report says promotion to end-to-end Decision Brain runtime still requires a real current Market Reader row plus official Murphy/Nison outputs.

## Separate policy gate
Outcome → Scenario Evidence classification remains a separate policy question. No BULL/BASE/BEAR numeric boundaries or calibration rules are to be invented in this integration layer.

## Next action
Implement and test the minimal Memory Evidence Package adapter, then run CircleCI regression before promoting it.
