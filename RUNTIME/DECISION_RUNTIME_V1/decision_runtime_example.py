from decision_runtime import MarketSnapshot, build_decision_event, to_dict

snapshot = MarketSnapshot(
    timestamp="2025-01-02T10:00:00Z",
    symbol="GBPUSD",
    values={"close": 1.2500},
)

event = build_decision_event(
    snapshot=snapshot,
    mode="PAPER",
    brain_assessment={"directional_bias": "bullish", "confidence": 0.80},
    murphy_evidence={"status": "PASS", "direction": "BULLISH", "source_rule_id": "MURPHY_0001"},
    nison_evidence={"confirmation": "CONFIRMED", "contradiction": False, "source_rule_id": "NISON_0001"},
    tiz_evidence={"process_gate": "PASS"},
    risk_evidence={"risk_pass": True},
    execution_plan={
        "status": "EXECUTABLE",
        "entry_price": 1.2500,
        "stop_loss": 1.2400,
        "take_profit": 1.2700,
    },
)

print(to_dict(event))
