import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps

response = requests.get('https://www.googleapis.com/books/v1/volumes?q=subject:japan&orderBy=relevance&maxResults=5')
#print(response.text)

data = response.json()
# bookstuff = {
#         "title": books["title"],
#         "author": books["authors"]
#     }

books = {}
for i in range(5):
        books[data["items"][i]["volumeInfo"]["title"]] = data["items"][i]["volumeInfo"]["authors"]

print(books)
# def lookup():

#      try:
#           response = requests.get("https://www.googleapis.com/books/v1/volumes?q=subject:japan&orderBy=relevance&maxResults=5")
#           response.raise_for_status()
#      except requests.RequestException:
#           return None

#     # Parse response
#      try:
#           books = response.json()
#           bookstuff = {
#               "name": books["title"],
#               "author": books["authors"]
#           }
#           print(bookstuff)
#           return 0
#      except (KeyError, TypeError, ValueError):
#           return None
