# MURPHY 0030–0032 — FREEZE BACKUP V1
Date: 2026-08-17
Status: PRODUCTION FROZEN

## Scope
Backup for MURPHY_0030, MURPHY_0031, and MURPHY_0032. The 12 previously frozen Murphy rules were not touched.

## Rule 0030 — P&F bullish support
### Problem
The rule was initially recorded without a deterministic executable P&F implementation/source-to-rule contract. The registry also needed exact Chapter 11 source mapping.
### Solution
Reuse the shared source-bounded 3-box P&F core. Map 0030 to Murphy Chapter 11 / Point & Figure. Construct X/O columns from completed D1 High/Low data using the directional priority rule. Produce the 45-degree bullish support reference from the base of the lowest O column. Keep 0030 structural/context-only; it does not invent an autonomous entry trigger.
### Evidence
The shared core and rule contract were implemented and deterministic tests passed. Historical calibration-only fold construction and prefix replay passed for 2019–2024.

## Rule 0031 — P&F long stop reference
### Problem
Murphy gives the structural placement relation but does not supply a numeric pip/ATR/percentage execution offset. A direct implementation could accidentally invent an offset.
### Solution
Reuse the same shared P&F core and expose only the source-supported reference: long stop relation = BELOW_PREVIOUS_O_COLUMN. Do not manufacture an offset.
### Evidence
Deterministic construction/replay passed under the same shared engine and calibration-only fold protocol.

## Rule 0032 — P&F short stop reference
### Problem
Same boundary in the bearish direction: Murphy specifies the structural relation but does not supply a numeric execution offset.
### Solution
Reuse the shared P&F core and expose only: short stop relation = ABOVE_PREVIOUS_X_COLUMN. No invented pip/ATR/percentage offset.
### Evidence
Deterministic construction/replay passed under the same shared engine and calibration-only fold protocol.

## Shared technical problems and solutions
### 1. Missing implementation entrypoint
Problem: 0030–0032 had a compatibility/entrypoint gap.
Solution: add the compatibility entrypoint and integrate the existing P&F core; no rebuild of the core.

### 2. High/Low ordering ambiguity
Problem: D1 OHLC does not reveal the intrabar order of High and Low.
Solution: use the source-bounded directional policy: in X, test High continuation first and only then Low for reversal; in O, test Low continuation first and only then High for reversal. No invented intrabar chronology.

### 3. No-lookahead / historical availability
Problem: later bars must not alter an earlier emitted P&F state.
Solution: deterministic prefix snapshots and replay checks. Prefix/no-lookahead passed for all executed folds.

### 4. Box-size policy
Problem: Murphy does not provide one universal GBPUSD numeric production box size, and the audited Tower formula is incomplete.
Solution: explicitly label the scaling as PROJECT_OPERATIONALIZATION rather than Murphy/Tower truth. Use the approved deterministic trailing-three-calendar-year sample standard deviation of daily log returns for calibration-only fold construction; freeze the resulting value per fold before OOS. Never select it by profitability and never use 2025 for tuning/selection.

### 5. Bootstrap policy
Problem: Murphy describes the construction after a column exists; initial chart seeding is an operational implementation boundary.
Solution: isolate bootstrap as a project-defined deterministic parameter and keep it separate from the source semantics. Do not claim the bootstrap is verbatim Murphy.

### 6. Avoiding false trading signals
Problem: 0030 could be incorrectly turned into an autonomous BUY/SELL trigger; 0031/0032 could be given invented stop offsets.
Solution: preserve each semantic contract: 0030 = structural bullish support evidence; 0031 = below previous O-column reference; 0032 = above previous X-column reference.

## QA evidence
- Existing local deterministic suite: 7/7 PASS.
- Canonical D1 dataset: 2,544 rows, 2016-01-03 through 2024-12-31.
- Calibration-only fold construction: 2019–2024.
- Deterministic construction: PASS for all six folds.
- Prefix replay/no-lookahead: PASS for all six folds.
- 2025: excluded from tuning, selection, calibration, and optimization.

## Governance boundary
The box scaling and bootstrap are explicitly project operationalization, not claims about an undocumented universal Murphy/Tower GBPUSD value. No profitability-based parameter selection was used.

## Frozen outputs
0030: PNF_BULLISH_SUPPORT_REFERENCE
0031: BELOW_PREVIOUS_O_COLUMN
0032: ABOVE_PREVIOUS_X_COLUMN

No autonomous BUY/SELL trigger and no invented stop offset are part of these frozen rules.

## Do-not-repeat list
- Do not reopen these rules for routine cleanup.
- Do not search again for a universal Murphy GBPUSD box number unless new authoritative evidence appears.
- Do not tune box size on 2025 or on profitability.
- Do not add ATR/pip offsets to 0031/0032.
- Do not turn 0030 into an entry signal.
- Do not rebuild the shared P&F core.
