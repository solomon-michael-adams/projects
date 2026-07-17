import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, usd

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
db = SQL("sqlite:///sneakster.db")


@app.route("/")
@login_required
def index():
    """Show profile of sneakers"""

    # Acquires sneakers and info for the users wishlist, purchases, and favorites
    wishlists = db.execute("SELECT * FROM sneakers WHERE id IN (SELECT shoe_id FROM profile WHERE wishlist = 'true' AND user_id = ?)", session["user_id"])
    purchases = db.execute("SELECT * FROM sneakers WHERE id IN (SELECT shoe_id FROM profile WHERE purchased = 'true' AND user_id = ?)", session["user_id"])
    tops = db.execute("SELECT * FROM sneakers WHERE id IN (SELECT shoe_id FROM profile WHERE top = 'true' AND user_id = ?)", session["user_id"])

    # Render homepage
    return render_template("index.html", wishlists=wishlists, purchases=purchases, tops=tops)


@app.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    """Remove sneakers from wishlist, purchased, or favorites"""

    if request.method == "POST":

        # Acquires sneakers and info for the users wishlist, purchases, and favorites
        wishlists = db.execute("SELECT * FROM sneakers WHERE id IN (SELECT shoe_id FROM profile WHERE wishlist = 'true' AND user_id = ?)", session["user_id"])
        purchases = db.execute("SELECT * FROM sneakers WHERE id IN (SELECT shoe_id FROM profile WHERE purchased = 'true' AND user_id = ?)", session["user_id"])
        tops = db.execute("SELECT * FROM sneakers WHERE id IN (SELECT shoe_id FROM profile WHERE top = 'true' AND user_id = ?)", session["user_id"])

        # Changes booleans to false so they are no longer displayed in favorites, purchased, or wishlist
        for top in tops:
            x = top["id"]
            y = "t" + str(x)
            z = request.form.get(y)
            if z == "true":
                db.execute("UPDATE profile SET top = 'false' WHERE user_id = ? AND shoe_id = ?", session["user_id"], x)

        for wishlist in wishlists:
            x = wishlist["id"]
            y = "w" + str(x)
            z = request.form.get(y)
            if z == "true":
                db.execute("UPDATE profile SET wishlist = 'false' WHERE user_id = ? AND shoe_id = ?", session["user_id"], x)

        for purchase in purchases:
            x = purchase["id"]
            y = "p" + str(x)
            z = request.form.get(y)
            if z == "true":
                db.execute("UPDATE profile SET purchased = 'false' WHERE user_id = ? AND shoe_id = ?", session["user_id"], x)

        # Redirect to index or homepage
        return redirect("/")

    else:

        # Acquires sneakers and info for the users wishlist, purchases, and favorites
        wishlists = db.execute("SELECT * FROM sneakers WHERE id IN (SELECT shoe_id FROM profile WHERE wishlist = 'true' AND user_id = ?)", session["user_id"])
        purchases = db.execute("SELECT * FROM sneakers WHERE id IN (SELECT shoe_id FROM profile WHERE purchased = 'true' AND user_id = ?)", session["user_id"])
        tops = db.execute("SELECT * FROM sneakers WHERE id IN (SELECT shoe_id FROM profile WHERE top = 'true' AND user_id = ?)", session["user_id"])

        # User reached route via GET (as by submitting a form via POST)
        return render_template("edit.html", wishlists=wishlists, purchases=purchases, tops=tops)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

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

        # Redirect to home page
        return redirect("/")

    else:

        # User reached route via GET (as by clicking a link or via redirect)
        return render_template("login.html")


@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    """Search sneaker."""

    if request.method == "POST":

        # No input to search
        if not request.form.get("search"):
            return render_template("search.html")

        shoe = request.form.get("search")

        # Lookup the sneaker that the user submitted
        sneakers = db.execute("SELECT * FROM sneakers WHERE name LIKE ?", (f'%{request.form.get("search")}%'))

        x = 0
        for sneaker in sneakers:
            x += 1

        if not sneakers:
            # User reached route via POST (by submitting sneaker name that cannot be found)
            return render_template("nonexistent.html", shoe=shoe)
        else:
            # User reached route via POST (by submitting sneaker name that was found)
            return render_template("searched.html", sneakers=sneakers, shoe=shoe, x=x)

    else:

        # User reached route via GET (as by clicking a link or via redirect)
        return render_template("search.html")


