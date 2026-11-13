#!/usr/bin/env python3
"""ai-happy-01 entry: "The Happiest Puddle".

Writes the entry image (art.png, shipped in this repo) to /output/entry.png.
Deterministic: the same bytes every run. No network, no randomness.
"""

import hashlib
import os
import shutil
import sys

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "art.png")
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
OUT = os.path.join(OUT_DIR, "entry.png")

MAX_BYTES = 1_048_576
MAX_DIM = 1024


def main():
    if not os.path.isfile(SRC):
        print("art.png missing", file=sys.stderr)
        return 1
    os.makedirs(OUT_DIR, exist_ok=True)
    shutil.copyfile(SRC, OUT)
    # Self-check: the output must be a whole image within the limits,
    # and byte-identical to the shipped source (determinism proof).
    with open(SRC, "rb") as f:
        src_digest = hashlib.sha256(f.read()).hexdigest()
    with open(OUT, "rb") as f:
        data = f.read()
    if hashlib.sha256(data).hexdigest() != src_digest:
        print("output differs from art.png", file=sys.stderr)
        return 1
    if len(data) > MAX_BYTES:
        print(f"entry too large: {len(data)} bytes", file=sys.stderr)
        return 1
    if not (data[:3] == b"\xff\xd8\xff" or data[:8] == b"\x89PNG\r\n\x1a\n"):
        print("entry is not a JPEG or PNG", file=sys.stderr)
        return 1
    digest = hashlib.sha256(data).hexdigest()
    print(f"wrote {OUT} ({len(data)} bytes, sha256 {digest})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
