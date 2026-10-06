from pathlib import Path

SRC = Path(__file__).with_name("murphy_0006_0007_nison_0001_0002_source_aligned_v2.pine").read_text(encoding="utf-8")

def check(name, condition):
    if not condition:
        raise AssertionError(name)

checks = [
    ("pine v6", SRC.splitlines()[0].strip() == "//@version=6"),
    ("0006 A2 precedes third", "lowPivotTime > bullA2Time" in SRC),
    ("0007 A2 precedes third", "highPivotTime > bearA2Time" in SRC),
    ("reaction after third", "reactionEligible" in SRC),
    ("post-touch break", "evTime > bullThirdTime" in SRC and "evTime > bearThirdTime" in SRC),
    ("real body engulfing", "realBodyEngulfs" in SRC),
    ("bull current Murphy bound", "bullNisonArmed and not na(bullMurphyPassTime) and time > bullMurphyPassTime" in SRC),
    ("bear current Murphy bound", "bearNisonArmed and not na(bearMurphyPassTime) and time > bearMurphyPassTime" in SRC),
    ("lookahead off", "lookahead=barmerge.lookahead_off" in SRC),
    ("orders disabled", '"Orders"), table.cell(dash, 1, 11, "DISABLED")' in SRC),
    ("2025 locked", '"2025"), table.cell(dash, 1, 9, "LOCKED / NO TUNING")' in SRC),
    ("frozen SL", 'input.float(0.75, "SL ATR multiple"' in SRC),
    ("frozen TP", 'input.float(2.0, "Target R:R"' in SRC),
]

for name, ok in checks:
    check(name, ok)

print(f"SOURCE-ALIGNED V2 STATIC TEST: {len(checks)}/{len(checks)} PASS")
