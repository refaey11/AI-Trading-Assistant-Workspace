# Paper execution next step

The repository already contains the governed Decision Brain runner and a separate Murphy diagnostic paper bot. The next integration must consume the existing Decision Brain event contract and must not create new trading semantics or tune 2025.

Required order:
1. Validate frozen 2025 source boundaries.
2. Aggregate existing Murphy/Nison evidence under their governed roles.
3. Call the existing Decision Brain.
4. Emit auditable decision events including Murphy direction, Nison confirmation/contradiction, Brain bias/confidence, and rejection reason.
5. Only aligned, risk-passing events may enter paper execution.
6. Execute at next H1 open with the frozen 0.75 ATR / 2R protocol.

2025 remains OOS and no profitability result is official until the existing governance gates pass.
