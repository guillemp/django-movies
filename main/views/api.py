from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from main.models import Movie, History, Watchlist, Blocklist

MOVIES_PER_PAGE = 20

def movies_view(request):
    movies_list = Movie.objects.all().order_by('-release_date')
    paginator = Paginator(movies_list, MOVIES_PER_PAGE)
    page = request.GET.get('page', 1)
    try:
        movies = paginator.page(page)
    except PageNotAnInteger:
        movies = paginator.page(1)
    except EmptyPage:
        movies = paginator.page(paginator.num_pages)
    
    data = []
    for movie in movies:
        data.append(movie_to_dict(movie))
    
    return JsonResponse({
        "status": "200",
        "count": MOVIES_PER_PAGE,
        "page": int(page),
        "movies": data,
    })

def movies_detail(request, movie_id):
    try:
        movie = Movie.objects.get(pk=movie_id)
        json_data = {
            "status": "200",
            "movies": movie_to_dict(movie),
        }
    except Movie.DoesNotExist:
        json_data = {
            "status": "404",
            "message": "Movie not found"
        }
    
    return JsonResponse(json_data)

def movies_top(request):
    movies_list = Movie.objects.filter(imdb_votes__gt=250000).order_by('-imdb_rating')
    paginator = Paginator(movies_list, MOVIES_PER_PAGE)
    page = request.GET.get('page', 1)
    try:
        movies = paginator.page(page)
    except PageNotAnInteger:
        movies = paginator.page(1)
    except EmptyPage:
        movies = paginator.page(paginator.num_pages)
    
    data = []
    for movie in movies:
        data.append(movie_to_dict(movie))
    
    return JsonResponse({
        "status": "200",
        "count": MOVIES_PER_PAGE,
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