@app.route("/shoe", methods=["GET", "POST"])
@login_required
def shoe():
    """Show card for sneaker and all information"""
    if request.method == "POST":
        # Retrieve shoe ID
        shoeID = request.form.get("tag")

        shoes = db.execute("SELECT * FROM sneakers where id = ?", shoeID)

        # User reached route via POST (as by clicking a link or via redirect)
        return render_template("shoe.html", shoes=shoes)

    else:

        return render_template("shoe.html")


@app.route("/add", methods=["GET", "POST"])
def add():
    """Add sneaker to database"""

    if request.method == "POST":

        # Gets inputted information from form
        name = request.form.get("name")
        description = request.form.get("description")
        colorway = request.form.get("colorway")
        release = request.form.get("release")
        price = request.form.get("price")
        style = request.form.get("style")
        image = request.form.get("image")
        purchase = request.form.get("purchase")

        # Checks if certain info wasn't provided
        if not name:
            return apology("must provide name", 400)
        elif not price:
            return apology("must provide price", 400)
        elif not description:
            description = "--"
        elif not colorway:
            colorway = "--"
        elif not release:
            release = "--"
        elif not style:
            style = "--"
        elif not image:
            image = "--"
        elif not purchase:
            purchase = "--"

        # Puts price in correct format for use of usd function
        price = float(price)
        price = round(price, 0)
        price = int(price)

        # Puts sneaker into database
        db.execute("INSERT into sneakers (name, colorway, description, releaseDate, retailPrice, styleID, image, purchase) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                   name, colorway, description, release, price, style, image, purchase)

        shoes = db.execute("SELECT * FROM sneakers WHERE name = ?", name)

        # User reached route via POST (as by clicking a link or via redirect)
        return render_template("shoe.html", shoes=shoes)

    else:

        # User reached route via GET (as by clicking a link or via redirect)
        return render_template("add.html")


@app.route("/append", methods=["POST", "GET"])
@login_required
def append():
    """Add sneaker to wishlist, favorites, or purchased"""

    if request.method == "POST":

        # Gets particular shoe and which list user wants it to be added to
        shoe = request.form.get("shoe")
        top = request.form.get("top")
        wish = request.form.get("wish")
        purchased = request.form.get("purchased")

        if top == None:
            top = "false"
        if wish == None:
            wish = "false"
        if purchased == None:
            purchased = "false"

        # Puts sneaker in selected lists
        db.execute("INSERT into profile (user_id, shoe_id, wishlist, top, purchased) VALUES (?, ?, ?, ?, ?)",
                   session["user_id"], shoe, wish, top, purchased)

        # Redirect to index or homepage
        return redirect("/")
    else:

        # User reached route via GET (as by clicking a link or via redirect)
        return render_template("shoe.html")


@app.route("/settings")
@login_required
def settings():
    """Goes to settings page"""

    # User reached template (as by clicking a link)
    return render_template("settings.html")


@app.route("/change", methods=["GET", "POST"])
@login_required
def change():
    """Changes password"""

    if request.method == "POST":

        password = generate_password_hash(request.form.get("password"))

        # Ensure password was submitted
        if not request.form.get("password"):
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

        # Changes password in user table
        db.execute("UPDATE users SET hash = ? WHERE id = ?", password, session["user_id"])

        return redirect("/logout")

    else:

        # User reached route via GET (as by clicking a link or via redirect)
        return render_template("change.html")


@app.route("/delete", methods=["GET", "POST"])
@login_required
def delete():
    """Deletes currently used account"""

    if request.method == "POST":

        # confirms user wants to delete account
        choice = request.form.get("choiceY")

        # deletes account
        if choice == "y":
            db.execute("DELETE FROM profile WHERE user_id = ?", session["user_id"])
            db.execute("DELETE FROM users WHERE id = ?", session["user_id"])

        # Redirect to index or homepage
        return redirect("/")

    else:

        # User reached route via GET (as by clicking a link or via redirect)
        return render_template("delete.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


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


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
