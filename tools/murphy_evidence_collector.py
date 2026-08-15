"""Deterministic local collector for Murphy Rule repository evidence.

The collector is intentionally source-agnostic: it does not infer missing
Murphy semantics. It extracts traceable repository facts from Git history and
files, leaving state reduction to murphy_evidence_chain.reduce_state().
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
import re
import subprocess
from typing import Iterable

RULE_RE = re.compile(r"(?<!\d)(?:00[0-9]|0[1-4][0-9]|05[01])(?!\d)")
OOS_RE = re.compile(r"\b2025\b|OOS", re.IGNORECASE)
STATUS_RE = re.compile(
    r"\b(FROZEN|QA_COMPLETE|TECHNICALLY_COMPLETE|INTEGRATION_PENDING|BLOCKED|UNVERIFIED|CONFLICT|COMPLETED)\b",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class EvidenceRecord:
    rule_id: str
    commit_sha: str
    timestamp: datetime
    artifact_path: str = ""
    evidence_type: str = "git_commit"
    status_claim: str | None = None
    supersedes: str | None = None
    blocker_id: str | None = None
    blocker_closed_by: str | None = None
    blocker_closure_traceable: bool = False
    blocker_closed_after_open: bool = False
    oos_used: bool = False
    oos_forbidden_purpose: bool = False
    future_data_contamination: bool = False
    authoritative: bool = True
    notes: str = ""


def _run(repo: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(repo), *args], text=True).strip()


def _commit_rows(repo: Path, max_count: int | None = None) -> list[tuple[str, datetime, str]]:
    args = ["log", "--format=%H%x09%cI%x09%s"]
    if max_count:
        args.insert(1, f"-n{max_count}")
    rows = []
    for line in _run(repo, *args).splitlines():
        sha, iso, subject = line.split("\t", 2)
        rows.append((sha, datetime.fromisoformat(iso).astimezone(timezone.utc), subject))
    return rows


def _rules(text: str) -> set[str]:
    return {m.group(0) for m in RULE_RE.finditer(text) if 1 <= int(m.group(0)) <= 51}


def _claim(subject: str) -> str | None:
    m = STATUS_RE.search(subject)
    if not m:
        return None
    value = m.group(1).upper()
    return "FROZEN" if value == "COMPLETED" else value


def collect_git_history(repo: Path, max_count: int | None = None) -> list[EvidenceRecord]:
    records: list[EvidenceRecord] = []
    for sha, timestamp, subject in _commit_rows(repo, max_count):
        rules = _rules(subject)
        if not rules:
            continue
        lower = subject.lower()
        evidence_type = "freeze" if "freeze" in lower else "status" if "status" in lower else "git_commit"
        claim = _claim(subject)
        for rule_id in sorted(rules):
            records.append(EvidenceRecord(
                rule_id=rule_id,
                commit_sha=sha,
                timestamp=timestamp,
                evidence_type=evidence_type,
                status_claim=claim,
                oos_used=bool(OOS_RE.search(subject)),
                notes=subject,
            ))
    return records


def collect_artifact_text(repo: Path, paths: Iterable[str]) -> list[EvidenceRecord]:
    records: list[EvidenceRecord] = []
    for raw_path in paths:
        path = repo / raw_path
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        sha = _run(repo, "rev-parse", "HEAD")
        timestamp = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
        rules = _rules(text)
        claim_match = STATUS_RE.search(text)
        claim = claim_match.group(1).upper() if claim_match else None
        for rule_id in sorted(rules):
            records.append(EvidenceRecord(
                rule_id=rule_id,
                commit_sha=sha,
                timestamp=timestamp,
                artifact_path=raw_path,
                evidence_type="artifact",
                status_claim=claim,
                oos_used=bool(OOS_RE.search(text)),
                notes=f"artifact scanned; bytes={len(text.encode('utf-8'))}",
            ))
    return records


def collect(repo: str | Path, artifact_paths: Iterable[str] = (), max_commits: int | None = None) -> list[EvidenceRecord]:
    root = Path(repo).resolve()
    if not (root / ".git").exists():
        raise ValueError(f"not a git repository: {root}")
    records = collect_git_history(root, max_commits)
    records.extend(collect_artifact_text(root, artifact_paths))
    return sorted(records, key=lambda r: (r.rule_id, r.timestamp, r.commit_sha, r.artifact_path))


def to_dicts(records: Iterable[EvidenceRecord]) -> list[dict]:
    return [asdict(r) for r in records]


if __name__ == "__main__":
    import argparse
    import json
    parser = argparse.ArgumentParser()
    parser.add_argument("repo")
    parser.add_argument("--artifact", action="append", default=[])
    parser.add_argument("--max-commits", type=int, default=None)
    args = parser.parse_args()
    print(json.dumps(to_dicts(collect(args.repo, args.artifact, args.max_commits)), default=str, indent=2))
