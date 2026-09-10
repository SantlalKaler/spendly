from datetime import datetime

from flask import Flask, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from database.db import get_db, init_db, seed_db

app = Flask(__name__)
app.secret_key = "spendly-dev-secret"

with app.app_context():
    init_db()
    seed_db()


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if session.get("user_id"):
        return redirect(url_for("landing"))

    if request.method == "GET":
        return render_template("register.html")

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    if not name:
        return render_template("register.html", error="Full name is required.", name=name, email=email)
    if not email or "@" not in email:
        return render_template("register.html", error="A valid email address is required.", name=name, email=email)
    if len(password) < 8:
        return render_template("register.html", error="Password must be at least 8 characters.", name=name, email=email)

    conn = get_db()
    existing = conn.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone()
    if existing:
        conn.close()
        return render_template(
            "register.html",
            error="An account with that email already exists.",
            name=name,
            email=email,
        )

    conn.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        (name, email, generate_password_hash(password)),
    )
    conn.commit()
    conn.close()

    flash("Account created! Please sign in.", "success")
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect(url_for("profile"))

    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    conn = get_db()
    user = conn.execute("SELECT id, name, password_hash FROM users WHERE email = ?", (email,)).fetchone()
    conn.close()

    if not email or not password or user is None or not check_password_hash(user["password_hash"], password):
        return render_template("login.html", error="Invalid email or password.")

    session["user_id"] = user["id"]
    session["user_name"] = user["name"]
    return redirect(url_for("profile"))


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("login"))


def _profile_transactions(user_id):
    """Subagent 1: recent transaction history for the profile page."""
    conn = get_db()
    rows = conn.execute(
        "SELECT date, description, category, amount FROM expenses "
        "WHERE user_id = ? ORDER BY date DESC, id DESC LIMIT 10",
        (user_id,),
    ).fetchall()
    conn.close()

    transactions = []
    for row in rows:
        d = datetime.strptime(row["date"], "%Y-%m-%d")
        date_str = f"{d.strftime('%b')} {d.day}, {d.year}"
        transactions.append(
            {
                "date": date_str,
                "description": row["description"],
                "category": row["category"],
                "amount": float(row["amount"]),
            }
        )
    return transactions


def _profile_stats(user_id):
    """Subagent 2: summary stats for the profile page."""
    conn = get_db()
    totals_row = conn.execute(
        "SELECT COALESCE(SUM(amount), 0) AS total, COUNT(*) AS cnt FROM expenses WHERE user_id = ?",
        (user_id,),
    ).fetchone()
    top_row = conn.execute(
        "SELECT category, SUM(amount) AS total FROM expenses WHERE user_id = ? "
        "GROUP BY category ORDER BY total DESC, category ASC LIMIT 1",
        (user_id,),
    ).fetchone()
    conn.close()

    top_category = top_row["category"] if top_row is not None else "No expenses yet"

    return {
        "total_spent": float(totals_row["total"]),
        "expense_count": int(totals_row["cnt"]),
        "top_category": top_category,
    }


def _profile_categories(user_id):
    """Subagent 3: category breakdown for the profile page."""
    conn = get_db()
    rows = conn.execute(
        "SELECT category, SUM(amount) AS total FROM expenses WHERE user_id = ? "
        "GROUP BY category ORDER BY total DESC",
        (user_id,),
    ).fetchall()
    conn.close()

    if not rows:
        return []

    max_total = rows[0]["total"]
    buckets = [100, 75, 35, 20]
    categories = []
    for row in rows:
        pct = (row["total"] / max_total) * 100
        closest = min(buckets, key=lambda b: abs(b - pct))
        categories.append(
            {
                "name": row["category"],
                "amount": float(row["total"]),
                "width_class": f"bar-w-{closest}",
            }
        )
    return categories


@app.route("/profile")
def profile():
    if not session.get("user_id"):
        return redirect(url_for("login"))

    user_id = session["user_id"]
    conn = get_db()
    row = conn.execute(
        "SELECT name, email, created_at FROM users WHERE id = ?", (user_id,)
    ).fetchone()
    conn.close()

    member_since = datetime.strptime(row["created_at"], "%Y-%m-%d %H:%M:%S").strftime("%B %Y")
    user = {"name": row["name"], "email": row["email"], "member_since": member_since}

    stats = _profile_stats(user_id)
    transactions = _profile_transactions(user_id)
    categories = _profile_categories(user_id)

    return render_template(
        "profile.html",
        user=user,
        stats=stats,
        transactions=transactions,
        categories=categories,
    )


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    app.run(debug=True, port=5001)
