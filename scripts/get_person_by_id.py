from django.utils import timezone
from main.models import Movie
from movies import config
import tmdbsimple as tmdb
import requests
import json

tmdb.API_KEY = config.TMDB_KEY

person_id = 6193 # leo
request = tmdb.People(person_id)
movies = request.movie_credits()

for movie in movies['cast']:
    print movie['id'], movie['title']