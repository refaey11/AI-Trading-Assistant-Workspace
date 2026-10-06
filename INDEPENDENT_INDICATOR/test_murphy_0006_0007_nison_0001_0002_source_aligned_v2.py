from pathlib import Path

PINE = Path(__file__).with_name("murphy_0006_0007_nison_0001_0002_source_aligned_v2.pine")
SRC = PINE.read_text(encoding="utf-8")

def check(name, condition):
    if not condition:
        raise AssertionError(name)

def main():
    lines = SRC.splitlines()
    check("pine v6 header", lines[0].strip() == "//@version=6")
    check("indicator header", lines[1].startswith('indicator("Murphy 0006/0007 + Nison 0001/0002'))

    for token in [
        "bullA1Price", "bullA2Price", "bullLineAvailableTime",
        "bullThirdCandidate", "bullMurphyPass", "lowPivotTime > bullA2Time",
        "bearA1Price", "bearA2Price", "bearLineAvailableTime",
        "bearThirdCandidate", "bearMurphyPass",
        "linePrice(", "lowPivotTime >= bullLineAvailableTime",
        "highPivotTime > bearA2Time", "highPivotTime >= bearLineAvailableTime", "reactionEligible",
    ]:
        check("Murphy token: " + token, token in SRC)

    for token in [
        "realBodyEngulfs",
        "bullEngulf = downTrendContext",
        "bearEngulf = upTrendContext",
        "close > bullEngulfHigh",
        "close < bearEngulfLow",
    ]:
        check("Nison token: " + token, token in SRC)

    for token in [
        "bullPin", "bearPin", "volumeMult", "rsiBull", "rsiBear",
        "scoreMin", "usePin", "useInsideBreak", "confirmWindow",
    ]:
        check("legacy proxy removed: " + token, token not in SRC)

    check("MTF lookahead off", "lookahead=barmerge.lookahead_off" in SRC)
    check("orders disabled", '"Orders"' in SRC and '"DISABLED"' in SRC)
    check("frozen SL", 'input.float(0.75, "SL ATR multiple"' in SRC)
    check("frozen TP", 'input.float(2.0, "Target R:R"' in SRC)
    check("2025 lock", "2025" in SRC and "LOCKED / NO TUNING" in SRC)
    check("post-touch break starts after touch", "evTime > bullThirdTime" in SRC and "evTime > bearThirdTime" in SRC)

    # Nison lifecycle must be bound to the current Murphy PASS; stale engulfings
    # from a previous setup must not survive into a new setup.
    for token in [
        "bullNisonArmed", "bearNisonArmed",
        "bullMurphyPassTime", "bearMurphyPassTime",
        "bullNisonArmed and not na(bullMurphyPassTime) and time > bullMurphyPassTime",
        "bearNisonArmed and not na(bearMurphyPassTime) and time > bearMurphyPassTime",
        "bearNisonPass := false", "bullNisonPass := false",
    ]:
        check("Nison lifecycle token: " + token, token in SRC)

    print("SOURCE-ALIGNED INDICATOR V2 STATIC TEST: PASS")

if __name__ == "__main__":
    main()
