# Spec: Expense List

## Overview
Add a `/expenses` route that displays all expenses belonging to the logged-in user in a
table, ordered by date descending. This is the core read view of the app — the page users
land on after logging in to see where their money has gone. It also shows a total spend
summary at the top and provides entry points to add, edit, and delete expenses.

## Depends on
- Step 01 — Database Setup (expenses table must exist)
- Step 02 — Registration (user must exist)
- Step 03 — Login (session-based auth must work)

## Routes
- `GET /expenses` — list all expenses for the logged-in user, ordered by date desc — logged-in only

## Database changes
No database changes. The `expenses` table (id, user_id, amount, category, date,
description, created_at) already exists from Step 01.

## Templates
- **Create:** `templates/expenses/list.html`
  - Extends `base.html`
  - Summary card: total spend (sum of all amounts)
  - Table columns: Date, Category, Description, Amount (₹)
  - Each row has placeholder Edit and Delete buttons (links for now; wired up in Step 07)
  - "Add Expense" button linking to `/expenses/add`
  - Empty state message when user has no expenses

## Files to change
- `app.py` — add `GET /expenses` route; redirect to `/login` if not logged in

## Files to create
- `templates/expenses/list.html`
- `static/css/expenses.css` — page-specific styles loaded via `{% block head %}`

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs — use `get_db()` with raw `sqlite3` queries
- Parameterised queries only — never interpolate user input into SQL strings
- Filter expenses by `user_id = session["user_id"]` — never expose other users' data
- Use CSS variables — never hardcode hex values in any new CSS
- All templates extend `base.html`
- Redirect unauthenticated users to `/login` via `url_for('login')`
- Use `url_for()` for all links — no hardcoded paths in templates
- Amount display: prefix with ₹ and format to 2 decimal places

## Definition of done
- [ ] `GET /expenses` with no session redirects to `/login`
- [ ] `GET /expenses` while logged in renders the expense list page
- [ ] All expenses belonging to the logged-in user appear in the table, ordered by date descending
- [ ] Expenses from other users do not appear
- [ ] Total spend is correctly summed and displayed
- [ ] An empty state message is shown when the user has no expenses
- [ ] "Add Expense" button is visible and links to `/expenses/add`
- [ ] Each row has Edit and Delete placeholders
