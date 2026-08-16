import pytest

from bridges.pivot_sequence_v2_availability_bridge import validate_confirmed_pivot_availability


def test_confirmed_pivot_is_available_only_after_two_bars():
    out = validate_confirmed_pivot_availability({
        "source_row": 10,
        "availability_row": 12,
        "confirmation_status": "CONFIRMED_AFTER_2_BARS",
        "year": 2024,
    })
    assert out["available"] is True
    assert out["lookahead_safe"] is True
    assert out["decision_hint"] == "neutral"


def test_early_availability_is_rejected():
    with pytest.raises(ValueError, match="source_row \+ 2"):
        validate_confirmed_pivot_availability({
            "source_row": 10,
            "availability_row": 11,
            "confirmation_status": "CONFIRMED_AFTER_2_BARS",
            "year": 2024,
        })


def test_wrong_confirmation_status_is_rejected():
    with pytest.raises(ValueError, match="Unexpected pivot confirmation status"):
        validate_confirmed_pivot_availability({
            "source_row": 10,
            "availability_row": 12,
            "confirmation_status": "UNCONFIRMED",
            "year": 2024,
        })


def test_2025_is_rejected_as_oos():
    with pytest.raises(ValueError, match="2025 is OOS"):
        validate_confirmed_pivot_availability({
            "source_row": 10,
            "availability_row": 12,
            "confirmation_status": "CONFIRMED_AFTER_2_BARS",
            "year": 2025,
        })
