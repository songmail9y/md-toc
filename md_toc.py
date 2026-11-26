#!/usr/bin/env python3
"""Generate a table of contents for a Markdown file."""
from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from pathlib import Path

HEADING = re.compile(r"^(#{2,6})\s+(.+?)\s*#*$")
FENCE = re.compile(r"^\s*(```|~~~)")


def slug(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    text = re.sub(r"[^a-zA-Z0-9\s-]", "", text).strip().lower()
    return re.sub(r"[\s-]+", "-", text)


def toc(lines: list[str], max_level: int) -> list[str]:
    out: list[str] = []
    in_fence = False
    for line in lines:
        if FENCE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        match = HEADING.match(line)
        if not match:
            continue
        level = len(match.group(1))
        if level > max_level:
            continue
        title = match.group(2).strip()
        out.append(f"{'  ' * (level - 2)}- [{title}](#{slug(title)})")
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a table of contents for a Markdown file.")
    parser.add_argument("path", type=Path)
    parser.add_argument("--max-level", type=int, default=3, choices=range(2, 7))
    args = parser.parse_args()
    lines = args.path.read_text(encoding="utf-8").splitlines()
    print("\n".join(toc(lines, args.max_level)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
