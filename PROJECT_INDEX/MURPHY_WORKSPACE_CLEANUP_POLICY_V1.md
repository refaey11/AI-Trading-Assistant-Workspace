# Murphy Workspace Cleanup Policy V1

## Purpose
Prevent historical freeze backups from being mixed with the current 51-rule status audit.

## Rules
1. Never delete historical freeze artifacts.
2. Never overwrite `MURPHY_51_MASTER_AUDIT.csv` merely to make it agree with an older backup.
3. Preserve the 33-rule backup as historical freeze evidence.
4. Use `ALIGNED_FROZEN` only when freeze evidence and the current master audit agree.
5. Use `CONFLICT_REQUIRES_RECONCILIATION` when they disagree.
6. Keep Rules 0013–0020 on their shared-primitive workflow.
7. 2025 remains OOS and is never used for tuning.
8. Keep Nison artifacts outside Murphy-only freeze packages.

## Current cleanup
- 19 rules: aligned between the 33-freeze backup and current master audit.
- 14 rules: conflicting and require artifact-level reconciliation.
- 18 rules: current master-audit status only; no assertion from the 33-freeze backup.

This policy preserves evidence and prevents silent status rewriting.
