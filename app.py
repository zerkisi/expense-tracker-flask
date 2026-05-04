from flask import Flask, render_template, request, redirect, session, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db, close_db, init_db
from logic import validate_expense, calculate_total

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

        db = get_db()
        hashed_password = generate_password_hash(password)

        try:
            db.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, hashed_password),
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

    db = get_db()

    if category:
        expenses = db.execute(
            "SELECT * FROM expenses WHERE user_id = ? AND category = ? ORDER BY expense_date DESC",
            (session["user_id"], category),
        ).fetchall()
    else:
        expenses = db.execute(
            "SELECT * FROM expenses WHERE user_id = ? ORDER BY expense_date DESC",
            (session["user_id"],),
        ).fetchall()

    total = calculate_total(expenses)

    categories = db.execute(
        "SELECT DISTINCT category FROM expenses WHERE user_id = ?",
        (session["user_id"],),
    ).fetchall()

    return render_template(
        "dashboard.html",
        expenses=expenses,
        total=total,
        categories=categories,
        selected_category=category,
    )


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


if __name__ == "__main__":
    app.run(debug=True)