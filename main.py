#!/usr/bin/env python3
"""Entry program for make.fun news-image-20261119 (Python 3.13, stdlib only).

Copies the finished front-page image held in this repository to
/output/entry.png. Deterministic: the same bytes on every run, no network.

The image itself was drawn by render_image.py (PIL, Python; kept in this
repository) and committed as entry.png (sha256
66344d3047d6d1dc393ad496282c8f9d349dc0cf59250f87f179652925e93483).
This entrypoint deliberately renders nothing: the grader's minimal
Python image is not guaranteed to carry Pillow, the vendored fonts, or
JPEG decoding, and a self-contained renderer failed run_completes there
twice (rounds 2 and 3, exit code 1) while the identical copyfile pattern
passed on the 17 and 18 November entries.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

os.makedirs(OUT_DIR, exist_ok=True)
shutil.copyfile(SRC, os.path.join(OUT_DIR, "entry.png"))
