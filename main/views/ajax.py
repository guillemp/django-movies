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

#
# ajax
#
@login_required
def history_add_remove(request):
    #time.sleep(1)
    movie_id = request.POST.get('movie_id', None)
    movie = get_object_or_404(Movie, pk=movie_id)
    exists = request.user.history.filter(movie=movie)
    if exists:
        exists.delete()
        return HttpResponse("removed")
    else:
        history = History()
        history.user = request.user
        history.movie = movie
        history.save()
        # delete from watchlist
        watchlist = request.user.watchlist.filter(movie=movie)
        watchlist.delete()
        # delete from blocklist
        blocklist = request.user.blocklist.filter(movie=movie)
        blocklist.delete()
        return HttpResponse("added")

@login_required
def watchlist_add_remove(request):
    #time.sleep(1)
    movie_id = request.POST.get('movie_id', None)
    movie = get_object_or_404(Movie, pk=movie_id)
    exists = request.user.watchlist.filter(movie=movie)
    if exists:
        exists.delete()
        return HttpResponse("removed")
    else:
        watchlist = Watchlist()
        watchlist.user = request.user
        watchlist.movie = movie
        watchlist.save()
        # delete from history
        history = request.user.history.filter(movie=movie)
        history.delete()
        # delete from blocklist
        blocklist = request.user.blocklist.filter(movie=movie)
        blocklist.delete()
        return HttpResponse("added")

@login_required
def blocklist_add_remove(request):
    movie_id = request.POST.get('movie_id', None)
    movie = get_object_or_404(Movie, pk=movie_id)
    exists = request.user.blocklist.filter(movie=movie)
    if exists:
        exists.delete()
        return HttpResponse("removed")
    else:
        blocklist = Blocklist()
        blocklist.user = request.user
        blocklist.movie = movie
        blocklist.save()
        # delete from history
        history = request.user.history.filter(movie=movie)
        history.delete()
        # delete from watchlist
        watchlist = request.user.watchlist.filter(movie=movie)
        watchlist.delete()
        return HttpResponse("added")

@login_required
def watchlist_important(request):
    movie_id = request.POST.get('movie_id', None)
    movie = get_object_or_404(Movie, pk=movie_id)
    exists = request.user.watchlist.filter(movie=movie)
    if exists:
        watchlist = exists[0]
        if watchlist.important:
            watchlist.important = False
            watchlist.save()
            return HttpResponse("removed")
        else:
            watchlist.important = True
            watchlist.save()
            return HttpResponse("added")
    
    return HttpResponse("error")

# ajax autocomplete
def autocomplete_view(request):
    #time.sleep(2)
    movies = []
    query = request.POST.get('query', '')
    if query:    
        movies = Movie.objects.filter(title__icontains=query).order_by('title') | Movie.objects.filter(original_title__icontains=query).order_by('original_title')
    
    if movies:
        return render(request, 'autocomplete.html', {
            'movies': movies[:6],
        })
    
    return HttpResponse("empty")
