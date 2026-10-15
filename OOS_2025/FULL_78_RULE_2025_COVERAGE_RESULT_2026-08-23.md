# Full 78-Rule 2025 Coverage Result — 2026-08-23

This is a whole-allowlist evidence-boundary run over the current 2025 rule-smoke stream.
It enumerates all 78 allowlisted rules (34 Murphy + 44 Nison) without inventing missing producer outputs or rule semantics.

## Result

| Family | Observed 2025 output | No 2025 output |
|---|---:|---:|
| Murphy | 8 | 26 |
| Nison | 0 | 44 |
| **Total** | **8** | **70** |

Observed Murphy rules are MURPHY_0003, 0004, 0021, 0022, 0023, 0028, 0029, and 0050.

MURPHY_0021 is the only currently observed rule with PASS events in this stream; its diagnostic run produced 2,772 PASS rows among 6,216 timestamps. The other observed rules are FAIL/NOT_EVALUABLE in the current smoke output.

## Interpretation

This completes the *coverage boundary* for all 78 allowlisted rules, but it is not a claim that all 78 have authoritative 2025 runtime evidence. The current source set has no authoritative 2025 Nison output, and 26 allowlisted Murphy rules have no 2025 producer output in the current smoke stream.

2025 remains OOS and is not used for tuning. No new thresholds, directions, TIZ semantics, or Risk semantics are introduced.

The Final 2025 Decision-Event Stream and Official OOS Backtest remain blocked until the missing authoritative producer outputs are connected.
