import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps

response = requests.get('https://api.themoviedb.org/3/discover/movie?api_key=5f5031efd18ddc70cf0fb5f7a558b1a8&language=en-US&sort_by=popularity.desc&include_adult=false&include_video=false&page=1&with_genres=99&with_keywords=5967')
moviedata = response.json()

#print(moviedata)

movies = {}
for i in range(5):
    movies[moviedata["results"][i]["title"]] = moviedata["results"][i]["release_date"]

print(movies)