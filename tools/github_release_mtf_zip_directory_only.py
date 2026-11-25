#!/usr/bin/env python3
"""GitHub Release ZIP central-directory inspection only.

Reads only the EOCD tail and central-directory byte range of a named GitHub
Release asset. Never reads local headers or member payloads.
"""
from __future__ import annotations
import json
import os
import struct
import sys
import urllib.request

ASSET_URL = "https://github.com/refaey11/AI-Trading-Assistant-Workspace/releases/download/workspace-v1/MULTI_TF_MARKET_DATA_V1.zip"
EXPECTED_SIZE = 96_751_936
TAIL_LIMIT = 65_557
EOCD = b"PK\\x05\\x06"
CD_SIG = b"PK\\x01\\x02"

def ranged(start: int, end: int, expected_total: int) -> bytes:
    req = urllib.request.Request(
        ASSET_URL,
        headers={"Range": f"bytes={start}-{end}", "Accept-Encoding": "identity"},
    )
    with urllib.request.urlopen(req, timeout=60) as response:
        status = getattr(response, "status", None)
        content_range = response.headers.get("Content-Range", "")
        data = response.read()
    if status != 206 or not content_range.startswith(f"bytes {start}-{end}/"):
        raise RuntimeError(
            f"SAFE_STOP_RANGE_UNSUPPORTED status={status} content_range={content_range!r}"
        )
    if len(data) != end - start + 1:
        raise RuntimeError(f"SAFE_STOP_RANGE_LENGTH expected={end-start+1} got={len(data)}")
    total = int(content_range.rsplit("/", 1)[1])
    if total != expected_total:
        raise RuntimeError(f"SAFE_STOP_ASSET_SIZE expected={expected_total} got={total}")
    return data

def main() -> int:
    tail_start = EXPECTED_SIZE - TAIL_LIMIT
    tail = ranged(tail_start, EXPECTED_SIZE - 1, EXPECTED_SIZE)
    pos = tail.rfind(EOCD)
    if pos < 0 or pos + 22 > len(tail):
        raise RuntimeError("SAFE_STOP_EOCD_NOT_FOUND")
    fields = struct.unpack_from("<4s4H2IH", tail, pos)
    _, disk, cd_disk, disk_entries, total_entries, cd_size, cd_offset, comment_len = fields
    if disk != 0 or cd_disk != 0 or disk_entries != total_entries:
        raise RuntimeError("SAFE_STOP_MULTIDISK_ZIP")
    if cd_offset + cd_size > EXPECTED_SIZE:
        raise RuntimeError("SAFE_STOP_INVALID_CENTRAL_DIRECTORY_BOUNDS")
    if cd_size > 16 * 1024 * 1024:
        raise RuntimeError("SAFE_STOP_CENTRAL_DIRECTORY_TOO_LARGE")
    central = ranged(cd_offset, cd_offset + cd_size - 1, EXPECTED_SIZE)
    entries = []
    cursor = 0
    for _ in range(total_entries):
        if central[cursor:cursor+4] != CD_SIG:
            raise RuntimeError(f"SAFE_STOP_BAD_CENTRAL_SIGNATURE at={cursor}")
        f = struct.unpack_from("<4s6H3I5H2I", central, cursor)
        name_len, extra_len, comment_len_entry = f[10], f[11], f[12]
        end = cursor + 46 + name_len + extra_len + comment_len_entry
        if end > len(central):
            raise RuntimeError("SAFE_STOP_TRUNCATED_CENTRAL_DIRECTORY")
        name_bytes = central[cursor+46:cursor+46+name_len]
        name = name_bytes.decode("utf-8", errors="replace")
        entries.append({
            "name": name,
            "compression_method": f[4],
            "compressed_size": f[8],
            "uncompressed_size": f[9],
            "local_header_offset": f[16],
        })
        cursor = end
    if cursor != len(central):
        raise RuntimeError(f"SAFE_STOP_CENTRAL_DIRECTORY_TRAILING_BYTES {len(central)-cursor}")
    print("GITHUB_RELEASE_ASSET_METADATA_ONLY")
    print(json.dumps({
        "asset_url": ASSET_URL,
        "expected_asset_size": EXPECTED_SIZE,
        "eocd_bytes_read": len(tail),
        "central_directory_bytes_read": len(central),
        "member_count": len(entries),
        "payload_bytes_read": 0,
        "local_headers_read": 0,
        "entries": entries,
    }, indent=2))
    return 0

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"SAFE_STOP: {type(exc).__name__}: {exc}", file=sys.stderr)
        raise SystemExit(2)
