# Spec: Login and Logout

## Overview
Implements session-based authentication for Spendly: a working `POST /login` that verifies
credentials against the `users` table and starts a Flask session, and a working `/logout` that
clears it. Registration (Step 2) already creates accounts but does not sign anyone in, and the
`login.html` template already posts `email`/`password` to `/login` and expects an `error` variable.
This step wires that up and makes the site session-aware so the nav reflects whether a visitor is
signed in, laying the groundwork for the `/profile` (Step 4) and expense routes to require login.

## Depends on
- Step 1 (Database Setup) — `get_db()`, `init_db()`, and the `users` table.
- Step 2 (Registration) — accounts must exist to log into; `POST /register` already creates rows
  in `users` with `password_hash`.

## Routes
- `POST /login` — validate submitted email/password against `users`, start a session on success
  (redirect to `/`), or re-render `login.html` with an `error` message on failure — public
- `GET /login` — unchanged, already implemented
- `GET /logout` — clear the session and redirect to `/` (or `/login`) with a flashed confirmation —
  logged-in only (safe no-op if no session exists)

## Database changes
No database changes. The existing `users` table (id, name, email, password_hash) already supports
this feature.

## Templates
- **Create:** none
- **Modify:**
  - `templates/base.html` — make the nav session-aware: when `session.get("user_id")` is set, show
    a "Logout" link (`{{ url_for('logout') }}`) instead of "Login"/"Get started"
  - `templates/login.html` — no structural changes; already renders `error` and posts the correct
    fields to `/login`

## Files to change
- `app.py`
  - Replace the GET-only `/login` route with a route that accepts `GET` and `POST`; on POST, look
    up the user by email, verify the password with `check_password_hash`, and on success store
    `session["user_id"]` and `session["user_name"]`, then redirect to `/`
  - Replace the stub `/logout` route: clear the session (`session.clear()`), flash a confirmation,
    and redirect to `/` or `/login`
- `templates/base.html` — conditional nav block based on session state

## Files to create
None.

## New dependencies
No new dependencies (`werkzeug.security.check_password_hash` is already available alongside
`generate_password_hash`).

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug — verify with `check_password_hash`, never compare plaintext
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- On POST `/login`, validate server-side: email and password must be non-empty; if the email is not
  found or the password does not match, show one generic error (e.g. "Invalid email or password") —
  do not reveal whether the email exists
- Do not re-populate the password field on error; re-populating email is fine
- Use Flask's built-in session (`from flask import session`) — no custom cookies or tokens
- `GET /logout` must not error if no one is logged in — just redirect
- Close every DB connection you open (no leaked `sqlite3.Connection` objects)
- Do not implement `/profile` or route-protection decorators here — that is Step 4; this step only
  establishes and clears the session

## Definition of done
- [ ] Submitting `/login` with the seeded demo account (`demo@spendly.com` / `demo123`) redirects to
      `/` and the nav shows a "Logout" link instead of "Login"
- [ ] Submitting `/login` with a wrong password or unknown email re-renders `login.html` with a
      visible generic error and does not start a session
- [ ] Visiting `/logout` while logged in clears the session and redirects, and the nav reverts to
      showing "Login"/"Get started"
- [ ] Visiting `/logout` while logged out does not error (redirects cleanly)
- [ ] `GET /login` still renders the empty form as before
- [ ] App starts and runs with no errors (`python app.py`)
- [ ] No raw string interpolation is used in any SQL statement
