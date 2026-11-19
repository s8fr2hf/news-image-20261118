#!/usr/bin/env python3
"""Entry program for make.fun news-image-20261118 (Python 3.13, stdlib only).

Copies the pre-rendered front-page poster (entry.png, built by render.py)
to /output/entry.png. Deterministic: the same input bytes are copied on
every run, so two runs write byte-identical output. No network.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    shutil.copyfile(
        os.path.join(HERE, "entry.png"),
        os.path.join(OUT_DIR, "entry.png"),
    )


if __name__ == "__main__":
    main()
