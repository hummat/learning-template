# Learning Template

Template for "explore topic X from scratch" repositories. Marimo notebooks + shared Python package + curated references.

Based on the pattern established in [diffusion-explorer](../diffusion-explorer/).

## What You Get

```
src/__PKG__/            # shared library — rename via init script
notebooks/              # Marimo notebooks, numbered by progression
references/
  papers/               # PDFs (gitignored, re-downloadable)
  blogs/                # blog post summaries as markdown
references.md           # reading order + resource-to-notebook mapping
scripts/
  download_papers.py    # bulk arXiv PDF downloader
  init_project.py       # rename placeholders -> your names
docs/superpowers/
  specs/                # design specs (brainstorming output)
  plans/                # implementation plans
AGENTS.md               # agent context (CLAUDE.md, GEMINI.md are symlinks)
```

## Quick Start

```bash
# 1. Copy the template
cp -r ~/git/learning-template ~/git/my-topic-explorer
cd ~/git/my-topic-explorer

# 2. Initialize with your package name
python scripts/init_project.py mypkg "Understanding topic X from scratch"

# 3. Initialize git
git init && git add -A && git commit -m "Initial scaffold from learning-template"

# 4. Curate your references
#    - Edit references.md with your reading order
#    - Edit scripts/download_papers.py with arXiv IDs
#    - Save blog summaries to references/blogs/

# 5. Install and start
uv sync --dev
python scripts/download_papers.py
uv run marimo edit notebooks/01_first_topic.py
```

## The Workflow

1. **Write a design spec.** What are you learning, why, and in what order? Save to `docs/superpowers/specs/`. This is the foundation.
2. **Curate references.** Phased reading order in `references.md` — one phase per notebook, with depth guidance. This is the learning plan.
3. **Download papers.** Add arXiv IDs to `scripts/download_papers.py`, run it.
4. **Save blog summaries.** One markdown file per blog in `references/blogs/`: URL, summary, "why this matters for the repo."
5. **Write an implementation plan.** Break the spec into concrete steps. Save to `docs/superpowers/plans/`.
6. **Build the shared library.** Reusable utilities in `src/`, tested with pytest.
7. **Write notebooks.** One Marimo notebook per concept, numbered by progression. Import from the shared library, focus on narrative and visualization.

## Conventions

- **Marimo over Jupyter** — reactive, pure `.py` files, clean git diffs, interactive widgets
- **Implement from scratch** — no high-level frameworks for the core concepts
- **Train fast** — toy problems that train in minutes, not hours
- **Visualize everything** — the plots are where intuition lives
- **Papers are gitignored** — large, re-downloadable. The download script is the source of truth.

## Customization

The `pyproject.toml` comes with `marimo`, `numpy`, `matplotlib` as base dependencies. Optional groups:

- `uv sync --dev --extra ml` — adds PyTorch
- `uv sync --dev --extra viz` — adds Plotly for interactive plots

Adjust to your topic — swap groups, add libraries, remove what you don't need.
