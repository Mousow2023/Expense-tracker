import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, usd

from datetime import datetime
now = datetime.now()

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///expense.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# List of potential categories
categories = [
    "Food & Dining",
    "Groceries",
    "Transportation",
    "Utilities",
    "Rent or Mortgage",
    " Health & Fitness",
    " Entertainment",
    "Travel",
    " Clothing",
    "Personal Care",
    " Education",
    "Gifts & Donations",
    "Home Improvement",
    "Insurance",
    "Taxes",
    "Electronics",
    "Pets",
    "Childcare",
    "Subscriptions",
    " Miscellaneous"
]

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # If the user reached route via POST
    if request.method == "POST":

        # Get form data
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Check if password meet all the requirements
        if not any(char.islower() for char in password):
            return apology("Password must contain at least one lowercase letter")

        if not any(char.isupper() for char in password):
            return apology("Password must contain at least one uppercase letter")

        if not any(not char.isalnum() for char in password):
            return apology("Password must contain at least one special character")

        if not any(char.isdigit() for char in password):
            return apology("Password must contain at least one digit")

        if len(password) < 8:
            return apology("Password must contain at least 8 character")

        # Unsure that password was confirmed
        if password != confirmation:
            return apology("Passwords do not match")

        # Check if the username already exists
        if len(db.execute("SELECT username FROM users WHERE username = ?", username)) != 0:
            return apology("Username already exists")

        # Insert the user into the users table
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, generate_password_hash(password))

        # Remember which user has registered in and log the user in
        session["user_id"] =  db.execute("SELECT id FROM users WHERE username = ?", username)[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # If the user reached route via GET
    else:
        return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    """return apology("TODO")"""
    # If user reached route via POST
    if request.method == "POST":

        # Ensure desciption is provided
        description = request.form.get("description")
        if not description:
            return apology("Missing description")
        if len(description) > 50:
            return apology("Description is too long")

        # Ensure amount is provided
        amount = request.form.get("amount").strip()
        if not amount:
            return apology("Missing amount")
        if not amount.isdigit():
            return apology("Amount must be number")
        amount = int(amount)
        if amount < 0:
            return apology("Amount must be a positive number")

        # Ensure category is provided
        category = request.form.get("category")
        if not category:
            return apology("Missing category")
        if category not in categories:
            return apology("invalid category")

        # Validate date
        input_date = request.form.get("date")

        if not input_date or not datetime.strptime(input_date, "%Y-%m-%d").date():
            date = now.strftime("%Y-%m-%d")
        else:
            date = datetime.strptime(input_date, "%Y-%m-%d").date()

        # Insert expense in date expense table
        db.execute("INSERT INTO expenses (user_id, description, amount, date, category) VALUES(?, ?, ?, ?, ?)", session["user_id"], description, amount, date, category)

        # Insert expense in date history table
        db.execute("INSERT INTO history (user_id, description, amount, expense_date, category) VALUES(?, ?, ?, ?, ?)", session["user_id"], description, amount, date, category)

        # Redirect user to the homepage
        return redirect("/")

    # If user reached route via GET
    else:
        return render_template("add.html", categories=categories)

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    # For all expenses of the user
    all_rows = db.execute("SELECT * FROM expenses WHERE user_id = ? ORDER BY date DESC", session["user_id"])

    user = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])

    username = user[0]["username"]
    if len(all_rows) == 0:
        return render_template("new.html", username=username)

    user = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
    username = user[0]["username"]


    # for the expenses by category
    rows = db.execute("SELECT category, SUM(amount) AS total_amount FROM expenses WHERE user_id = ? GROUP BY category", session["user_id"])

    total = db.execute("SELECT SUM(amount) AS total_expense FROM expenses WHERE user_id = ?", session["user_id"])
    total_expense = total[0]["total_expense"]

    return render_template("index.html", rows=rows, username=username, all_rows=all_rows, total_expense=total_expense)

@app.route("/delete", methods=["POST"])
@login_required
def delete():
    id = request.form.get("id")

    if id:
        db.execute("DELETE FROM expenses WHERE id = ?", id)

    return redirect("/")

@app.route("/reset", methods=["GET", "POST"])
def reset():

    # If user reached route via POST
    if request.method == "POST":
        old = request.form.get("old_password")
        new = request.form.get("new_password")
        confirmation = request.form.get("confirmation")

        # Select user infos
        user = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
        # Unsure old password is correct
        if not check_password_hash(user[0]["hash"], old):
            return apology("Password is incorrect")

        # Unsure new passoword is confirmed
        if new != confirmation:
            return apology("New passwords do not match!")

        # Check if password meet all the requirements
        if not any(char.islower() for char in new):
            return apology("Password must contain at least one lowercase letter")

        if not any(char.isupper() for char in new):
            return apology("Password must contain at least one uppercase letter")

        if not any(not char.isalnum() for char in new):
            return apology("Password must contain at least one special character")

        if not any(char.isdigit() for char in new):
            return apology("Password must contain at least one digit")

        if len(new) < 8:
            return apology("Password must contain at least 8 character")

        # Hash the new password
        new_password = generate_password_hash(new)

        # Change the new password in the databes
        db.execute("UPDATE users SET hash = ? WHERE id = ?", new_password, session["user_id"])

        # redirect user
        return render_template("reset_successful.html")

    return render_template("reset.html")

@app.route("/history")
def history():
    rows = db.execute("SELECT * FROM history WHERE user_id = ?", session["user_id"])

    user = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
    username = user[0]["username"]

    if len(rows) == 0:
        return render_template("new.html", username=username)

    return render_template("history.html", rows=rows)