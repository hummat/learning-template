#!/usr/bin/env python3
"""Render reference blog posts / course pages to PDF via headless Chromium.

Usage:
    python scripts/download_blogs.py

PDFs are saved to references/blogs/ (alongside the markdown summaries)
and are gitignored via `references/blogs/*.pdf`. Re-running skips
existing files.

Requires `chromium` on PATH (fallbacks: google-chrome, chrome,
chromium-browser).
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

# fmt: off
# Edit this dict: filename (without .pdf) -> blog URL
# Filenames should match the corresponding markdown summary files in
# references/blogs/ so the PDF and summary live side-by-side.
BLOGS: dict[str, str] = {
    # "author-year-short-title": "https://example.com/blog-post",
}
# fmt: on

BLOGS_DIR = Path(__file__).parent.parent / "references" / "blogs"


def find_chromium() -> str | None:
    for name in ("chromium", "google-chrome", "chrome", "chromium-browser"):
        path = shutil.which(name)
        if path:
            return path
    return None


def render(chromium: str, name: str, url: str) -> str:
    path = BLOGS_DIR / f"{name}.pdf"
    if path.exists():
        return f"SKIP  {path.stat().st_size // 1024:>5}K  {name}.pdf"
    try:
        subprocess.run(
            [
                chromium,
                "--headless=new",
                "--disable-gpu",
                "--no-sandbox",
                # 10s of virtual time so late-loading JS (KaTeX, MathJax,
                # syntax highlighters) finishes rendering before capture.
                "--virtual-time-budget=10000",
                "--run-all-compositor-stages-before-draw",
                f"--print-to-pdf={path}",
                "--print-to-pdf-no-header",
                url,
            ],
            check=True,
            capture_output=True,
            timeout=60,
        )
        if not path.exists() or path.stat().st_size == 0:
            return f"FAIL         {name}.pdf: empty output"
        size = path.stat().st_size // 1024
        return f"OK    {size:>5}K  {name}.pdf"
    except subprocess.CalledProcessError as e:
        return f"FAIL         {name}.pdf: {e.stderr.decode()[:120]}"
    except subprocess.TimeoutExpired:
        return f"FAIL         {name}.pdf: timeout"


def main() -> None:
    if not BLOGS:
        print("No blogs configured. Edit BLOGS dict in this script.")
        return

    chromium = find_chromium()
    if not chromium:
        print("Error: no Chromium binary found on PATH.", file=sys.stderr)
        sys.exit(1)

    BLOGS_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Rendering {len(BLOGS)} blogs to {BLOGS_DIR}/ using {chromium}\n")

    with ThreadPoolExecutor(max_workers=3) as pool:
        results = pool.map(lambda item: render(chromium, *item), BLOGS.items())

    for r in sorted(results):
        print(r)


if __name__ == "__main__":
    main()
