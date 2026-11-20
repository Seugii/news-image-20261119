#!/usr/bin/env python3
"""The World in One Page - 19 November 2026.

Delivers the finished front page image for the make.fun
news-image-20261119 competition.

The image itself (entry.png) is already rendered and committed
alongside this program. This program only copies it to the
output location the grader expects, so it needs nothing but
the Python standard library and no network access.

Usage: python3 main.py
Writes entry.png to $MAKEFUN_OUTPUT_DIR, else to /output when
that directory exists, else to ./entry.png.
"""

import hashlib
import os
import shutil
import sys

SOURCE_NAME = "entry.png"


def find_output_path():
    """Pick where entry.png should be written."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if out_dir and os.path.isdir(out_dir):
        return os.path.join(out_dir, SOURCE_NAME)
    if os.path.isdir("/output"):
        return os.path.join("/output", SOURCE_NAME)
    return os.path.join(os.getcwd(), SOURCE_NAME)


def sha256_of(path):
    """Return the hex sha256 digest of a file."""
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, SOURCE_NAME)
    if not os.path.isfile(source):
        print("error: %s not found next to main.py" % source, file=sys.stderr)
        return 1
    destination = find_output_path()
    if os.path.abspath(source) == os.path.abspath(destination):
        # Already where it needs to be; report it without a copy.
        print("wrote %s sha256=%s" % (destination, sha256_of(destination)))
        return 0
    try:
        shutil.copyfile(source, destination)
    except OSError as exc:
        print("error: could not write %s: %s" % (destination, exc),
              file=sys.stderr)
        return 1
    print("wrote %s sha256=%s" % (destination, sha256_of(destination)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
