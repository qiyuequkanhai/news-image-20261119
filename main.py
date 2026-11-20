#!/usr/bin/env python3
"""Entrypoint: copy the finished front page into the output directory.

The grader runs this with no network on a read-only filesystem, so the
only job is a plain file copy from the repository into $MAKEFUN_OUTPUT_DIR
(or /output when that variable is unset).
"""

import os
import shutil


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    if not os.path.isfile(source):
        raise SystemExit("entry.png not found next to main.py")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    shutil.copyfile(source, target)
    print("wrote", target, os.path.getsize(target), "bytes")


if __name__ == "__main__":
    main()
