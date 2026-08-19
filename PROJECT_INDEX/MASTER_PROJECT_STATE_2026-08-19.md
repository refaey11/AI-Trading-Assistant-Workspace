# MASTER PROJECT STATE — 2026-08-19

## Purpose
Single operational control record for the AI Trading Assistant / Decision Brain workspace.

This file resolves status confusion without deleting historical artifacts.

## CURRENT STATUS

| Component | Operational status | Rule/entry count | Authority |
|---|---|---:|---|
| Murphy | CLOSED | 33 / 51 | `PROJECT_INDEX/MURPHY_33_MASTER_FREEZE_MANIFEST_V1.json` |
| Nison | FROZEN | 44 / 44 | `NISON/NISON_STATUS_CHECKPOINT_2026-08-19.md` |
| Trading in the Zone | Process/Psychology layer | 7 / 7 | latest TIZ workstream state |
| Similarity Engine | Historical evidence only | V2 | existing project artifacts |
| Rule Adapter | Integration contract / validation track | — | `contracts/` + adapter contract |
| Decision Brain | Integration track | V1/V1.1 | existing project artifacts |
| Official Baseline V2 + 4H | CANDIDATE | — | `OFFICIAL_BASELINE_AUDIT_V1` |
| 2025 | OOS | — | global project governance |

## WHAT IS PROTECTED

### Murphy — 33 closed
The current 33-rule closure scope is the consolidated freeze manifest. Do not reopen those rules merely because older snapshots report lower counts.

### Nison — 44 frozen
The current Nison checkpoint explicitly records 44/44 frozen. Do not reopen the registry because an older snapshot says otherwise.

## WHAT IS STILL OPEN

### Murphy remaining closure track
18 Murphy rules remain outside the current 33-rule closure scope. They are a parallel workstream, not a blocker for continuing Decision Brain integration or the baseline work.

### Official baseline
V2 + 4H is still a candidate. The official gate requires one uniform protocol:

- Calibration 2016–2023 -> OOS 2024
- Calibration 2016–2024 -> OOS 2025
- same signal, k, SL/TP, ambiguity policy, costs, and execution assumptions
- no tuning on OOS
- leakage audit

## ARCHITECTURE BOUNDARIES

- Murphy = primary technical context / market structure.
- Nison = confirmation/context; cannot create direction alone.
- Trading in the Zone = process/psychology gate; cannot generate direction.
- Similarity = historical memory/evidence only; never sole decision maker.
- Risk = hard gate.
- Decision Brain = synthesizes current market evidence, book knowledge, historical memory, and risk.
- Rule Adapter = normalizes existing rule outputs; it must not copy the 102 registry rules into the Brain.

## REPOSITORY ORGANIZATION

### Canonical control plane
`PROJECT_INDEX/`

### Component knowledge
`01_Murphy/`
`02_Nison/`
`03_TIZ/`

### Integration
`contracts/`
`bridges/`

### Evidence and computation
`data/`
`tools/`
`audits/`

### Frozen/history
`FREEZES/`
`backups/`

### Automation
`.github/workflows/`

## HANDLING OLD FILES

Old status snapshots are historical evidence. Do not delete them merely because they are stale. They are not allowed to override this master state.

If an artifact conflicts with the current state, preserve it and record the conflict in the reconciliation registry. Never silently rewrite historical evidence.

## NEXT WORK ORDER

1. Protect 33 Murphy + 44 Nison.
2. Continue the 18-rule Murphy closure track.
3. Validate Rule Adapter compatibility.
4. Integrate frozen evidence into Decision Brain.
5. Run uniform V2 + 4H walk-forward.
6. Run leakage/robustness gates.
7. Only after passing those gates, label the baseline OFFICIAL and advance the final Decision Brain release gate.

## NON-NEGOTIABLE

2025 is OOS and must never be used for tuning, calibration, selection, or optimization.

Do not rebuild existing project knowledge from scratch. Audit and integrate it first.
