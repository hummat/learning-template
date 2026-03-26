#!/usr/bin/env bash
# Initialize the learning template with a project name.
#
# Usage:
#   ./scripts/init_project.sh <package_name> "<description>"
#
# Example:
#   ./scripts/init_project.sh diffex "Diffusion model exploration on toy 2D problems"
#
# This renames PLACEHOLDER -> package_name and DESCRIPTION -> description
# throughout the project, then moves src/PLACEHOLDER/ -> src/<package_name>/.

set -euo pipefail

if [[ $# -lt 1 ]]; then
    echo "Usage: $0 <package_name> [description]"
    exit 1
fi

PKG="$1"
DESC="${2:-$PKG}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

# Validate package name (Python identifier)
if ! python3 -c "import keyword; n='$PKG'; assert n.isidentifier() and not keyword.iskeyword(n)" 2>/dev/null; then
    echo "Error: '$PKG' is not a valid Python package name."
    exit 1
fi

echo "Initializing project: $PKG"
echo "Description: $DESC"
echo "Root: $ROOT"
echo

# Replace PLACEHOLDER and DESCRIPTION in all text files
find "$ROOT" -type f \( -name '*.toml' -o -name '*.py' -o -name '*.md' \) \
    -not -path '*/.git/*' \
    -exec sed -i "s/PLACEHOLDER/$PKG/g; s/DESCRIPTION/$DESC/g; s/TOPIC_NAME/$PKG/g; s/TOPIC/$PKG/g" {} +

# Rename the package directory
if [[ -d "$ROOT/src/PLACEHOLDER" ]]; then
    mv "$ROOT/src/PLACEHOLDER" "$ROOT/src/$PKG"
    echo "Renamed src/PLACEHOLDER/ -> src/$PKG/"
fi

echo
echo "Done. Next steps:"
echo "  1. Edit references.md with your reading list"
echo "  2. Edit scripts/download_papers.py with arXiv IDs"
echo "  3. Edit CLAUDE.md with notebook progression"
echo "  4. Run: uv sync --dev"
echo "  5. Run: python scripts/download_papers.py"
