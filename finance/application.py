import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # Query database for current user cash amount
    cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])

    # Create grandTotal and money variables for later use
    grandTotal = cash[0]["cash"]
    money = cash[0]["cash"]

    # Query database for the symbols and shares that current user currently owns
    stocks = db.execute(
        "SELECT symbol, SUM(shares) FROM buy WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0",
        session["user_id"])

    # Create counter
    i = 0

    # Loop through stocks dictionary to acquire then input name, price, shares, and update grandTotal
    for stock in stocks:
        quote = lookup(stocks[i]["symbol"])
        stocks[i]["name"] = quote["name"]
        stocks[i]["price"] = quote["price"]
        stocks[i]["shares"] = stocks[i]["SUM(shares)"]
        value = stocks[i]["price"] * stocks[i]["SUM(shares)"]
        stocks[i]["value"] = value
        grandTotal = grandTotal + value
        i += 1

    # Render homepage passing in grandTotal, stocks dictionary, and user's current cash amount
    return render_template("index.html", grandTotal=grandTotal, stocks=stocks, money=money)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":

        # Ensure symbol is submitted
        if not request.form.get("symbol"):
            return apology("must provide symbol", 400)

        # Ensure shares is submitted and not less than 1
        elif not request.form.get("shares"):
            return apology("must provide shares", 400)

        # Create variable for the inputted shares
        shareValue = request.form.get("shares")

        # Ensure shares is a number
        if shareValue.isnumeric() == True:
            # Set share value to integer
            shareValue = int(shareValue)
            # Ensure shares is greater than 0
            if shareValue < 1:
                return apology("shares must be positive integer", 400)
        else:

            # If not numeric send apology
            return apology("shares must be positive integer", 400)

        # Lookup symbol submitted by user
        quote = lookup(request.form.get("symbol"))

        # Ensure quote exists
        if quote == None:
            return apology("symbol does not exist", 400)

        # Query database for current user's cash
        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        compare = cash[0]["cash"]

        # Get price and shares requested to calculate total cost
        shares = int(request.form.get("shares"))
        price = quote["price"]
        total = shares * price

        # Ensure user has sufficient cash amount to purchase shares
        if total > compare:
            return apology("insufficient funds", 400)
        else:
            # Update transactions database and update the user's cash amount
            insertion = db.execute("INSERT into buy (user_id, symbol, price, shares) VALUES (?, ?, ?, ?)",
                                    session["user_id"], quote["symbol"], quote["price"], shares)
            update = db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", total, session["user_id"])
            return redirect("/")
    else:

        # User reached route via GET (as by clicking a link or via redirect)
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # Query database for transactions and update history page based on all transactions
    transactions = db.execute("SELECT * FROM buy ORDER BY date")
    return render_template("history.html", transactions=transactions)


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

    else:

        # User reached route via GET (as by clicking a link or via redirect)
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "POST":

        # Ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide symbol", 400)

        # Lookup the symbol that the user submitted
        quote = lookup(request.form.get("symbol"))

        # Ensure quote exists
        if quote == None:
            return apology("symbol does not exist", 400)
        else:
            return render_template("quoted.html", quote=quote)

    else:

        # User reached route via GET (as by clicking a link or via redirect)
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":

        # Once all checks are passed, save username and hashed password into variables
        username = request.form.get("username")
        password = generate_password_hash(request.form.get("password"))

        # Query database for all existing usernames
        users = db.execute("SELECT username FROM users WHERE username = ?", username)

        # Ensure username is unique
        if users:
            return apology("username already exists", 400)

        # Ensure username was submitted
        elif not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure password was submitted again
        elif not request.form.get("confirmation"):
            return apology("must confirm password", 400)

        # Ensure passwords match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords must match", 400)

        # Create array of special characters
        special = ['$', '@', '#', '*', '&', '!']

        # Prescribe length, case, and special character requirements for password
        if len(request.form.get("password")) < 6:
            return apology("length should be at least 6")
        elif len(request.form.get("password")) > 15:
            return apology("length should be less than 15")
        elif not any(char.isdigit() for char in request.form.get("password")):
            return apology("password should contain at least one number")
        elif not any(char.isupper() for char in request.form.get("password")):
            return apology("password should contain at least one upper case letter")
        elif not any(char.islower() for char in request.form.get("password")):
            return apology('password should contain at least one lower case letter')
        elif not any(char in special for char in request.form.get("password")):
            return apology('password should contain at least one special character ($, @, #, *, &, !)')

        # Retrieve current user_id
        number = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, password)

        # Set session id to the user_id
        session["user_id"] = number

        # Redirect to index or homepage
        return redirect("/")

    else:

        # User reached route via GET (as by clicking a link or via redirect)
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    if request.method == "POST":

        # Ensure symbol is submitted
        if not request.form.get("symbol"):
            return apology("must provide symbol", 400)

        # Ensure shares is submitted and not less than 1
        elif not request.form.get("shares"):
            return apology("must provide shares", 400)

        # Get the requested shares and avaible shares
        shares = int(request.form.get("shares"))
        available = db.execute("SELECT SUM(shares) FROM buy WHERE user_id = ? AND symbol = ?",
                                session["user_id"], request.form.get("symbol"))

        # Check if available is correct
        if len(available) != 1:
            return apology("invalid number of shares", 400)

        # Query database for current cash amount
        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])

        # Get price -> calculate total cost of # of shares -> make negative because they're selling
        quote = lookup(request.form.get("symbol"))
        price = quote["price"]
        total = shares * price
        negativeShares = shares * -1

        # Make sure they have enough shares to sell
        if shares > available[0]["SUM(shares)"]:
            return apology("too many shares", 400)

        else:
            # Update database for transactions and user's cash amount
            db.execute("INSERT into buy (user_id, symbol, price, shares) VALUES (?, ?, ?, ?)",
                       session["user_id"], quote["symbol"], quote["price"], negativeShares)
            db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", total, session["user_id"])
            return redirect("/")

    else:
        # Query database for symbols of shares that user has purchased and update options to show these symbols
        symbols = db.execute("SELECT symbol from buy WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0", session["user_id"])
        return render_template("sell.html", symbols=symbols)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
