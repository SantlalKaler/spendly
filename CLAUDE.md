# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

"Spendly" — a Flask expense tracker built as a step-by-step learning project. The codebase is
intentionally incomplete: routes and modules exist as stubs with comments describing what to build
in each numbered "Step" (see `app.py` and `database/db.py`). When asked to implement a feature, check
for an existing stub/comment first and follow its intended shape rather than redesigning from scratch.

## Commands

Two virtualenvs exist at the repo root (`venv/` and `.venv/`) — either works, but use whichever already
has dependencies installed (check with `pip list`) rather than creating a third.

```bash
# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the dev server (http://127.0.0.1:5001)
python app.py

# Run tests (pytest + pytest-flask are installed; no tests exist yet)
pytest
pytest path/to/test_file.py::test_name   # single test
```

There is no lint/format tooling configured in this repo.

## Architecture

- **`app.py`** — single-file Flask app; all routes are defined here directly on a module-level `app`
  instance (no blueprints, no app factory). Templates are rendered via `render_template`.
- **`database/db.py`** — intended to hold `get_db()` (SQLite connection with `row_factory` and foreign
  keys enabled), `init_db()` (idempotent `CREATE TABLE IF NOT EXISTS` schema), and `seed_db()` (dev
  sample data). Currently unimplemented — this is the Step 1 task. The DB file is `expense_tracker.db`
  (gitignored, created at runtime, not committed).
- **`templates/`** — Jinja2 templates. `base.html` defines the shared shell (nav, footer, block
  structure: `title`, `head`, `content`, `scripts`) that every page extends. Auth pages (`login.html`,
  `register.html`) already have complete forms (POSTing to `/login` and `/register`) and expect an
  `error` template variable for validation feedback — the backing POST handlers are not yet written.
- **`static/`** — one global stylesheet (`style.css`) and one JS entrypoint (`main.js`, currently
  empty) shared across all pages; no per-page or component-scoped assets.

## Route status (as of last read)

Implemented (GET, template render only): `/`, `/register`, `/login`, `/terms`, `/privacy`.

Stubbed placeholders returning plain strings, to be implemented in later steps: `/logout` (Step 3),
`/profile` (Step 4), `/expenses/add` (Step 7), `/expenses/<id>/edit` (Step 8), `/expenses/<id>/delete`
(Step 9). `/register` and `/login` also need POST handling (currently GET-only, despite the templates
having forms).
