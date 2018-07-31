from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404, render, render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Sum, Count
from main.models import Movie, History, Watchlist, Blocklist, Person, Activity
from django.utils import timezone
from datetime import datetime
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
    
    context = {
        'movies': movies,
        'count': movies_list.count(),
    }
    return render(request, 'index.html', context)


# latest
@login_required
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
    
    context = {
        'movies': movies,
        'count': movies_list.count(),
    }
    return render(request, 'latest.html', context)


# search view
@login_required
def search_view(request):
    kwargs = {}
    movies_list = []
    movies_count = 0
    
    title = request.GET.get('title', '')
    year_from = request.GET.get('year_from', 0)
    year_to = request.GET.get('year_to', 0)
    imdb_rating_from = request.GET.get('imdb_rating_from', 0)
    imdb_rating_to = request.GET.get('imdb_rating_to', 0)
    faff_rating_from = request.GET.get('faff_rating_from', 0)
    faff_rating_to = request.GET.get('faff_rating_to', 0)
    show_watchlist = request.GET.get('watchlist', False)
    show_history = request.GET.get('history', False)
    show_blocklist = request.GET.get('blocklist', False)
    get_order = request.GET.get('order', '')
    get_asc_desc = request.GET.get('asc_desc', '')
    
    if title:
        kwargs['title__icontains'] = title
    if year_from:
        year_from = int(year_from)
        kwargs['release_date__gte'] = datetime(year_from, 1, 1)
    if year_to:
        year_to = int(year_to)
        kwargs['release_date__lte'] = datetime(year_to, 12, 31)
    if imdb_rating_from:
        imdb_rating_from = int(imdb_rating_from)
        kwargs['imdb_rating__gte'] = imdb_rating_from
    if imdb_rating_to:
        imdb_rating_to = int(imdb_rating_to)
        kwargs['imdb_rating__lte'] = imdb_rating_to
    if faff_rating_from:
        faff_rating_from = int(faff_rating_from)
        kwargs['faff_rating__gte'] = faff_rating_from
    if faff_rating_to:
        faff_rating_to = int(faff_rating_to)
        kwargs['faff_rating__lte'] = faff_rating_to
    
    order_options = {
        "date": "release_date",
        "imdb_rating": "imdb_rating",
        "faff_rating": "faff_rating"
    }
    order_by = 'date'
    if get_order:
        order_by = get_order
    
    asc_desc_options = {
        "asc": "",
        "desc": "-"
    }
    asc_desc = "desc"
    if get_asc_desc:
        asc_desc = get_asc_desc
    
    query_order = '{}{}'.format(asc_desc_options[asc_desc], order_options[order_by])
    
    movies_list = Movie.objects.filter(**kwargs).order_by(query_order)
    
    if request.user.is_authenticated():
        if not show_watchlist:
            watchlist = Watchlist.objects.filter(user=request.user).values_list('movie', flat=True)
            movies_list = movies_list.exclude(pk__in=watchlist)
        if not show_history:
            history = History.objects.filter(user=request.user).values_list('movie', flat=True)
            movies_list = movies_list.exclude(pk__in=history)
        if not show_blocklist:
            blocklist = Blocklist.objects.filter(user=request.user).values_list('movie', flat=True)
            movies_list = movies_list.exclude(pk__in=blocklist)
    
    paginator = Paginator(movies_list, MOVIES_PER_PAGE)
    page = request.GET.get('page')
    try:
        movies = paginator.page(page)
    except PageNotAnInteger:
        movies = paginator.page(1)
    except EmptyPage:
        movies = paginator.page(paginator.num_pages)
    
    context = {
        'movies': movies,
        'title': title,
        'year_from': year_from,
        'year_to': year_to,
        'imdb_rating_from': imdb_rating_from,
        'imdb_rating_to': imdb_rating_to,
        'faff_rating_from': faff_rating_from,
        'faff_rating_to': faff_rating_to,
        'show_watchlist': show_watchlist,
        'show_history': show_history,
        'show_blocklist': show_blocklist,
        'rating_range': range(5, 10),
        'year_range': reversed(range(1970, 2019)),
        'order_options': order_options,
        'asc_desc_options': asc_desc_options,
        'order_by': order_by,
        'asc_desc': asc_desc,
    }
    return render(request, 'search.html', context)


