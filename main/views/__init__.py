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

def index_view(request):
    if request.user.is_authenticated():
        # exclude blocklist movies
        blocklist_ids = Blocklist.objects.filter(user=request.user).values_list('movie', flat=True)
        movies_list = Movie.objects.exclude(id__in=blocklist_ids).order_by('-release_date')
    else:
        movies_list = Movie.objects.all().order_by('-release_date')
    
    paginator = Paginator(movies_list, MOVIES_PER_PAGE)
    page = request.GET.get('page')
    try:
        movies = paginator.page(page)
    except PageNotAnInteger:
        movies = paginator.page(1)
    except EmptyPage:
        movies = paginator.page(paginator.num_pages)
    
    return render(request, 'index.html', {
        'movies': movies,
        'count': movies_list.count(),
    })

# latest
def latest_view(request):
    movies_list = Movie.objects.all().order_by('-created')
    
    paginator = Paginator(movies_list, MOVIES_PER_PAGE)
    page = request.GET.get('page')
    try:
        movies = paginator.page(page)
    except PageNotAnInteger:
        movies = paginator.page(1)
    except EmptyPage:
        movies = paginator.page(paginator.num_pages)
    
    return render(request, 'latest.html', {
        'movies': movies,
        'count': movies_list.count(),
    })

# search view
def search_view(request):
    movies_list = []
    movies_count = 0
    
    query = request.GET.get('query', '')
    if query:
        if query.startswith('tt'):
            try:
                movie = Movie.objects.get(imdb_id=query)
                return redirect(movie.url())
            except:
                pass
            
        movies_list = Movie.objects.filter(title__icontains=query).order_by('-release_date') | Movie.objects.filter(original_title__icontains=query).order_by('-release_date')
    
    paginator = Paginator(movies_list, MOVIES_PER_PAGE)
    page = request.GET.get('page')
    try:
        movies = paginator.page(page)
    except PageNotAnInteger:
        movies = paginator.page(1)
    except EmptyPage:
        movies = paginator.page(paginator.num_pages)
    
    return render(request, 'search.html', {
        'movies': movies,
        'count': movies_list.count(),
        'search_query': query,
    })

