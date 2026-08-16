from src.rule_factory.murphy_boundary_provenance_adapter_v1 import validate_boundary_provenance


def test_all_pivots_available():
    result = validate_boundary_provenance(
        {"pivots": [
            {"availability_timestamp": "2026-01-01T10:00:00+00:00"},
            {"availability_timestamp": "2026-01-01T10:05:00+00:00"},
        ]},
        "2026-01-01T10:05:00+00:00",
    )
    assert result["status"] == "PASS"


def test_future_pivot_fails_closed():
    result = validate_boundary_provenance(
        {"pivots": [{"availability_timestamp": "2026-01-01T10:06:00+00:00"}]},
        "2026-01-01T10:05:00+00:00",
    )
    assert result["status"] == "NOT_EVALUABLE"


def test_missing_timestamp_fails_closed():
    result = validate_boundary_provenance(
        {"pivots": [{"price": 1.25}]},
        "2026-01-01T10:05:00+00:00",
    )
    assert result["status"] == "NOT_EVALUABLE"
