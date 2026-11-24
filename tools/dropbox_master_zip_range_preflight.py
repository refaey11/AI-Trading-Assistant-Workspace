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


def main() -> int:
    token = os.environ.get("DROPBOX_ACCESS_TOKEN", "").strip()
    token = re.sub(r"^Bearer\\s+", "", token, flags=re.I).strip().strip('"')
    if not token:
        raise RuntimeError("DROPBOX_ACCESS_TOKEN_MISSING")

    req = urllib.request.Request(
        API,
        data=json.dumps({"path": PATH}).encode(),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as response:
        metadata = json.loads(response.read().decode("utf-8"))

    size = int(metadata["size"])
    if size < 22:
        raise RuntimeError(f"INVALID_ZIP_SIZE={size}")

    # Read only the fixed 22-byte ZIP EOCD footer. Do not expand the range
    # if the archive uses a comment or the server does not honor Range.
    start, end = size - 22, size - 1
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
        raise RuntimeError(f"RANGE_PREFLIGHT_HTTP_{exc.code}") from exc

    with response:
        status = getattr(response, "status", response.getcode())
        content_range = response.headers.get("Content-Range", "")
        content_length = response.headers.get("Content-Length", "")
        if status != 206:
            # Close without reading any body if Range was ignored.
            raise RuntimeError(f"RANGE_NOT_HONORED_STATUS={status};_BODY_NOT_READ")
        expected = f"bytes {start}-{end}/{size}"
        if content_range != expected:
            raise RuntimeError(
                f"CONTENT_RANGE_MISMATCH expected={expected!r} actual={content_range!r};_BODY_NOT_READ"
            )
        if content_length and int(content_length) != 22:
            raise RuntimeError(f"RANGE_LENGTH_MISMATCH={content_length};_BODY_NOT_READ")
        footer = response.read(23)
        if len(footer) != 22:
            raise RuntimeError(f"RANGE_BODY_LENGTH_MISMATCH={len(footer)}")
        if footer[:4] != b"PK\\x05\\x06":
            raise RuntimeError("ZIP_EOCD_NOT_AT_FINAL_22_BYTES;_NO_WIDER_READ_ATTEMPTED")

        entries = int.from_bytes(footer[10:12], "little")
        cd_size = int.from_bytes(footer[12:16], "little")
        cd_offset = int.from_bytes(footer[16:20], "little")
        if entries == 0xFFFF or cd_size == 0xFFFFFFFF or cd_offset == 0xFFFFFFFF:
            raise RuntimeError("ZIP64_ARCHIVE_REQUIRES_SEPARATE_REVIEW")

    print(json.dumps({
        "status": "RANGE_SUPPORTED_EOCD_ONLY",
        "dropbox_path": PATH,
        "archive_size": size,
        "range_requested": f"bytes={start}-{end}",
        "bytes_read": 22,
        "zip_entries_from_eocd": entries,
        "central_directory_size": cd_size,
        "central_directory_offset": cd_offset,
        "policy": "Only final 22-byte ZIP EOCD read; no member payload read; no 2025/2026 data accessed.",
    }, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"SAFE_PREFLIGHT_STOP: {type(exc).__name__}: {exc}", file=sys.stderr)
        raise SystemExit(2)
