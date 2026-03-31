#!/usr/bin/env python3
"""Initialize the learning template with a project name.

Usage:
    python scripts/init_project.py <package_name> ["description"]

Example:
    python scripts/init_project.py diffex "Diffusion model exploration on toy 2D problems"

Replaces __PKG__, __DESCRIPTION__, and __TOPIC__ tokens in template files,
renames src/__PKG__/ to src/<package_name>/, and creates agent symlinks.
"""

from __future__ import annotations

import keyword
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Files that contain placeholder tokens. Explicit list, not a glob sweep.
TOKEN_FILES = [
    "pyproject.toml",
    "AGENTS.md",
    "references.md",
    "src/__PKG__/__init__.py",
]

TOKENS = ("__PKG__", "__DESCRIPTION__", "__TOPIC__")


def validate_pkg_name(name: str) -> None:
    if not name.isidentifier() or keyword.iskeyword(name):
        print(f"Error: '{name}' is not a valid Python package name.", file=sys.stderr)
        sys.exit(1)


def replace_tokens(path: Path, replacements: dict[str, str]) -> bool:
    """Replace tokens in a file. Returns True if any replacement was made."""
    text = path.read_text()
    original = text
    for token, value in replacements.items():
        text = text.replace(token, value)
    if text != original:
        path.write_text(text)
        return True
    return False


def main() -> None:
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <package_name> [description]", file=sys.stderr)
        sys.exit(1)

    pkg = sys.argv[1]
    description = sys.argv[2] if len(sys.argv) > 2 else pkg

    validate_pkg_name(pkg)

    replacements = {
        "__PKG__": pkg,
        "__DESCRIPTION__": description,
        "__TOPIC__": pkg,
    }

    print(f"Initializing project: {pkg}")
    print(f"Description: {description}")
    print(f"Root: {ROOT}\n")

    # Replace tokens in template files
    for rel_path in TOKEN_FILES:
        path = ROOT / rel_path
        if not path.exists():
            # Token file may already have been renamed (e.g. re-running)
            continue
        if replace_tokens(path, replacements):
            print(f"  Updated {rel_path}")

    # Rename package directory
    src_dir = ROOT / "src" / "__PKG__"
    dst_dir = ROOT / "src" / pkg
    if src_dir.exists():
        src_dir.rename(dst_dir)
        print(f"  Renamed src/__PKG__/ -> src/{pkg}/")
    elif dst_dir.exists():
        print(f"  src/{pkg}/ already exists, skipping rename")

    # Create agent symlinks
    os.chdir(ROOT)
    for name in ("CLAUDE.md", "GEMINI.md"):
        link = ROOT / name
        if link.is_symlink() or link.exists():
            link.unlink()
        link.symlink_to("AGENTS.md")
    print("  Created CLAUDE.md -> AGENTS.md and GEMINI.md -> AGENTS.md symlinks")

    print(f"""
Done. Next steps:
  1. Write a design spec in docs/superpowers/specs/
  2. Edit references.md with your reading list
  3. Edit scripts/download_papers.py with arXiv IDs
  4. Edit AGENTS.md with notebook progression
  5. Run: uv sync --dev
  6. Run: python scripts/download_papers.py""")


if __name__ == "__main__":
    main()
