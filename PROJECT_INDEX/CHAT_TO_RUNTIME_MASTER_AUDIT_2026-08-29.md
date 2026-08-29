# AI Trading Assistant — Chat-to-Runtime Master Audit
Date: 2026-08-29

## 1. Project objective
Build one unified AI Trading Assistant / Decision Brain that reads the market, combines governed evidence, produces BUY/SELL/NO_TRADE with traceable reasons, applies Risk, creates a Trade Plan, and eventually connects to MT5/n8n.

## 2. Non-negotiable architecture
- Reuse existing modules; do not rebuild them.
- Murphy = primary technical/directional context under the governed rule boundary.
- Nison = confirmation/contradiction only; cannot originate direction.
- Similarity / Historical Memory = evidence only; cannot decide alone.
- TIZ = process/psychology only; cannot generate direction. If unavailable, record NOT_EVALUABLE/UNVERIFIED rather than invent state.
- Risk = hard execution gate.
- Point-in-time evidence is mandatory; no future evidence.
- 2025 = OOS only; never use it for tuning, calibration, threshold selection, implementation selection, or fitting.

## 3. Work completed before the current runtime effort
### Knowledge / source normalization
- Master Knowledge Base V1 reorganized the project into source-aware folders.
- 1179 source files copied into the master structure; Murphy 138 files, Nison 996 files, TIZ 44 files, shared 1, unattributed 1.
- 102 candidate rules were indexed.
- The old Three-Book Integration package explicitly connected the roles conceptually, but its own README recorded that this was architecture integration, not performance validation. It listed 44 Nison rules, 7 TIZ process items, and the remaining rules as not yet attributed in that package.

### Trading Rules V2
- 102 unique candidate rules.
- 23 marked ready for backtest; 79 incomplete / needing explicit definition.
- No profitability claim was made.
- Recognition-only rules can remain building blocks of composite setups.

### Market / MTF / Memory layers
- Market State Reader is descriptive and not a strategy.
- Early MTF Reader is H4/H1 research-only; it does not generate a trade decision and explicitly says M15 must not be fabricated from H1.
- Historical Context Memory and Historical Outcome Memory exist as evidence layers, not strategies.
- Similarity V2 is historical context retrieval and not a strategy.
- Context-Aware Retrieval is interpretation / knowledge retrieval, not a trade signal.
- Early Nison context/candle engines are operational prototypes and were explicitly not claimed to reproduce verbatim book thresholds.

### True Backtest / early strategy evidence
- TRUE_BACKTEST_V2 completed an earlier memory/strategy-style backtest, with positive aggregate expectancy in some configurations, but these results are not the final integrated Decision Brain result.
- The final project rule remains: no profitability claim until the governed unified path is tested with leakage/provenance controls.

## 4. Murphy work supplied and recovered
The current user-supplied Murphy archive `قواعد مورفي  2(6).zip` was inspected recursively, including nested ZIPs.

It contains rule-specific evidence, QA, freeze, provenance, and replay artifacts covering multiple Murphy groups including:
- 0003/0004
- 0006/0007
- 0021/0023
- 0028/0029
- 0030/0032
- 0033
- 0034–0045
- 0047–0049
- 0050/0051
- additional continuity/recovery artifacts

Important source-status examples:
- Murphy 0028 evidence manifest: 5,819 rows; historical QA PASS; availability/leakage PASS; 2025 rows excluded.
- Murphy 0034–0045 local production freeze record: 12 rules represented; frozen as rule contract/evidence freeze, not profitability claim.
- Murphy 0047–0049 has closed-final replay and canonical breadth artifacts.
- Murphy 0050/0051 has final process-gate closure artifacts.

The archive is a source/evidence pack, not itself proof that the full 34-rule Decision Brain fan-in is already wired to the live runtime.

## 5. Official governed rule boundary
The frozen Decision Brain allowlist currently defines exactly:
- 34 Murphy runtime-verified rules
- 44 Nison runtime-verified rules
- total governed rule count = 78
- Murphy 0008 is explicitly blocked / NOT_EVALUABLE

Therefore the project must not be described as 79 governed runtime rules.

## 6. Integration work already completed in GitHub history
The existing project history contains:
- Full Decision Brain orchestration path.
- Historical event producer.
- OOS assembler.
- Point-in-time evidence architecture / adapters.
- Execution adapter.
- A decision-boundary correction requiring full 34 Murphy + 44 Nison evidence to be consumed when governed full envelopes are present.

