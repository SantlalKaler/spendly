# Spec: Registration

## Overview
Implements the POST handler for `/register` so a visitor can actually create a Spendly account.
The `register.html` template and its form already exist (`name`, `email`, `password` fields posting
to `/register`) but the route only handles GET today. This step adds server-side validation, duplicate
email handling, and account creation, then show a success message and sends the new user to `/login` to sign in. It does not add
sessions or log the user in automatically — that belongs to a future Login/session step.

## Depends on
Step 1 (Database Setup) — requires `get_db()`, `init_db()`, and the `users` table (id, name, email,
password_hash, created_at) to already exist and be working.

## Routes
- `POST /register` — validate submitted name/email/password, create the user, redirect to `/login` on
  success or re-render `register.html` with an `error` message on failure — public
- `GET /register` — unchanged, already implemented

## Database changes
No database changes. The existing `users` table (with its `UNIQUE` constraint on `email`) already
supports this feature.

## Templates
- **Create:** none
- **Modify:** none — `templates/register.html` already renders the `error` variable and posts the
  correct fields to `/register`; no template changes are required

## Files to change
- `app.py` — replace the GET-only `/register` route with a route that accepts `GET` and `POST`;
  on POST, validate input, insert the user via `get_db()`, handle duplicate-email failures, and
  redirect to `/login` on success

## Files to create
None.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug (`generate_password_hash`)
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Validate server-side even though the form has `required` attributes: name and email must be
  non-empty (after `.strip()`), email must contain `@`, password must be at least 8 characters
- On any validation failure, re-render `register.html` with `error` set and re-populate `name`/`email`
  into the form so the user doesn't retype everything (do not re-populate password)
- Catch the duplicate-email case explicitly (`sqlite3.IntegrityError` or a pre-check `SELECT`) and show
  a clear error such as "An account with that email already exists" — never let the exception crash
  the request
- Do not create a session or log the user in on success — this step ends with `redirect(url_for("login"))`
- Close every DB connection you open (no leaked `sqlite3.Connection` objects)

## Definition of done
- [ ] Submitting the register form with valid, unique data creates a row in `users` with a hashed
      password (verify via sqlite browser or a quick `SELECT`) and redirects to `/login`
- [ ] Submitting with an email that already exists (e.g. `demo@spendly.com`) re-renders `register.html`
      with a visible error and does not create a duplicate row
- [ ] Submitting with a missing name, invalid email, or password under 8 characters re-renders
      `register.html` with a visible error and does not create a row
- [ ] `GET /register` still renders the empty form as before
- [ ] App starts and runs with no errors (`python app.py`)
- [ ] No raw string interpolation is used in any SQL statement
