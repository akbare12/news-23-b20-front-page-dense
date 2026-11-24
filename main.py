#!/usr/bin/env python3
"""news-23 b20 front-page-dense: copy entry.png (1024x1024) to $MAKEFUN_OUTPUT_DIR/entry.png.

Stdlib only. Never writes next to itself: it writes only to MAKEFUN_OUTPUT_DIR,
and it refuses to run from a read-only copy (it reads entry.png from the repo
directory, which is allowed to be read-only).
"""
import os
import shutil
import struct
import sys

MAX_BYTES = 1024 * 1024
EXPECTED_W, EXPECTED_H = 1024, 1024


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    dst = os.path.join(out_dir, "entry.png")
    with open(src, "rb") as f:
        data = f.read()
    if len(data) > MAX_BYTES:
        print("entry.png exceeds 1 MiB", file=sys.stderr)
        return 1
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        print("entry.png is not a PNG", file=sys.stderr)
        return 1
    # Parse IHDR manually: length (4) + type (4) + width (4) + height (4).
    ihdr_len = struct.unpack(">I", data[8:12])[0]
    ihdr_type = data[12:16]
    if ihdr_len != 13 or ihdr_type != b"IHDR":
        print("entry.png has a bad IHDR chunk", file=sys.stderr)
        return 1
    w, h = struct.unpack(">II", data[16:24])
    if (w, h) != (EXPECTED_W, EXPECTED_H):
        print("entry.png is %dx%d, expected 1024x1024" % (w, h), file=sys.stderr)
        return 1
    if data[-12:] != b"\x00\x00\x00\x00IEND\xaeB`\x82":
        print("entry.png has a bad IEND trailer", file=sys.stderr)
        return 1
    os.makedirs(out_dir, exist_ok=True)
    if os.path.abspath(dst) == os.path.abspath(src):
        print("refusing to overwrite the source entry.png", file=sys.stderr)
        return 1
    with open(dst, "wb") as f:
        f.write(data)
    # Re-read the copy and confirm it is byte-identical to the source.
    with open(dst, "rb") as f:
        if f.read() != data:
            print("output copy does not match source", file=sys.stderr)
            return 1
    print("wrote %s (%d bytes)" % (dst, len(data)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