# movie detail
@login_required
def movie_view(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    
    history_users = History.objects.filter(movie=movie_id)
    watchlist_users = Watchlist.objects.filter(movie=movie_id)
    
    cast = movie.cast.all().order_by('moviecast__order')[:6]
    
    if request.POST:
        faff_id = request.POST.get("faff_id", None)
        movie.faff_id = faff_id
        movie.save()
    
    context = {
        'movie': movie,
        'history_users': history_users,
        'watchlist_users': watchlist_users,
        'cast': cast,
    }
    return render(request, 'movie.html', context)


# person detail
@login_required
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
    
    context = {
        'person': person,
        'movies': movies,
        'count': movies_count,
        'history_count': history_count,
        'percentage': percentage,
    }
    return render(request, 'person.html', context)


# users
@login_required
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
    
    context = {
        'users': users,
        'users_count': users_list.count(),
        'query': query,
    }
    return render(request, 'users.html', context)


# top imdb
@login_required
def top_imdb_view(request):
    if request.GET.get('mode', '') == 'discover':
        seen_movies = History.objects.filter(user=request.user).values_list('movie', flat=True)
        movies_list = Movie.objects.filter(imdb_votes__gt=250000).exclude(pk__in=seen_movies).order_by('-imdb_rating', '-imdb_votes')
    else:
        movies_list = Movie.objects.filter(imdb_votes__gt=250000).order_by('-imdb_rating', '-imdb_votes')
    
    paginator = Paginator(movies_list, MOVIES_PER_PAGE)
    page = request.GET.get('page')
    try:
        movies = paginator.page(page)
    except PageNotAnInteger:
        movies = paginator.page(1)
    except EmptyPage:
        movies = paginator.page(paginator.num_pages)
    
    context = {
        'movies': movies,
        'count': movies_list.count(),
    }
    return render(request, 'top.html', context)


# top FA
@login_required
def top_fa_view(request):
    if request.GET.get('mode', '') == 'discover':
        seen_movies = History.objects.filter(user=request.user).values_list('movie', flat=True)
        movies_list = Movie.objects.exclude(faff_id__exact='').exclude(pk__in=seen_movies).order_by('-faff_rating', '-faff_votes')
    else:
        movies_list = Movie.objects.exclude(faff_id__exact='').order_by('-faff_rating', '-faff_votes')
    
    paginator = Paginator(movies_list, MOVIES_PER_PAGE)
    page = request.GET.get('page')
    try:
        movies = paginator.page(page)
    except PageNotAnInteger:
        movies = paginator.page(1)
    except EmptyPage:
        movies = paginator.page(paginator.num_pages)
    
    context = {
        'movies': movies,
        'count': movies_list.count(),
    }
    return render(request, 'top_faff.html', context)


# profile
@login_required
def profile_view(request, username):
    profile = get_object_or_404(User, username=username)
    history_count = profile.history.count()
    watchlist_count = profile.watchlist.count()
    blocklist_count = profile.blocklist.count()
    added_count = profile.added_movies.count()
    
    context = {
        'profile': profile,
        'history_count': history_count,
        'watchlist_count': watchlist_count,
        'blocklist_count': blocklist_count,
        'added_count': added_count,
    }
    return render(request, 'profile.html', context)


# history
@login_required
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
    
    context = {
        'profile': profile,
        'movies': movies,
        'count': movies_list.count(),
        'total_runtime': total_runtime,
    }
    return render(request, 'history.html', context)


# watchlist
@login_required
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
    
    context = {
        'profile': profile,
        'movies': movies,
        'count': watchlist.count(),
    }
    return render(request, 'watchlist.html', context)


# blocklist
@login_required
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
    
    context = {
        'profile': profile,
        'movies': movies,
        'count': blocklist.count(),
    }
    return render(request, 'blocklist.html', context)


# added
@login_required
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
    
    context = {
        'profile': profile,
        'movies': movies,
        'count': movies_list.count(),
    }
    return render(request, 'added.html', context)


# discover
@login_required
def discover_view(request):
    return redirect('/search/')
    
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
    
    context = {
        'movies': movies,
        'count': movies_list.count(),
        'get_order': get_order,
        'order_options': order_options.keys(),
        'years': years,
        'get_year': int(get_year),
    }
    return render(request, 'discover.html', context)


@login_required
def activity_view(request):
    activity_list = Activity.objects.all().order_by('-created')
    
    paginator = Paginator(activity_list, MOVIES_PER_PAGE)
    page = request.GET.get('page')
    try:
        activity = paginator.page(page)
    except PageNotAnInteger:
        activity = paginator.page(1)
    except EmptyPage:
        activity = paginator.page(paginator.num_pages)
    
    context = {
        "activity": activity
    }
    return render(request, 'activity.html', context)