Important PR history:
- PR #55 merged the rebased Full Decision Brain OOS assembler onto main.
- PR #56 merged the rebased historical event producer.
- PR #57 merged a governed 78-rule final OOS path recovery.
- PR #60 remains open and is the focused decision-boundary fix for full 34 Murphy + 44 Nison fan-in.
- PR #64 is an open TIZ audit-only compatibility fix.
- PR #62 is a WIP dynamic MTF runtime resolver; do not treat it as the production decision brain.

## 7. Gate 1 and Gate 2 status — important interpretation
Gate 1 is a PASS for canonical assembly of the supplied 2016 GBPUSD artifacts:
- 401 events
- 120 executable
- 56 candidate
- 225 no-trade
- same-timestamp evidence
- Nison/TIZ/historical memory not given directional authority
- no 2025 tuning

Gate 2 is a PASS for deterministic replay of the same integrated artifact path:
- 120 executable events
- 56.67% win rate
- PF 1.455
- expectancy +0.173R
- total +20.74R
- max DD -11.93R
- 120/120 matched outcomes
- chronological and no-new-lookahead claims in the artifact

These two gates prove an integrated historical artifact/runtime path, but they do NOT by themselves certify the recovered production Decision Brain's full 34+44 evidence consumption.

## 8. Current Decision Runtime work
Branch: `build/decision-runtime-v1`

Existing runtime intent:
Market Snapshot -> Existing Evidence Adapters -> Decision Brain -> Three-Book Gate -> Execution Plan.

The runtime is orchestration only; it does not invent book-rule semantics.

Created/recorded in this continuation:
- `RUNTIME/DECISION_RUNTIME_V1/single_event_gate.py`
- `RUNTIME/DECISION_RUNTIME_V1/historical_context_memory_pit_adapter_v1.py`
- `RUNTIME/DECISION_RUNTIME_V1/MURPHY_SOURCE_AUDIT_2026-08-29.md`
- `RUNTIME/DECISION_RUNTIME_V1/MURPHY_SOURCE_BINDING_PLAN_V1.md`
- `PROJECT_INDEX/CHAT_TO_RUNTIME_MASTER_AUDIT_2026-08-29.md`

## 9. PIT Memory work
The PIT adapter is transport/validation only.

Rule: a historical-memory candidate is eligible only when:
- same pair
- same context signature
- candidate timestamp is strictly earlier than query_as_of

For the checked GBPUSD event at `2016-01-08T06:00:00Z`, local validation returned:
- PASS
- 10 eligible candidates
- latest eligible candidate `2016-01-08T04:00:00Z`
- 7,456 future rows excluded
- 1 self-match excluded

This fixes the identified future/self leakage risk in the memory lookup path.

## 10. The remaining real blocker
The architecture is not broken. The remaining work is proof of the existing Full Brain decision boundary, not rebuilding the system.

The next gate is Gate 3C:
ONE real pre-2025 GBPUSD event through:
Market/MTF -> full governed Murphy evidence -> full governed Nison evidence -> PIT memory evidence -> TIZ state -> recovered Decision Brain -> Risk -> Trade Plan.

Acceptance:
- one authoritative as_of
- no future evidence
- full 34 Murphy + 44 Nison consumed when governed envelopes are present
- Nison cannot create direction
- Memory cannot decide alone
- TIZ cannot create direction
- Risk hard gate respected
- decision + trade plan traceable to inputs

## 11. Current caution
A prior test against an old E2E artifact produced a mismatch between the legacy event's SELL direction and a recovered Brain assessment of NEUTRAL. This is not evidence that Murphy is missing. It is evidence that the legacy artifact representation and the recovered Brain input contract are not yet proven identical. The correct response is to use the supplied rule/evidence producers with the recovered Brain contract, not to invent a new Murphy direction mapping.

## 12. Post-Gate-3C path
Gate 3C PASS -> unified 2016–2024 replay -> leakage/provenance/QA -> freeze candidate -> 2025 OOS -> paper -> MT5 Demo -> n8n -> controlled live.

## 13. Cost-control rule
No exploratory CircleCI runs. Local/deterministic validation first. CI only when the candidate is ready for a governed run.

## 14. User-provided Murphy archive handling rule
Do NOT ask the user to resend Murphy merely because the current archive is grouped or nested. The archive is already a valid source/evidence pack. Request another upload only if an exact required artifact is proven missing or unreadable after searching all current project sources.

## 15. Final conclusion
The project is not being restarted.
The work is now at the integration/proof layer:

EXISTING MODULES -> ONE GOVERNED EVENT -> RECOVERED DECISION BRAIN -> RISK -> TRADE PLAN.

No new strategy, no new book semantics, and no 2025 tuning should be introduced during this gate.
