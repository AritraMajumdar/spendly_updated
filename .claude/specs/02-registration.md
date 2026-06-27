# Spec: Registration

## Overview
Implement the POST handler for `/register` so new users can create a Spendly account. The route already renders the form on GET; this step adds form processing: validate inputs, hash the password with werkzeug, insert the new user row, and redirect to the login page on success. Duplicate-email and short-password errors are surfaced via the existing `.auth-error` block in `register.html`.

## Depends on
Step 01 — Database Setup (users table must exist via `init_db()`).

## Routes
- `POST /register` — process registration form — public
  (The existing `GET /register` remains unchanged; the route decorator gains `methods=['GET', 'POST']`)

## Database changes
No database changes. The `users` table (id, name, email, password_hash, created_at) already exists from Step 01.

## Templates
- **Modify:** `templates/register.html`
  - Change `action="/register"` → `action="{{ url_for('register') }}"` (CLAUDE.md convention)

## Files to change
- `app.py` — extend `/register` to handle POST; add `request`, `redirect` to Flask imports
- `templates/register.html` — fix hardcoded form action to use `url_for()`

## Files to create
No new files.

## New dependencies
No new dependencies. `werkzeug.security` ships with Flask.

## Rules for implementation
- No SQLAlchemy or ORMs — use `get_db()` with raw `sqlite3` queries
- Parameterised queries only — never interpolate user input into SQL strings
- Hash passwords with `werkzeug.security.generate_password_hash`; never store plaintext
- Use CSS variables — never hardcode hex values in any new CSS
- All templates extend `base.html`
- Keep validation server-side; HTML `required` and `minlength` attributes are UI hints only
- Detect duplicate email via `sqlite3.IntegrityError` (the email column has a UNIQUE constraint)
- Minimum password length: 8 characters
- On success: `redirect(url_for('login'))`
- On error: `return render_template('register.html', error=<message>)`
- Do not implement login (POST /login) in this step

## Definition of done
- [ ] Visiting `/register` still renders the form (GET unchanged)
- [ ] Submitting the form with valid name, email, and password ≥ 8 chars creates a new row in `users` and redirects to `/login`
- [ ] Submitting with a missing field shows an `.auth-error` message (browser-level `required` catches this, but the route handles it defensively)
- [ ] Submitting with a password shorter than 8 characters shows an `.auth-error` message on the register page
- [ ] Submitting with an email that already exists shows an `.auth-error` message ("Email already registered")
- [ ] The registered user's password is stored as a hash (not plaintext) in `database/spendly.db`
- [ ] The form `action` uses `url_for('register')`, not a hardcoded string
