#!/usr/bin/env python3
"""Sorry, I Heard That Wrong — make.fun bounty entry.

Writes one line to $MAKEFUN_OUTPUT_DIR/entry.txt (default /output/entry.txt):
the apology a smart speaker gives its owner after mishearing them.
Pure standard library, deterministic, no network, no secrets.
"""

import os
import sys

LINE = (
    "Sorry \u2014 I heard 'delete that song' as 'delete that playlist,' "
    "so your 400 favourites are gone. They were mostly jazz anyway."
)


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    path = os.path.join(out_dir, "entry.txt")

    text = LINE
    if not (1 <= len(text) <= 140):
        print(f"entry must be 1-140 chars, got {len(text)}", file=sys.stderr)
        return 1
    if text != text.strip() or "\n" in text:
        print("entry must be a single non-blank line", file=sys.stderr)
        return 1
    data = text.encode("utf-8")
    data.decode("utf-8")  # raises if not valid UTF-8

    os.makedirs(out_dir, exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "wb") as f:
        f.write(data)
    os.replace(tmp, path)

    with open(path, "rb") as f:
        if f.read() != data:
            print("verify failed: written bytes differ", file=sys.stderr)
            return 1
    print(f"wrote {len(data)} bytes ({len(text)} chars) to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
