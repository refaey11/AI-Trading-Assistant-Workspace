import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPLAY_PATH = ROOT / "DEVELOPMENT_2016_2024/current_stack_historical_replay_v5_4.py"


def _load_v5_4_module():
    root_text = str(ROOT)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)
    spec = importlib.util.spec_from_file_location("v5_4_contract_subject", REPLAY_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {REPLAY_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_nison_is_optional_confirmation_evidence():
    # Inspect the actual transformed V4 source, not the wrapper's replacement
    # string literals. Import also fails closed if any expected V4 patch drifts.
    transformed = _load_v5_4_module().source
    assert "ng is None or any(pd.isna(mtf_row.get(k)) for k in MTF_FIELDS)" not in transformed
    assert "if nids != NISON_IDS:" not in transformed
    assert 'if market_row is None or mtf_row is None or any(pd.isna(mtf_row.get(k)) for k in MTF_FIELDS):' in transformed
    assert 'ng = pd.DataFrame(columns=["source_rule_id", "expanded_ids", "status", "direction"])' in transformed
    assert '"status":"AVAILABLE" if nids else "ABSENT"' in transformed


def test_only_opposite_nison_pass_can_contradict():
    transformed = _load_v5_4_module().source
    assert "contradiction = bool(opposite)" in transformed
    assert 'opposite = normalized_ndirs & ({"SELL"} if murphy_direction == "BUY" else {"BUY"})' in transformed


def test_frozen_candidate_risk_is_075_atr_and_2r():
    transformed = _load_v5_4_module().source
    assert "SL_ATR = 0.75" in transformed
    assert "TP_R = 2.0" in transformed
    assert "reward_distance = TP_R * stop_distance" in transformed
    assert "rr_target = TP_R * stop_distance" in transformed
    assert "stop_distance=stop_distance," in transformed


if __name__ == "__main__":
    test_nison_is_optional_confirmation_evidence()
    test_only_opposite_nison_pass_can_contradict()
    test_frozen_candidate_risk_is_075_atr_and_2r()
    print("V5.4 contract tests: PASS")
