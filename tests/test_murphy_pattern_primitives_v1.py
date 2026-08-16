from src.murphy_pattern_primitives.pattern_primitives_v1 import (
    Status,
    horizontal_level_without_approved_tolerance,
    boundary_relationship_without_approved_tolerance,
    breakout_without_approved_filter,
    flagpole_without_approved_sharpness,
)


def test_horizontal_level_refuses_invented_tolerance():
    x = horizontal_level_without_approved_tolerance(
        level_id="L1", level_price=1.25, role="SUPPORT", availability_timestamp="2024-01-01"
    )
    assert x.status is Status.NOT_EVALUABLE


def test_boundary_relationship_refuses_invented_threshold():
    x = boundary_relationship_without_approved_tolerance(
        upper_boundary_id="U", lower_boundary_id="D", availability_timestamp="2024-01-01"
    )
    assert x.relationship == "NOT_EVALUABLE"


def test_breakout_refuses_unapproved_filter():
    x = breakout_without_approved_filter(
        boundary_id="B", direction="UP", availability_timestamp="2024-01-01"
    )
    assert x.status is Status.NOT_EVALUABLE
    assert x.breakout_timestamp is None


def test_flagpole_refuses_unapproved_sharpness():
    x = flagpole_without_approved_sharpness(availability_timestamp="2024-01-01")
    assert x.status is Status.NOT_EVALUABLE
    assert x.relation_to_formation == "PRECEDES"
