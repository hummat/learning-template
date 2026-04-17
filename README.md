# Learning Template

Template for "explore topic X from scratch" repositories. Marimo notebooks + shared Python package + curated references.

Based on the pattern established in [diffusion-explorer](../diffusion-explorer/) and [material-explorer](../material-explorer/).

## What You Get

```
src/__PKG__/            # shared library — rename via init script
notebooks/              # Marimo notebooks, numbered by progression
references/
  papers/               # PDFs (gitignored, re-downloadable)
  blogs/                # markdown summaries + rendered blog PDFs (*.pdf gitignored)
references.md           # reading order + resource-to-notebook mapping
scripts/
  download_papers.py    # bulk arXiv PDF downloader
  download_blogs.py     # render blog posts / course pages to PDF (Chromium headless)
  init_project.py       # rename placeholders -> your names
docs/superpowers/
  specs/                # design specs (brainstorming output)
  plans/                # implementation plans (intent only, no reference code)
AGENTS.md               # agent context (CLAUDE.md, GEMINI.md are symlinks)
HANDOFF.md.template     # session-handoff skeleton; copy to HANDOFF.md (gitignored)
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
#    - Edit scripts/download_blogs.py with blog/course URLs
#    - Save blog summaries to references/blogs/

# 5. Install and start
uv sync --dev
python scripts/download_papers.py
python scripts/download_blogs.py   # needs `chromium` on PATH
uv run marimo edit notebooks/01_first_topic.py
```

## The Workflow

1. **Write a design spec.** What are you learning, why, and in what order? Save to `docs/superpowers/specs/`. This is the foundation.
2. **Curate references.** Phased reading order in `references.md` — one phase per notebook, with depth guidance. This is the learning plan.
3. **Download papers + blogs.** Add arXiv IDs to `scripts/download_papers.py` and URLs to `scripts/download_blogs.py`, run them. Local reference material lets session-one start with reading, not downloading.
4. **Save blog summaries.** One markdown file per blog in `references/blogs/`: URL, summary, "why this matters for the repo." The rendered PDF lives alongside.
5. **Write an implementation plan.** Break the spec into concrete steps. Save to `docs/superpowers/plans/`. **Intent and cell structure only — no full reference code.** See "Answer-key discipline" below.
6. **Build the shared library.** Reusable utilities in `src/`, tested with pytest — but only for modules that are genuinely testable (analytic limits, known invariants). Skip tests for visualization / data-loading / rasterization modules; verify those end-to-end in notebooks.
7. **Write notebooks.** One Marimo notebook per concept, numbered by progression. Import from the shared library, focus on narrative and visualization.

## Answer-Key Discipline

**Reference implementations do not live in this repo.** When you want to check your work against a known-correct version, the reference code goes at `~/.local/share/<repo-name>-answer-key/` — out-of-tree, on a full path that requires friction to open.

Why: "the code IS the learning artifact" fails the moment the answer is glanceable in the repo. A 1500-line implementation plan with complete code blocks is the same failure mode as an in-tree `answer-key/` directory — copy-pasting from either is the path of least resistance while "thinking." Physical distance protects the learning.

**Implementation plan style:** plans describe cell structure and algorithmic intent. They do NOT contain full reference implementations. A good plan tells you what the third cell of NB02 should accomplish, what analytic limit to test against, and what visualization to produce. It does not give you the `torch.autograd.grad(...)` line to copy.

## Session Handoffs

`HANDOFF.md.template` is a skeleton for end-of-session handoff notes. Copy to `HANDOFF.md` (gitignored) at session end and fill it in. The convention — Current State, Session Context, Next Steps, Do NOT, Key Files — is designed so a future fresh agent can pick up work without re-deriving this session's decisions.

## Conventions

- **Marimo over Jupyter** — reactive, pure `.py` files, clean git diffs, interactive widgets
- **Implement from scratch** — no high-level frameworks for the core concepts
- **Train fast** — toy problems that train in minutes, not hours
- **Visualize everything** — the plots are where intuition lives
- **Papers + rendered blog PDFs are gitignored** — large, re-downloadable. The download scripts are the source of truth.
- **Tests only where they catch bugs** — analytic limits yes, visual-output-verification no

## Customization

The `pyproject.toml` comes with `marimo`, `numpy`, `matplotlib` as base dependencies. Optional extras:

- `uv sync --dev --extra ml` — adds PyTorch
- `uv sync --dev --extra viz` — adds Plotly for interactive plots

Adjust to your topic — swap extras, add libraries, remove what you don't need.
