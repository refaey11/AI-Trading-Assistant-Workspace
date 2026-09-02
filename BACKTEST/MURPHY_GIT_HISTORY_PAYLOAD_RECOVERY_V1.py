#!/usr/bin/env python3
"""
Audit/recover historical Murphy producer payloads that are still present in Git history.

This tool is intentionally evidence-preserving:
- searches all reachable Git history for producer/freeze-related payload files;
- copies exact historical blobs without rewriting contents;
- records the commit/path/blob identity for every recovered payload;
- reports possible 2025 presence separately and never uses it for eligibility;
- does not modify the governed fan-in, rule semantics, or decision eligibility.
"""

from __future__ import annotations

import csv
import hashlib
import json
import os
import re
import subprocess
from pathlib import Path
from typing import Iterable

OUT = Path(os.environ.get("MURPHY_RECOVERY_OUT", "murphy_git_history_recovery"))
OUT.mkdir(parents=True, exist_ok=True)
PAYLOADS = OUT / "payloads"
PAYLOADS.mkdir(parents=True, exist_ok=True)

# Historical freeze/producer families explicitly identified by the current audit.
PATTERNS = [
    r"MURPHY[_-]000[3-8]",
    r"MURPHY[_-](0018|0019)",
    r"MURPHY[_-](0021|0022|0023|0025|0026|0028|0029)",
    r"MURPHY[_-](0030|0031|0032|0033)",
    r"MURPHY[_-](0034|0035|0036|0037|0038|0039|0040|0041)",
    r"MURPHY[_-](0047|0048|0049|0050|0051)",
    r"PIVOT[_-]SEQUENCE",
    r"TRENDLINE[_-]GEOMETRY",
    r"FOUR[_-]WEEK[_-]LOOKBACK",
    r"DMI[_-]ADX",
    r"PARABOLIC[_-]SAR",
    r"OSCILLATOR[_-]DIVERGENCE",
    r"OBV",
    r"VOLUME[_-]CONFIRMATION",
    r"OPEN[_-]INTEREST",
    r"MURPHY.*(FREEZE|CLOSURE|EVIDENCE|EVALUATION|HISTORICAL)",
]
RX = re.compile("|".join(PATTERNS), re.I)

FREEZE_SHAS = {
    "MURPHY_0018_0019": ["05da42997104bcc9970a501150895ade5b45a85e", "ae510cc85089ae0e3d2804295e25da497c0a9fcb"],
    "MURPHY_0030_0032": ["0b6bb1f1636dc2265317634948d80fd7ec58460e"],
    "MURPHY_0033": ["cc7e4e4a8515683fe6d6e6d152ddab6d469b6b889", "0d66be46c37c39904bf4a42fd309c59eaaee6a12", "b20a2a5723dbdc9d26d0c61a61362ef343e90d49"],
    "MURPHY_0034_0045": ["109e1611395f44a5c4fd970d0eb96112ca1d81c3", "3cf864579677f36bd3f7c9e0d3afe46a40c3d649"],
    "MURPHY_0047_0049": ["efbbd43970487b6205c671ba94a98afd949ca508", "d2a035b33c620190bd0a287644960f1b6a13b476", "597368c4c8a06c6601761082da70f1a71bda2096"],
    "MURPHY_0050_0051": ["597368c4c8a06c6601761082da70f1a71bda2096"],
    "MURPHY_0025_0026": ["a8cc1ae3f2bd0c51204f08904fe2938976916dbe", "9b719c80f4e60fb0831ed20e9442ab69dbfa38a4"],
}


def run(*args: str) -> str:
    p = subprocess.run([*args], check=True, text=True, stdout=subprocess.PIPE)
    return p.stdout


def git(*args: str) -> str:
    return run("git", *args)


def safe_name(path: str) -> str:
    return path.replace("/", "__")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def reachable_commits() -> list[str]:
    return [x.strip() for x in git("rev-list", "--all").splitlines() if x.strip()]


def candidate_paths() -> list[str]:
    lines = git("log", "--all", "--format=%H", "--name-only", "--diff-filter=ACMR").splitlines()
    paths: set[str] = set()
    for line in lines:
        line = line.strip()
        if not line or re.fullmatch(r"[0-9a-f]{40}", line):
            continue
        if RX.search(line):
            paths.add(line)
    return sorted(paths)


