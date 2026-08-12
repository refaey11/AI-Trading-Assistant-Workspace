# AI Trading Assistant — Decision Brain
## Current Project Status — 2026-08-12

### Purpose
This file records the latest verified stopping point so future work resumes from the exact current state instead of rebuilding or guessing.

### Source-of-truth policy
- Workspace / File Library artifacts are the project source of truth.
- GitHub is the development/provenance mirror and must not silently replace Workspace truth.
- Existing components must be audited and integrated, not rebuilt.
- Compatibility audit is required before any new integration.
- 2025 = OOS and must never be used for tuning, threshold selection, or implementation selection.

### Architecture status
- John Murphy technical context / market structure: integrated work exists.
- Steve Nison: integrated confirmation knowledge exists.
- Trading in the Zone: psychology/process gate; it cannot generate market direction.
- Similarity / Historical Memory: historical evidence only; it cannot be the sole decision maker.
- Decision Brain: combines current market evidence, book knowledge, historical memory, and risk.
- Existing Trendline Geometry V1 is an upstream primitive and must not be rebuilt.
- Existing Pivot Sequence V2 is also upstream infrastructure and must be reused.

### Murphy 0006–0007 source status
The source semantics were recovered from the uploaded full Chapter 4 of John Murphy and reviewed against the project artifacts.

MURPHY_0006:
- reaction lows / LOW family
- uptrend / UP geometry
- two points establish the tentative line
- third test/touch is the confirming test when successful
- successful test includes reaction/rebound away from the line
- the line must hold without a meaningful break
- expected direction: BULLISH

MURPHY_0007:
- reaction highs / HIGH family
- downtrend / DOWN geometry
- two points establish the tentative line
- third test/touch is the confirming test when successful
- successful test includes reaction/rebound away from the line
- the line must hold without a meaningful break
- expected direction: BEARISH

The chapter also distinguishes meaningful trendline breaks from mere intraday penetration and discusses price/time filters as general breakout filters. Those examples are NOT automatically assigned as numeric thresholds to 0006/0007.

### Work completed today
1. Reviewed the existing Murphy 0006–0007 project state and identified the source-contract gap.
2. Reviewed the full uploaded Murphy Chapter 4 and corrected the earlier conclusion that the source had no no-break semantics.
3. Confirmed the source-defined third-test / reaction / hold semantics for 0006–0007.
4. Confirmed that existing Trendline Geometry V1 and Pivot Sequence V2 must be reused rather than rebuilt.
5. Audited GitHub and the full-project artifacts for an existing approved operational break contract. No explicit 0006/0007 binding was proven.
6. Determined that a separate Murphy Confirmation Layer is appropriate if no existing component can provide the required evidence.
7. Created `audits/MURPHY_0006_0007_BOOK_OPERATOR_CLARIFICATION_V2.md` documenting the corrected source interpretation.
8. Created `audits/MURPHY_0006_0007_CONFIRMATION_LAYER_CONTRACT_V1.md` defining the proposed derived evidence layer without inventing thresholds.
9. Confirmed `HISTORICAL_MEMORY_V1.zip` exists as a GitHub release asset and must be treated as Historical Evidence infrastructure, not as a rule generator.

### Confirmation Layer contract status
The proposed layer sits ABOVE existing Geometry and does not modify it.

Inputs:
- line_id
- LOW/HIGH family
- UP/DOWN direction
- anchor 1 and anchor 2 timestamps/prices
- line availability timestamp
- completed-bar data after availability
- approved project break semantics if an existing contract is found

Outputs:
- third_touch_timestamp
- third_touch_price
- third_touch_detected
- reaction_detected
- no_break_valid
- confirmation_timestamp
- confirmation_available_timestamp
- rule_id
- PASS / FAIL / NOT_EVALUABLE

Hard constraints:
- no invented ATR threshold
- no invented percentage touch tolerance
- no invented lookback
- no invented execution timeframe
- no automatic assignment of Murphy's general 3%/2-day examples to 0006/0007
- no lookahead
- no tuning with 2025

### Historical Memory status
`HISTORICAL_MEMORY_V1.zip` is present in the GitHub `workspace-v1` release. SHA-256:
`f11d6930583adb2d7b4a1b7c0c2796e01943f305cce36cbc3accd93df5356d30`

The ZIP binary itself has NOT been treated as inspected merely from release metadata. The next audit must inspect its accessible contracts/artifacts and determine whether it provides useful historical evidence/lineage for the Murphy Confirmation Layer.

### Current blocking item
The project is NOT production-frozen.

The exact remaining work is:
1. Compatibility audit of the new Murphy Confirmation Layer against Workspace + Full Project + GitHub + Historical Memory.
2. Verify whether an existing approved break/no-break contract can be reused.
3. If no such contract exists, operationalize only the source-backed third-touch/reaction semantics without inventing unsupported numeric thresholds.
4. Implement the smallest derived evidence layer required.
5. Unit tests / deterministic edge cases.
6. Historical QA on 2016–2024.
7. Freeze only after all gates pass.

### What is already CLOSED
- Source recovery for the qualitative Murphy 0006/0007 semantics: CLOSED.
- Direction mapping at the semantic level: CLOSED (0006 bullish/uptrend; 0007 bearish/downtrend), subject to final project record verification.
- Decision to preserve existing Geometry V1/Pivot V2: CLOSED.
- Decision that Historical Memory is evidence-only: CLOSED.

### What is NOT CLOSED
- Exact project-approved operational touch/reaction detector.
- Exact project-approved no-break operator binding.
- Evaluator implementation.
- Unit tests.
- Historical QA.
- Production Freeze.

### Exact stopping point
STOP immediately before the final compatibility audit of the new Murphy Confirmation Layer against the existing project components, especially Historical Memory and any existing break/no-break evaluator/contract.

### Resume rule
When resuming, do NOT re-open the source question from scratch. Start with the Confirmation Layer contract and perform the compatibility audit across Workspace, Full Project, GitHub, and Historical Memory. Preserve all existing components and contracts. 2025 remains OOS.
