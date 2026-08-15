from src.murphy_0030_0032.evaluator_v1 import evaluate_series
from src.murphy_0030_0032.pnf_3box_log_reference import PNFBar


def bars(*rows):
    return [PNFBar(*r) for r in rows]


def test_0030_requires_an_o_column():
    data = bars(
        ("2024-01-01", 100, 101, 99, 101),
        ("2024-01-02", 101, 104, 100, 103),
    )
    result = evaluate_series(data, 0.01)
    assert all(r.rules[0].rule_id == "MURPHY_0030" for r in result if r.rules)
    assert all(r.rules[0].status == "NOT_EVALUABLE" for r in result if r.rules)


def test_0030_is_structural_origin_only_and_has_no_entry_trigger():
    data = bars(
        ("2024-01-01", 100, 101, 99, 101),
        ("2024-01-02", 101, 104, 100, 103),
        ("2024-01-03", 103, 104, 97, 100),
    )
    evidence = evaluate_series(data, 0.01)[-1].rules[0]
    assert evidence.status == "AVAILABLE"
    assert evidence.direction == "BULLISH"
    assert evidence.evidence_type == "PNF_BULLISH_SUPPORT_ORIGIN"
    assert evidence.role == "STRUCTURAL_REFERENCE"
    assert evidence.entry_trigger is None
    assert evidence.availability_timestamp == "2024-01-03"


def test_0032_is_available_on_downtrend_with_previous_x_and_is_risk_only():
    data = bars(
        ("2024-01-01", 100, 101, 99, 101),
        ("2024-01-02", 101, 104, 100, 103),
        ("2024-01-03", 103, 104, 97, 100),
    )
    evidence = evaluate_series(data, 0.01)[-1].rules[2]
    assert evidence.status == "AVAILABLE"
    assert evidence.placement_relation == "ABOVE_PREVIOUS_X_COLUMN"
    assert evidence.role == "RISK_REFERENCE"
    assert evidence.entry_trigger is None
    assert evaluate_series(data, 0.01)[-1].rules[1].status == "NOT_EVALUABLE"


def test_0031_is_available_on_uptrend_with_previous_o_and_is_risk_only():
    data = bars(
        ("2024-01-01", 100, 101, 99, 101),
        ("2024-01-02", 101, 104, 100, 103),
        ("2024-01-03", 103, 104, 97, 100),
        ("2024-01-04", 100, 100, 94, 95),
        ("2024-01-05", 95, 99, 95, 98),
        ("2024-01-06", 98, 104, 98, 103),
    )
    evidence = evaluate_series(data, 0.01)[-1].rules[1]
    assert evidence.status == "AVAILABLE"
    assert evidence.placement_relation == "BELOW_PREVIOUS_O_COLUMN"
    assert evidence.role == "RISK_REFERENCE"
    assert evidence.entry_trigger is None


def test_prefix_replay_is_future_suffix_invariant():
    prefix = bars(
        ("2024-01-01", 100, 101, 99, 101),
        ("2024-01-02", 101, 104, 100, 103),
        ("2024-01-03", 103, 104, 97, 100),
    )
    suffix = bars(
        ("2024-01-04", 100, 100, 94, 95),
        ("2024-01-05", 95, 99, 95, 98),
    )
    p = evaluate_series(prefix, 0.01)
    f = evaluate_series(prefix + suffix, 0.01)

    def signature(row):
        return [
            (e.rule_id, e.status, e.direction, e.evidence_type, e.role,
             e.reference_column_index, e.reference_price,
             e.placement_relation, e.entry_trigger, e.availability_timestamp)
            for e in row.rules
        ]

    assert [signature(r) for r in p] == [signature(r) for r in f[:len(p)]]


def test_malformed_bar_is_not_evaluable():
    data = bars(
        ("2024-01-01", 100, 99, 101, 100),
    )
    result = evaluate_series(data, 0.01)
    assert result[0].status == "NOT_EVALUABLE"