def file_versions(path: str) -> list[str]:
    out = git("rev-list", "--all", "--", path)
    return [x.strip() for x in out.splitlines() if x.strip()]


def extract_at(commit: str, path: str) -> tuple[bytes, str] | None:
    proc = subprocess.run(["git", "cat-file", "-p", f"{commit}:{path}"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    if proc.returncode != 0:
        return None
    return proc.stdout, sha256_bytes(proc.stdout)


def classify(path: str) -> str:
    upper = path.upper()
    if "PIVOT_SEQUENCE" in upper:
        return "PIVOT_SEQUENCE"
    if "TRENDLINE_GEOMETRY" in upper:
        return "TRENDLINE_GEOMETRY"
    if "FOUR_WEEK_LOOKBACK" in upper:
        return "FOUR_WEEK_LOOKBACK"
    if "DMI_ADX" in upper:
        return "DMI_ADX"
    if "PARABOLIC_SAR" in upper:
        return "PARABOLIC_SAR"
    if "OSCILLATOR_DIVERGENCE" in upper:
        return "OSCILLATOR_DIVERGENCE"
    if re.search(r"(^|[_/])OBV([_/.-]|$)", upper):
        return "OBV"
    if "VOLUME_CONFIRMATION" in upper:
        return "VOLUME_CONFIRMATION"
    if "OPEN_INTEREST" in upper:
        return "OPEN_INTEREST"
    return "MURPHY_RULE_OR_FREEZE"


def has_2025(data: bytes, path: str) -> bool:
    if "2025" in path:
        return True
    sample = data[:5_000_000]
    return b"2025" in sample


def main() -> int:
    commits = reachable_commits()
    paths = candidate_paths()
    manifest: list[dict] = []
    extracted_blobs: set[str] = set()

    for path in paths:
        versions = file_versions(path)
        # Keep the exact historical versions, but deduplicate identical blobs.
        for commit in versions:
            found = extract_at(commit, path)
            if found is None:
                continue
            data, blob_hash = found
            out_name = f"{blob_hash}__{safe_name(path)}"
            out_path = PAYLOADS / out_name
            if blob_hash not in extracted_blobs:
                out_path.write_bytes(data)
                extracted_blobs.add(blob_hash)
            manifest.append({
                "commit": commit,
                "path": path,
                "blob_sha256": blob_hash,
                "bytes": len(data),
                "family": classify(path),
                "contains_2025": has_2025(data, path),
                "output": str(out_path.relative_to(OUT)),
            })

    with (OUT / "inventory.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["commit","path","blob_sha256","bytes","family","contains_2025","output"])
        w.writeheader()
        w.writerows(manifest)

    summary = {
        "schema_version": "1.0",
        "purpose": "Historical Git payload recovery audit only",
        "reachable_commits_scanned": len(commits),
        "candidate_paths": len(paths),
        "historical_versions_recovered": len(manifest),
        "unique_blobs_recovered": len(extracted_blobs),
        "contains_2025_versions": sum(1 for x in manifest if x["contains_2025"]),
        "locked_year": 2025,
        "decision_eligibility_changed": False,
        "fan_in_changed": False,
        "synthetic_evidence_created": False,
        "freeze_reference_shas": FREEZE_SHAS,
        "notes": [
            "Recovered blobs are exact historical Git contents.",
            "2025-containing payloads are quarantined by metadata only and are not admitted to development evidence.",
            "Historical Git presence does not equal current governed fan-in eligibility.",
        ],
    }
    (OUT / "RECOVERY_SUMMARY.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    readme = [
        "# Murphy Git History Payload Recovery V1",
        "",
        "Audit-only recovery of producer/evidence payloads still reachable in Git history.",
        "",
        f"Recovered unique blobs: **{len(extracted_blobs)}**",
        f"Historical versions: **{len(manifest)}**",
        f"Candidate paths: **{len(paths)}**",
        "",
        "No fan-in promotion, semantic rewrite, synthetic data generation, or 2025 admission is performed by this package.",
    ]
    (OUT / "README.md").write_text("\n".join(readme) + "\n", encoding="utf-8")

    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
