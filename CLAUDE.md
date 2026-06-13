# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Spendly is a personal expense tracker (Flask + SQLite + Jinja2 + vanilla CSS/JS), built incrementally as a learning project. Run with `python app.py` — serves on **port 5001** (non-default, intentional, matches README).

## Architecture

- Single-file Flask app (`app.py`), no blueprints or app factory.
- `app.py` placeholder routes (`/logout`, `/profile`, `/expenses/...`) return raw strings tagged "coming in Step N" — these correspond to checklist items in README.md. When implementing one, replace the placeholder with a real route/template **and** check off the matching item in the README.
- No ORM — DB access is raw `sqlite3`. `database/db.py` is currently an empty stub; it must expose:
  - `get_db()` — SQLite connection with `row_factory` set and foreign keys enabled
  - `init_db()` — `CREATE TABLE IF NOT EXISTS` schema
  - `seed_db()` — sample data
- Templates extend `base.html` and use its blocks: `title`, `head`, `content`, `scripts`.
- Currency throughout the UI is ₹ (INR).

## Conventions

- Use `url_for()` for route links/redirects in templates and Python (existing `login.html`/`register.html` forms hardcode `action="/login"` etc. — don't copy that pattern for new code).
- Login/register templates check `{% if error %}` and render an `.auth-error` div — follow this pattern when a route needs to surface a form error.

## Workflow

- Implement requested features end-to-end (routes, DB, templates) rather than leaving them as exercises.
- No test suite exists yet (despite `pytest`/`pytest-flask` in requirements.txt) — don't add tests unless asked.
