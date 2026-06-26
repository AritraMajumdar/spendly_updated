import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "spendly.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    db = get_db()
    db.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            name          TEXT    NOT NULL,
            email         TEXT    NOT NULL UNIQUE,
            password_hash TEXT    NOT NULL,
            created_at    TEXT    DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS expenses (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL,
            amount      REAL    NOT NULL,
            category    TEXT    NOT NULL,
            date        TEXT    NOT NULL,
            description TEXT,
            created_at  TEXT    DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
    """)
    db.close()


def seed_db():
    from werkzeug.security import generate_password_hash

    db = get_db()
    if db.execute("SELECT COUNT(*) FROM users").fetchone()[0] == 0:
        db.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            ("Demo User", "demo@spendly.com", generate_password_hash("demo123")),
        )

        user = db.execute("SELECT id FROM users WHERE email='demo@spendly.com'").fetchone()
        sample_expenses = [
            (user[0], 250.00,  "Food",          "2026-06-20", "Lunch at canteen"),
            (user[0], 150.00,  "Transport",      "2026-06-21", "Auto to office"),
            (user[0], 1200.00, "Bills",          "2026-06-18", "Electricity bill"),
            (user[0], 899.00,  "Shopping",       "2026-06-22", "New headphones"),
            (user[0], 350.00,  "Entertainment",  "2026-06-23", "Movie night"),
            (user[0], 500.00,  "Health",         "2026-06-15", "Doctor consultation"),
            (user[0], 200.00,  "Other",          "2026-06-24", "Miscellaneous"),
            (user[0], 180.00,  "Food",           "2026-06-25", "Dinner with friends"),
        ]
        db.executemany(
            "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
            sample_expenses,
        )
        db.commit()
    db.close()
