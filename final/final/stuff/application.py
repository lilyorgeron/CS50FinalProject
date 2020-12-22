import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookupbooks, lookupmovies, lookuptracks

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


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///collection.db")



# Using the history table to find past countries seacrched in each category to create a history page
@app.route("/library")
@login_required
def library():
    """Show search history of movies or videos"""

    bookcount = db.execute("SELECT country FROM history WHERE user_id = :user_id AND type = :type GROUP BY country ORDER BY country",
                          user_id=session["user_id"], type="book")

    moviecount = db.execute("SELECT country FROM history WHERE user_id = :user_id AND type = :type GROUP BY country",
                           user_id=session["user_id"], type="movies")

    songcount = db.execute("SELECT country FROM history WHERE user_id = :user_id AND type = :type GROUP BY country",
                           user_id=session["user_id"], type="song")

    # Creating nested dictionaries to contain each country and each country's information
    bookhist = {}
    for info in bookcount:
        name = info['country']
        bookhist[name] = lookupbooks(name)


    moviehist = {}
    for info in moviecount:
        name = info['country']
        moviehist[name] = lookupmovies(name)

    songhist = {}
    for info in songcount:
        name = info['country']
        songhist[name] = lookuptracks(name)

    return render_template("library.html", bookhist=bookhist, moviehist=moviehist, songhist=songhist)

# Link to the home page
@app.route("/")
def home():
    return render_template("home.html")

# Link to the about page
@app.route("/about")
def about():
    return render_template("about.html")


# Login
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
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

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

# Log out
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")



# Register
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":

        # checking that inputs exist and meet requirements
        if not request.form.get("username"):
            return apology("must provide username", 403)

        elif not request.form.get("password"):
            return apology("must provide password", 403)

        elif not request.form.get("confirmation"):
            return apology("must provide confirmation", 403)

        if request.form.get("password") != request.form.get("confirmation"):
            return apology("password must match confirmation")

        # inserting info into database and checking for unique username
        ids = db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)",
                         username=request.form.get("username"), hash=generate_password_hash(request.form.get("password")))

        if not ids:
            return apology("username is taken")

        # logging newly registered user in
        session["user_id"] = ids

        return redirect("/")

    else:
        return render_template("register.html")

# Uses lookupbooks to search for top 5 most relevant books
@app.route("/searchbooks", methods=["GET", "POST"])
@login_required
def searchBooks():
    """Search books"""

    if request.method == "POST":

        # Checking for input
        if not request.form.get("country"):
            return apology("must provide country", 403)

        # Getting the country inputted and looking of the books
        country = request.form.get("country")
        info = lookupbooks(country)
        if not info:
            return apology("must provide country listed")

        # Storing search in the history table
        db.execute("INSERT INTO history (user_id, country, type) VALUES (:user_id, :country, :type)",
                   user_id=session["user_id"], country=country, type="book")

        # Returning the results page
        return render_template("bookresults.html", info=info, country=country)

    else:
        return render_template("searchbooks.html")


# Using lookupmovies to search top 5 documentaries about each country
@app.route("/searchmovies", methods=["GET", "POST"])
@login_required
def searchMovies():
    """Search movies"""

    if request.method == "POST":

        # Checking for input
        if not request.form.get("country"):
            return apology("must provide country", 403)

        # Taking in input and using function to find the movies
        country = request.form.get("country")
        info = lookupmovies(country)
        if not info:
            return apology("must provide country listed")

        # Storing movie search in the history table
        db.execute("INSERT INTO history (user_id, country, type) VALUES (:user_id, :country, :type)",
                   user_id=session["user_id"], country=country, type="movies")

        return render_template("movieresults.html", info=info, country=country)

    else:
        return render_template("searchmovies.html")


# Using lookuptracks to find top tracks of the last week in each country
@app.route("/searchsongs", methods=["GET", "POST"])
@login_required
def searchSongs():
    """Search songs"""

    if request.method == "POST":

        # Checking for input
        if not request.form.get("country"):
            return apology("must provide country", 403)


        # Taking in input and using function to find the songs
        country = request.form.get("country")
        info = lookuptracks(country)
        if not info:
            return apology("must provide country listed")

        # Storing song search into table
        db.execute("INSERT INTO history (user_id, country, type) VALUES (:user_id, :country, :type)",
                   user_id=session["user_id"], country=country, type="song")

        # Returning page of song results
        return render_template("songresults.html", info=info, country=country)

    else:
        return render_template("searchsongs.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
