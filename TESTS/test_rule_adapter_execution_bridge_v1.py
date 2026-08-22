import sys
sys.path.insert(0, '/mnt/data')

from ADAPTERS.rule_adapter_execution_bridge_v1 import normalize_rule_output, build_execution_event


def test_allowlisted_murphy_rule_normalizes():
    r = normalize_rule_output(rule_id='MURPHY_0021', statement='volume supports bullish context',
                              direction='BULLISH', strength=0.7, available=True,
                              gate='pass', conflict='supports')
    assert r.status == 'PASS'
    assert r.decision_hint == 'bullish'
    assert r.evidence['source_rule_id'] == 'MURPHY_0021'


def test_nison_cannot_create_direction():
    r = normalize_rule_output(rule_id='NISON_0001', statement='bullish engulfing',
                              direction='BUY', strength=1.0, available=True,
                              gate='pass', conflict='supports')
    assert r.status == 'PASS'
    assert r.decision_hint == 'neutral'


def test_unknown_rule_is_rejected():
    r = normalize_rule_output(rule_id='MURPHY_0008', statement='blocked rule',
                              direction='SELL', strength=1.0, available=True,
                              gate='pass', conflict='supports')
    assert r.status == 'REJECTED'
    assert r.reason == 'RULE_NOT_IN_ALLOWLIST'


def test_execution_event_fails_closed_without_authoritative_gates():
    decision = {
        'signal': {'direction': 'BUY', 'status': 'EXECUTABLE'},
        'audit': {'backtest_status': 'UNTESTED'},
        'trading_zone': {'process_state': 'NOT_READY'},
        'risk_engine': {'risk_pass': False},
    }
    event = build_execution_event(timestamp='2025-01-02T10:00:00Z', symbol='GBPUSD',
                                  decision=decision, source_rule_ids=['MURPHY_0021'])
    assert event['decision'] == 'NO_TRADE'
    assert event['status'] == 'REJECTED'
    assert event['execution_ready'] is False


def test_execution_event_preserves_existing_executable_decision():
    decision = {
        'signal': {'direction': 'SELL', 'status': 'EXECUTABLE'},
        'audit': {'backtest_status': 'UNTESTED'},
        'trading_zone': {'process_state': 'READY'},
        'risk_engine': {
            'risk_pass': True, 'risk_percent': 0.005,
            'stop_loss': '1.2800', 'take_profit': '1.2600', 'position_size': '1.0'
        },
    }
    event = build_execution_event(timestamp='2025-01-02T10:00:00Z', symbol='GBPUSD',
                                  decision=decision,
                                  source_rule_ids=['MURPHY_0021', 'NISON_0001'])
    assert event['decision'] == 'SELL'
    assert event['status'] == 'EXECUTABLE'
    assert event['execution_ready'] is True
