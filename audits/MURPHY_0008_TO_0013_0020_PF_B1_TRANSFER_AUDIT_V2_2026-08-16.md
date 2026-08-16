# Murphy 0008 → 0013–0020 PF-B1 Transfer Audit V2

Date: 2026-08-16
Status: TRANSFER AUDIT / NOT A PRODUCTION FREEZE

## 1. New authoritative finding
Git history contains a later authoritative production-freeze reconciliation for Murphy 0008:
- `515aac5785ed36529763cbf1b4e0f8324b2aeee3` — merge/freeze Murphy 0008 validated path.
- `cf964403c1a944fefdb0e4596e160effb982dc12` — later reconciliation explicitly records the final production-frozen state.

Therefore the earlier 0008 audit documents that still say “NOT PRODUCTION FROZEN” are historical/source-era records and must not be treated as the latest state.

## 2. What is actually frozen for 0008
The final validated path froze the following operationalization:

PF-H1:
- singleton confirmed LOW pivot from canonical PIVOT_SEQUENCE_V2;
- pivot price is the Support boundary;
- no clustering/tolerance;
- support availability must precede the break observation.

PF-B1:
- TIME_FILTER;
- two successive completed D1 closes beyond the Support boundary in the break direction;
- first close = candidate break;
- second successive close = decisive confirmation;
- confirmation becomes available at completion/close of the second D1 bar;
- later retest evidence begins strictly after confirmation.

The project explicitly preserves the distinction that this is an operationalization and not a claim that Murphy literally writes “0008 = two days.”

## 3. What can be reused by 0013–0020

### Reuse as shared architecture: YES
Reuse the 0008 PF-B1 design as the shared breakout interface:
- boundary identity;
- direction;
- raw/candidate break timestamp;
- confirmation timestamp;
- availability timestamp;
- explicit status;
- fail-closed `NOT_EVALUABLE` when required evidence is unavailable;
- no-lookahead chronology;
- no duplicate breakout engine per rule.

### Reuse the exact 0008 policy unchanged: NO, not automatically
The 0008 policy is frozen in a specific context: GBPUSD D1 Support → downside break → role reversal. 0013–0020 are different pattern rules with their own boundaries and source semantics. The frozen 0008 policy is therefore evidence of an approved operationalization pattern, not automatic authorization to bind every later rule to the same policy.

## 4. Transfer candidate for 0013–0020
The strongest reusable candidate is:

`TIME_FILTER = two successive completed closes beyond the pattern boundary in the breakout direction.`

This should be treated as a **shared PF-B1 operationalization candidate**, not yet as a blanket production rule for all eight patterns.

For a pattern with an upper boundary:
- upside breakout candidate = completed close above the same boundary;
- next completed close also above = candidate decisive confirmation.

For a pattern with a lower boundary:
- downside breakout candidate = completed close below the same boundary;
- next completed close also below = candidate decisive confirmation.

Confirmation availability is the close of the second completed bar. No future bars may be used earlier.

## 5. Pattern-specific compatibility gate
Before binding the two-close operator to a rule, the rule must have:
1. a canonical boundary identity;
2. a defined breakout direction;
3. a defined evaluation timeframe;
4. evidence that a completed close outside that boundary is the intended breakout event for that rule;
5. no conflicting source-specific confirmation contract.

If any prerequisite is missing or ambiguous, PF-B1 returns `NOT_EVALUABLE` for that rule rather than inventing a policy.

## 6. 0013–0020 preliminary compatibility

| Rule | Boundary | Direction(s) | Two-close transfer candidate | Current decision |
|---|---|---|---|---|
| 0013 Symmetrical Triangle | G1 upper/lower | UP or DOWN | Potentially compatible | Requires pattern contract approval |
| 0014 Ascending Triangle | upper horizontal + rising lower | UP | Potentially compatible | Requires pattern contract approval |
| 0015 Descending Triangle | falling upper + lower horizontal | DOWN | Potentially compatible | Requires pattern contract approval |
| 0016 Flag | channel boundaries | UP or DOWN | Potentially compatible | F1 + pattern breakout semantics required |
| 0017 Pennant | converging boundaries | UP or DOWN | Potentially compatible | F1 + pattern breakout semantics required |
| 0018 Falling Wedge | G1 upper/lower | UP | Potentially compatible | Requires pattern contract approval |
| 0019 Rising Wedge | G1 upper/lower | DOWN | Potentially compatible | Requires pattern contract approval |
| 0020 Rectangle | horizontal upper/lower | UP or DOWN | Potentially compatible | H1/G1 + pattern breakout semantics required |

“Potentially compatible” is deliberate: this table does not silently freeze the 0008 policy for the later rules.

## 7. What we do NOT transfer
- 0008 Support identity as a universal Support/Resistance rule.
- 0008 D1 timeframe as a universal timeframe.
- 0008 downside-only direction.
- 0008 role-reversal/retest semantics as a prerequisite for pattern breakout rules.
- Any 0008 historical counts as a tuning target.
- Any 2025 data.

## 8. Decision

**REUSE THE 0008 PF-B1 ARCHITECTURE.**

**REUSE THE TWO-CLOSE OPERATIONALIZATION AS A CANDIDATE SHARED POLICY, SUBJECT TO EXPLICIT 0013–0020 COMPATIBILITY APPROVAL.**

Do not create another breakout engine.
Do not copy 0008's Support/reversal semantics into the pattern rules.
Do not tune the two-close condition using 2016–2024 outcomes.
Do not use 2025.

## 9. Next gate
Create a single shared `PF-B1 0013–0020 compatibility contract` that binds the two-close operator only where each pattern's canonical boundary/direction/timeframe semantics support it. Then run deterministic tests and actual no-lookahead QA for all eight rules.
