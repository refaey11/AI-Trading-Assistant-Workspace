from __future__ import annotations

"""Audit-only validation of the original split Murphy evaluator workspace.

This script deliberately does NOT generate rule evidence, merge fan-in, or promote
any rule to decision eligibility. It reconstructs the three original archive parts,
checks ZIP integrity, inventories exact mapping files/contracts/producer outputs,
and writes a machine-readable inventory for subsequent semantic/as-of binding.

2016-2024 is the only development scope. 2025 is not admitted by this audit.
"""

import csv
import hashlib
import json
import os
import shutil
import subprocess
import urllib.request
import zipfile
from pathlib import Path

REMOTE_PARTS = [
    "/GBPUSD_RULE_EVALUATOR_V2_WORKSPACE_PART_01_OF_03.zip.part",
    "/GBPUSD_RULE_EVALUATOR_V2_WORKSPACE_PART_02_OF_03.zip.part",
    "/GBPUSD_RULE_EVALUATOR_V2_WORKSPACE_PART_03_OF_03.zip.part",
]

RULE_IDS = [
    "0003","0004","0006","0007","0018","0019","0021","0022","0023",
    "0025","0026","0028","0029","0030","0031","0032","0033","0034",
    "0035","0036","0037","0038","0039","0040","0041","0042","0043",
    "0044","0045","0047","0048","0049","0050","0051",
]

EXPECTED_FAMILIES = [
    "FOUR_WEEK_LOOKBACK_V1_OUTPUT",
    "DMI_ADX_V1_OUTPUT",
    "PARABOLIC_SAR_V1_OUTPUT",
    "OSCILLATOR_DIVERGENCE_V1_OUTPUT",
    "TRENDLINE_GEOMETRY_V1_OUTPUT",
    "OBV_V1_OUTPUT",
    "VOLUME_CONFIRMATION_INTEGRATION_V1_OUTPUT",
    "VOLUME_CONFIRMATION_V2_OUTPUT",
    "OPEN_INTEREST_V1_OUTPUT",
    "PIVOT_SEQUENCE_V1_OUTPUT",
    "PIVOT_SEQUENCE_V2_OUTPUT",
]


def download(token: str, remote_path: str, output: Path) -> None:
    req = urllib.request.Request(
        "https://content.dropboxapi.com/2/files/download",
        data=b"",
        method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "Dropbox-API-Arg": json.dumps({"path": remote_path}),
        },
    )
    with urllib.request.urlopen(req, timeout=900) as response, output.open("wb") as handle:
        while True:
            chunk = response.read(4 * 1024 * 1024)
            if not chunk:
                break
            handle.write(chunk)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    token = os.environ.get("DROPBOX_ACCESS_TOKEN", "")
    if not token:
        raise SystemExit("BLOCKED: DROPBOX_ACCESS_TOKEN is not configured")

    root = Path("artifacts/murphy_34_workspace_audit")
    parts_dir = root / "parts"
    extract_dir = root / "extracted"
    parts_dir.mkdir(parents=True, exist_ok=True)
    extract_dir.mkdir(parents=True, exist_ok=True)

    for i, remote_path in enumerate(REMOTE_PARTS, start=1):
        local = parts_dir / f"part{i}.zip.part"
        print(f"DOWNLOAD part={i} path={remote_path}")
        download(token, remote_path, local)
        print(f"DOWNLOADED part={i} bytes={local.stat().st_size} sha256={sha256(local)}")

    reconstructed = root / "GBPUSD_RULE_EVALUATOR_V2_WORKSPACE_FULL.zip"
    with reconstructed.open("wb") as out:
        for i in range(1, 4):
            with (parts_dir / f"part{i}.zip.part").open("rb") as src:
                shutil.copyfileobj(src, out, length=8 * 1024 * 1024)

    print(f"RECONSTRUCTED bytes={reconstructed.stat().st_size} sha256={sha256(reconstructed)}")

    try:
        with zipfile.ZipFile(reconstructed) as archive:
            bad = archive.testzip()
            if bad is not None:
                raise SystemExit(f"ZIP_INTEGRITY_FAILED first_bad_member={bad}")
            names = archive.namelist()
            archive.extractall(extract_dir)
    except zipfile.BadZipFile as exc:
        raise SystemExit(f"ZIP_INTEGRITY_FAILED error={exc}") from exc

    family_inventory = {family: sorted({n.split('/')[0] for n in names if n.startswith(family + "/")}) for family in EXPECTED_FAMILIES}
    family_counts = {family: sum(1 for n in names if n.startswith(family + "/")) for family in EXPECTED_FAMILIES}

    mapping_files = sorted(n for n in names if "MURPHY_" in n and "EXACT_MAPPING" in n and n.lower().endswith((".csv", ".json")))
    evaluator_files = sorted(n for n in names if "MURPHY_EVALUATORS_V1" in n)
    contract_files = sorted(n for n in names if n.lower().endswith("_contract_v1.json") or "CONTRACT_V2" in n)

    # A central-directory filename hit is an inventory fact only.
    report = {
        "schema_version": "1.0",
        "status": "PASS" if mapping_files else "FAIL",
        "scope": "2016-2024",
        "locked_year": 2025,
        "synthetic_evidence_generated": False,
        "decision_eligibility_promoted": False,
        "zip_test": "PASS",
        "archive_bytes": reconstructed.stat().st_size,
        "archive_sha256": sha256(reconstructed),
        "entry_count": len(names),
        "mapping_file_count": len(mapping_files),
        "evaluator_file_count": len(evaluator_files),
        "contract_file_count": len(contract_files),
        "expected_producer_families": EXPECTED_FAMILIES,
        "producer_family_presence": {family: bool(family_counts[family]) for family in EXPECTED_FAMILIES},
        "producer_family_entry_counts": family_counts,
        "mapping_files": mapping_files,
        "evaluator_files": evaluator_files,
        "contract_files": contract_files,
        "governed_rule_ids": [f"MURPHY_{rid}" for rid in RULE_IDS],
        "next_gate": "exact semantic field binding + provenance + producer availability timestamp + strict-as-of replay",
    }

    (root / "MURPHY_34_WORKSPACE_ARCHIVE_INVENTORY_V1.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    # CSV is intentionally inventory-only; no pass/fail decision evidence is inferred.
    with (root / "MURPHY_PRODUCER_FAMILY_INVENTORY_V1.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["producer_family", "archive_members", "presence", "decision_eligible"])
        for family in EXPECTED_FAMILIES:
            writer.writerow([family, family_counts[family], family_counts[family] > 0, "UNVERIFIED"])

    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
