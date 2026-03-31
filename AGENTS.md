# __TOPIC__

Personal learning repo for understanding __TOPIC__ from scratch.

## Project Structure

```
src/__PKG__/              # shared library (reusable utilities across notebooks)
notebooks/                # Marimo notebooks (one per concept, numbered by progression)
references/               # papers (PDFs, gitignored) + blog summaries (markdown)
scripts/                  # download_papers.py and other utilities
docs/superpowers/specs/   # design specs
docs/superpowers/plans/   # implementation plans
```

## Key Docs

- **References + reading order:** `references.md`
- **Paper download script:** `scripts/download_papers.py`

## Notebook Progression

1. **NOTEBOOK_01** — ...
2. **NOTEBOOK_02** — ...
3. **NOTEBOOK_03** — ...

## Stack

- **Python 3.11+**, Marimo, Matplotlib, NumPy (PyTorch optional via `[ml]`)
- **uv** for dependency management, editable install
- No heavy frameworks — build from scratch

## Development Commands

```bash
uv sync --dev                              # install deps
uv run pytest -v                           # run tests
uv run marimo edit notebooks/01_topic.py   # open notebook
uv run ruff check src/ tests/              # lint
python scripts/download_papers.py          # download papers
python scripts/init_project.py <pkg> "<description>"  # initialize from template
```

## Philosophy

This is a learning repo. The code IS the learning artifact. Implement from scratch, annotate heavily, visualize everything.
