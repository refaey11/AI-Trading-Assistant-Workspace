from __future__ import annotations

import json
import os
import re
import sys
import urllib.request
import zlib
import binascii

API = "https://api.dropboxapi.com/2/files/get_metadata"
CONTENT = "https://content.dropboxapi.com/2/files/download"
PATH = "/GBPUSD_M1_MASTER_2016_2026_V1.zip"
SAFE_DOCS = {"README.md", "VALIDATION_SUMMARY.json"}


def range_read(token: str, start: int, length: int, size: int) -> bytes:
    end = start + length - 1
    if start < 0 or length <= 0 or end >= size:
        raise RuntimeError(f"INVALID_RANGE start={start} length={length} size={size}")
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
        status = getattr(response, "status", response.getcode())
        expected = f"bytes {start}-{end}/{size}"
        actual = response.headers.get("Content-Range", "")
        if status != 206 or actual != expected:
            raise RuntimeError(f"RANGE_NOT_EXACT status={status} expected={expected!r} actual={actual!r};_BODY_NOT_READ")
        body = response.read(length)
        if len(body) != length:
            raise RuntimeError(f"RANGE_LENGTH_MISMATCH expected={length} actual={len(body)}")
        return body


def read_member(token: str, archive_size: int, entry: dict) -> str:
    name = entry["name"]
    if name not in SAFE_DOCS:
        raise RuntimeError(f"MEMBER_NOT_ALLOWLISTED={name}")
    if entry["compressed_size"] > 1024 * 1024 or entry["uncompressed_size"] > 1024 * 1024:
        raise RuntimeError(f"SAFE_DOC_TOO_LARGE={name}")
    offset = entry["local_header_offset"]
    header = range_read(token, offset, 30, archive_size)
    if header[:4] != b"PK\x03\x04":
        raise RuntimeError(f"LOCAL_HEADER_SIGNATURE_INVALID={name}")
    flags = int.from_bytes(header[6:8], "little")
    method = int.from_bytes(header[8:10], "little")
    name_len = int.from_bytes(header[26:28], "little")
    extra_len = int.from_bytes(header[28:30], "little")
    if flags & 1:
        raise RuntimeError(f"ENCRYPTED_MEMBER={name}")
    local_name = range_read(token, offset + 30, name_len, archive_size)
    decoded_name = local_name.decode("utf-8" if flags & 0x800 else "cp437")
    if decoded_name != name:
        raise RuntimeError(f"LOCAL_CENTRAL_NAME_MISMATCH central={name!r} local={decoded_name!r}")
    data_offset = offset + 30 + name_len + extra_len
    compressed = range_read(token, data_offset, entry["compressed_size"], archive_size)
    if method == 0:
        raw = compressed
    elif method == 8:
        raw = zlib.decompress(compressed, -15)
    else:
        raise RuntimeError(f"UNSUPPORTED_COMPRESSION_METHOD={method} member={name}")
    if len(raw) != entry["uncompressed_size"]:
        raise RuntimeError(f"UNCOMPRESSED_SIZE_MISMATCH={name}")
    crc = binascii.crc32(raw) & 0xFFFFFFFF
    if crc != int(entry["crc32_hex"], 16):
        raise RuntimeError(f"CRC32_MISMATCH={name}")
    return raw.decode("utf-8-sig")


def main() -> int:
    token = os.environ.get("DROPBOX_ACCESS_TOKEN", "").strip()
    token = re.sub(r"^Bearer\s+", "", token, flags=re.I).strip().strip('"')
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
    if footer[:4] != b"PK\x05\x06":
        raise RuntimeError("ZIP_EOCD_NOT_AT_FINAL_22_BYTES")
    entries_count = int.from_bytes(footer[10:12], "little")
    cd_size = int.from_bytes(footer[12:16], "little")
    cd_offset = int.from_bytes(footer[16:20], "little")
    if any(x == sentinel for x, sentinel in ((entries_count, 0xFFFF), (cd_size, 0xFFFFFFFF), (cd_offset, 0xFFFFFFFF))):
        raise RuntimeError("ZIP64_REQUIRES_REVIEW")
    directory = range_read(token, cd_offset, cd_size, size)
    entries, pos = [], 0
    for _ in range(entries_count):
        if directory[pos:pos+4] != b"PK\x01\x02":
            raise RuntimeError("CENTRAL_DIRECTORY_SIGNATURE_INVALID")
        flags = int.from_bytes(directory[pos+8:pos+10], "little")
        method = int.from_bytes(directory[pos+10:pos+12], "little")
        crc = int.from_bytes(directory[pos+16:pos+20], "little")
        comp = int.from_bytes(directory[pos+20:pos+24], "little")
        uncomp = int.from_bytes(directory[pos+24:pos+28], "little")
        nl = int.from_bytes(directory[pos+28:pos+30], "little")
        el = int.from_bytes(directory[pos+30:pos+32], "little")
        cl = int.from_bytes(directory[pos+32:pos+34], "little")
        local = int.from_bytes(directory[pos+42:pos+46], "little")
        name = directory[pos+46:pos+46+nl].decode("utf-8" if flags & 0x800 else "cp437")
        entries.append({"name":name,"flags":flags,"method":method,"crc32_hex":f"{crc:08x}","compressed_size":comp,"uncompressed_size":uncomp,"local_header_offset":local})
        pos += 46 + nl + el + cl
    docs = [e for e in entries if e["name"] in SAFE_DOCS]
    if {e["name"] for e in docs} != SAFE_DOCS:
        raise RuntimeError(f"EXPECTED_SAFE_DOCS_MISSING found={[e['name'] for e in docs]}")
    outputs = {}
    for entry in docs:
        outputs[entry["name"]] = read_member(token, size, entry)
    print(json.dumps({
        "status":"SAFE_METADATA_DOCS_READ",
        "archive":PATH,
        "read_members":list(outputs),
        "documents":outputs,
        "not_read":"GBPUSD_M1_MASTER_2016_2026.csv",
        "policy":"Only ZIP directory plus README.md and VALIDATION_SUMMARY.json member bytes read. Market-data CSV payload not accessed; no 2025/2026 candles accessed."
    },indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"SAFE_PREFLIGHT_STOP: {type(exc).__name__}: {exc}",file=sys.stderr)
        raise SystemExit(2)
