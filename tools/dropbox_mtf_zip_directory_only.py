from __future__ import annotations

import json
import os
import re
import sys
import urllib.request

API = "https://api.dropboxapi.com/2/files/get_metadata"
CONTENT = "https://content.dropboxapi.com/2/files/download"
PATH = "/MULTI_TF_MARKET_DATA_V1.zip"


def range_read(token: str, start: int, length: int, size: int) -> bytes:
    end = start + length - 1
    if start < 0 or length <= 0 or end >= size:
        raise RuntimeError("INVALID_RANGE")
    req = urllib.request.Request(
        CONTENT,
        headers={
            "Authorization": f"Bearer {token}",
            "Dropbox-API-Arg": json.dumps({"path": PATH}, separators=(",", ":")),
            "Range": f"bytes={start}-{end}",
        },
        method="GET",
    )
    with urllib.request.urlopen(req, timeout=30) as response:
        expected = f"bytes {start}-{end}/{size}"
        actual = response.headers.get("Content-Range", "")
        if response.status != 206 or actual != expected:
            raise RuntimeError(f"RANGE_NOT_EXACT expected={expected!r} actual={actual!r}; body not read")
        body = response.read(length)
        if len(body) != length:
            raise RuntimeError("RANGE_LENGTH_MISMATCH")
        return body


def main() -> int:
    token = os.environ.get("DROPBOX_ACCESS_TOKEN", "").strip()
    token = re.sub(r"^Bearer\\s+", "", token, flags=re.I).strip().strip('"')
    if not token:
        raise RuntimeError("DROPBOX_ACCESS_TOKEN_MISSING")
    req = urllib.request.Request(
        API, data=json.dumps({"path": PATH}).encode(),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as response:
        metadata = json.loads(response.read().decode("utf-8"))
    size = int(metadata["size"])
    footer = range_read(token, size - 22, 22, size)
    if footer[:4] != b"PK\\x05\\x06":
        raise RuntimeError("ZIP_EOCD_NOT_AT_FINAL_22_BYTES")
    count = int.from_bytes(footer[10:12], "little")
    cd_size = int.from_bytes(footer[12:16], "little")
    cd_offset = int.from_bytes(footer[16:20], "little")
    if any(x == sentinel for x, sentinel in ((count, 0xFFFF), (cd_size, 0xFFFFFFFF), (cd_offset, 0xFFFFFFFF))):
        raise RuntimeError("ZIP64_REQUIRES_REVIEW")
    directory = range_read(token, cd_offset, cd_size, size)
    entries, pos = [], 0
    for _ in range(count):
        if directory[pos:pos+4] != b"PK\\x01\\x02":
            raise RuntimeError("CENTRAL_DIRECTORY_SIGNATURE_INVALID")
        flags = int.from_bytes(directory[pos+8:pos+10], "little")
        method = int.from_bytes(directory[pos+10:pos+12], "little")
        comp = int.from_bytes(directory[pos+20:pos+24], "little")
        uncomp = int.from_bytes(directory[pos+24:pos+28], "little")
        nl = int.from_bytes(directory[pos+28:pos+30], "little")
        el = int.from_bytes(directory[pos+30:pos+32], "little")
        cl = int.from_bytes(directory[pos+32:pos+34], "little")
        local = int.from_bytes(directory[pos+42:pos+46], "little")
        name = directory[pos+46:pos+46+nl].decode("utf-8" if flags & 0x800 else "cp437")
        entries.append({
            "name": name, "compression_method": method,
            "compressed_size": comp, "uncompressed_size": uncomp,
            "local_header_offset": local
        })
        pos += 46 + nl + el + cl
    print(json.dumps({
        "status": "MTF_CENTRAL_DIRECTORY_ONLY",
        "archive": PATH,
        "archive_size": size,
        "directory_bytes_read": 22 + cd_size,
        "entries": entries,
        "policy": "Only ZIP EOCD and central-directory metadata read. No local headers, member payloads, candles, or 2025/2026 data accessed."
    }, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"SAFE_PREFLIGHT_STOP: {type(exc).__name__}: {exc}", file=sys.stderr)
        raise SystemExit(2)
