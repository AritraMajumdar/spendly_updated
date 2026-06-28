# Spec: Edit and Delete Expense

## Overview
Implement edit and delete for individual expenses. The edit route renders a pre-filled form
and processes updates. The delete route removes the expense row. Both routes must verify the
expense belongs to the logged-in user before acting — accessing another user's expense returns
a 403. The existing `GET /expenses/<id>/delete` stub must be replaced with a `POST` handler
invoked from an HTML form (no GET-based deletes).

## Depends on
- Step 01 — Database Setup (expenses table must exist)
- Step 05 — Expense List (list page must exist; both actions redirect back to it)
- Step 06 — Add Expense (edit form reuses the same field set and category list)

## Routes
- `GET /expenses/<int:id>/edit` — render pre-filled edit form — logged-in only, must own expense
- `POST /expenses/<int:id>/edit` — validate and update expense — logged-in only, must own expense
- `POST /expenses/<int:id>/delete` — delete expense — logged-in only, must own expense
  (replaces the existing `GET` stub — change decorator to `methods=["POST"]`)

## Database changes
No database changes.

## Templates
- **Create:** `templates/expenses/edit.html`
  - Extends `base.html`
  - Same fields as add form (amount, category, date, description) pre-populated with current values
  - Inline error display via `{% if error %}` / `.auth-error` pattern
  - Cancel button linking back to `/expenses`
- **Modify:** `templates/expenses/list.html`
  - Edit button: `<a href="{{ url_for('edit_expense', id=expense.id) }}">Edit</a>`
  - Delete button: `<form method="POST" action="{{ url_for('delete_expense', id=expense.id) }}">` with a submit button

## Files to change
- `app.py`
  - Replace `GET /expenses/<int:id>/edit` stub with `GET`/`POST` handler
  - Replace `GET /expenses/<int:id>/delete` stub with `POST`-only handler
- `templates/expenses/list.html` — wire up Edit links and Delete forms

## Files to create
- `templates/expenses/edit.html`

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs — use `get_db()` with raw `sqlite3` queries
- Parameterised queries only — never interpolate user input into SQL strings
- Ownership check: after fetching the expense by id, verify `expense["user_id"] == session["user_id"]`; return `abort(403)` if not
- Return 404 if the expense id does not exist (`fetchone()` returns `None`)
- Use CSS variables — never hardcode hex values in any new CSS
- All templates extend `base.html`
- Redirect unauthenticated users to `/login` via `url_for('login')`
- Use `url_for()` for all links and form actions — no hardcoded paths
- Delete must use `POST` — no `GET`-based deletes (CLAUDE.md requirement)
- On successful edit: `redirect(url_for('expense_list'))`
- On successful delete: `redirect(url_for('expense_list'))`
- Validation rules for edit are identical to add (positive amount, valid category, valid date)

## Definition of done
- [ ] `GET /expenses/<id>/edit` with no session redirects to `/login`
- [ ] `GET /expenses/<id>/edit` for an expense owned by the user renders a pre-filled form
- [ ] `GET /expenses/<id>/edit` for another user's expense returns 403
- [ ] `GET /expenses/<id>/edit` for a non-existent id returns 404
- [ ] `POST /expenses/<id>/edit` with valid data updates the row and redirects to `/expenses`
- [ ] `POST /expenses/<id>/edit` with invalid data re-renders the form with an error
- [ ] `POST /expenses/<id>/delete` removes the row and redirects to `/expenses`
- [ ] `POST /expenses/<id>/delete` for another user's expense returns 403
- [ ] Delete button in the list is a POST form, not a plain link
- [ ] The old `GET /expenses/<id>/delete` route no longer exists
