# MTF New Workspace Data & Policy Audit — 2026-08-26

## Scope
This audit records the newly recovered workspace evidence before any Direction Arbitration V2 profitability change.

## Confirmed timeframes in the new workspace
- M5
- M15
- M30
- H1
- H4
- D1

The recovered workspace contains M5/M15/M30 outputs for 2016–2024, including trendline geometry, pivot sequence, OBV, and volume-context artifacts.

## Dynamic MTF contract
`DYNAMIC_MTF_BINDING_CONTRACT_V1.json` states:
- timeframe role is selected dynamically from available market context and setup evidence;
- macro context prefers MONTHLY/WEEKLY;
- context prefers WEEKLY/DAILY/H4/H1;
- setup candidates are H4/H1/M30/M15/M5;
- confirmation candidates are H1/M30/M15/M5;
- execution candidates are M30/M15/M5;
- higher timeframe is evaluated before lower timeframe;
- lower timeframe cannot override higher timeframe context without an explicit contradiction state;
- 2025 performance must not select a timeframe;
- missing required timeframe data must yield NOT_EVALUABLE rather than a silent substitute;
- the MTF layer assigns roles/evidence and does not generate BUY/SELL itself.

## Critical compatibility finding
`MURPHY_51_RULE_TO_MTF_FUNCTION_CONTRACT_V1.json` says timeframe assignment for each Murphy rule is **UNRESOLVED_BY_RULE** and must be resolved by an explicit MTF Decision Policy/Contract. The rule-to-MTF map repeatedly uses `UNRESOLVED_BY_RULE` / `DYNAMIC—NOT FIXED`.

Therefore, the next valid engineering gate is **not** to invent a fixed timeframe per Murphy rule. The next gate is to validate the existing runtime Dynamic MTF policy against the actual new M5/M15/M30/H1/H4/D1 evidence and record the selected role/evidence trace.

## Decision-Arbitration constraint
No change to Murphy semantics, Nison semantics, TIZ policy, risk policy, or 2025 OOS is authorized by this audit. Any Arbitration V2 candidate must remain shadow/diagnostic until the MTF role-selection trace is deterministic and auditable.

## Result
M5/M15/M30 are confirmed present in the new workspace. The prior H1/H4-only limitation was a stale-source issue. The remaining blocker is policy/traceability: the rule-level MTF mapping is intentionally dynamic and unresolved by individual rule, so arbitration must consume the runtime MTF role/evidence trace rather than guess a timeframe.
