from MURPHY_EVALUATORS_V1.murphy_batch_evaluators_0034_0045_recovered_v1 import *


def test_recovered_0034_0045_exact_paths():
    assert wave2(110, 100, 101).state == "PASS"
    assert wave3(5, 6, 7).state == "PASS"
    assert wave4(100, 110, 111).state == "PASS"
    assert fib_zone(38.2).state == "PASS"
    assert cycle_period(10, 20).state == "PASS"
    assert system_discipline(True, True).state == "PASS"
    assert psar_regime(True).state == "PASS"
    assert adx_regime(30, 25).state == "PASS"
    assert capital_reserve(50).state == "PASS"
    assert single_market_exposure(15).state == "PASS"
    assert market_risk(5).state == "PASS"
    assert total_margin(25).state == "PASS"


def test_recovered_0034_0045_fail_closed():
    assert wave3(None, 6, 7).state == "NOT_EVALUABLE"
    assert adx_regime(None, 25).state == "NOT_EVALUABLE"
    assert market_risk(None).state == "NOT_EVALUABLE"
