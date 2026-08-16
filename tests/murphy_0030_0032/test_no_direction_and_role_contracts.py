"""Role/decision-boundary contracts for Murphy P&F rules 0030-0032."""

from pathlib import Path

AUDIT = Path("audits/MURPHY_0030_0032_COMPATIBILITY_AUDIT_V2_2026-08-16.md")


def test_0030_is_trendline_origin_not_static_support():
    text = AUDIT.read_text(encoding="utf-8")
    assert "45-degree bullish support trendline" in text
    assert "support_origin" in text
    assert "reference_price" in text


def test_0030_cannot_be_entry_direction_signal():
    text = AUDIT.read_text(encoding="utf-8")
    assert "no entry/direction signal" in text


def test_0031_and_0032_are_risk_references():
    text = AUDIT.read_text(encoding="utf-8")
    assert "0031 → below previous O column" in text
    assert "0032 → above previous X column" in text
    assert "risk evidence" in text


def test_box_policy_and_bootstrap_are_not_claimed_as_verbatim_murphy():
    text = AUDIT.read_text(encoding="utf-8")
    assert "operationalization proposals" in text
    assert "cannot be presented as verbatim Murphy rules" in text
