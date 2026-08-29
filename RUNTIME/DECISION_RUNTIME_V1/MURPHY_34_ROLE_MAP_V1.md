# Murphy 34 — Role Map V1
Date: 2026-08-29
Status: IN PROGRESS — SOURCE-BACKED ROLE CLASSIFICATION

## Purpose
Classify the existing Murphy 34 rule contracts by runtime role without changing rule semantics. This is an integration map, not a new strategy.

## Rules with source-backed role evidence in the supplied Murphy package

| Rule | Runtime role | Current evidence status | Integration boundary |
|---|---|---|---|
| 0003 | Direction / technical context | Historical evidence present | Decision Brain |
| 0004 | Direction / technical context | Historical evidence present | Decision Brain |
| 0006 | Direction / technical context | Historical QA present | Decision Brain |
| 0007 | Direction / technical context | Historical QA present | Decision Brain |
| 0012 | Context / technical evidence | Frozen continuity package present | Decision Brain context |
| 0021 | Direction / technical context | Historical evidence present | Decision Brain |
| 0022 | Direction / technical context | Historical evidence present | Decision Brain |
| 0023 | Direction / technical context | Historical evidence present | Decision Brain |
| 0028 | Confirmation / context | Historical QA present | Decision Brain evidence |
| 0029 | Confirmation / context | Historical QA present | Decision Brain evidence |
| 0030 | Context / structure | Historical P&F replay/QA present | Decision Brain context |
| 0031 | Context / structure | Historical P&F replay/QA present | Decision Brain context |
| 0032 | Context / structure | Historical P&F replay/QA present | Decision Brain context |
| 0033 | Context / technical evidence | Local freeze/QA package present | Decision Brain context pending final contract check |
| 0034 | Candidate validation | Candidate evidence only | Upstream candidate gate; not independent direction |
| 0035 | Candidate validation | Candidate evidence only | Upstream candidate gate; not independent direction |
| 0036 | Candidate validation | Candidate evidence only | Upstream candidate gate; not independent direction |
| 0037 | Context / evidence | 2016–2024 replay evidence present | Decision Brain context |
| 0038 | Context / evidence | 2016–2024 replay evidence present | Decision Brain context |
| 0039 | Process / governance | Contract/process evidence | Governance boundary |
| 0040 | Trend context | 2016–2024 replay evidence present | Decision Brain context |
| 0041 | Regime context | 2016–2024 replay evidence present | Decision Brain context |
| 0042 | Risk / portfolio constraint | Contract/freeze evidence; historical QA not proven | Risk boundary |
| 0043 | Risk / portfolio constraint | Contract/freeze evidence; historical QA not proven | Risk boundary |
| 0044 | Risk / portfolio constraint | Contract/freeze evidence; historical QA not proven | Risk boundary |
| 0045 | Risk / portfolio constraint | Contract/freeze evidence; historical QA not proven | Risk boundary |
| 0047 | Cross-market breadth context | Historical evidence is NYSE, not GBPUSD | Do not fan into GBPUSD without approved cross-market contract |
| 0048 | Cross-market breadth context | Historical evidence is NYSE/TRIN, not GBPUSD | Do not fan into GBPUSD without approved cross-market contract |
| 0049 | Cross-market breadth context | Historical evidence is NYSE/TRIN, not GBPUSD | Do not fan into GBPUSD without approved cross-market contract |
| 0050 | Process / governance | Final closure/process package | Governance boundary |
| 0051 | Process / governance | Final closure/process package | Governance boundary |

## Rules not proven by the supplied package

0018, 0019, 0025, 0026 remain NOT_PROVEN_IN_EXTRACT. No synthetic producer or mapping is authorized.

## Integration rule
A rule must enter the Decision Brain only through its source-backed role. Risk/portfolio rules bypass directional scoring and enter Risk. Process rules do not generate direction. Candidate-validation rules cannot become independent signals. Cross-market evidence cannot be silently treated as GBPUSD evidence.

## Non-negotiable
- Murphy remains primary technical context/direction where the source contract says so.
- Nison remains confirmation/contradiction only.
- TIZ remains process-only and optional/unverified when unavailable.
- Similarity/historical memory remains evidence only.
- No new numerical encodings or strategy semantics are introduced here.
- 2025 is excluded from tuning.

## Next gate
Use this role map to build the wiring-only Murphy adapter into the canonical Decision Event, then validate one pre-2025 integrated event before any unified 2016–2024 run.