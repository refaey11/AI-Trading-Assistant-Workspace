from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence

ALLOWED_MURPHY = {
    'MURPHY_0003','MURPHY_0004','MURPHY_0006','MURPHY_0007',
    'MURPHY_0018','MURPHY_0019','MURPHY_0021','MURPHY_0022','MURPHY_0023',
    'MURPHY_0025','MURPHY_0026','MURPHY_0028','MURPHY_0029','MURPHY_0030',
    'MURPHY_0031','MURPHY_0032','MURPHY_0033','MURPHY_0034','MURPHY_0035',
    'MURPHY_0036','MURPHY_0037','MURPHY_0038','MURPHY_0039','MURPHY_0040',
    'MURPHY_0041','MURPHY_0042','MURPHY_0043','MURPHY_0044','MURPHY_0045',
    'MURPHY_0047','MURPHY_0048','MURPHY_0049','MURPHY_0050','MURPHY_0051',
}
ALLOWED_NISON = {f'NISON_{i:04d}' for i in range(1, 45)}
ALLOWED_RULES = ALLOWED_MURPHY | ALLOWED_NISON

@dataclass(frozen=True)
class AdapterResult:
    status: str
    evidence: dict[str, Any]
    gate: str
    conflict: str
    decision_hint: str
    reason: str | None = None

def normalize_rule_output(*, rule_id: str, statement: str, direction: str | None,
                          strength: float | None, available: bool,
                          gate: str = 'needs_review', conflict: str = 'neutral') -> AdapterResult:
    rid = str(rule_id)
    if rid not in ALLOWED_RULES:
        return AdapterResult('REJECTED', {}, 'fail', 'insufficient', 'no_trade', 'RULE_NOT_IN_ALLOWLIST')
    normalized_gate = str(gate).lower()
    normalized_conflict = str(conflict).lower()
    if normalized_gate not in {'pass', 'fail', 'needs_review'}:
        return AdapterResult('REJECTED', {}, 'fail', 'insufficient', 'no_trade', 'INVALID_GATE')
    if normalized_conflict not in {'supports', 'contradicts', 'neutral', 'insufficient'}:
        return AdapterResult('REJECTED', {}, 'fail', 'insufficient', 'no_trade', 'INVALID_CONFLICT')
    d = (direction or '').strip().lower()
    if d in {'buy', 'bull', 'bullish'}:
        hint = 'bullish'
    elif d in {'sell', 'bear', 'bearish'}:
        hint = 'bearish'
    elif d in {'neutral', 'no_trade', 'no-trade', ''}:
        hint = 'neutral'
    else:
        return AdapterResult('REJECTED', {}, 'fail', 'insufficient', 'no_trade', 'INVALID_DIRECTION')
    if rid.startswith('NISON_'):
        hint = 'neutral'
    evidence = {
        'module': 'rule_adapter', 'statement': statement, 'direction': d or 'neutral',
        'strength': strength, 'available': bool(available), 'source_rule_id': rid,
    }
    return AdapterResult('PASS', evidence, normalized_gate, normalized_conflict, hint)

def build_execution_event(*, timestamp: str, symbol: str, decision: Mapping[str, Any],
                          source_rule_ids: Sequence[str]) -> dict[str, Any]:
    if not timestamp or not symbol:
        raise ValueError('timestamp and symbol are required')
    ids = [str(x) for x in source_rule_ids]
    if not ids or any(x not in ALLOWED_RULES for x in ids):
        raise ValueError('source_rule_ids contain unknown or non-allowlisted rules')
    signal = decision.get('signal')
    audit = decision.get('audit')
    risk = decision.get('risk_engine', {})
    tiz = decision.get('trading_zone', {})
    if not isinstance(signal, Mapping) or not isinstance(audit, Mapping):
        raise ValueError('decision must contain signal and audit objects')
    direction = str(signal.get('direction', 'NO_TRADE')).upper()
    status = str(signal.get('status', 'REJECTED')).upper()
    if direction not in {'BUY', 'SELL', 'NO_TRADE'}:
        raise ValueError('invalid decision direction')
    if status not in {'CANDIDATE', 'EXECUTABLE', 'REJECTED'}:
        raise ValueError('invalid decision status')
    process_state = str(tiz.get('process_state', '')).upper()
    risk_pass = risk.get('risk_pass') is True
    executable = status == 'EXECUTABLE' and direction in {'BUY', 'SELL'} and process_state == 'READY' and risk_pass
    return {
        'timestamp': timestamp, 'symbol': symbol,
        'decision': direction if executable else 'NO_TRADE',
        'status': 'EXECUTABLE' if executable else 'REJECTED',
        'source_rule_ids': ids, 'tiz_process_state': process_state,
        'risk_pass': risk_pass, 'risk_percent': risk.get('risk_percent'),
        'stop_loss': risk.get('stop_loss'), 'take_profit': risk.get('take_profit'),
        'position_size': risk.get('position_size'),
        'audit_status': audit.get('backtest_status', 'UNTESTED'),
        'execution_ready': executable,
    }
