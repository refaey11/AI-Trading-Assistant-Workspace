from __future__ import annotations
from pathlib import Path
from typing import Any
import pandas as pd

ALLOWED_RULES = {f'NISON_{i:04d}' for i in range(1, 45)} | {
    'MURPHY_0003','MURPHY_0004','MURPHY_0006','MURPHY_0007','MURPHY_0018','MURPHY_0019',
    'MURPHY_0021','MURPHY_0022','MURPHY_0023','MURPHY_0025','MURPHY_0026','MURPHY_0028',
    'MURPHY_0029','MURPHY_0030','MURPHY_0031','MURPHY_0032','MURPHY_0033','MURPHY_0034',
    'MURPHY_0035','MURPHY_0036','MURPHY_0037','MURPHY_0038','MURPHY_0039','MURPHY_0040',
    'MURPHY_0041','MURPHY_0042','MURPHY_0043','MURPHY_0044','MURPHY_0045','MURPHY_0047',
    'MURPHY_0048','MURPHY_0049','MURPHY_0050','MURPHY_0051'}


def build_from_frames(market: pd.DataFrame, mtf: pd.DataFrame, smoke: pd.DataFrame) -> pd.DataFrame:
    for df in (market, mtf, smoke):
        df['timestamp'] = pd.to_datetime(df['timestamp'], utc=True)
    market = market[market.timestamp.dt.year.eq(2025)]
    mtf = mtf[mtf.timestamp.dt.year.eq(2025)]
    smoke = smoke[smoke.timestamp.dt.year.eq(2025)]
    agg = smoke.groupby('timestamp', as_index=False).agg(
        murphy_pass=('status', lambda s: int((s == 'PASS').sum())),
        murphy_fail=('status', lambda s: int((s == 'FAIL').sum())),
        murphy_not_evaluable=('status', lambda s: int((s == 'NOT_EVALUABLE').sum())),
        directional_confirmation=('directional_confirmation', lambda s: '|'.join(sorted(set(x for x in s.dropna().astype(str) if x not in {'UNKNOWN','NONE'})))),
        source_rule_ids=('rule_id', lambda s: '|'.join(sorted(set(x for x in s if x in ALLOWED_RULES)))),
    )
    m = market.merge(mtf, on='timestamp', how='left', suffixes=('_market','_mtf')).merge(agg, on='timestamp', how='left')
    m['murphy_pass'] = m['murphy_pass'].fillna(0).astype(int)
    m['murphy_fail'] = m['murphy_fail'].fillna(0).astype(int)
    m['murphy_not_evaluable'] = m['murphy_not_evaluable'].fillna(0).astype(int)
    m['nison_status'] = 'NOT_EVALUABLE'
    m['tiz_process_state'] = 'NOT_EVALUABLE'
    m['risk_pass'] = False
    m['missing_authoritative'] = 'nison_evidence|tiz_evidence|risk_evidence'
    return m[['timestamp','murphy_pass','murphy_fail','murphy_not_evaluable','directional_confirmation',
              'source_rule_ids','trend','structure_event','location','volatility_state','volume_state',
              'mtf_state','h4_trend','h4_structure','atr20','nison_status','tiz_process_state',
              'risk_pass','missing_authoritative']]


def build_from_paths(root: str) -> pd.DataFrame:
    p = Path(root)
    return build_from_frames(
        pd.read_csv(p/'state_inspect/GBPUSD_MARKET_STATE.csv'),
        pd.read_csv(p/'mtf_inspect/GBPUSD_MTF_H4_H1.csv'),
        pd.read_csv(p/'GBPUSD_2025_RULE_SMOKE_2026-08-23.csv'))
