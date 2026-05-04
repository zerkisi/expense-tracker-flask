import csv
import io
from flask import Flask, render_template, request, redirect, session, url_for, flash, Response
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db, close_db, init_db
from logic import (
    validate_expense,
    calculate_total,
    calculate_average,
    count_expenses,
    calculate_category_totals,
    find_highest_expense,
    calculate_remaining_budget,
    is_over_budget,
)

app = Flask(__name__)
app.secret_key = "expense-tracker-secret-key"

app.teardown_appcontext(close_db)


@app.cli.command("init-db")
def init_db_command():
    init_db(app)
    print("Database initialized.")


@app.route("/")
def index():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if not username or not password:
            flash("Username and password are required.")
            return redirect(url_for("register"))

        if len(password) < 4:
            flash("Password must be at least 4 characters.")
            return redirect(url_for("register"))

        db = get_db()
        hashed_password = generate_password_hash(password)

        try:
            db.execute(
                "INSERT INTO users (username, password, monthly_budget) VALUES (?, ?, ?)",
                (username, hashed_password, 0),
            )
            db.commit()
        except:
            flash("Username already exists.")
            return redirect(url_for("register"))

        flash("Registration successful. Please login.")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,),
        ).fetchone()

        if user is None or not check_password_hash(user["password"], password):
            flash("Invalid username or password.")
            return redirect(url_for("login"))

        session.clear()
        session["user_id"] = user["id"]
        session["username"] = user["username"]

        return redirect(url_for("dashboard"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    category = request.args.get("category")
    search = request.args.get("search")

    db = get_db()

    query = "SELECT * FROM expenses WHERE user_id = ?"
    params = [session["user_id"]]

    if category:
        query += " AND category = ?"
        params.append(category)

    if search:
        query += " AND (title LIKE ? OR note LIKE ?)"
        params.append(f"%{search}%")
        params.append(f"%{search}%")

    query += " ORDER BY expense_date DESC"

    expenses = db.execute(query, params).fetchall()

    total = calculate_total(expenses)
    average = calculate_average(expenses)
    expense_count = count_expenses(expenses)
    category_totals = calculate_category_totals(expenses)
    highest_expense = find_highest_expense(expenses)

    user = db.execute(
        "SELECT monthly_budget FROM users WHERE id = ?",
        (session["user_id"],),
    ).fetchone()

    monthly_budget = user["monthly_budget"] if user else 0
    remaining_budget = calculate_remaining_budget(monthly_budget, total)
    over_budget = is_over_budget(monthly_budget, total)

    categories = db.execute(
        "SELECT DISTINCT category FROM expenses WHERE user_id = ?",
        (session["user_id"],),
    ).fetchall()

    return render_template(
        "dashboard.html",
        expenses=expenses,
        total=total,
        average=average,
        expense_count=expense_count,
        category_totals=category_totals,
        highest_expense=highest_expense,
        monthly_budget=monthly_budget,
        remaining_budget=remaining_budget,
        over_budget=over_budget,
        categories=categories,
        selected_category=category,
        search=search,
    )


@app.route("/budget", methods=["POST"])
def update_budget():
    if "user_id" not in session:
        return redirect(url_for("login"))

    monthly_budget = request.form["monthly_budget"]

    try:
        monthly_budget = float(monthly_budget)
        if monthly_budget < 0:
            flash("Budget cannot be negative.")
            return redirect(url_for("dashboard"))
    except:
        flash("Invalid budget amount.")
        return redirect(url_for("dashboard"))

    db = get_db()
    db.execute(
        "UPDATE users SET monthly_budget = ? WHERE id = ?",
        (monthly_budget, session["user_id"]),
    )
    db.commit()

    flash("Monthly budget updated.")
    return redirect(url_for("dashboard"))


@app.route("/add", methods=["GET", "POST"])
def add_expense():
    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        title = request.form["title"]
        amount = request.form["amount"]
        category = request.form["category"]
        expense_date = request.form["expense_date"]
        note = request.form["note"]

        valid, message = validate_expense(title, amount, category)

        if not valid:
            flash(message)
            return redirect(url_for("add_expense"))

        db = get_db()
        db.execute(
            """
            INSERT INTO expenses (user_id, title, amount, category, expense_date, note)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (session["user_id"], title, float(amount), category, expense_date, note),
        )
        db.commit()

        return redirect(url_for("dashboard"))

    return render_template("add_expense.html")


@app.route("/edit/<int:expense_id>", methods=["GET", "POST"])
def edit_expense(expense_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    db = get_db()

    expense = db.execute(
        "SELECT * FROM expenses WHERE id = ? AND user_id = ?",
        (expense_id, session["user_id"]),
    ).fetchone()

    if expense is None:
        flash("Expense not found.")
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        title = request.form["title"]
        amount = request.form["amount"]
        category = request.form["category"]
        expense_date = request.form["expense_date"]
        note = request.form["note"]

        valid, message = validate_expense(title, amount, category)

        if not valid:
            flash(message)
            return redirect(url_for("edit_expense", expense_id=expense_id))

        db.execute(
            """
            UPDATE expenses
            SET title = ?, amount = ?, category = ?, expense_date = ?, note = ?
            WHERE id = ? AND user_id = ?
            """,
            (title, float(amount), category, expense_date, note, expense_id, session["user_id"]),
        )
        db.commit()

        return redirect(url_for("dashboard"))

    return render_template("edit_expense.html", expense=expense)


@app.route("/delete/<int:expense_id>")
def delete_expense(expense_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    db = get_db()
    db.execute(
        "DELETE FROM expenses WHERE id = ? AND user_id = ?",
        (expense_id, session["user_id"]),
    )
    db.commit()

    return redirect(url_for("dashboard"))


@app.route("/export")
def export_expenses():
    if "user_id" not in session:
        return redirect(url_for("login"))

    db = get_db()
    expenses = db.execute(
        """
        SELECT title, amount, category, expense_date, note
        FROM expenses
        WHERE user_id = ?
        ORDER BY expense_date DESC
        """,
        (session["user_id"],),
    ).fetchall()

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(["Title", "Amount", "Category", "Date", "Note"])

    for expense in expenses:
        writer.writerow([
            expense["title"],
            expense["amount"],
            expense["category"],
            expense["expense_date"],
            expense["note"],
        ])

    response = Response(output.getvalue(), mimetype="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=expenses.csv"

    return response


if __name__ == "__main__":
    app.run(debug=True)