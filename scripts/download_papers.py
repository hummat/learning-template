#!/usr/bin/env python3
"""Download arXiv papers listed in PAPERS below.

Usage:
    python scripts/download_papers.py

Papers are saved to references/papers/ (gitignored).
Uses concurrent downloads for speed. Re-running skips existing files.
"""

from __future__ import annotations

import os
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

# fmt: off
# Edit this dict: filename -> arXiv URL
PAPERS: dict[str, str] = {
    # "author-year-short-title.pdf": "https://arxiv.org/pdf/XXXX.XXXXX",
}
# fmt: on

PAPERS_DIR = Path(__file__).parent.parent / "references" / "papers"


def download(name: str, url: str) -> str:
    path = PAPERS_DIR / name
    if path.exists():
        return f"SKIP  {path.stat().st_size // 1024:>5}K  {name}"
    try:
        urllib.request.urlretrieve(url, path)
        size = path.stat().st_size // 1024
        return f"OK    {size:>5}K  {name}"
    except Exception as e:
        return f"FAIL         {name}: {e}"


def main() -> None:
    if not PAPERS:
        print("No papers configured. Edit PAPERS dict in this script.")
        return

    PAPERS_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Downloading {len(PAPERS)} papers to {PAPERS_DIR}/\n")

    with ThreadPoolExecutor(max_workers=6) as pool:
        results = pool.map(lambda item: download(*item), PAPERS.items())

    for r in sorted(results):
        print(r)


if __name__ == "__main__":
    main()
