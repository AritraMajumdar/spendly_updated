import os
import sqlite3

from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from database.db import get_db, init_db, seed_db

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-fallback-key")


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #


@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    name     = request.form.get("name", "").strip()
    email    = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    if not name or not email or not password:
        return render_template("register.html", error="All fields are required.")
    if len(password) < 8:
        return render_template("register.html", error="Password must be at least 8 characters.")

    try:
        db = get_db()
        db.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            (name, email, generate_password_hash(password)),
        )
        db.commit()
        db.close()
    except sqlite3.IntegrityError:
        return render_template("register.html", error="Email already registered.")

    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    email    = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    if not email or not password:
        return render_template("login.html", error="Email and password are required.")

    db   = get_db()
    user = db.execute(
        "SELECT id, name, password_hash FROM users WHERE email = ?", (email,)
    ).fetchone()
    db.close()

    if user is None or not check_password_hash(user["password_hash"], password):
        return render_template("login.html", error="Invalid email or password.")

    session["user_id"]   = user["id"]
    session["user_name"] = user["name"]
    return redirect(url_for("landing"))


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("landing"))


@app.route("/profile", methods=["GET", "POST"])
def profile():
    if not session.get("user_id"):
        return redirect(url_for("login"))

    db   = get_db()
    user = db.execute(
        "SELECT id, name, email, created_at FROM users WHERE id = ?",
        (session["user_id"],),
    ).fetchone()

    if request.method == "GET":
        db.close()
        return render_template("profile.html", user=user)

    action = request.form.get("action")

    if action == "update_info":
        name  = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        if not name or not email:
            db.close()
            return render_template("profile.html", user=user,
                                   info_error="Name and email are required.")
        try:
            db.execute(
                "UPDATE users SET name = ?, email = ? WHERE id = ?",
                (name, email, session["user_id"]),
            )
            db.commit()
            session["user_name"] = name
            user = db.execute(
                "SELECT id, name, email, created_at FROM users WHERE id = ?",
                (session["user_id"],),
            ).fetchone()
            db.close()
            return render_template("profile.html", user=user,
                                   info_success="Profile updated.")
        except sqlite3.IntegrityError:
            db.close()
            return render_template("profile.html", user=user,
                                   info_error="That email is already in use.")

    if action == "change_password":
        current  = request.form.get("current_password", "")
        new_pw   = request.form.get("new_password", "")
        confirm  = request.form.get("confirm_password", "")
        pw_row   = db.execute(
            "SELECT password_hash FROM users WHERE id = ?", (session["user_id"],)
        ).fetchone()
        if not check_password_hash(pw_row["password_hash"], current):
            db.close()
            return render_template("profile.html", user=user,
                                   pw_error="Current password is incorrect.")
        if len(new_pw) < 8:
            db.close()
            return render_template("profile.html", user=user,
                                   pw_error="New password must be at least 8 characters.")
        if new_pw != confirm:
            db.close()
            return render_template("profile.html", user=user,
                                   pw_error="Passwords do not match.")
        db.execute(
            "UPDATE users SET password_hash = ? WHERE id = ?",
            (generate_password_hash(new_pw), session["user_id"]),
        )
        db.commit()
        db.close()
        return render_template("profile.html", user=user,
                               pw_success="Password updated successfully.")

    db.close()
    return redirect(url_for("profile"))


@app.route("/expenses")
def expense_list():
    if not session.get("user_id"):
        return redirect(url_for("login"))

    db       = get_db()
    expenses = db.execute(
        "SELECT id, amount, category, date, description FROM expenses "
        "WHERE user_id = ? ORDER BY date DESC",
        (session["user_id"],),
    ).fetchall()
    total = sum(e["amount"] for e in expenses)
    db.close()

    return render_template("expenses/list.html", expenses=expenses, total=total)


EXPENSE_CATEGORIES = [
    "Food", "Transport", "Bills", "Shopping", "Entertainment", "Health", "Other"
]


@app.route("/expenses/add", methods=["GET", "POST"])
def add_expense():
    if not session.get("user_id"):
        return redirect(url_for("login"))

    if request.method == "GET":
        return render_template("expenses/add.html", categories=EXPENSE_CATEGORIES)

    amount      = request.form.get("amount", "").strip()
    category    = request.form.get("category", "").strip()
    date        = request.form.get("date", "").strip()
    description = request.form.get("description", "").strip()

    def bad(msg):
        return render_template(
            "expenses/add.html",
            categories=EXPENSE_CATEGORIES,
            error=msg,
            form={"amount": amount, "category": category, "date": date, "description": description},
        )

    if not amount:
        return bad("Amount is required.")
    try:
        amount_f = float(amount)
        if amount_f <= 0:
            raise ValueError
    except ValueError:
        return bad("Amount must be a positive number.")
    if not category or category not in EXPENSE_CATEGORIES:
        return bad("Please select a valid category.")
    if not date:
        return bad("Date is required.")

    db = get_db()
    db.execute(
        "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
        (session["user_id"], amount_f, category, date, description),
    )
    db.commit()
    db.close()

    return redirect(url_for("expense_list"))


@app.route("/expenses/<int:id>/edit", methods=["GET", "POST"])
def edit_expense(id):
    if not session.get("user_id"):
        return redirect(url_for("login"))

    db      = get_db()
    expense = db.execute(
        "SELECT id, user_id, amount, category, date, description FROM expenses WHERE id = ?", (id,)
    ).fetchone()

    if expense is None:
        db.close()
        return "Expense not found.", 404
    if expense["user_id"] != session["user_id"]:
        db.close()
        return "Forbidden.", 403

    if request.method == "GET":
        db.close()
        return render_template("expenses/edit.html", expense=expense, categories=EXPENSE_CATEGORIES)

    amount      = request.form.get("amount", "").strip()
    category    = request.form.get("category", "").strip()
    date        = request.form.get("date", "").strip()
    description = request.form.get("description", "").strip()

    def bad(msg):
        return render_template(
            "expenses/edit.html",
            expense=expense,
            categories=EXPENSE_CATEGORIES,
            error=msg,
            form={"amount": amount, "category": category, "date": date, "description": description},
        )

    if not amount:
        return bad("Amount is required.")
    try:
        amount_f = float(amount)
        if amount_f <= 0:
            raise ValueError
    except ValueError:
        return bad("Amount must be a positive number.")
    if not category or category not in EXPENSE_CATEGORIES:
        return bad("Please select a valid category.")
    if not date:
        return bad("Date is required.")

    db.execute(
        "UPDATE expenses SET amount = ?, category = ?, date = ?, description = ? WHERE id = ?",
        (amount_f, category, date, description, id),
    )
    db.commit()
    db.close()

    return redirect(url_for("expense_list"))


@app.route("/expenses/<int:id>/delete", methods=["POST"])
def delete_expense(id):
    if not session.get("user_id"):
        return redirect(url_for("login"))

    db      = get_db()
    expense = db.execute(
        "SELECT user_id FROM expenses WHERE id = ?", (id,)
    ).fetchone()

    if expense is None:
        db.close()
        return "Expense not found.", 404
    if expense["user_id"] != session["user_id"]:
        db.close()
        return "Forbidden.", 403

    db.execute("DELETE FROM expenses WHERE id = ?", (id,))
    db.commit()
    db.close()

    return redirect(url_for("expense_list"))


with app.app_context():
    init_db()
    seed_db()

if __name__ == "__main__":
    app.run(debug=True, port=5001)
