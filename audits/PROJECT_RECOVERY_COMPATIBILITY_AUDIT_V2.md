# AI Trading Assistant / Decision Brain — Project Recovery & Compatibility Audit V2

Date: 2026-08-12

## 1. Executive finding

**Project status: ALIVE / SUBSTANTIAL ASSETS INTACT / NOT PRODUCTION-COMPLETE.**

The project is not broken. The Workspace contains a large, coherent research/infrastructure base, including Market Intelligence, Pivot Sequence V2, Trendline Geometry V1, Volume Confirmation V2, Dynamic MTF, RSI Divergence, DMI/ADX, SAR, OBV, Open Interest, Historical Memory, Similarity Memory, Risk Engine research, Decision Engine research prototypes, and a Rule Adapter design/implementation.

The main failure was execution management: work was allowed to become too focused on individual Murphy rules, while the authoritative roadmap has a larger gate structure. This audit resets execution around the actual project gates without deleting or rebuilding existing components.

## 2. Authoritative project rules

- Workspace/File Library is Source of Truth.
- Existing components must not be rebuilt without compatibility audit.
- 2025 is OOS and must not be used for tuning, implementation selection, or forcing agreement.
- Murphy = Market Structure / Technical Context.
- Nison = Confirmation only.
- Trading in the Zone = Psychology / Process Gate and cannot generate direction.
- Similarity = historical memory/evidence only and never the sole decision maker.
- Risk = hard gate.
- Final Decision Brain is not yet verified complete.

## 3. What is actually present

### Knowledge / rule layer
- 102 total rules: 51 Murphy, 44 Nison, 7 Trading in the Zone.
- 23 currently marked ready for backtest.
- 79 incomplete / needing rule definition.
- 0 conflict-review queue in the project-state audit.

### Existing technical/evidence components
- Pivot Sequence V2
- Trendline Geometry V1
- Four-Week Lookback V1
- Volume Confirmation V2
- Dynamic MTF Binding V1
- RSI Divergence V1
- DMI/ADX V1
- Parabolic SAR V1
- OBV V1
- Open Interest V1 (availability-aligned for its stated scope)
- Market Breadth/TRIN remains blocked because the project lacks a valid breadth dataset.

### Existing research/integration components
- Market Reader / Market Intelligence
- Market State Reader
- Context-Aware Retrieval
- Scenario Engine
- Multi-Timeframe Reader
- Historical Context Memory
- Historical Outcome Memory
- Similarity Memory
- Risk Engine research
- Decision Engine / Decision Layer research prototypes
- n8n contracts
- Rule Adapter implementation + contract
- MT5 live execution OFF

## 4. What is verified vs what is not

### Murphy 0003–0004
- Correct joint peak + trough semantics are implemented in V2 with unit tests.
- Existing historical/provenance mismatch remains unresolved.
- Do not tune current code to old unreproducible counts.
- Not Production Frozen.

### Murphy 0006–0007
- Source material resolves the qualitative trendline concepts.
- Working mapping currently recorded as 0006 -> LOW/UP/BULLISH and 0007 -> HIGH/DOWN/BEARISH.
- Existing Trendline Geometry V1 must be reused.
- Operational evidence for third-touch/successful-reaction/no-break/availability is not yet proven by the authoritative project contract.
- Do not invent numeric tolerance.

### Murphy 0021–0023
- Existing evaluator, unit tests, and historical evaluation artifacts exist.
- Contract explicitly says no thresholds added, dynamic MTF, and 2025_used=false.
- Next intended action is integration into Rule Adapter / Decision Brain without changing source rules.

### Murphy 0027–0029
- 0028/0029 evaluator and tests exist.
- 0027 is intentionally blocked pending exact trend-vs-ranging regime operator.
- No invented ADX threshold or fixed timeframe.

## 5. Existing Decision Brain architecture status

The project already has a Rule Adapter contract and implementation.

Adapter purpose:
- Normalize existing book-rule outputs into Decision Brain evidence.
- Do not rewrite/copy the 102 rules.

