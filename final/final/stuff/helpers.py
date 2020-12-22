import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps

# Apology
def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code

# Log in details
def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

# Country keys necessary for the movie API to use as keyword
countrykeys = {
        "France": 254,
        "Japan": 233,
        "Russia": 2139,
        "Italy": 131,
        "Mexico": 534,
        "Sweden": 1192,
        "Turkey": 5733,
        "Austria": 1201,
        "Greece": 1200,
        "Israel": 536,
        "Mongolia": 4719,
        "India": 14636,
        "Germany": 74,
        "Thailand": 3434,
        "Philippines": 6895,
        "Peru": 5967,
        "Argentina": 10596,
        "Egypt": 1160,
        "Morocco": 1629
}


# Lookup function for googlebooks API
def lookupbooks(country):
    """Look up relevant books."""

    try:
        response = requests.get(f'https://www.googleapis.com/books/v1/volumes?q=subject:{urllib.parse.quote_plus(country)}&orderBy=relevance&maxResults=5')
        response.raise_for_status()
    except requests.RequestException:
        return None

    try:
        data = response.json()
        books = {}
        for i in range(5):
            books[data["items"][i]["volumeInfo"]["title"]] = data["items"][i]["volumeInfo"]["authors"]
        return books
    except (KeyError, TypeError, ValueError):
        return None

# Lookup function for TMDB API
def lookupmovies(country):
    """Look up relevant movies."""

    try:
        response = requests.get(f'https://api.themoviedb.org/3/discover/movie?api_key=5f5031efd18ddc70cf0fb5f7a558b1a8&language=en-US&sort_by=popularity.desc&include_adult=false&include_video=false&page=1&with_genres=99&with_keywords={urllib.parse.quote_plus(str(countrykeys[country]))}')
        response.raise_for_status()
    except requests.RequestException:
        return None

    try:
        moviedata = response.json()
        movies = {}
        for i in range(5):
            movies[moviedata["results"][i]["title"]] = moviedata["results"][i]["release_date"]
        return movies
    except (KeyError, TypeError, ValueError):
        return None

# Lookup function for the last.fm API
def lookuptracks(country):
    """Look up relevant songs."""

    try:
        response = requests.get(f'http://ws.audioscrobbler.com/2.0/?method=geo.gettoptracks&country={urllib.parse.quote_plus(country)}&api_key=9c80406a377a98a06f526d699d22cb7b&format=json')
        response.raise_for_status()
    except requests.RequestException:
        return None

    try:
        songdata = response.json()
        songs = {}
        for i in range(5):
            songs[songdata["tracks"]["track"][i]["name"]] = songdata["tracks"]["track"][i]["artist"]["name"]
        return songs
    except (KeyError, TypeError, ValueError):
        return None