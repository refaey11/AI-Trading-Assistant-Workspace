from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT / "DEVELOPMENT_2016_2024/current_stack_historical_replay_v5_4.py").read_text(encoding="utf-8")


def test_nison_is_optional_confirmation_evidence():
    assert 'ng is None or any(pd.isna(mtf_row.get(k)) for k in MTF_FIELDS)' not in SOURCE
    assert 'if nids != NISON_IDS:' not in SOURCE
    assert 'ng = pd.DataFrame(columns=["source_rule_id", "expanded_ids", "status", "direction"])' in SOURCE
    assert '"status":"AVAILABLE" if nids else "ABSENT"' in SOURCE


def test_only_opposite_nison_pass_can_contradict():
    assert 'contradiction = bool(opposite)' in SOURCE
    assert 'opposite = normalized_ndirs & ({"SELL"} if murphy_direction == "BUY" else {"BUY"})' in SOURCE


def test_frozen_candidate_risk_is_075_atr_and_2r():
    assert "SL_ATR = 0.75" in SOURCE
    assert "TP_R = 2.0" in SOURCE
    assert "reward_distance = TP_R * stop_distance" in SOURCE
    assert 'rr_target = TP_R * stop_distance' in SOURCE
    assert 'stop_distance=stop_distance,' in SOURCE


if __name__ == "__main__":
    test_nison_is_optional_confirmation_evidence()
    test_only_opposite_nison_pass_can_contradict()
    test_frozen_candidate_risk_is_075_atr_and_2r()
    print("V5.4 contract tests: PASS")
