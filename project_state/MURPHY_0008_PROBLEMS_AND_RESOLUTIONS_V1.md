# Murphy 0008 — Problems Encountered and Resolutions V1

Date: 2026-08-15
Status: Historical project record

## 1. Support identity was not frozen
Problem: 0008 required a Support boundary, but no production contract established which existing support representation to use. Clustering/tolerance was not authorized.
Resolution: use one confirmed LOW pivot from canonical PIVOT_SEQUENCE_V2 as the singleton Support boundary for 0008. Do not merge nearby pivots. Freeze limited to 0008.

## 2. "Decisive/significant break" was not deterministic
Problem: Murphy's semantic wording did not by itself specify an executable numeric predicate. The project forbids silently inventing 1%, 3%, ATR, pips, arbitrary tolerance, or historical-performance thresholds.
Resolution: freeze the 0008 operational policy as two successive completed D1 closes strictly beyond Support: first close = candidate; immediately following close = decisive confirmation.

## 3. Risk of building a duplicate breakout engine
Problem: a new breakout engine could duplicate existing project logic and violate compatibility architecture.
Resolution: keep 0008 as an evidence evaluator/adapter around the existing project primitives and frozen contracts; no second breakout engine.

## 4. Early replay produced an incorrect 324 confirmations
Problem: the first replay allowed any later pair of consecutive closes below Support, rather than requiring the immediately following completed D1 close to confirm the first candidate.
Resolution: rewrite the executable operator to enforce immediate-next-bar confirmation. Recomputed result: 242 confirmations. The 324 result is explicitly superseded.

## 5. Authoritative data lineage ambiguity
Problem: the reconstructed workspace did not contain a standalone raw `D1/GBPUSD_D1_STRUCTURE.csv` at the expected path.
Resolution: use the lineage-validated D1 path present in the workspace and preserve the limitation explicitly. The project evidence records reconciliation of the reconstructed D1 path against `d1_ref.csv` across 2,544 common 2016–2024 dates.

## 6. Retest could accidentally introduce lookahead
Problem: searching for retest on or before the confirmation bar would leak future information into the event.
Resolution: retest observation starts strictly after the confirmation close. No future pivot may redefine the historical Support boundary.

## 7. Edge cases were at risk of being treated as failures
Problem: some confirmed breaks have no later retest before the dataset ends, and some retests have no later close-below-support evidence.
Resolution: preserve them as valid evidence outcomes, not evaluator failures: 9 confirmed events had no later range intersection; 13 had a later intersection but no later intersecting close below Support.

## 8. 2025 contamination risk
Problem: using 2025 for rule selection or tuning would violate the project OOS policy.
Resolution: 2025 excluded from policy selection, tuning, replay, and confirmation counts. Recorded contamination count: 0.

## 9. Confusing evidence frequency with trading performance
Problem: high retest/role-reversal percentages could be misread as win rate or profitability.
Resolution: explicitly classify 233/242 retests and 229/242 role-reversal events as evidence-frequency diagnostics only, not profitability metrics.

## 10. Production-freeze governance gap
Problem: technical QA passing did not itself authorize production promotion.
Resolution: create a final freeze manifest, submit PR #10 for governance review, then merge PR #10 into main after the repository reported the PR mergeable. Merge commit: `515aac5785ed36529763cbf1b4e0f8324b2aeee3`.

## Final lesson
Do not restart or retune 0008. The frozen production contract is the current source of truth. Any future modification requires a new version, compatibility audit, fresh 2016–2024 validation, provenance preservation, and an explicit freeze decision. 2025 remains OOS.
