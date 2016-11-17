from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from main.models import Movie, History, Watchlist, Blocklist

MOVIES_PER_PAGE = 20

def movies_view(request):
    movies_list = Movie.objects.all().order_by('-release_date')
    movies_count = Movie.objects.all().count()
    paginator = Paginator(movies_list, MOVIES_PER_PAGE)
    page = request.GET.get('page', 1)
    try:
        movies = paginator.page(page)
    except PageNotAnInteger:
        movies = paginator.page(1)
    except EmptyPage:
        movies = []#paginator.page(paginator.num_pages)
    
    data = []
    for movie in movies:
        data.append(movie_to_dict(movie))
    
    return JsonResponse({
        "status": "200",
        "count": int(len(data)),
        "total": int(movies_count),
        "page": int(page),
        "movies": data,
    })

def movies_detail(request, movie_id):
    json_data = {}
    try:
        movie = Movie.objects.get(pk=movie_id)
        json_data['movie'] = movie_to_dict(movie)
        json_data['status'] = "200"
    except Movie.DoesNotExist:
        raise Http404
    
    return JsonResponse(json_data)

def movies_top(request):
    movies_list = Movie.objects.filter(imdb_votes__gt=250000).order_by('-imdb_rating')
    movies_count = Movie.objects.filter(imdb_votes__gt=250000).count()
    
    paginator = Paginator(movies_list, MOVIES_PER_PAGE)
    page = request.GET.get('page', 1)
    try:
        movies = paginator.page(page)
    except PageNotAnInteger:
        movies = paginator.page(1)
    except EmptyPage:
        movies = []#paginator.page(paginator.num_pages)
    
    data = []
    for movie in movies:
        data.append(movie_to_dict(movie))
    
    return JsonResponse({
        "status": "200",
        "count": int(len(data)),
        "total": int(movies_count),
        "page": int(page),
        "movies": data,
    })

def latest_view(request):
    movies_list = Movie.objects.all().order_by('-created')
    movies_count = Movie.objects.all().count()
    
    paginator = Paginator(movies_list, MOVIES_PER_PAGE)
    page = request.GET.get('page', 1)
    try:
        movies = paginator.page(page)
    except PageNotAnInteger:
        movies = paginator.page(1)
    except EmptyPage:
        movies = []#paginator.page(paginator.num_pages)
    
    data = []
    for movie in movies:
        data.append(movie_to_dict(movie))
    
    return JsonResponse({
        "status": "200",
        "count": int(len(data)),
        "total": int(movies_count),
        "page": int(page),
        "movies": data,
    })

def history_view(request, username):
    profile = get_object_or_404(User, username=username)
    
    history_ids = History.objects.filter(user=profile).values_list('movie', flat=True)
    movies_list = Movie.objects.filter(id__in=history_ids).order_by('-release_date')
    movies_count = Movie.objects.filter(id__in=history_ids).count()
    
    paginator = Paginator(movies_list, MOVIES_PER_PAGE)
    page = request.GET.get('page', 1)
    try:
        movies = paginator.page(page)
    except PageNotAnInteger:
        movies = paginator.page(1)
    except EmptyPage:
        movies = []#paginator.page(paginator.num_pages)
    
    data = []
    for movie in movies:
        data.append(movie_to_dict(movie))
    
    return JsonResponse({
        "status": "200",
        "count": int(len(data)),
        "total": int(movies_count),
        "page": int(page),
        "movies": data,
    })

def watchlist_view(request, username):
    profile = get_object_or_404(User, username=username)
    
    watchlist = profile.watchlist.all().order_by('-important', '-movie__release_date')
    movies_list = [w.movie for w in watchlist]
    movies_count = profile.watchlist.all().count()
        
    paginator = Paginator(movies_list, MOVIES_PER_PAGE)
    page = request.GET.get('page', 1)
    try:
        movies = paginator.page(page)
    except PageNotAnInteger:
        movies = paginator.page(1)
    except EmptyPage:
        movies = []#paginator.page(paginator.num_pages)
    
    data = []
    for movie in movies:
        data.append(movie_to_dict(movie))
    
    return JsonResponse({
        "status": "200",
        "count": int(len(data)),
        "total": int(movies_count),
        "page": int(page),
        "movies": data,
    })

def blocklist_view(request, username):
    profile = get_object_or_404(User, username=username)
    
    blocklist = profile.blocklist.all().order_by('-movie__release_date')
    movies_list = [b.movie for b in blocklist]
    movies_count = profile.blocklist.all().count()
        
    paginator = Paginator(movies_list, MOVIES_PER_PAGE)
    page = request.GET.get('page', 1)
    try:
        movies = paginator.page(page)
    except PageNotAnInteger:
        movies = paginator.page(1)
    except EmptyPage:
        movies = []#paginator.page(paginator.num_pages)
    
    data = []
    for movie in movies:
        data.append(movie_to_dict(movie))
    
    return JsonResponse({
        "status": "200",
        "count": int(len(data)),
        "total": int(movies_count),
        "page": int(page),
        "movies": data,
    })


def movie_to_dict(movie):
    movie_dict = {
        "id": movie.id,
        "title": movie.title,
        "original_title": movie.original_title,
        "tagline": movie.tagline,
        "overview": movie.overview,
        "release_date": str(movie.release_date),
        "original_language": movie.original_language,
        "runtime": movie.runtime,
        "imdb_id": movie.imdb_id,
        "imdb_rating": movie.imdb_rating,
        "imdb_votes": movie.imdb_votes,
        "imdb_link": "http://www.imdb.com/title/{}/".format(movie.imdb_id),
        "tmdb_link": "https://www.themoviedb.org/movie/{}/".format(movie.id),
        "poster": "https://image.tmdb.org/t/p/w370{}".format(movie.poster_path),
        "backdrop": "https://image.tmdb.org/t/p/w780{}".format(movie.backdrop_path),
    }
    return movie_dict