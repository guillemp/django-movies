from django.utils import timezone
from main.models import Movie
from movies import config
import tmdbsimple as tmdb
import requests
import json

tmdb.API_KEY = config.TMDB_KEY

movie_id = 299687
request = tmdb.Movies(movie_id)
response = request.info()

try:
    movie = Movie()
    movie.id = response['id']
    movie.title = response['title'] or ''
    movie.original_title = response['original_title'] or ''
    movie.tagline = response['tagline'] or ''
    movie.overview = response['overview'] or ''
    movie.imdb_id = response['imdb_id'] or ''
    movie.release_date = response['release_date'] or None
    movie.original_language = response['original_language'] or ''
    movie.poster_path = response['poster_path'] or ''
    movie.backdrop_path = response['backdrop_path'] or ''
    movie.runtime = response['runtime'] or ''
    movie.save()
except Exception, e:
    print movie_id, str(e)