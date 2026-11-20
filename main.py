#!/usr/bin/env python3
"""Entry for make.fun's news-image-20261119 bounty.

Copies the bundled front-page image (entry.png) to /output/entry.png.
The image sums up the world news of Thursday 19 November 2026; it
was drawn by tools/build_image.py from headlines verified against
several news sources (see README.md).

Offline and deterministic: pure standard library, no network, no
clock, no randomness, so two runs write byte-identical output.
"""

import hashlib
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
OUT_DIR = "/output"
OUT = os.path.join(OUT_DIR, "entry.png")
LIMIT = 1048576


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    shutil.copyfile(SRC, OUT)
    with open(OUT, "rb") as handle:
        digest = hashlib.sha256(handle.read()).hexdigest()
    size = os.path.getsize(OUT)
    print(f"wrote {OUT} ({size} bytes, sha256 {digest})")
    assert size <= LIMIT, "entry.png exceeds 1 MiB"


if __name__ == "__main__":
    main()
