from datetime import datetime, timezone

import decision_brain
from compatibility.decision_brain_final_e2e_readiness_v1 import run_final_e2e_readiness
from risk_engine.risk_execution_runtime_v1 import RiskRequest, evaluate_risk


def _row():
    return {
        "mtf_trend_score": 0.7,
        "M5_trend_regime": 0.4,
        "M15_trend_regime": 0.3,
        "M30_trend_regime": 0.2,
        "H1_trend_regime": 0.4,
        "H4_trend_regime": 0.5,
        "D1_trend_regime": 0.3,
        "volume_available": True,
        "M5_volume_regime": 0.2,
        "M15_volume_regime": 0.2,
        "M30_volume_regime": 0.1,
        "H1_volume_regime": 0.1,
        "H4_volume_regime": 0.2,
        "D1_volume_regime": 0.2,
    }


def test_pre_2025_readiness_passes_and_is_not_profitability_claim():
    result = run_final_e2e_readiness(
        decision_brain,
        row=_row(),
        query_as_of=datetime(2024, 12, 31, tzinfo=timezone.utc),
        murphy_evidence={"rules": ["MURPHY_0003"], "attributed": True},
        nison_evidence={"confirmation": "CONFIRMED", "contradiction": False},
        tiz_evidence={"authoritative": False, "status": "NOT_EVALUABLE"},
        risk_evidence={"authoritative": False, "status": "NOT_EVALUABLE"},
        historical_evidence={"retrieval_status": "PASS", "candidate_count": 20},
    )
    assert result["status"] == "PASS"
    assert result["execution"]["eligible"] is False
    assert "TIZ_NOT_PRODUCTION_AUTHORIZED" in result["execution"]["needs_review"]
    assert "RISK_NOT_PRODUCTION_AUTHORIZED" in result["execution"]["needs_review"]
    assert result["governance"]["final_e2e_is_profitability_test"] is False
    assert result["governance"]["production_execution_claimed"] is False


def test_risk_runtime_validates_and_sizes_execution():
    request = RiskRequest(
        equity=10000.0,
        risk_percent=0.005,
        entry_price=1.2500,
        stop_distance=0.0050,
        take_profit_distance=0.0075,
        stop_mode="structure",
        risk_budget_locked=True,
    )
    result = evaluate_risk(request, "BUY", 0.005)
    assert result.risk_pass is True
    assert result.risk_money == 50.0
    assert result.position_size == 10000.0
    assert result.stop_loss == 1.245
    assert result.take_profit == 1.2575


def test_risk_runtime_fails_closed_for_bad_stop_and_profile():
    request = RiskRequest(
        equity=10000.0,
        risk_percent=0.0075,
        entry_price=1.2500,
        stop_distance=0.0005,
        take_profit_distance=0.0075,
        stop_mode="structure",
        risk_budget_locked=True,
    )
    result = evaluate_risk(request, "BUY", 0.005)
    assert result.risk_pass is False
    assert result.reason == "RISK_PROFILE_NOT_FROZEN"


def test_2025_development_is_locked():
    result = run_final_e2e_readiness(
        decision_brain,
        row=_row(),
        query_as_of=datetime(2025, 6, 1, tzinfo=timezone.utc),
        murphy_evidence={},
        nison_evidence={},
        tiz_evidence={},
        risk_evidence={},
        historical_evidence={},
    )
    assert result["status"] == "NOT_EVALUABLE"
    assert result["reason"] == "2025_OOS_LOCKED"


def test_future_data_is_forbidden():
    result = run_final_e2e_readiness(
        decision_brain,
        row=_row(),
        query_as_of=datetime(2026, 1, 1, tzinfo=timezone.utc),
        murphy_evidence={},
        nison_evidence={},
        tiz_evidence={},
        risk_evidence={},
        historical_evidence={},
    )
    assert result["status"] == "NOT_EVALUABLE"
    assert result["reason"] == "2025_OOS_LOCKED"


