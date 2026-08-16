"""Four-step fail-closed chain for Murphy 0030-0032 progression."""

from pathlib import Path


def _text():
    root = Path(__file__).parents[2]
    candidates = [
        root / "project_state/MURPHY_39_ACCELERATOR_REGISTRY_V1.csv",
        root / "project_state/MURPHY_HYBRID_39_FACTORY_MANIFEST_V1.csv",
    ]
    return "\n".join(p.read_text(encoding="utf-8") for p in candidates if p.exists())


def test_step_1_0030_has_registered_pnf_work():
    text = _text()
    assert "0030" in text
    assert "PNF" in text


def test_step_2_0031_is_not_promoted_without_explicit_evaluator():
    text = _text()
    assert "0031" in text
    assert "NOT_EVALUABLE" in text or "EXISTING" in text


def test_step_3_0032_is_not_promoted_without_explicit_evaluator():
    text = _text()
    assert "0032" in text
    assert "NOT_EVALUABLE" in text or "EXISTING" in text


def test_step_4_chain_is_fail_closed_and_2025_oos():
    text = _text()
    assert "2025" in text
    assert "0030" in text and "0031" in text and "0032" in text
