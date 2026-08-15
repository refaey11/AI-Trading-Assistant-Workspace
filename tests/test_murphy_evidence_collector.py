from pathlib import Path
import subprocess

from tools.murphy_evidence_collector import collect, collect_git_history


def git(repo: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(repo), *args], text=True).strip()


def test_commit_history_collector_is_rule_scoped_and_deterministic(tmp_path: Path):
    git(tmp_path, "init", "-q")
    git(tmp_path, "config", "user.email", "test@example.com")
    git(tmp_path, "config", "user.name", "Test")

    (tmp_path / "status.md").write_text("0025 FROZEN\n", encoding="utf-8")
    git(tmp_path, "add", ".")
    git(tmp_path, "commit", "-m", "status: Murphy 0025 completed QA")
    (tmp_path / "status.md").write_text("0025 FROZEN\n0005 BLOCKED\n", encoding="utf-8")
    git(tmp_path, "add", ".")
    git(tmp_path, "commit", "-m", "status: Murphy 0005 blocked")

    first = collect_git_history(tmp_path)
    second = collect_git_history(tmp_path)
    assert first == second
    assert [r.rule_id for r in first] == ["0005", "0025"]
    assert any(r.status_claim == "FROZEN" for r in first if r.rule_id == "0025")
    assert any(r.status_claim == "BLOCKED" for r in first if r.rule_id == "0005")


def test_artifact_timestamp_uses_git_commit_not_filesystem_mtime(tmp_path: Path):
    git(tmp_path, "init", "-q")
    git(tmp_path, "config", "user.email", "test@example.com")
    git(tmp_path, "config", "user.name", "Test")
    artifact = tmp_path / "FREEZES.md"
    artifact.write_text("0021 FROZEN\n", encoding="utf-8")
    git(tmp_path, "add", ".")
    git(tmp_path, "commit", "-m", "freeze: Murphy 0021")

    records = collect(tmp_path, ["FREEZES.md"])
    artifact_records = [r for r in records if r.evidence_type == "artifact"]
    assert len(artifact_records) == 1
    assert artifact_records[0].rule_id == "0021"
    assert artifact_records[0].commit_sha == git(tmp_path, "log", "-1", "--format=%H", "--", "FREEZES.md")


def test_non_rule_numbers_are_not_emitted(tmp_path: Path):
    git(tmp_path, "init", "-q")
    git(tmp_path, "config", "user.email", "test@example.com")
    git(tmp_path, "config", "user.name", "Test")
    (tmp_path / "x").write_text("2025 0052 0000 0100", encoding="utf-8")
    git(tmp_path, "add", ".")
    git(tmp_path, "commit", "-m", "2025 OOS audit")
    assert collect_git_history(tmp_path) == []
