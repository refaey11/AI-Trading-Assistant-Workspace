from pathlib import Path

PINE = Path(__file__).with_name("murphy_0006_0007_nison_0001_0002_source_aligned_v2.pine")
src = PINE.read_text(encoding="utf-8")

def test_pine_v6_indicator_header():
    lines = src.splitlines()
    assert lines[0].strip() == "//@version=6"
    assert lines[1].startswith('indicator("Murphy 0006/0007 + Nison 0001/0002')

def test_murphy_0006_0007_lifecycle_is_present():
    required = [
        "bullA1Price", "bullA2Price", "bullLineAvailableTime",
        "bullThirdCandidate", "bullMurphyPass",
        "bearA1Price", "bearA2Price", "bearLineAvailableTime",
        "bearThirdCandidate", "bearMurphyPass",
        "linePrice(", "lowPivotTime >= bullLineAvailableTime",
        "highPivotTime >= bearLineAvailableTime",
        "reactionEligible"
    ]
    for token in required:
        assert token in src, token

def test_nison_real_body_and_explicit_break_trigger():
    required = [
        "realBodyEngulfs",
        "bullEngulf = downTrendContext",
        "bearEngulf = upTrendContext",
        "close > bullEngulfHigh",
        "close < bearEngulfLow"
    ]
    for token in required:
        assert token in src, token

def test_no_legacy_proxy_confirmation_layers():
    forbidden = [
        "bullPin", "bearPin", "volumeMult", "rsiBull", "rsiBear",
        "scoreMin", "usePin", "useInsideBreak", "confirmWindow"
    ]
    for token in forbidden:
        assert token not in src, token

def test_mtf_uses_lookahead_off_and_orders_disabled():
    assert "lookahead=barmerge.lookahead_off" in src
    assert '"Orders"' in src
    assert '"DISABLED"' in src

def test_frozen_execution_values_are_visible():
    assert 'input.float(0.75, "SL ATR multiple"' in src
    assert 'input.float(2.0, "Target R:R"' in src

def test_2025_lock_is_documented():
    assert "2025" in src
    assert "LOCKED / NO TUNING" in src
