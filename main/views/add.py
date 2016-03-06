from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404, render, render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Sum, Count
from main.models import Movie, History, Watchlist, Blocklist, Person
from django.utils import timezone
from movies import config
import tmdbsimple as tmdb
import requests
import random
import json
import time

tmdb.API_KEY = config.TMDB_KEY
MOVIES_PER_PAGE = 30
USERS_PER_PAGE = 30

@login_required
def movie_add(request):
    query = ''
    movies = []
    if request.GET:
        query = request.GET.get('query')
        if query.isdigit():
            movies = get_tmdb_movie_by_id(query)
        else:
            movies = get_tmdb_movie_by_title(query)
    
    for movie in movies:
        try:
            exists = Movie.objects.get(pk=movie['id'])
            movie['in_database'] = True
        except Movie.DoesNotExist:
            movie['in_database'] = False
    
    return render(request, 'add.html', {
        'movies': movies,
        'query': query,
    })

def get_tmdb_movie_by_id(movie_id):
    search = tmdb.Movies(movie_id)
    return [search.info()]

def get_tmdb_movie_by_title(query):
    search = tmdb.Search()
    response = search.movie(query=query)
    return search.results

#
# save movie to db
#
@login_required
def movie_save(request):
    if request.POST:
        movie_id = request.POST.get('movie_id', None)
        try:
            movie = Movie.objects.get(pk=movie_id)
        except Movie.DoesNotExist:
            movie = Movie()
            m = tmdb.Movies(movie_id)
            response_to_movie(request, movie, m.info())
            movie.save()
            return HttpResponse("saved")
        except Exception, e:
            return HttpResponse(str(e))
    return HttpResponse("error")

@login_required
def movie_update(request):
    if request.POST:
        movie_id = request.POST.get('movie_id', None)
        try:
            m = tmdb.Movies(movie_id)
            movie = Movie.objects.get(pk=movie_id)
            response_to_movie(request, movie, m.info())
            movie.updated = timezone.now()
            movie.save()
            return HttpResponse("updated")
        except Exception, e:
            return HttpResponse(str(e))
    return HttpResponse("error")

def add_movie_by_id(request, movie_id):
    m = tmdb.Movies(movie_id)
    response = m.info()
    
    try:
        movie = Movie.objects.get(pk=movie_id)
        response_to_movie(request, movie, response)
        movie.updated = timezone.now
        movie.save()
    except Movie.DoesNotExist:
        movie = Movie()
        response_to_movie(request, movie, response)
        movie.save()
    
    return movie

def response_to_movie(request, movie, response):
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
    movie.user = request.user
    
    # movie cast add
    
    if movie.imdb_id:
        url = 'http://www.omdbapi.com/?i=%s&plot=short&r=json' % movie.imdb_id
        try:
            r = requests.get(url)
            data = json.loads(r.text)
            
            if data.get('imdbRating', False):
                if data['imdbRating'] != "N/A":
                    rating = float(data['imdbRating'])
                    movie.imdb_rating = rating
        
            if data.get('imdbVotes', False):
                if data['imdbVotes'] != "N/A":
                    votes = int(data['imdbVotes'].replace(",", ""))
                    movie.imdb_votes = votes
        except Exception, e:
            print movie.id, movie.title, str(e)