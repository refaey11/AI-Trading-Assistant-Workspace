# Murphy Git History Payload Recovery — Result

Date: 2026-09-03
Branch: `diagnostic/murphy-34-recovery-2026-09-02`
Scope: governed Murphy 34 historical producer/evidence recovery
Locked year: 2025

## Execution

Workflow: `Murphy Git History Payload Recovery`
Run: `33686093857`
Conclusion: `success`
Artifact: `murphy-git-history-payload-recovery-v1`
Artifact ID: `9868160184`
Artifact ZIP SHA256: `a26a43a073b3ff089dad719af027e9d823bd01f76cb8e15f7d1382ba08fc0691`

## Recovery result

The workflow checked out the full reachable Git history across repository branches and tags and searched historical file paths for Murphy rule, freeze, evidence, evaluator, and producer-family payloads.

- Reachable commits scanned: **2,457**
- Candidate historical paths: **501**
- Historical file versions recovered: **611**
- Unique blob payloads recovered: **604**
- Versions containing `2025`: **428** (quarantined by metadata; not admitted)
- Synthetic evidence created: **false**
- Current governed fan-in changed: **false**
- Decision eligibility changed: **false**

## Material historical payloads actually recovered

The Git history contains real non-2025 historical evidence artifacts, including:

- Murphy 0006/0007 real-data candidate/confirmation evidence CSVs (small historical samples / candidate evidence).
- Murphy 0003/0004 historical comparison CSV for D1/H1/H4 2016–2024.
- Murphy 0021–0023 historical summary CSV and a clean evaluation CSV (the latter is empty in the recovered version).
- Murphy 0025/0026 evaluator source and compatibility/freeze artifacts.
- Murphy 0030–0032 P&F implementation, tests, and freeze/QA artifacts.
- Murphy 0033 runtime/freeze artifacts.
- Murphy 0034–0045 recovered evaluator/runtime source plus freeze/compatibility artifacts.
- Murphy 0047 runtime/closure artifacts.
- Murphy 0050/0051 process-gate closure artifacts.
- Historical Pivot Sequence availability bridge/test artifacts.

## Important negative finding

No complete 2016–2024 producer-family datasets for the broader discovered families (for example the full DMI/ADX, Parabolic SAR, Trendline Geometry, OBV, Volume Confirmation, or Open Interest historical output tables) were recovered as committed Git payloads from the reachable repository history.

The recovery therefore proves that the repository retains substantial rule/evaluator/freeze history and several real historical evidence artifacts, but it does **not** replace the missing full producer datasets in the current governed fan-in.

## Governance decision

Keep the current producer map / fan-in eligibility unchanged.

Do not promote a rule merely because its evaluator, freeze record, or source code exists in Git history.

For any future promotion, the recovered evidence still has to pass:
1. exact producer-field/semantic binding;
2. provenance verification;
3. availability timestamp verification;
4. strict-as-of verification;
5. 2016–2024 scope verification;
6. explicit exclusion of 2025 from development evidence.

## Next execution target

Use the original Dropbox Murphy split archive as the remaining source of truth for the missing full producer outputs, using the audit-only ZIP reconstruction path already prepared in `BACKTEST/MURPHY_ARCHIVE_PRODUCER_BINDING_AUDIT_V1.py`.
