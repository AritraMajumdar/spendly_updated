# Spec: Add Expense

## Overview
Implement the `/expenses/add` route so logged-in users can log a new expense. The GET
renders a form with fields for amount, category, date, and description. The POST validates
the input, inserts a row into the `expenses` table tied to the current user, and redirects
to the expense list on success. Validation errors are surfaced inline on the form.

## Depends on
- Step 01 — Database Setup (expenses table must exist)
- Step 05 — Expense List (`/expenses` must exist to redirect to on success)

## Routes
- `GET /expenses/add` — render add-expense form — logged-in only
- `POST /expenses/add` — validate and insert new expense, redirect to `/expenses` — logged-in only

## Database changes
No database changes. The `expenses` table already exists from Step 01.

## Templates
- **Create:** `templates/expenses/add.html`
  - Extends `base.html`
  - Form fields: Amount (number, required), Category (select, required), Date (date, required), Description (text, optional)
  - Category options: Food, Transport, Bills, Shopping, Entertainment, Health, Other
  - Inline error display following the `{% if error %}` / `.auth-error` pattern from login/register
  - Cancel button linking back to `/expenses`
- **Modify:** `templates/expenses/list.html`
  - "Add Expense" button href should already use `url_for('add_expense')` — verify it does

## Files to change
- `app.py` — replace `GET /expenses/add` stub with full `GET`/`POST` handler

## Files to create
- `templates/expenses/add.html`

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs — use `get_db()` with raw `sqlite3` queries
- Parameterised queries only — never interpolate user input into SQL strings
- Always set `user_id = session["user_id"]` — never trust a user-supplied user_id
- Use CSS variables — never hardcode hex values in any new CSS
- All templates extend `base.html`
- Redirect unauthenticated users to `/login` via `url_for('login')`
- Use `url_for()` for all links and redirects — no hardcoded paths
- Validation rules:
  - Amount: required, must be a positive number
  - Category: required, must be one of the allowed values
  - Date: required, must be a valid date string (YYYY-MM-DD)
  - Description: optional, store empty string if blank
- On success: `redirect(url_for('expense_list'))`
- On error: re-render form with `error=<message>` and preserve submitted values

## Definition of done
- [ ] `GET /expenses/add` with no session redirects to `/login`
- [ ] `GET /expenses/add` while logged in renders the add-expense form
- [ ] Submitting with valid data inserts a row in `expenses` with the correct `user_id` and redirects to `/expenses`
- [ ] Submitting with a missing amount shows an inline error
- [ ] Submitting with a missing category shows an inline error
- [ ] Submitting with a missing date shows an inline error
- [ ] Submitting with a non-positive amount shows an inline error
- [ ] The newly added expense appears in the expense list after redirect