Adapter output concept:
- module
- source_rule_id
- statement
- direction
- strength
- available
- gate
- conflict

Current precedence:
1. Process gate failure blocks execution.
2. Risk failure blocks execution.
3. Murphy invalidation blocks directional setup.
4. Nison can confirm or contradict, but cannot create direction alone.
5. Similarity can support/weaken, but cannot override hard gates.
6. Decision Brain synthesizes; adapter only normalizes.

**Important:** the adapter contract is `DESIGN_ONLY`; the final integrated Decision Brain is not verified complete.

## 6. Official roadmap gate that must control execution

The project freeze plan identifies:

**Next gate: Uniform Official Walk-Forward + Leakage Audit**

Then:

**After gate: Official Baseline Freeze → Decision Brain V1**

The official candidate is Similarity Engine V2 + 4H, but it remains candidate-only until the uniform walk-forward is completed.

Therefore the project must NOT treat the candidate or research Decision Engine as the final production brain.

## 7. Recovery decision

We will NOT:
- restart the project;
- rebuild existing engines;
- force all 102 rules to become evaluatable before moving forward;
- allow a single unresolved Murphy rule to block all work;
- freeze the Decision Brain before the official baseline gate;
- use 2025 for tuning.

We WILL:
1. Preserve current assets and provenance.
2. Use the official uniform walk-forward + leakage gate as the principal baseline gate.
3. Continue targeted rule-evaluator closure where it can be completed from authoritative sources and existing artifacts.
4. Maintain the Revisit Queue for unresolved rules/operators.
5. Integrate existing engines only after interface compatibility checks.
6. Build the final Decision Brain only from verified evidence contracts.
7. Run full-system validation after integration, with 2025 locked OOS.

## 8. Final execution map

### Gate A — Rule / Evidence readiness
- Verify the existing 102-rule registry and evaluator coverage.
- Close high-confidence evaluator gaps.
- Keep unresolved source/operator items in Revisit Queue.

### Gate B — Uniform Official Walk-Forward
- Fresh end-to-end run across EURUSD, GBPUSD, USDJPY, USDCAD, XAUUSD.
- Use the frozen project protocol.
- Leakage audit.
- No OOS tuning.

### Gate C — Official Baseline Freeze
- Freeze only after Gate B passes.

### Gate D — Decision Brain V1
Integrate existing:
- Murphy context
- MTF alignment
- Nison confirmation
- Similarity evidence
- Trading in the Zone process gate
- Risk hard gate
- Evidence/conflict resolution

### Gate E — Full-System validation
- Decision Brain end-to-end backtest.
- Leakage checks.
- Robustness/stress.
- Final locked OOS validation.

### Gate F — Deployment gates
- Freeze Decision/Risk/Execution contract.
- MT5 demo/paper.
- Monitoring.
- Live only after all prior gates pass.

## 9. Current bottlenecks ranked

1. **Uniform Official Walk-Forward + Leakage Audit** — highest project-level gate.
2. **Official baseline freeze** — blocked by #1.
3. **Final Decision Brain integration** — blocked by #2 per project freeze plan.
4. **Rule/evaluator gaps** — important, but should be handled in parallel and revisited systematically, not allowed to stall the whole project.
5. **0003–0004 provenance recovery** — separate unresolved provenance issue; do not alter current evaluator to force old results.
6. **0006–0007 operational evidence** — mapping working-resolved, evaluator closure pending upstream evidence.
7. **Nison and Trading in the Zone incomplete rules** — project state reports substantial incomplete coverage and must be addressed before claiming full rule coverage.

## 10. Recovery conclusion

The project does **not** need a restart. It needs disciplined execution against the real gates.

The next project-level action is to recover/verify the exact Uniform Official Walk-Forward execution inputs and leakage-audit procedure from the Workspace, then execute that gate. Rule-specific unresolved items remain tracked in the Revisit Queue and are revisited after the principal gate is cleared.

This audit supersedes conversational drift. It does not delete, replace, or rewrite existing project components.
