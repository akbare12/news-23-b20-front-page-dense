#!/usr/bin/env python3
"""Copy entry.png to MAKEFUN_OUTPUT_DIR/entry.png.

The program never writes next to itself: the grader runs it with a
read-only /bot, so the only writable destination is the directory named
by MAKEFUN_OUTPUT_DIR (default "out" for local runs).
"""
import hashlib
import os
import shutil
import struct
import sys

MAX_BYTES = 1048576


def main():
    src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    with open(src, "rb") as fh:
        data = fh.read()
    if len(data) > MAX_BYTES:
        print(f"entry.png is {len(data)} bytes, over the 1 MiB limit")
        return 1
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        print("entry.png is not a PNG")
        return 1
    width, height = struct.unpack(">II", data[16:24])
    if width != 1024 or height != 1024:
        print(f"entry.png is {width}x{height}, expected 1024x1024")
        return 1
    shutil.copyfile(src, dst)
    with open(dst, "rb") as fh:
        copied = fh.read()
    if hashlib.sha256(copied).hexdigest() != hashlib.sha256(data).hexdigest():
        print("copy mismatch")
        return 1
    if len(copied) > MAX_BYTES:
        print(f"copied file is {len(copied)} bytes, over the 1 MiB limit")
        return 1
    print(f"OK: wrote {dst} ({width}x{height}, {len(copied)} bytes, "
          f"sha256 {hashlib.sha256(copied).hexdigest()[:16]}...)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
