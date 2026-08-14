import os
import sqlite3
from datetime import date

from werkzeug.security import generate_password_hash

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "expense_tracker.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now'))
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT,
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """
    )
    conn.commit()
    conn.close()


def seed_db():
    conn = get_db()

    existing = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    if existing > 0:
        conn.close()
        return

    cursor = conn.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        ("Demo User", "demo@spendly.com", generate_password_hash("demo123")),
    )
    user_id = cursor.lastrowid

    today = date.today()
    month_prefix = today.strftime("%Y-%m")

    sample_expenses = [
        (user_id, 42.50, "Food", f"{month_prefix}-02", "Groceries"),
        (user_id, 15.00, "Transport", f"{month_prefix}-03", "Bus pass"),
        (user_id, 120.00, "Bills", f"{month_prefix}-05", "Electricity bill"),
        (user_id, 60.00, "Health", f"{month_prefix}-08", "Pharmacy"),
        (user_id, 25.75, "Entertainment", f"{month_prefix}-11", "Movie tickets"),
        (user_id, 89.99, "Shopping", f"{month_prefix}-14", "New shoes"),
        (user_id, 10.00, "Other", f"{month_prefix}-17", "Miscellaneous"),
        (user_id, 33.20, "Food", f"{month_prefix}-20", "Restaurant"),
    ]

    conn.executemany(
        """
        INSERT INTO expenses (user_id, amount, category, date, description)
        VALUES (?, ?, ?, ?, ?)
        """,
        sample_expenses,
    )

    conn.commit()
    conn.close()
