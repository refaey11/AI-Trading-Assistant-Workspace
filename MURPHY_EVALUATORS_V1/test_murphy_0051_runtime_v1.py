from MURPHY_EVALUATORS_V1.murphy_0051_runtime_v1 import evaluate_0051

BASE = {
    'direction': 'LONG',
    'stance': 'BULLISH',
    'position_size': 1.0,
    'acceptable_loss': 100,
    'profit_objective': 200,
    'entry': 1.2700,
    'order_type': 'LIMIT',
    'stop_loss': 1.2600,
}


def test_0051_pass_complete_plan():
    out = evaluate_0051(BASE)
    assert out['status'] == 'PASS'
    assert out['direction_generation'] is False


def test_0051_fail_explicit_empty_field():
    payload = dict(BASE)
    payload['stop_loss'] = ''
    out = evaluate_0051(payload)
    assert out['status'] == 'FAIL'
    assert 'stop_loss' in out['missing_fields']


def test_0051_not_evaluable_unknown_field():
    payload = dict(BASE)
    del payload['stop_loss']
    out = evaluate_0051(payload)
    assert out['status'] == 'NOT_EVALUABLE'
    assert 'stop_loss' in out['missing_status_fields']


if __name__ == '__main__':
    test_0051_pass_complete_plan()
    test_0051_fail_explicit_empty_field()
    test_0051_not_evaluable_unknown_field()
    print('0051: 3/3 PASS')
