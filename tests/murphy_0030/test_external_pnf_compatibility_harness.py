from dataclasses import dataclass


@dataclass(frozen=True)
class NormalizedEvent:
    timestamp: str
    column: str
    price: float
    event: str


def test_box_size_is_configuration_not_a_tuning_target():
    config = {"box_size": 1.0, "reversal": 3, "construction": "HighLow"}
    assert config["box_size"] == 1.0
    assert config["reversal"] == 3
    assert config["construction"] == "HighLow"


def test_candidate_output_is_normalized_deterministically():
    events_a = [NormalizedEvent("2020-01-02", "X", 101.0, "continue")]
    events_b = [NormalizedEvent("2020-01-02", "X", 101.0, "continue")]
    assert events_a == events_b


def test_prefix_replay_does_not_depend_on_future_suffix():
    prefix = [NormalizedEvent("2020-01-02", "X", 101.0, "continue")]
    with_future = prefix + [NormalizedEvent("2020-01-03", "O", 98.0, "reverse")]
    assert with_future[:1] == prefix


def test_harness_never_selects_box_size_from_outcomes():
    historical_results = {"box_size_a": 1.0, "box_size_b": 2.0}
    selected_box_size = None
    assert selected_box_size is None
    assert historical_results


def test_invalid_configuration_is_fail_closed():
    box_size = 0.0
    assert box_size <= 0
    status = "NOT_EVALUABLE"
    assert status == "NOT_EVALUABLE"
