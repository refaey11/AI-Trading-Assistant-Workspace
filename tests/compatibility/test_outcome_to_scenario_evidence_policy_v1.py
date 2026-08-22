from compatibility.outcome_to_scenario_evidence_policy_v1 import attach_outcome_evidence


def base_scenario():
    return {
        "pair": "GBPUSD",
        "primary_scenario": "NEUTRAL / TWO-SIDED",
        "decision": "WAIT",
        "confidence": 0.5,
        "bullish_score": 1,
        "bearish_score": 2,
        "neutral_score": 3,
    }


def base_memory_package():
    return {
        "memory_role": "EVIDENCE_ONLY",
        "direction": None,
        "final_trade_decision": None,
        "historical_outcome": {
            "pair": "GBPUSD",
            "occurrences": 100,
            "positive_rate_6h": 0.52,
            "median_return_6h": 0.001,
        },
    }


def test_outcome_attaches_without_overriding_scenario():
    scenario = base_scenario()
    result = attach_outcome_evidence(
        scenario=scenario,
        memory_package=base_memory_package(),
    )
    assert result.status == "PASS"
    assert result.scenario["primary_scenario"] == scenario["primary_scenario"]
    assert result.scenario["decision"] == scenario["decision"]
    assert result.scenario["confidence"] == scenario["confidence"]
    assert result.scenario["bullish_score"] == scenario["bullish_score"]
    assert result.scenario["bearish_score"] == scenario["bearish_score"]
    assert result.scenario["neutral_score"] == scenario["neutral_score"]
    assert result.scenario["historical_outcome_evidence"]["positive_rate_6h"] == 0.52
    assert result.scenario["historical_outcome_role"] == "DESCRIPTIVE_EVIDENCE_ONLY"
    assert result.scenario["historical_outcome_can_override_scenario"] is False
    assert result.scenario["historical_outcome_used_for_direction"] is False
    assert result.scenario["final_trade_decision"] is None


def test_non_evidence_memory_fails_closed():
    package = base_memory_package()
    package["memory_role"] = "STRATEGY"
    result = attach_outcome_evidence(scenario=base_scenario(), memory_package=package)
    assert result.status == "NOT_EVALUABLE"
    assert result.reason == "MEMORY_NOT_EVIDENCE_ONLY"


def test_directional_memory_fails_closed():
    package = base_memory_package()
    package["direction"] = "BUY"
    result = attach_outcome_evidence(scenario=base_scenario(), memory_package=package)
    assert result.status == "NOT_EVALUABLE"
    assert result.reason == "MEMORY_DIRECTION_FORBIDDEN"


def test_directional_outcome_fails_closed():
    package = base_memory_package()
    package["historical_outcome"]["direction"] = "SELL"
    result = attach_outcome_evidence(scenario=base_scenario(), memory_package=package)
    assert result.status == "NOT_EVALUABLE"
    assert result.reason == "DIRECTIONAL_OUTCOME_EVIDENCE_FORBIDDEN"


def test_pair_mismatch_fails_closed():
    package = base_memory_package()
    package["historical_outcome"]["pair"] = "EURUSD"
    result = attach_outcome_evidence(scenario=base_scenario(), memory_package=package)
    assert result.status == "NOT_EVALUABLE"
    assert result.reason == "PAIR_MISMATCH"


def test_incomplete_scenario_fails_closed():
    scenario = base_scenario()
    scenario.pop("confidence")
    result = attach_outcome_evidence(scenario=scenario, memory_package=base_memory_package())
    assert result.status == "NOT_EVALUABLE"
    assert result.reason == "INCOMPLETE_SCENARIO"
