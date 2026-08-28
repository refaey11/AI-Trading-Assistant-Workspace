from __future__ import annotations
from pathlib import Path

p = Path('artifacts/decision_brain_backtest_2016_2024/decision_events_2016_2024.csv')
if not p.is_file():
    raise SystemExit(f'MISSING_BACKTEST_OUTPUT {p}')
text = p.read_text(encoding='utf-8', errors='ignore')
if '2025-' in text:
    raise SystemExit('2025 LOCK VIOLATION')
print('OOS_2025_LOCK_CONFIRMED')