def test_circleci_governed_final_78_rule_path_uses_full_evidence():
    """Run governed 2025 validation and profitability while preserving diagnostics as CI artifacts."""
    import json
    import os
    import shutil
    import subprocess
    import tempfile
    import urllib.request
    import zipfile
    from pathlib import Path

    if os.environ.get("CIRCLE_JOB") != "decision_brain_final_e2e_readiness_v1":
        return
    if not os.environ.get("CIRCLECI"):
        return

    token = os.environ.get("DROPBOX_ACCESS_TOKEN")
    if not token:
        raise AssertionError("DROPBOX_ACCESS_TOKEN is required for governed Final 78-rule CI execution")

    repo_root = Path(__file__).resolve().parents[2]
    artifact_dir = repo_root / "artifacts" / "final_78_ci"
    shutil.rmtree(artifact_dir, ignore_errors=True)
    artifact_dir.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="final_78_ci_") as td:
        work = Path(td)
        h1_zip = work / "h1.zip"
        m1_zip = work / "m1.zip"
        h1_dir = work / "h1"
        m1_dir = work / "m1"
        h1_dir.mkdir()
        m1_dir.mkdir()

        def download_dropbox(path: str, dest: Path) -> None:
            req = urllib.request.Request(
                "https://content.dropboxapi.com/2/files/download",
                headers={
                    "Authorization": f"Bearer {token}",
                    "Dropbox-API-Arg": json.dumps({"path": path}),
                },
            )
            with urllib.request.urlopen(req, timeout=120) as response, dest.open("wb") as fh:
                shutil.copyfileobj(response, fh)

        source_url = os.environ.get("NISON_2025_SOURCE_URL")
        if source_url:
            urllib.request.urlretrieve(source_url, h1_zip)
        else:
            download_dropbox("/GBPUSD_H1_2016_2025_MASTER.zip", h1_zip)

        m1_url = os.environ.get("MURPHY_M1_SOURCE_URL")
        if m1_url:
            urllib.request.urlretrieve(m1_url, m1_zip)
        else:
            download_dropbox("/GBPUSD_M1_MASTER_2016_2026_V1.zip", m1_zip)

        with zipfile.ZipFile(h1_zip) as zf:
            zf.extractall(h1_dir)
        with zipfile.ZipFile(m1_zip) as zf:
            zf.extractall(m1_dir)

        h1_csv = next(h1_dir.rglob("GBPUSD_H1_2016_2025_MASTER.csv"))
        m1_matches = list(m1_dir.rglob("GBPUSD_M1_MASTER_2016_2026.csv"))
        assert m1_matches, "Canonical M1 source GBPUSD_M1_MASTER_2016_2026.csv not found"
        m1_csv = m1_matches[0]

        subprocess.run(
            ["python", "-m", "pip", "install", "--disable-pip-version-check", "pandas"],
            check=True,
            stdout=subprocess.DEVNULL,
        )

        pit_csv = work / "MURPHY_0022_0023_2025.csv"
        pit_manifest = work / "MURPHY_0022_0023_2025_MANIFEST.json"
        subprocess.run(
            [
                "python",
                str(repo_root / "OOS_2025/run_murphy_0022_0023_2025_pit_v1.py"),
                "--h1", str(h1_csv),
                "--m1", str(m1_csv),
                "--oi", str(repo_root / "evidence/cftc/2025/6b_oi_pit_bound_v1.json"),
                "--output", str(pit_csv),
                "--manifest", str(pit_manifest),
            ],
            check=True,
            cwd=repo_root,
        )

        subprocess.run(
            [
                "python",
                str(repo_root / "OOS_2025/run_final_2025_governed_78_rule_v2.py"),
                "--h1", str(h1_csv),
                "--m1", str(m1_csv),
                "--murphy-0022-0023", str(pit_csv),
                "--output-dir", str(artifact_dir),
                "--validation-only",
            ],
            check=True,
            cwd=repo_root,
        )

        validation_manifest = json.loads(
            (artifact_dir / "FINAL_2025_GOVERNED_78_RULE_VALIDATION_MANIFEST.json").read_text(encoding="utf-8")
        )
        assert validation_manifest["status"] == "PASS"
        assert validation_manifest["murphy_rule_count"] == 34
        assert validation_manifest["nison_rule_count"] == 44
        assert validation_manifest["fan_in_mode"] == "LOSSLESS_FULL_EVIDENCE_WITH_LEGACY_DECISION_COMPAT"
        assert validation_manifest["oos_tuning"] is False
        assert validation_manifest["new_rule_semantics"] is False
        assert validation_manifest["profitability_executed"] is False

        subprocess.run(
            [
                "python",
                str(repo_root / "OOS_2025/run_final_2025_governed_78_rule_v2.py"),
                "--h1", str(h1_csv),
                "--m1", str(m1_csv),
                "--murphy-0022-0023", str(pit_csv),
                "--output-dir", str(artifact_dir),
            ],
            check=True,
            cwd=repo_root,
        )

        profitability_manifest = json.loads(
            (artifact_dir / "FINAL_2025_GOVERNED_78_RULE_MANIFEST.json").read_text(encoding="utf-8")
        )
        provenance = profitability_manifest["final_brain_provenance"]
        assert provenance["murphy_rule_count"] == 34
        assert provenance["nison_rule_count"] == 44
        assert provenance["fan_in_mode"] == "LOSSLESS_FULL_EVIDENCE_WITH_LEGACY_DECISION_COMPAT"
        assert provenance["source_manifest"]["oos_tuning"] is False
        assert provenance["source_manifest"]["new_rule_semantics"] is False

        diagnostic = json.loads(
            (artifact_dir / "FINAL_2025_NO_TRADE_DIAGNOSTIC.json").read_text(encoding="utf-8")
        )
        required_diagnostic_keys = {
            "events",
            "executable",
            "no_trade",
            "not_evaluable",
            "primary_reason_counts",
            "event_status_counts",
            "execution_status_counts",
            "risk_pass_counts",
            "tiz_status_counts",
        }
        missing_diagnostic = sorted(required_diagnostic_keys - set(diagnostic))
        assert not missing_diagnostic, f"Diagnostic keys missing: {missing_diagnostic}"
        print("FINAL_2025_NO_TRADE_DIAGNOSTIC=" + json.dumps(diagnostic, sort_keys=True))

        core = profitability_manifest.get("core")
        assert isinstance(core, dict), "Canonical profitability core metrics are missing"
        required_metric_keys = {
            "trades",
            "win_rate",
            "profit_factor",
            "expectancy_R",
            "total_R",
            "pnl",
        }
        missing = sorted(required_metric_keys - set(core))
        if missing:
            raise AssertionError(f"Profitability core metrics missing: {missing}")
        assert "max_drawdown_core" in profitability_manifest