# movie detail
def movie_view(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    
    history_users = History.objects.filter(movie=movie_id)
    watchlist_users = Watchlist.objects.filter(movie=movie_id)
    
    cast = movie.cast.all().order_by('moviecast__order')[:6]
    
    return render(request, 'movie.html', {
        'movie': movie,
        'history_users': history_users,
        'watchlist_users': watchlist_users,
        'cast': cast,
    })

# person detail
def person_view(request, person_id):
    person = get_object_or_404(Person, pk=person_id)
    movies_list = person.movies.all().order_by('-release_date')
    movies_count = movies_list.count()
    
    paginator = Paginator(movies_list, MOVIES_PER_PAGE)
    page = request.GET.get('page')
    try:
        movies = paginator.page(page)
    except PageNotAnInteger:
        movies = paginator.page(1)
    except EmptyPage:
        movies = paginator.page(paginator.num_pages)
    
    percentage = 0
    history_count = 0
    if request.user.is_authenticated():
        history_count = request.user.history.filter(movie__cast=person).count()
        percentage = int(float(history_count)/float(movies_count)*100)
    
    return render(request, 'person.html', {
        'person': person,
        'movies': movies,
        'count': movies_count,
        'history_count': history_count,
        'percentage': percentage,
    })

#users
def users_view(request):
    query = request.GET.get('query', '')
    if query:
        users_list = User.objects.filter(username__icontains=query).order_by('username')
    else:
        users_list = User.objects.all().order_by('username')

    paginator = Paginator(users_list, USERS_PER_PAGE)
    page = request.GET.get('page')
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    return render(request, 'users.html', {
        'users': users,
        'users_count': users_list.count(),
        'query': query,
    })

# top imdb
def top_imdb_view(request):
    movies_list = Movie.objects.filter(imdb_votes__gt=250000).order_by('-imdb_rating', '-imdb_votes')
    
    paginator = Paginator(movies_list, MOVIES_PER_PAGE)
    page = request.GET.get('page')
    try:
        movies = paginator.page(page)
    except PageNotAnInteger:
        movies = paginator.page(1)
    except EmptyPage:
        movies = paginator.page(paginator.num_pages)
    
    return render(request, 'top.html', {
        'movies': movies,
        'count': movies_list.count(),
    })

# top FA
def top_fa_view(request):
    movies_list = Movie.objects.exclude(faff_id__exact='').order_by('-faff_rating', '-faff_votes')
    
    paginator = Paginator(movies_list, MOVIES_PER_PAGE)
    page = request.GET.get('page')
    try:
        movies = paginator.page(page)
    except PageNotAnInteger:
        movies = paginator.page(1)
    except EmptyPage:
        movies = paginator.page(paginator.num_pages)
    
    return render(request, 'top_faff.html', {
        'movies': movies,
        'count': movies_list.count(),
    })

# profile
def profile_view(request, username):
    profile = get_object_or_404(User, username=username)
    history_count = profile.history.count()
    watchlist_count = profile.watchlist.count()
    blocklist_count = profile.blocklist.count()
    added_count = profile.added_movies.count()
    
    return render(request, 'profile.html', {
        'profile': profile,
        'history_count': history_count,
        'watchlist_count': watchlist_count,
        'blocklist_count': blocklist_count,
        'added_count': added_count,
    })

# history
def history_view(request, username):
    profile = get_object_or_404(User, username=username)
    
    history_ids = History.objects.filter(user=profile).values_list('movie', flat=True)
    movies_list = Movie.objects.filter(id__in=history_ids).order_by('-release_date')
    
    paginator = Paginator(movies_list, MOVIES_PER_PAGE)
    page = request.GET.get('page')
    try:
        movies = paginator.page(page)
    except PageNotAnInteger:
        movies = paginator.page(1)
    except EmptyPage:
        movies = paginator.page(paginator.num_pages)
    
    total_runtime = 0
    if history_ids:
        sum_runtime = Movie.objects.filter(id__in=history_ids).aggregate(Sum('runtime'))
        total_runtime = int(sum_runtime['runtime__sum']) / 60
    
    return render(request, 'history.html', {
        'profile': profile,
        'movies': movies,
        'count': movies_list.count(),
        'total_runtime': total_runtime,
    })

# watchlist
def watchlist_view(request, username):
    profile = get_object_or_404(User, username=username)
    
    #watchlist_ids = Watchlist.objects.filter(user=profile).values_list('movie', flat=True)
    #movies_list = Movie.objects.filter(id__in=watchlist_ids).order_by('-release_date')
    #movies_count = Movie.objects.filter(id__in=watchlist_ids).count()
    
    watchlist = profile.watchlist.all().order_by('-important', '-movie__release_date')
    movies_list = []
    for obj in watchlist:
        #obj.movie['important'] = obj.important
        movies_list.append(obj.movie)
        
    paginator = Paginator(movies_list, MOVIES_PER_PAGE)
    page = request.GET.get('page')
    try:
        movies = paginator.page(page)
    except PageNotAnInteger:
        movies = paginator.page(1)
    except EmptyPage:
        movies = paginator.page(paginator.num_pages)
    
    return render(request, 'watchlist.html', {
        'profile': profile,
        'movies': movies,
        'count': watchlist.count(),
    })

# blocklist
def blocklist_view(request, username):
    profile = get_object_or_404(User, username=username)
    
    blocklist = profile.blocklist.all().order_by('-movie__release_date')
    movies_list = [b.movie for b in blocklist]
        
    paginator = Paginator(movies_list, MOVIES_PER_PAGE)
    page = request.GET.get('page')
    try:
        movies = paginator.page(page)
    except PageNotAnInteger:
        movies = paginator.page(1)
    except EmptyPage:
        movies = paginator.page(paginator.num_pages)
    
    return render(request, 'blocklist.html', {
        'profile': profile,
        'movies': movies,
        'count': blocklist.count(),
    })

# added
def added_view(request, username):
    profile = get_object_or_404(User, username=username)
    
    movies_list = profile.added_movies.all().order_by('-release_date')
        
    paginator = Paginator(movies_list, MOVIES_PER_PAGE)
    page = request.GET.get('page')
    try:
        movies = paginator.page(page)
    except PageNotAnInteger:
        movies = paginator.page(1)
    except EmptyPage:
        movies = paginator.page(paginator.num_pages)
    
    return render(request, 'added.html', {
        'profile': profile,
        'movies': movies,
        'count': movies_list.count(),
    })

# discover
@login_required
def discover_view(request):
    
    history_ids = History.objects.filter(user=request.user).values_list('movie', flat=True)
    watchlist_ids = Watchlist.objects.filter(user=request.user).values_list('movie', flat=True)
    blocklist_ids = Blocklist.objects.filter(user=request.user).values_list('movie', flat=True)
    
    
    get_year = request.GET.get('year', 0)
    get_order = request.GET.get('order', 'date')
    
    kwargs = {}
    if get_year:
        kwargs['release_date__year'] = get_year
    
    order_options = {
        "date": "-release_date",
        "rating": "-imdb_rating",
        "votes": "-imdb_votes",
        "title": "title",
    }
    order = order_options[get_order]
    
    movies_list = Movie.objects.exclude(id__in=history_ids).exclude(id__in=watchlist_ids).exclude(id__in=blocklist_ids).filter(**kwargs).order_by(order)
            
    paginator = Paginator(movies_list, MOVIES_PER_PAGE)
    page = request.GET.get('page')
    try:
        movies = paginator.page(page)
    except PageNotAnInteger:
        movies = paginator.page(1)
    except EmptyPage:
        movies = paginator.page(paginator.num_pages)
    
    history_commas = ",".join(str(x) for x in history_ids)
    watchlist_commas = ",".join(str(x) for x in watchlist_ids)
    blocklist_commas = ",".join(str(x) for x in blocklist_ids)
    
    years = []
    if history_commas or watchlist_commas or blocklist_commas:
        aaa = history_commas + watchlist_commas + blocklist_commas
        sql_query = "SELECT id, year(release_date) AS g FROM main_movie WHERE id NOT IN ({}) GROUP BY g ORDER BY g DESC".format(aaa)
        years = Movie.objects.raw(sql_query)
    
    return render(request, 'discover.html', {
        'movies': movies,
        'count': movies_list.count(),
        'get_order': get_order,
        'order_options': order_options.keys(),
        'years': years,
        'get_year': int(get_year),
    })
