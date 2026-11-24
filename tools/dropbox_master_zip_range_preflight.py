from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request

API = "https://api.dropboxapi.com/2/files/get_metadata"
CONTENT = "https://content.dropboxapi.com/2/files/download"
PATH = "/GBPUSD_M1_MASTER_2016_2026_V1.zip"


def range_read(token: str, start: int, length: int, size: int) -> bytes:
    end = start + length - 1
    if start < 0 or length <= 0 or end >= size:
        raise RuntimeError(f"INVALID_RANGE start={start} length={length} size={size}")
    arg = json.dumps({"path": PATH}, separators=(",", ":"))
    req = urllib.request.Request(
        CONTENT,
        headers={
            "Authorization": f"Bearer {token}",
            "Dropbox-API-Arg": arg,
            "Range": f"bytes={start}-{end}",
        },
        method="GET",
    )
    try:
        response = urllib.request.urlopen(req, timeout=30)
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"RANGE_HTTP_{exc.code} start={start} length={length}") from exc
    with response:
        status = getattr(response, "status", response.getcode())
        content_range = response.headers.get("Content-Range", "")
        expected = f"bytes {start}-{end}/{size}"
        if status != 206:
            raise RuntimeError(f"RANGE_NOT_HONORED status={status};_BODY_NOT_READ")
        if content_range != expected:
            raise RuntimeError(f"CONTENT_RANGE_MISMATCH expected={expected!r} actual={content_range!r};_BODY_NOT_READ")
        body = response.read(length)
        if len(body) != length:
            raise RuntimeError(f"RANGE_BODY_LENGTH_MISMATCH expected={length} actual={len(body)}")
        return body


def main() -> int:
    token = os.environ.get("DROPBOX_ACCESS_TOKEN", "").strip()
    token = re.sub(r"^Bearer\s+", "", token, flags=re.I).strip().strip('"')
    if not token:
        raise RuntimeError("DROPBOX_ACCESS_TOKEN_MISSING")

    req = urllib.request.Request(
        API,
        data=json.dumps({"path": PATH}).encode(),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as response:
        metadata = json.loads(response.read().decode("utf-8"))
    size = int(metadata["size"])
    if size < 22:
        raise RuntimeError(f"INVALID_ZIP_SIZE={size}")

    eocd_offset = size - 22
    footer = range_read(token, eocd_offset, 22, size)
    if footer[:4] != b"PK\x05\x06":
        raise RuntimeError("ZIP_EOCD_NOT_AT_FINAL_22_BYTES;_NO_WIDER_READ_ATTEMPTED")
    disk_no = int.from_bytes(footer[4:6], "little")
    cd_disk = int.from_bytes(footer[6:8], "little")
    entries_disk = int.from_bytes(footer[8:10], "little")
    entries_total = int.from_bytes(footer[10:12], "little")
    cd_size = int.from_bytes(footer[12:16], "little")
    cd_offset = int.from_bytes(footer[16:20], "little")
    comment_len = int.from_bytes(footer[20:22], "little")
    if comment_len != 0:
        raise RuntimeError(f"ZIP_COMMENT_PRESENT length={comment_len};_NO_EXPANDED_FOOTER_READ")
    if disk_no != 0 or cd_disk != 0 or entries_disk != entries_total:
        raise RuntimeError("MULTI_DISK_ZIP_UNSUPPORTED")
    if entries_total == 0xFFFF or cd_size == 0xFFFFFFFF or cd_offset == 0xFFFFFFFF:
        raise RuntimeError("ZIP64_ARCHIVE_REQUIRES_SEPARATE_REVIEW")
    if cd_offset + cd_size > eocd_offset:
        raise RuntimeError("CENTRAL_DIRECTORY_BOUNDS_INVALID")
    if cd_size > 1024 * 1024:
        raise RuntimeError(f"CENTRAL_DIRECTORY_TOO_LARGE={cd_size}")

    directory = range_read(token, cd_offset, cd_size, size)
    entries = []
    pos = 0
    for index in range(entries_total):
        if pos + 46 > len(directory) or directory[pos:pos+4] != b"PK\x01\x02":
            raise RuntimeError(f"CENTRAL_DIRECTORY_ENTRY_INVALID index={index}")
        flags = int.from_bytes(directory[pos+8:pos+10], "little")
        method = int.from_bytes(directory[pos+10:pos+12], "little")
        crc32 = int.from_bytes(directory[pos+16:pos+20], "little")
        compressed = int.from_bytes(directory[pos+20:pos+24], "little")
        uncompressed = int.from_bytes(directory[pos+24:pos+28], "little")
        name_len = int.from_bytes(directory[pos+28:pos+30], "little")
        extra_len = int.from_bytes(directory[pos+30:pos+32], "little")
        comment_len = int.from_bytes(directory[pos+32:pos+34], "little")
        local_offset = int.from_bytes(directory[pos+42:pos+46], "little")
        total = 46 + name_len + extra_len + comment_len
        if pos + total > len(directory):
            raise RuntimeError(f"CENTRAL_DIRECTORY_ENTRY_OVERRUN index={index}")
        name_bytes = directory[pos+46:pos+46+name_len]
        name = name_bytes.decode("utf-8" if flags & 0x800 else "cp437")
        if compressed == 0xFFFFFFFF or uncompressed == 0xFFFFFFFF or local_offset == 0xFFFFFFFF:
            raise RuntimeError(f"ZIP64_MEMBER_REQUIRES_REVIEW name={name!r}")
        entries.append({
            "name": name,
            "compressed_size": compressed,
            "uncompressed_size": uncompressed,
            "compression_method": method,
            "flags": flags,
            "crc32_hex": f"{crc32:08x}",
            "local_header_offset": local_offset,
        })
        pos += total
    if pos != len(directory):
        raise RuntimeError(f"CENTRAL_DIRECTORY_TRAILING_BYTES={len(directory)-pos}")

    print(json.dumps({
        "status": "CENTRAL_DIRECTORY_READ_ONLY",
        "dropbox_path": PATH,
        "archive_size": size,
        "bytes_read_this_run": 22 + cd_size,
        "eocd_bytes": 22,
        "central_directory_bytes": cd_size,
        "entry_count": entries_total,
        "entries": entries,
        "policy": "Only ZIP EOCD and central-directory metadata read. No local headers or member payloads read. No 2025/2026 data accessed.",
    }, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"SAFE_PREFLIGHT_STOP: {type(exc).__name__}: {exc}", file=sys.stderr)
        raise SystemExit(2)
