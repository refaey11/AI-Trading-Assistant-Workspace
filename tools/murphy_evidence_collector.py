"""Deterministic local collector for Murphy Rule repository evidence.

The collector extracts traceable repository facts from Git history and known
project evidence surfaces. It deliberately does not infer missing Murphy
semantics; reduction is delegated to ``murphy_evidence_chain.reduce_state``.
"""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import re
import subprocess
from typing import Iterable

from tools.murphy_evidence_chain import EvidenceRecord

RULE_RE = re.compile(r"(?<!\d)00(?:0[1-9]|[1-4][0-9]|5[01])(?!\d)")
OOS_RE = re.compile(r"\b2025\b|OOS", re.IGNORECASE)
STATUS_RE = re.compile(
    r"\b(FROZEN|QA_COMPLETE|TECHNICALLY_COMPLETE|INTEGRATION_PENDING|BLOCKED|UNVERIFIED|CONFLICT|COMPLETED)\b",
    re.IGNORECASE,
)
DEFAULT_EVIDENCE_ROOTS = (
    "FREEZES",
    "PROJECT_INDEX",
    "audits",
    "project_state",
    "PROJECT_STATUS_CURRENT_2026-08-12.md",
    "PROJECT_STATUS_CURRENT_2026-08-13.md",
)


def _run(repo: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(repo), *args], text=True).strip()


def _commit_rows(repo: Path, max_count: int | None = None) -> list[tuple[str, datetime, str]]:
    args = ["log", "--format=%H%x09%cI%x09%s"]
    if max_count:
        args.insert(1, f"-n{max_count}")
    rows: list[tuple[str, datetime, str]] = []
    output = _run(repo, *args)
    if not output:
        return rows
    for line in output.splitlines():
        sha, iso, subject = line.split("\t", 2)
        rows.append((sha, datetime.fromisoformat(iso).astimezone(timezone.utc), subject))
    return rows


def _rules(text: str) -> set[str]:
    return {m.group(0) for m in RULE_RE.finditer(text)}


def _claim(subject: str) -> str | None:
    match = STATUS_RE.search(subject)
    if not match:
        return None
    value = match.group(1).upper()
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


def _path_timestamp(repo: Path, path: str) -> tuple[str, datetime] | None:
    """Return last committed SHA/time for a tracked artifact; never use mtime."""
    try:
        row = _run(repo, "log", "-1", "--format=%H%x09%cI", "--", path)
    except subprocess.CalledProcessError:
        return None
    if not row:
        return None
    sha, iso = row.split("\t", 1)
    return sha, datetime.fromisoformat(iso).astimezone(timezone.utc)


def _iter_paths(repo: Path, roots: Iterable[str]) -> list[str]:
    """Expand known evidence roots deterministically without scanning data payloads."""
    paths: list[str] = []
    for raw_root in roots:
        root = repo / raw_root
        if root.is_file():
            paths.append(raw_root)
            continue
        if not root.is_dir():
            continue
        for path in sorted(root.rglob("*")):
            if not path.is_file():
                continue
            # Avoid collecting generated caches/large datasets as evidence text.
            if any(part in {"__pycache__", ".git"} for part in path.parts):
                continue
            rel = path.relative_to(repo).as_posix()
            if path.suffix.lower() in {".md", ".json", ".yaml", ".yml", ".txt", ".csv"}:
                paths.append(rel)
    return paths


def collect_artifact_text(repo: Path, paths: Iterable[str]) -> list[EvidenceRecord]:
    records: list[EvidenceRecord] = []
    for raw_path in sorted(set(paths)):
        path = repo / raw_path
        if not path.is_file():
            continue
        stamp = _path_timestamp(repo, raw_path)
        if stamp is None:
            continue
        sha, timestamp = stamp
        text = path.read_text(encoding="utf-8", errors="replace")
        for rule_id in sorted(_rules(text)):
            claim_match = STATUS_RE.search(text)
            claim = claim_match.group(1).upper() if claim_match else None
            if claim == "COMPLETED":
                claim = "FROZEN"
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


def collect_repository_surface(
    repo: str | Path,
    evidence_roots: Iterable[str] = DEFAULT_EVIDENCE_ROOTS,
    max_commits: int | None = None,
) -> list[EvidenceRecord]:
    """Collect Git-history plus traceable text evidence for the known evidence surface."""
    root = Path(repo).resolve()
    if not (root / ".git").exists():
        raise ValueError(f"not a git repository: {root}")
    records = collect_git_history(root, max_commits)
    paths = _iter_paths(root, evidence_roots)
    records.extend(collect_artifact_text(root, paths))
    return sorted(records, key=lambda r: (r.rule_id, r.timestamp, r.commit_sha, r.artifact_path, r.evidence_type))


def collect(repo: str | Path, artifact_paths: Iterable[str] = (), max_commits: int | None = None) -> list[EvidenceRecord]:
    """Backward-compatible collector; explicit artifacts remain supported."""
    root = Path(repo).resolve()
    if not (root / ".git").exists():
        raise ValueError(f"not a git repository: {root}")
    records = collect_git_history(root, max_commits)
    records.extend(collect_artifact_text(root, artifact_paths))
    return sorted(records, key=lambda r: (r.rule_id, r.timestamp, r.commit_sha, r.evidence_type))


def to_dicts(records: Iterable[EvidenceRecord]) -> list[dict]:
    return [record.__dict__ for record in records]


if __name__ == "__main__":
    import argparse
    import json
    parser = argparse.ArgumentParser()
    parser.add_argument("repo")
    parser.add_argument("--artifact", action="append", default=[])
    parser.add_argument("--repository-surface", action="store_true")
    parser.add_argument("--max-commits", type=int, default=None)
    args = parser.parse_args()
    if args.repository_surface:
        records = collect_repository_surface(args.repo, max_commits=args.max_commits)
    else:
        records = collect(args.repo, args.artifact, args.max_commits)
    print(json.dumps(to_dicts(records), default=str, indent=2))
