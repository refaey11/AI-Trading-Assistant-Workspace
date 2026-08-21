# AI Trading Assistant — Project State Reconstruction

**Recorded:** 2026-08-21
**Purpose:** Prevent repeated recovery/re-audit loops and preserve the verified project state reconstructed from the project conversation and prior project artifacts.

## 1. John Murphy — PARTIALLY CLOSED

- Total rules: **51**
- Officially closed/verified: **35**
- Remaining: **16**

The 16 remaining rules must remain open at their current governance state. Murphy is **not fully complete**.

## 2. Steve Nison — CLOSED

- Nison rules are **all completed/closed**.
- Role in the Decision Brain:
  - Confirmation
  - Contradiction
- Nison must **not generate LONG/SHORT direction by itself**.

## 3. Trading in the Zone — PROCESS / PSYCHOLOGY GATE

- PASS: evaluation may continue.
- FAIL: BLOCK / NO TRADE.
- Must not generate LONG, SHORT, or independent market direction.

## 4. Historical Memory / Similarity

The following are historical evidence only:

- Similarity Engine
- Historical Context Memory
- Historical Outcome Memory

They must not:

- become the sole decision maker;
- independently reverse/generate direction;
- override hard gates.

## 5. Multi-Timeframe Context — CONFIRMED

The confirmed six-timeframe context is:

- M5
- M15
- M30
- H1
- H4
- D1

Do not rebuild the timeframe layer from scratch merely because a later integration audit is running.

## 6. Data Governance — LOCKED

### 2016–2024

Used for:

- development;
- training/research where applicable;
- validation;
- integration testing.

### 2025

**LOCKED — FINAL OOS ONLY**

2025 must not be used for:

- training;
- tuning;
- iterative rule changes based on its results.

It is reserved for the final out-of-sample evaluation after the project integration is frozen.

## 7. Decision Brain — EXISTING / DO NOT REBUILD

Decision Brain recovery/architecture work has already been performed in prior project work. Do not restart a full Decision Brain recovery or rebuild the Decision Brain from scratch without first proving that recovery is genuinely required.

The current work must proceed through compatibility, integration, and runtime validation of the existing project components.

## 8. Current Integration / Validation Target

The project is at the Rule Adapter + integration validation stage.

The intended validation boundaries are:

1. **Murphy**
   - Accept only the 35 officially closed rules.
   - Normalize them into unified evidence.
   - Preserve Murphy as the primary technical context.

2. **Nison**
   - Operate as confirmation/contradiction only.
   - Must not independently generate direction.

3. **Trading in the Zone**
   - PASS allows evaluation to continue.
   - FAIL produces BLOCK / NO TRADE.
   - Must not generate direction.

4. **Historical Evidence**
   - Similarity / Historical Context / Historical Outcome remain evidence only.
   - Must not independently determine or reverse direction.

5. **Point-in-Time Market State (2016–2024)**
   - Market Structure
   - MTF Context
   - Volatility
   - Volume Availability
   - Current Price Action

Historical point-in-time state is sufficient for current validation. A live market feed is **not required** for this phase.

## 9. Integration Boundary Principle

Do not force market-state data into the Rule Adapter merely because a current_state field exists in a contract.

The working principle is:

Market Evidence
→ Knowledge Alignment / Integration Boundary
→ Existing Decision Brain

while preserving:

- Murphy → Primary Technical Context
- Nison → Confirmation / Contradiction
- Trading in the Zone → Process Gate
- Historical Memory → Evidence Only

Any code or contract change must be the smallest necessary change justified by a demonstrated compatibility gap.

## 10. Current Project State

| Component | Status |
|---|---|
| Murphy | 35 / 51 CLOSED; 16 REMAINING |
| Nison | ALL CLOSED |
| Trading in the Zone | Process Gate role fixed |
| Historical Memory | Evidence only |
| MTF 6 TF | CONFIRMED |
| Decision Brain | Existing; do not rebuild/recover from scratch |
| 2016–2024 | Current development/validation range |
| 2025 | LOCKED FINAL OOS |
| Current phase | Rule Adapter + Integration Validation |

## 11. Anti-Loop Rule — MANDATORY

Before declaring a gap, restarting a phase, repeating recovery, or rebuilding a component:

1. Check this state record.
2. Check existing GitHub artifacts/contracts.
3. Check relevant project archives/workspaces.
4. Determine whether the step was already completed, partially completed, or merely planned.
5. Do not restart completed work without explicit evidence.

## 12. Immediate Next Sequence

1. Validate existing Rule Adapter boundaries and precedence.
2. Validate integration of the five evidence boundaries above.
3. Make only the smallest necessary compatibility change if a real gap is proven.
4. Run end-to-end validation on 2016–2024.
5. Freeze the integrated version.
6. Use 2025 once as the final OOS evaluation.

**Status:** ACTIVE PROJECT STATE RECORD
**Supersedes:** ad-hoc conversational recollection when deciding whether to repeat completed work.
