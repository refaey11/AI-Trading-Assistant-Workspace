from pathlib import Path

TARGET = Path(__file__).with_name("current_stack_historical_replay_v5_4.py")
SOURCE = TARGET.read_text(encoding="utf-8")

assert "SL_ATR = 0.75" in SOURCE
assert "TP_R = 2.0" in SOURCE
assert "rr_target = 1.5 * atr" not in SOURCE
assert "stop_distance = SL_ATR * atr" in SOURCE
assert "rr_target = TP_R * stop_distance" in SOURCE
assert "take_profit_distance=stop_distance" not in SOURCE
assert "take_profit_distance=rr_target" in SOURCE

print("CANONICAL_PIPELINE_RISK_CONTRACT_PASS")
print("SL_ATR=0.75")
print("TP_R=2.0")
print("NO_1.5_ATR_TARGET_BUG=True")
