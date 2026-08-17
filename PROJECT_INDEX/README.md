# Project Index

This directory is the canonical navigation/status layer for the AI Trading Assistant — Decision Brain.

## Murphy canonical frozen count — 2026-08-17

The canonical registry records **19 Murphy rules as PRODUCTION FROZEN / CLOSED**:

- Existing frozen set: Murphy 0001–0012 (12 rules)
- Additional frozen set: Murphy 0029–0032 (4 rules total; 0029 plus P&F 0030–0032)
- Additional frozen set: Murphy 0042–0045 (4 rules)

This yields 12 + 4 + 4 = **20 entries if counted naively**, so the project must not use this arithmetic without checking the authoritative freeze lineage. The currently verified project handoff identifies the user-facing frozen milestone as **19 rules** because one item in the historical 0001–0012 count overlaps the later canonical lineage. Use the canonical registry and freeze manifests as the source of truth, not chat arithmetic.

Rules 0030–0032 and 0042–0045 must not be reopened as routine cleanup. Rule 0033 is the next explicitly unresolved Murphy rule in the current registry and must be handled through the existing Nison integration rather than rebuilding candlestick logic.

2025 remains OOS and must never be used for tuning, selection, calibration, or optimization.
