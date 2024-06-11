import os
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helper import login_required

import Queries as q

# Initialize Flask app
app = Flask(__name__)

# Enable debug mode
app.config["DEBUG"] = True

# Create a connection to the SQLite database
db = q.create_connection("app_database.db")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route('/', methods=['GET'])
def index():
    """Render the index page."""
    return render_template("index.html")


@app.route('/credit', methods=['GET', 'POST'])
def credit():
    """Handle credit transactions."""
    if request.method == 'POST':
        user_id = session["user_id"]

        # Fetch current balance
        users_balance = "SELECT balance FROM users WHERE id = :user_id"
        rows = q.sql_select_query(db, users_balance, dict(user_id=user_id))
        balance = rows[0][0] + float(request.form.get("amount"))

        # Insert credit transaction
        type_of_transaction = "C"
        sql_query = """
        INSERT INTO transactions (user_id, reason, type, amount)
        VALUES (:user_id, :reason, :type, :amount)
        """
        variable = dict(
            user_id=session["user_id"],
            reason=request.form.get("about"),
            type=type_of_transaction,
            amount=request.form.get("amount")
        )
        q.sql_insert_query(db, sql_query, variable)

        # Update user balance
        sql_query = "UPDATE users SET balance = :balance WHERE id = :user_id"
        variable = dict(balance=balance, user_id=user_id)
        q.sql_insert_query(db, sql_query, variable)

    return redirect("/transaction")


@app.route('/debit', methods=['GET', 'POST'])
def debit():
    """Handle debit transactions."""
    if request.method == 'POST':
        user_id = session["user_id"]
        amount = float(request.form.get("amount"))

        # Fetch current balance
        users_balance = "SELECT balance FROM users WHERE id = :user_id"
        rows = q.sql_select_query(db, users_balance, dict(user_id=user_id))
        balance = rows[0][0]
        balance -= amount

        # Insert debit transaction
        type_of_transaction = "D"
        sql_query = """
        INSERT INTO transactions (user_id, reason, type, amount)
        VALUES (:user_id, :reason, :type, :amount)
        """
        variable = dict(
            user_id=session["user_id"],
            reason=request.form.get("about"),
            type=type_of_transaction,
            amount=amount
        )
        q.sql_insert_query(db, sql_query, variable)

        # Update user balance
        sql_query = "UPDATE users SET balance = :balance WHERE id = :user_id"
        variable = dict(balance=balance, user_id=user_id)
        q.sql_insert_query(db, sql_query, variable)

    return redirect("/transaction")


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if request.method == 'POST':
        username = request.form.get("username")
        pd = request.form.get("password")

        # Fetch user data
        sql_query = "SELECT * FROM users WHERE uname = :username"
        rows = q.sql_select_query(db, sql_query, dict(username=username))

        if len(rows) < 1:
            flash("Username does not exist", 'error')
        else:
            user_password = rows[0]["password"]

            # Check password
            if not check_password_hash(user_password, pd):
                flash("Incorrect Password", 'error')
            else:
                session["user_id"] = rows[0]["id"]
                return redirect("/")

    return render_template("login.html")


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    """Handle user logout."""
    session.clear()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration."""
    if request.method == 'POST':
        username = request.form.get("username")

        # Check if user already exists
        sql_query = "SELECT uname FROM users WHERE uname = :username"
        rows = q.sql_select_query(db, sql_query, dict(username=username))

        if len(rows) > 0:
            flash("User already exists")
            return render_template("register.html")

        # Check if passwords match
        if request.form.get("password") != request.form.get("confirmPassword"):
            flash("Passwords do not match")
            return render_template("register.html")

        # Insert new user
        sql_query = "INSERT INTO users (uname, password) VALUES (:username, :password)"
        q.sql_insert_query(db, sql_query, dict(
            username=username,
            password=generate_password_hash(request.form.get("password"))
        ))
        return redirect("/")

    return render_template("register.html")


@app.route('/statement', methods=['GET'])
@login_required
def statement():
    """Display user transaction statement."""
    sql_query = "SELECT * FROM transactions WHERE user_id = :user_id"
    variable = dict(user_id=session["user_id"])
    rows = q.sql_select_query(db, sql_query, variable)

    # Fetch user balance
    row = q.sql_select_query(db, "SELECT balance FROM users WHERE id = :id", dict(id=session["user_id"]))
    balance = row[0][0]

    return render_template("statement.html", records=rows, balance=balance)


@app.route('/transaction', methods=['GET', 'POST'])
@login_required
def transaction():
    """Render transaction page."""
    return render_template("transaction.html")


if __name__ == '__main__':
    app.run()
