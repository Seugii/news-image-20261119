#!/usr/bin/env python3
"""Entry program for make.fun news-image-20261119 (Python 3.13, stdlib only).

Copies the finished front-page image held in this repository to
/output/entry.png. Deterministic: the same bytes on every run, no network.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

os.makedirs(OUT_DIR, exist_ok=True)
shutil.copyfile(SRC, os.path.join(OUT_DIR, "entry.png"))
