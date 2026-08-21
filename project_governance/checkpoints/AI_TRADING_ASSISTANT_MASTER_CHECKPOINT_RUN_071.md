# AI Trading Assistant — Master Project Map & Checkpoint

**Checkpoint:** RUN_071
**Created:** 20260821T011743Z
**Purpose:** Official project order, current status, remaining work, and mandatory backup protocol.

## Non-negotiable governance
- Murphy = technical context and market structure.
- Nison = confirmation / contradiction evidence.
- Trading in the Zone = psychology/process gate only; it cannot generate market direction.
- Similarity = historical evidence only; never the sole decision maker.
- 2025 = OOS and must never be used for tuning/calibration.
- Do not rebuild existing project knowledge from scratch; audit and integrate existing artifacts first.
- Before each new integration, perform a compatibility audit.

## Final architecture
Market Data
→ Market Reader
→ Market State / Market Structure
→ Dynamic MTF / Time Context
→ Current Market Evidence

Technical / knowledge evidence:
- Murphy
- Nison
- Trading in the Zone process gate

Historical evidence:
- Similarity Engine
- Historical Context Memory
- Historical Outcome Memory

Then:
→ Rule / Evidence Normalization
→ Knowledge Alignment
→ Evidence Agreement
→ Contradiction Gate
→ Decision Brain
→ Candidate: LONG / SHORT / NO TRADE
→ Risk Engine
→ Position Sizing
→ Execution Contract
→ Backtest / Robustness
→ 2025 OOS
→ Freeze Decision + Risk + Execution contracts
→ MT5 Demo
→ Monitoring
→ Real trading only after all gates pass

## Completed / integrated
### Historical evidence layer
- Similarity evidence contract governed as evidence-only.
- Historical Context Memory integrated.
- Historical Outcome Memory integrated.
- AS-OF and future-leakage guards applied.
- 2025 OOS lock preserved.
- Decision Brain historical evidence integration smoke test: RUN_070 PASS.
- Legacy decision_brain.py was not overwritten.
- Similarity did not provide predicted_return, direction, BUY/SELL, entry, SL/TP, or final decision.

## Current next phase
1. Compatibility audit of the existing Market Pipeline:
   - Market Reader
   - Market State Reader
   - Market Scenario Engine
   - Multi-Timeframe Reader
   - Dynamic MTF / Time Context
2. Integrate official current-market outputs with the Decision Brain evidence layer.
3. Integrate Murphy + Nison + Trading in the Zone.
4. Build/verify Knowledge Alignment.
5. Build/verify Evidence Agreement + Contradiction Gate.
6. Run end-to-end Decision Brain integration.
7. Integrate Risk Engine + Position Sizing.
8. Official Backtest / Robustness.
9. 2025 OOS.
10. Freeze contracts, then MT5 Demo and monitoring.

## Mandatory backup protocol from now on
After every completed project part/module:
1. Create a checkpoint summary.
2. Create/update a backup manifest with completed artifacts and status.
3. Save the checkpoint to GitHub.
4. Save the checkpoint to Dropbox.
5. Create a downloadable local ZIP backup when the completed artifacts are available in the runtime.
6. Only then move to the next part.

This checkpoint is the current master execution order and must be updated rather than replaced by an invented architecture.
