from MURPHY_0006_0007_TRENDLINE_SOURCE_CONTRACT_V1 import evaluate_trendline_confirmation


def test_uptrend_third_touch_bounce_and_no_break_pass():
    r = evaluate_trendline_confirmation(
        rule_id="MURPHY_0006",
        trendline_type="UP",
        anchor_count=2,
        third_touch=True,
        reaction_bounce=True,
        no_break=True,
        confirmation_available_timestamp="2018-01-02T10:00:00Z",
    )
    assert r["status"] == "PASS"
    assert r["direction"] == "BULLISH_STRUCTURE"


def test_downtrend_third_touch_bounce_and_no_break_pass():
    r = evaluate_trendline_confirmation(
        rule_id="MURPHY_0007",
        trendline_type="DOWN",
        anchor_count=2,
        third_touch=True,
        reaction_bounce=True,
        no_break=True,
        confirmation_available_timestamp="2018-01-02T10:00:00Z",
    )
    assert r["status"] == "PASS"
    assert r["direction"] == "BEARISH_STRUCTURE"


def test_touch_without_bounce_fails():
    r = evaluate_trendline_confirmation(
        rule_id="MURPHY_0006",
        trendline_type="UP",
        anchor_count=2,
        third_touch=True,
        reaction_bounce=False,
        no_break=True,
        confirmation_available_timestamp="2018-01-02T10:00:00Z",
    )
    assert r["status"] == "FAIL"
    assert r["direction"] == "NONE"


def test_touch_with_bounce_but_break_fails():
    r = evaluate_trendline_confirmation(
        rule_id="MURPHY_0006",
        trendline_type="UP",
        anchor_count=2,
        third_touch=True,
        reaction_bounce=True,
        no_break=False,
        confirmation_available_timestamp="2018-01-02T10:00:00Z",
    )
    assert r["status"] == "FAIL"
    assert r["direction"] == "NONE"


def test_missing_geometry_is_not_evaluable():
    r = evaluate_trendline_confirmation(
        rule_id="MURPHY_0006",
        trendline_type="UP",
        anchor_count=2,
        third_touch=True,
        reaction_bounce=None,
        no_break=True,
        confirmation_available_timestamp="2018-01-02T10:00:00Z",
    )
    assert r["status"] == "NOT_EVALUABLE"


def test_rule_binding_mismatch_is_not_evaluable():
    r = evaluate_trendline_confirmation(
        rule_id="MURPHY_0006",
        trendline_type="DOWN",
        anchor_count=2,
        third_touch=True,
        reaction_bounce=True,
        no_break=True,
        confirmation_available_timestamp="2018-01-02T10:00:00Z",
    )
    assert r["status"] == "NOT_EVALUABLE"


def test_one_anchor_is_not_evaluable():
    r = evaluate_trendline_confirmation(
        rule_id="MURPHY_0007",
        trendline_type="DOWN",
        anchor_count=1,
        third_touch=True,
        reaction_bounce=True,
        no_break=True,
        confirmation_available_timestamp="2018-01-02T10:00:00Z",
    )
    assert r["status"] == "NOT_EVALUABLE"
